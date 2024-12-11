import datetime
import tkinter as tk
import math
from typing import Optional
from tkinter import font
from dataclasses import dataclass, field
from DLMS_SPODES.cosem_interface_classes import activity_calendar
from .base import CDT, Array, Simple, CidPar
from tKot.common import Point
from . import colors


@dataclass
class DaySchedule(CDT):
    with_time: bool = True
    day_c_id: int = field(init=False)

    def __post_init__(self):
        self._day_width = self.font_.measure("00:00")
        self._day_height = self._day_width * 7
        """ width of one day widget """
        self._font_height = self.font_.metrics('linespace')
        self.actions_cids: list[int] = list()
        """sort according with timestamp"""
        self.actions_label_cids: list[int] = list()
        """sort according with timestamp"""
        self.output_indexes: list[int] = list()
        """according with input value"""
        self.action_sel: int | None = None

    def place2(self, p: Point, data: activity_calendar.DaySchedule) -> Point:
        d_p_a: activity_calendar.DayProfileAction

        def get_pos(value: datetime.time, width: int) -> int:
            """ return position coordinate by width """
            return round((value.hour * 60 + value.minute) / 1440 * width)

        size = Point(self._day_width, self._day_height)
        self.day_c_id = self.can.create_rectangle(
            *p,
            *(p + size),
            width=2,
            fill='white')
        for d_p_a in sorted(data):
            action_p = p + Point(y=get_pos(t := d_p_a.start_time.decode(), self._day_height))
            color = colors.day_profile_action_color.get(int(d_p_a.script_selector), colors.DEFAULT)
            self.actions_cids.insert(0, self.can.create_rectangle(  # big time is first for action select
                *action_p,
                *(p + size),
                fill=color.back,
            ))
            self.output_indexes.append(data.values.index(d_p_a))
            if self.with_time:
                self.actions_label_cids.insert(0, self.can.create_text(
                    *action_p,
                    text=t.isoformat('minutes'),
                    anchor=tk.NW,
                    fill=color.fill,
                    font=self.font_
                ))
        self.output_indexes.reverse()
        return size

    def get_select2(self, cids: tuple[int, ...], cidpar: list[CidPar]):
        i: int
        for i, cid, l_cid in zip(self.output_indexes, self.actions_cids, self.actions_label_cids):
            if cid in cids:
                if self.action_sel is not None:
                    self.can.itemconfigure(
                        tagOrId=self.actions_cids[self.action_sel],
                        width=1)
                    print(F"{self.action_sel=}")
                self.action_sel = i
                self.can.itemconfigure(
                    tagOrId=cid,
                    width=3)
                cidpar.append(CidPar(self.cid, self.param + i.to_bytes(1, "big")))  # return cid all Schedule
            if l_cid in cids:
                cidpar.append(CidPar(l_cid, self.param + i.to_bytes(1, "big") + b'\x00'))  # add start_time


