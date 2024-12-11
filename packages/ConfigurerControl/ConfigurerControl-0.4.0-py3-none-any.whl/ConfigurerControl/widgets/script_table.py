from dataclasses import dataclass, field
from typing import Optional
from ConfigurerControl.widgets.base import CidPar, CDT, Array
from DLMS_SPODES.cosem_interface_classes import script_table
from tKot.common import Point
from . import colors


@dataclass
class Script(CDT):

    def __post_init__(self):
        self._height = self.font_.measure("00000")
        """height of cube"""
        self.label_cid: Optional[int] = None

    def place2(self, p: Point, data: script_table.Script) -> Point:
        size = Point(self._height, self._height)
        self.can.create_rectangle(
            *p,
            *(p+size),
            width=2,
            fill=colors.day_profile_action_color.get(int(data.script_identifier), colors.DEFAULT).back
        )
        self.label_cid = self.can.create_text(
            *(p + size // 2),
            text=str(data.script_identifier),
            fill=colors.day_profile_action_color.get(int(data.script_identifier), colors.DEFAULT).fill,
            font=self.font_)
        return Point(self._height, self._height)

    def get_select2(self, cids: tuple[int, ...], cidpar: list[CidPar]):
        if self.label_cid in cids:
            cidpar.append(CidPar(self.label_cid, self.param + b'\x00'))


@dataclass
class Scripts(Array):
    elements: list[Script] = field(init=False, default_factory=list)
    el_t: Script = field(init=False, default=Script)

    def place2(self, p: Point, data: script_table.Scripts) -> Point:
        return self.place_horizontal(p, data)
