import asyncio
import logging
import traceback
import typing
from collections.abc import Callable
from CommonClient import CommonContext, gui_enabled, get_base_parser, server_loop,ClientCommandProcessor
import os
import time
import sys
from typing import Dict, Optional
from BaseClasses import Region,Location

from BaseClasses import CollectionState,MultiWorld
from Options import StartInventoryPool
from settings import get_settings
from Utils import __version__, output_path
from worlds import AutoWorld
from worlds.tracker import TrackerWorld

from Generate import main as GMain

#webserver imports
import urllib.parse

logger = logging.getLogger("Client")

DEBUG = False
ITEMS_HANDLING = 0b111




class TrackerCommandProcessor(ClientCommandProcessor):

    def _cmd_update(self):
        """Print the Updated Accessable Location set"""
        #self.ctx.tracker_page.content.data = new_data = []
        updateTracker(self.ctx)

    def _cmd_inventory(self):
        """Print the list of current items in the inventory"""
        logger.info("Current Inventory:")
        for item in self.ctx.items_received:
            logger.info( self.ctx.multiworld.worlds[self.ctx.player_id].item_id_to_name[item[0]])


class TrackerGameContext(CommonContext):
    from kvui import GameManager
    game = ""
    httpServer_task: typing.Optional["asyncio.Task[None]"] = None
    tags = CommonContext.tags|{"Tracker"}
    command_processor = TrackerCommandProcessor
    tracker_page = None
    watcher_task = None
    update_callback: Callable[[list[str]], bool] = None
    gen_error = None

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.items_handling = ITEMS_HANDLING
        self.locations_checked = []
        self.datapackage = []
        self.multiworld:MultiWorld = None
        self.player_id = None

    def clear_page(self):
        if self.tracker_page is not None:
            self.tracker_page.resetData()

    def log_to_tab(self,line: str, sort:bool = False):
        if self.tracker_page is not None:
            self.tracker_page.addLine(line,sort)

    def set_callback(self,func:Callable[[list[str]],bool]):
        self.update_callback = func

    def build_gui(self,manager : GameManager):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.tabbedpanel import TabbedPanelItem
        from kivy.uix.recycleview import RecycleView


        class TrackerLayout(BoxLayout):
            pass

        class TrackerView(RecycleView):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.data = []
                self.data.append({"text":"Tracker Initializing"})
            
            def resetData(self):
                self.data.clear()

            def addLine(self, line:str,sort:bool = False):
                self.data.append({"text":line})
                if sort:
                    self.data.sort(key=lambda e: e["text"])

        tracker_page = TabbedPanelItem(text="Tracker Page")
        
        try:
            tracker = TrackerLayout(orientation="horizontal")
            tracker_view = TrackerView()
            tracker.add_widget(tracker_view)
            self.tracker_page = tracker_view
            tracker_page.content = tracker
            if self.gen_error is not None:
                for line in self.gen_error.split("\n"):
                    self.log_to_tab(line,False)
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)
        manager.tabs.add_widget(tracker_page)
        

    def run_gui(self):
        from kvui import GameManager

        class TrackerManager(GameManager):
            logging_pairs = [
                ("Client","Archipelago")
            ]
            base_title = "Archipelago Tracker Client"


            def build(self):
                container = super().build()
                self.tabs.do_default_tab = True
                self.tabs.current_tab.height = 40
                self.tabs.tab_height = 40
                self.ctx.build_gui(self)
                
                return container


        self.ui = TrackerManager(self)
        self.load_kv()
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
        return self

    def load_kv(self):
        from kivy.lang import Builder
        import pkgutil

        data = pkgutil.get_data(TrackerWorld.__module__, "Tracker.kv").decode()
        Builder.load_string(data)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TrackerGameContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            if self.multiworld is None:
                self.log_to_tab("Internal world was not able to be generated, check your yamls and relaunch",False)
                return
            player_ids = [i for i,n in self.multiworld.player_name.items() if n==self.username]
            if len(player_ids) < 1:
                self.log_to_tab("Player's Yaml not in tracker's list",False)
                return
            self.player_id = player_ids[0] #should only really ever be one match

            if callable(getattr(self.multiworld.worlds[self.player_id],"interpret_slot_data",None)):
                self.multiworld.worlds[self.player_id].interpret_slot_data(args["slot_data"])

            updateTracker(self)
            self.watcher_task = asyncio.create_task(game_watcher(self), name="GameWatcher")
        elif cmd == 'RoomUpdate':
            updateTracker(self)
    
    def run_generator(self):
        try:
            #strip command line args, they won't be useful from the client anyway
            sys.argv = sys.argv[:1]
            GMain(None, self.TMain)
        except Exception as e:
            tb = traceback.format_exc()
            self.gen_error = tb
            logger.error(tb)

    def TMain(self, args, seed=None, baked_server_options: Optional[Dict[str, object]] = None):
        
        if not baked_server_options:
            baked_server_options = get_settings().server_options.as_dict()
        assert isinstance(baked_server_options, dict)
        if args.outputpath:
            os.makedirs(args.outputpath, exist_ok=True)
            output_path.cached_path = args.outputpath

        start = time.perf_counter()
        # initialize the world
        world = MultiWorld(args.multi)

        logger = logging.getLogger()
        world.set_seed(seed, args.race, str(args.outputname) if args.outputname else None)
        world.plando_options = args.plando_options

        world.shuffle = args.shuffle.copy()
        world.logic = args.logic.copy()
        world.mode = args.mode.copy()
        world.difficulty = args.difficulty.copy()
        world.item_functionality = args.item_functionality.copy()
        world.timer = args.timer.copy()
        world.goal = args.goal.copy()
        world.boss_shuffle = args.shufflebosses.copy()
        world.enemy_health = args.enemy_health.copy()
        world.enemy_damage = args.enemy_damage.copy()
        world.beemizer_total_chance = args.beemizer_total_chance.copy()
        world.beemizer_trap_chance = args.beemizer_trap_chance.copy()
        world.countdown_start_time = args.countdown_start_time.copy()
        world.red_clock_time = args.red_clock_time.copy()
        world.blue_clock_time = args.blue_clock_time.copy()
        world.green_clock_time = args.green_clock_time.copy()
        world.dungeon_counters = args.dungeon_counters.copy()
        world.triforce_pieces_available = args.triforce_pieces_available.copy()
        world.triforce_pieces_required = args.triforce_pieces_required.copy()
        world.shop_shuffle = args.shop_shuffle.copy()
        world.shuffle_prizes = args.shuffle_prizes.copy()
        world.sprite_pool = args.sprite_pool.copy()
        world.dark_room_logic = args.dark_room_logic.copy()
        world.plando_items = args.plando_items.copy()
        world.plando_texts = args.plando_texts.copy()
        world.plando_connections = args.plando_connections.copy()
        world.required_medallions = args.required_medallions.copy()
        world.game = args.game.copy()
        world.player_name = args.name.copy()
        world.sprite = args.sprite.copy()
        world.glitch_triforce = args.glitch_triforce  # This is enabled/disabled globally, no per player option.

        world.set_options(args)
        world.set_item_links()
        world.state = CollectionState(world)
        logger.info('Archipelago Version %s  -  Seed: %s\n', __version__, world.seed)

        logger.info(f"Found {len(AutoWorld.AutoWorldRegister.world_types)} World Types:")
        longest_name = max(len(text) for text in AutoWorld.AutoWorldRegister.world_types)

        max_item = 0
        max_location = 0
        for cls in AutoWorld.AutoWorldRegister.world_types.values():
            if cls.item_id_to_name:
                max_item = max(max_item, max(cls.item_id_to_name))
                max_location = max(max_location, max(cls.location_id_to_name))

        item_digits = len(str(max_item))
        location_digits = len(str(max_location))
        item_count = len(str(max(len(cls.item_names) for cls in AutoWorld.AutoWorldRegister.world_types.values())))
        location_count = len(str(max(len(cls.location_names) for cls in AutoWorld.AutoWorldRegister.world_types.values())))
        del max_item, max_location

        for name, cls in AutoWorld.AutoWorldRegister.world_types.items():
            if not cls.hidden and len(cls.item_names) > 0:
                logger.info(f" {name:{longest_name}}: {len(cls.item_names):{item_count}} "
                            f"Items (IDs: {min(cls.item_id_to_name):{item_digits}} - "
                            f"{max(cls.item_id_to_name):{item_digits}}) | "
                            f"{len(cls.location_names):{location_count}} "
                            f"Locations (IDs: {min(cls.location_id_to_name):{location_digits}} - "
                            f"{max(cls.location_id_to_name):{location_digits}})")

        del item_digits, location_digits, item_count, location_count

        # This assertion method should not be necessary to run if we are not outputting any multidata.
        if not args.skip_output:
            AutoWorld.call_stage(world, "assert_generate")

        AutoWorld.call_all(world, "generate_early")

        logger.info('')

        for player in world.player_ids:
            for item_name, count in world.worlds[player].options.start_inventory.value.items():
                for _ in range(count):
                    world.push_precollected(world.create_item(item_name, player))

            for item_name, count in world.start_inventory_from_pool.setdefault(player, StartInventoryPool({})).value.items():
                for _ in range(count):
                    world.push_precollected(world.create_item(item_name, player))
                # remove from_pool items also from early items handling, as starting is plenty early.
                early = world.early_items[player].get(item_name, 0)
                if early:
                    world.early_items[player][item_name] = max(0, early-count)
                    remaining_count = count-early
                    if remaining_count > 0:
                        local_early = world.early_local_items[player].get(item_name, 0)
                        if local_early:
                            world.early_items[player][item_name] = max(0, local_early - remaining_count)
                        del local_early
                del early

        logger.info('Creating World.')
        AutoWorld.call_all(world, "create_regions")

        logger.info('Creating Items.')
        AutoWorld.call_all(world, "create_items")

        logger.info('Calculating Access Rules.')

        for player in world.player_ids:
            # items can't be both local and non-local, prefer local
            world.worlds[player].options.non_local_items.value -= world.worlds[player].options.local_items.value
            world.worlds[player].options.non_local_items.value -= set(world.local_early_items[player])

        AutoWorld.call_all(world, "set_rules")


        self.multiworld = world
        return

