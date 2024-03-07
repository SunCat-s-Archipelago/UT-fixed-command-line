from typing import Callable, Dict, NamedTuple, Optional,TYPE_CHECKING

import random

from BaseClasses import Item, ItemClassification, MultiWorld

baseId = 219990

class GrimDawnItem(Item):
    game = "Grim Dawn"


class GrimDawnItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    quantity: int = 1
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True

_item_data_list: list[tuple[str,ItemClassification,int,int,Optional[Callable[[MultiWorld, int], bool]]]] = [
    ("Strange Key",                                         ItemClassification.progression,                  219990,                       1,                            None),
    ("5 Scrap",                                             ItemClassification.progression,                  219991,                       5,                            None),
    ("Flooded Passage Destroy Blockade",                    ItemClassification.progression,                  219992,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.one_shot.value == 1 or multiworld.worlds[player].options.lore.value == 1)),
    ("Lower Crossing Destroy Blockade",                     ItemClassification.progression,                  219993,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.lore.value == 1)),
    ("East Marsh Bridge Repair",                            ItemClassification.progression,                  219994,                       1,                            None),
    ("Warden Boss Door Unlock",                             ItemClassification.progression,                  219995,                       1,                            None),
    ("Arkovia Bridge Repair",                               ItemClassification.progression,                  219996,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    ("Arkovian Foothills Destroy Barricade",                ItemClassification.progression,                  219997,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    ("New Harbor Destroy Barricade",                        ItemClassification.progression,                  219998,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1 and multiworld.worlds[player].options.secret_chest.value == 1)),
    ("Prospector's Trail Destroy Barricade",                ItemClassification.progression,                  219999,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    ("Twin Falls Bridge Repair",                            ItemClassification.progression,                  220000,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    ("Homestead Side Doors Unlock",                         ItemClassification.progression,                  220001,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    ("Rotting Croplands Destroy South Blockade",            ItemClassification.progression,                  220002,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    ("Rotting Croplands Destroy North Blockade",            ItemClassification.progression,                  220003,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1 and multiworld.worlds[player].options.one_shot.value == 1)),
    ("Royal Hive Queen Door Unlock",                        ItemClassification.progression,                  220004,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    ("Conflagration Destroy Barricade",                     ItemClassification.progression,                  220005,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1 and multiworld.worlds[player].options.forbidden_dungeons.value == 1)),
    ("Homestead Main Doors Unlock",                         ItemClassification.progression,                  220006,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    ("Witch Gods Temple Unlock",                            ItemClassification.progression,                  220007,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    ("Fort Ikon Gate Unlock",                               ItemClassification.progression,                  220008,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    ("Fort Ikon Destroy Blockade",                          ItemClassification.progression,                  220009,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    ("Old Grove Bridge Repair",                             ItemClassification.progression,                  220010,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    ("Necropolis Bridge Repair",                            ItemClassification.progression,                  220011,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    ("Tomb of the Watchers Door Unlock",                    ItemClassification.progression,                  220012,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    ("Loghorrean Seal Unlock",                              ItemClassification.progression,                  220013,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    ("Gloomwald Destroy Blockade",                          ItemClassification.progression,                  220014,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Nane's Hideout Destroy Barricade",                    ItemClassification.progression,                  220015,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Ugdenbog Destroy Barricade",                          ItemClassification.progression,                  220016,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Forlorn Cellar Unlock",                               ItemClassification.progression,                  220017,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Altar of Rattosh Portal",                             ItemClassification.progression,                  220018,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Malmouth Bridge Lowered",                             ItemClassification.progression,                  220019,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Malmouth Sewers Destroy Blockade",                    ItemClassification.progression,                  220020,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Candle District Door Unlock",                         ItemClassification.progression,                  220021,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Steelcap District Door Unlock",                       ItemClassification.progression,                  220022,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Malmouth Harbor Destroy Barricade",                   ItemClassification.progression,                  220023,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Crown Hill Destroy Gates",                            ItemClassification.progression,                  220024,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Crown Hill Open Flesh Barrier",                       ItemClassification.progression,                  220025,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Fleshworks Open Flesh Barrier",                       ItemClassification.progression,                  220026,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Wightmire Bridge Repair",                             ItemClassification.useful,                       220027,                       1,                            None),
    ("Malmouth Harbor Shortcut",                            ItemClassification.useful,                       220028,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    ("Skill Points +4",                                     ItemClassification.useful,                       220029,                       0,                            lambda multiworld, player: False),
    ("Aether Crystals",                                     ItemClassification.filler,                       220030,                       0,                            lambda multiworld, player: False),
    ("Frozen Heart",                                        ItemClassification.filler,                       220031,                       0,                            lambda multiworld, player: False),
    ("Black Tallow",                                        ItemClassification.filler,                       220032,                       0,                            lambda multiworld, player: False),
    ("Blessed Steel",                                       ItemClassification.filler,                       220033,                       0,                            lambda multiworld, player: False),
    ("Chipped Claw",                                        ItemClassification.filler,                       220034,                       0,                            lambda multiworld, player: False),
    ("Hallowed Fang",                                       ItemClassification.filler,                       220035,                       0,                            lambda multiworld, player: False),
    ("Imbued Silver",                                       ItemClassification.filler,                       220036,                       0,                            lambda multiworld, player: False),
    ("Polished Emerald",                                    ItemClassification.filler,                       220037,                       0,                            lambda multiworld, player: False),
    ("Ectoplasm",                                           ItemClassification.filler,                       220038,                       0,                            lambda multiworld, player: False),
    ("Reinforced Shell",                                    ItemClassification.filler,                       220039,                       0,                            lambda multiworld, player: False),
    ("Riftstone",                                           ItemClassification.filler,                       220040,                       0,                            lambda multiworld, player: False),
    ("Rigid Shell",                                         ItemClassification.filler,                       220041,                       0,                            lambda multiworld, player: False),
    ("Severed Claw",                                        ItemClassification.filler,                       220042,                       0,                            lambda multiworld, player: False),
    ("Spined Carapace",                                     ItemClassification.filler,                       220043,                       0,                            lambda multiworld, player: False),
    ("Wardstone",                                           ItemClassification.filler,                       220044,                       0,                            lambda multiworld, player: False),
    ("Extra EXP",                                           ItemClassification.filler,                       220045,                       0,                            lambda multiworld, player: False),
    ("Relic - Calamity",                                    ItemClassification.useful,                       220046,                       0,                            lambda multiworld, player: False),
    ("Relic - Ruination",                                   ItemClassification.useful,                       220047,                       0,                            lambda multiworld, player: False),
    ("Relic - Equilibrium",                                 ItemClassification.useful,                       220048,                       0,                            lambda multiworld, player: False),
    ("Relic - Glacier",                                     ItemClassification.useful,                       220049,                       0,                            lambda multiworld, player: False),
    ("Relic - Squall",                                      ItemClassification.useful,                       220050,                       0,                            lambda multiworld, player: False),
    ("Relic - Inferno",                                     ItemClassification.useful,                       220051,                       0,                            lambda multiworld, player: False),
    ("Relic - Corruption",                                  ItemClassification.useful,                       220052,                       0,                            lambda multiworld, player: False),
    ("Relic - Sanctuary",                                   ItemClassification.useful,                       220053,                       0,                            lambda multiworld, player: False),
    ("Relic - Guile",                                       ItemClassification.useful,                       220054,                       0,                            lambda multiworld, player: False),
    ("Relic - Rampage",                                     ItemClassification.useful,                       220055,                       0,                            lambda multiworld, player: False),
    ("Relic - Mistborne Talisman",                          ItemClassification.useful,                       220056,                       0,                            lambda multiworld, player: False),
    ("Relic - Bladesworn Talisman",                         ItemClassification.useful,                       220057,                       0,                            lambda multiworld, player: False),
    ("Relic - Gunslinger Talisman",                         ItemClassification.useful,                       220058,                       0,                            lambda multiworld, player: False),
    ("Skeleton Keys",                                       ItemClassification.useful,                       220059,                       5,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1 and multiworld.worlds[player].options.forbidden_dungeons.value == 1)),
    ("Forbidden Door Unlock",                               ItemClassification.progression,                  220060,                       1,                            lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1 and multiworld.worlds[player].options.forbidden_dungeons.value == 1)),
]

relic_table = [
    "Relic - Calamity",
	"Relic - Ruination",
	"Relic - Equilibrium",
	"Relic - Glacier",
	"Relic - Squall",
	"Relic - Inferno",
	"Relic - Corruption",
	"Relic - Sanctuary",
	"Relic - Guile",
	"Relic - Rampage",
	"Relic - Mistborne Talisman",
	"Relic - Bladesworn Talisman",
	"Relic - Gunslinger Talisman",
]

_filler_data_table={
    "Relic":5,
    "Skill Points +4":15,
    "Aether Crystals":1,
    "Frozen Heart":1,
    "Black Tallow":1,
    "Blessed Steel":1,
    "Chipped Claw":1,
    "Hallowed Fang":1,
    "Imbued Silver":1,
    "Polished Emerald":1,
    "Ectoplasm":1,
    "Reinforced Shell":1,
    "Riftstone":1,
    "Rigid Shell":1,
    "Severed Claw":1,
    "Spined Carapace":1,
    "Wardstone":1,
    "Extra EXP":65
}

filler_table = [k for k,v in _filler_data_table.items()]
filler_weights = [v for k,v in _filler_data_table.items()]

def get_unique_relic(rand: random.Random) -> str:
    if len(get_unique_relic.local_relic_table) > 0:
        rand.shuffle( get_unique_relic.local_relic_table)
        return get_unique_relic.local_relic_table.pop()
    else:
        return ""
    
get_unique_relic.local_relic_table = relic_table.copy()


item_data_table: Dict[str, GrimDawnItemData] = { item[0]: GrimDawnItemData(code=item[2],can_create=(item[4] if item[4] is not None else (lambda multiworld, player: True)),type=(item[1]),quantity=(item[3])) for index,item in enumerate(_item_data_list)}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