@dataclass
class DayID(Simple):
    cid: int = field(init=False)

    def __post_init__(self):
        self._day_height = self.font_.measure("00:00")
        self.__big_font = font.Font(
            root=self.can,
            family=self.font_.cget("family"),
            size=int(self.font_.cget("size")*1.2))

    def place2(self, p: Point, data: activity_calendar.cdt.Unsigned) -> Point:
        size = Point(self._day_height, self._day_height)
        self.cid = self.can.create_rectangle(
            *p,
            *(p + size),
            fill='white')
        self.can.create_text(
            *(p + size // 2),
            text=str(data),
            font=self.__big_font)
        return size


@dataclass
class DayProfile(Array):
    elements: tuple[DayID, DaySchedule] = field(init=False)
    d_s: DaySchedule = field(init=False)

    def __post_init__(self):
        print(F"{self.__class__.__name__}: {self.param}")
        self._day_height = self.font_.measure("00:00")
        self._day_width = self._day_height * 7
        """ width of one day widget """
        self.__offset = self.font_.metrics('linespace')
        self.__big_font = font.Font(
            root=self.can,
            family=self.font_.cget("family"),
            size=int(self.font_.cget("size")*1.2))

    def place2(self, p: Point, data: activity_calendar.DayProfile) -> Point:
        param = bytearray(self.param)
        param.append(0)
        did = DayID(
            can=self.can,
            param=bytes(param),
            font_=self.font_)
        did.place(p, data.day_id)
        param[-1] = 1
        d_s_p = p + Point(y=did.size.y)
        self.d_s = DaySchedule(
            can=self.can,
            param=bytes(param),
            font_=self.font_)
        self.d_s.place(d_s_p, data.day_schedule)
        self.elements = (did, self.d_s)
        return Point(
            self.d_s.size.x,
            did.size.y + self.d_s.size.y)


@dataclass
class DayProfileTable(Array):
    elements: list[DayProfile] = field(init=False, default_factory=list)
    el_t: CDT = field(init=False, default=DayProfile)

    def place2(self, p: Point, data: activity_calendar.DayProfileTable) -> Point:
        return self.place_horizontal(p, data)


@dataclass
class WeekProfile(CDT):
    def __post_init__(self):
        self.__days = ("пн", "вт", "ср", "чт", "пт", "сб", "вс")
        self.__size = self.font_.measure("0000")
        self.elements: list[int] = [-1]  # week_profile_name not use(-1)
        self.name_cid: Optional[int] = None

    def place2(self, p: Point, data: tuple[activity_calendar.WeekProfile, activity_calendar.DayProfileTable]) -> Point:
        x, y = p
        w_p, d_p_t = data
        diam = int(self.__size * 5)
        big_diam = int(self.__size * 6)
        day_degree = 360 / 7
        """degree of one day"""
        day_rad = 2 * math.pi / 7
        """radians in one day"""
        t_r = int(diam*0.7)
        """text radius"""
        i_r = int(diam*0.25)
        """index radius"""
        c = big_diam // 2
        """center"""
        x_off = x+self.__size
        """offset to x"""
        y_off = y+self.__size
        """offset to y"""
        a_width = int(self.__size*1.2)
        """action color width"""
        self.name_cid = self.can.create_text(
            x_off+c, y,
            anchor=tk.CENTER,
            text=w_p.week_profile_name.to_str(encoding="utf-8"))
        for i in range(7):
            self.elements.insert(1, self.can.create_arc(
                x_off, y_off,
                x_off+big_diam, y_off+big_diam,
                extent=day_degree,
                start=day_degree * i,
                fill="white",
                style=tk.PIESLICE))
        for i, v in zip(range(7), tuple(w_p)[1:]):
            r = day_rad * (i + 0.5)
            self.can.create_text(
                x_off + c + math.cos(r) * t_r, y_off + c + math.sin(r) * t_r,
                text=self.__days[i])
            self.can.create_text(
                x_off + c + math.cos(r) * i_r, y_off + c + math.sin(r) * i_r,
                text=str(v))
            if d_p_t:
                offset = (big_diam - diam) // 2
                for d_p in d_p_t:
                    d_p: activity_calendar.DayProfile
                    if v == d_p.day_id:
                        for d_p_a in sorted(d_p.day_schedule):
                            d_p_a: activity_calendar.DayProfileAction
                            self.can.create_arc(
                                x_off+offset, y_off+offset, x_off+diam + offset, y_off+diam + offset,
                                extent=min(359.9, 360 - day_degree*(i+(d_p_a.start_time.hour * 60 + d_p_a.start_time.minute) / 1440)),
                                start=0,
                                outline=colors.day_profile_action_color.get(int(d_p_a.script_selector), colors.DEFAULT).back,
                                style=tk.ARC,
                                width=a_width)
        return Point(big_diam+self.__size*2, big_diam+self.__size*2)

    def get_select2(self, cids: tuple[int, ...], cidpar: list[CidPar]):
        if self.name_cid in cids:
            cidpar.append(CidPar(self.name_cid, bytes(self.param) + b'\x00'))
        for i, cid in enumerate(self.elements):
            if cid in cids:
                param = bytearray(self.param)
                param.append(i)
                cidpar.append(CidPar(cid, bytes(param)))


@dataclass
class WeekProfileTable(Array):
    elements: list[WeekProfile] = field(init=False, default_factory=list)
    el_t: CDT = field(init=False, default=WeekProfile)

    def place2(self, p: Point, data: tuple[activity_calendar.WeekProfileTable, activity_calendar.DayProfileTable]) -> Point:
        return self.place_horizontal2(p, data)
