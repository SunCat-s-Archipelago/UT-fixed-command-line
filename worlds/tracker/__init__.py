
from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def launch_client(*args):
    from .TrackerClient import launch as TCMain
    launch_subprocess(TCMain, name="Universal Tracker client")

class TrackerWorld:
    pass

components.append(Component("Universal Tracker", None, func=launch_client, component_type=Type.CLIENT))
