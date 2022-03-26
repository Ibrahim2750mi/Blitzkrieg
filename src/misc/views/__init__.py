from misc.views.battle import Battle as Bat
from misc.views.map import Map as Ma


def Map(main_window, main_view):
    return Ma(main_window, main_view)


def Battle(main_window, main_view):
    return Bat(main_window, main_view)
