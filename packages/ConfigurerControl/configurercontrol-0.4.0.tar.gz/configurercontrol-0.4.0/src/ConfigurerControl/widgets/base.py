from abc import ABC, abstractmethod
from functools import cached_property
from dataclasses import dataclass, field
from tkinter import font
from copy import copy
import tkinter as tk
from typing import TypeAlias, Self
from DLMS_SPODES.types import cdt
from PIL.ImageChops import offset
from tKot.common import Point


IID: TypeAlias = str
Parameter: TypeAlias = bytes


@dataclass
class IIDContainer(ABC):
    """name field iid"""


@dataclass
class CidPar:
    cid: int
    par: Parameter

    def __lt__(self, other: Self):
        if len(self.par) > len(other.par):
            return True
        else:
            return False


@dataclass
class ObjListWidget(ABC):
    can: tk.Canvas
    iids: IIDContainer
    cid: int = field(init=False, default=None)
    """ common widget CID"""

    def find_ids(self, e: tk.Event) -> tuple[int, ...]:
        """ find canvas IDs by event. Clear day_info if not selected """
        y = self.can.canvasy(e.y)
        x = self.can.canvasx(e.x)
        result = self.can.find_overlapping(x-3, y-3, x+3, y+3)
        return result

    @abstractmethod
    def get_event(self, e: tk.Event) -> int | None:
        """"""

    @abstractmethod
    def update_data(self, iid: IID, value: cdt.CommonDataType):
        pass

    @abstractmethod
    def place(self, x: int, y: int):
        pass

    @cached_property
    @abstractmethod
    def size(self) -> Point:
        """ x, y size widget depend from font size"""


@dataclass
class CDT(ABC):
    """widget for DLMSCommonDataType"""
    can: tk.Canvas
    param: bytes
    font_: font.Font
    """bind with font size"""
    name: str = None
    """name of widget"""
    cid: int = field(init=False)
    size: Point = field(init=False)

    def __post_init__(self):
        print(F"{self.__class__.__name__}: {self.param}")

    def place(self, p: Point,  data: cdt.CommonDataType | tuple[cdt.CommonDataType, ...]) -> Point:
        m_p = copy(p)
        self.size = Point()
        self.cid = self.can.create_rectangle(
            0,0,0,0,
            width=1 if isinstance(self, Array) else 0,
            fill="white")
        if self.name is not None:
            self.can.create_text(
                *p,
                text=self.name,
                anchor=tk.NW)
            m_p.y += self.font_.metrics("linespace")
        self.size = self.place2(m_p, data)
        self.can.coords(
            self.cid,
            *m_p,
            *(self.size + m_p))
        self.size.y += (m_p.y - p.y)
        return self.size

    @abstractmethod
    def place2(self, p: Point, data: cdt.CommonDataType | tuple[cdt.CommonDataType, ...]) -> Point:
        """place and return size"""

    def get_select(self, cids: tuple[int, ...], cidpar: list[CidPar]):
        self.get_select2(cids, cidpar)
        if self.cid in cids:
            cidpar.append(CidPar(self.cid, self.param))

    @abstractmethod
    def get_select2(self, cids: tuple[int, ...], cidpar: list[CidPar]):
        """return iid and nested params in bytes"""

    def get_new(self, par: Parameter, point: Point, data_t: type[cdt.CommonDataType]) -> cdt.CommonDataType:
        pass


class Simple(CDT, ABC):
    def get_select2(self, cids: tuple[int, ...], cidpar: list[CidPar]):
        """nothing select"""


class Array(CDT, ABC):
    elements: list[CDT]
    offset: int = 10
    el_t: type[CDT] = field(init=False, default=None)

    def get_select2(self, cids: tuple[int, ...], cidpar: list[CidPar]):
        for el in self.elements:
            el.get_select(cids, cidpar)

    def place_horizontal(self, p: Point, data: cdt.CommonDataType) -> Point:
        i: int
        el: cdt.CommonDataType
        size = Point(0, self.offset)
        for i, el in enumerate(data):
            size.x += self.offset
            self.elements.append(self.el_t(
                can=self.can,
                param=self.param + i.to_bytes(1),
                font_=self.font_
            ))
            size.x += self.elements[-1].place(p + size, el).x + self.offset
        if self.elements:
            size.y += self.elements[-1].size.y
        else:  # empty array
            size.x += 2*self.offset
        size.y += self.offset
        return size

    def place_horizontal2(self, p: Point, data: tuple[cdt.CommonDataType, cdt.CommonDataType]) -> Point:
        i: int
        el: cdt.CommonDataType
        size = Point(0, self.offset)
        data, add_data = data
        for i, el in enumerate(data):
            size.x += self.offset
            self.elements.append(self.el_t(
                can=self.can,
                param=self.param + i.to_bytes(1),
                font_=self.font_
            ))
            size.x += self.elements[-1].place(p + size, (el, add_data)).x + self.offset
        if self.elements:
            size.y += self.elements[-1].size.y
        else:  # empty array
            size.x += 2*self.offset
        size.y += self.offset
        return size
