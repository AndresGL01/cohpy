from enum import Enum


class Codes(Enum):
    """
    Shortcut for leaderboards ID

    USF => American

    UKF => British

    GER => German

    DAK => Afrika Korps
    """
    USF1v1 = 2130255
    UKF1v1 = 2130257
    GER1v1 = 2130261
    DAK1v1 = 2130259

    USF2v2 = 2130300
    UKF2v2 = 2130302
    GER2v2 = 2130306
    DAK2v2 = 2130304

    USF3v3 = 2130329
    UKF3v3 = 2130331
    GER3v3 = 2130335
    DAK3v3 = 2130333

    USF4v4 = 2130353
    UKF4v4 = 2130356
    GER4v4 = 2130360
    DAK4v4 = 2130358


class SortType(Enum):
    """
    Shortcut for Type filter

    ELO => 0
    WINS => 1
    """
    ELO = 0
    WINS = 1