def updateTracker(ctx: TrackerGameContext):
    if ctx.player_id is None or ctx.multiworld is None:
        logger.error("Player YAML not installed or Generator failed")
        ctx.log_to_tab("Check Player YAMLs for error",False)
        return

    state = CollectionState(ctx.multiworld)
    state.sweep_for_events(location for location in ctx.multiworld.get_locations() if not location.address)

    callback_list = []

    for item in ctx.items_received:
        state.collect(ctx.multiworld.create_item(ctx.multiworld.worlds[ctx.player_id].item_id_to_name[item[0]],ctx.player_id))

    state.sweep_for_events(location for location in ctx.multiworld.get_locations() if not location.address)
    
    ctx.clear_page()
    for temp_loc in ctx.multiworld.get_reachable_locations(state,ctx.player_id):
        if temp_loc.address == None:
            continue
        if (temp_loc.address in ctx.missing_locations):
            #logger.info("YES rechable (" + temp_loc.name + ")")
            if temp_loc.parent_region is None:
                ctx.log_to_tab("|" + temp_loc.name ,True)
            else:
                ctx.log_to_tab(temp_loc.parent_region.name + " | " + temp_loc.name,True )
            callback_list.append(temp_loc.name)
    ctx.tracker_page.refresh_from_data()
    if ctx.update_callback is not None:
        ctx.update_callback(callback_list)
    if len(callback_list) == 0:
        ctx.log_to_tab("Nothing! Congrats!")

async def game_watcher(ctx: TrackerGameContext) -> None:
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
        except asyncio.TimeoutError:
            continue
        ctx.watcher_event.clear()
        try:
            updateTracker(ctx)
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)


async def main(args):
 
    ctx = TrackerGameContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    ctx.run_generator()

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():

    parser = get_base_parser(description="Gameless Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args()

    if args.url:
        url = urllib.parse.urlparse(args.url)
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)


    asyncio.run(main(args))