from enum import IntEnum, auto


class HandleAction(IntEnum):
    SET = auto()
    SEARCH = auto()
    GET_BLE_CHARACTERISTICS = auto()
    RELEASE_CLIENT = auto()
