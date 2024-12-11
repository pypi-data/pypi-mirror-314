import logging
from dataclasses import dataclass
from DLMS_SPODES.config_parser import get_values


@dataclass
class Color:
    fill: str
    back: str


DEFAULT = Color("white", "black")


day_profile_action_color: dict[int, Color] = {
    1: Color('black', '#EB4C42'),
    2: Color('black', '#50C878'),
    3: Color('black', '#6495ED'),
    4: Color('black', '#FFF44F')}

if _conf := get_values("VIEW", "day_profile_action_color"):
    for k, v in _conf.items():
        try:
            day_profile_action_color[int(k)] = Color(*v)
        except Exception as e:
            logging.error(F"in fill color: {e}")
