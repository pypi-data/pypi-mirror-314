"""dataclasses for interaction control module with view"""
import dataclasses
import logging
from dataclasses import dataclass
from enum import IntFlag, auto
from typing import Any, Self
from DLMS_SPODES.types.implementations import enums, bitstrings
from DLMSCommunicationProfile import communication_profile
from DLMS_SPODES.config_parser import config
from DLMS_SPODES.cosem_interface_classes.association_ln import mechanism_id
from DLMS_SPODES.hdlc import frame

logger = logging.getLogger(__name__)
logger.level = logging.INFO


class CommunicationChannel:
    """"""


@dataclass
class SerialPort(CommunicationChannel):
    port: str = "COM3"
    baudrate: str = "9600"


@dataclass
class RS485(SerialPort):
    """"""


@dataclass
class Network(CommunicationChannel):
    host: str = "127.0.0.1"
    port: str = "8888"


@dataclass
class KPZBLE1(CommunicationChannel):
    mac: str = "00:00:00:00:00:00"
    name: str = None
    rssi: int = None
    m_data: bytes = None
    """manufacture data"""

    def __lt__(self, other: Self):
        match self.rssi, other.rssi:
            case _, None:                return True
            case None, _:                return False
            case int() as f, int() as s: return f < s


type CommunicationTransport = SerialPort | RS485 | Network | KPZBLE1


class Representation(IntFlag):
    HEX = 0
    ASCII = auto()
    HIDDEN = auto()
    ASCII_HIDDEN = ASCII | HIDDEN


class Secret(bytes):
    """ representation for secret """
    __representation: Representation = Representation.HEX
    # used for set class property from instance

    def __setattr__(self, key, value):
        match key:
            case 'representation' if not isinstance(value, Representation): raise ValueError(F"Error representation type")
            case 'representation' as rep:                                   Secret.__representation = value
            case _:                                                         super().__setattr__(key, value)

    @property
    def representation(self) -> Representation:
        """used for set class property from instance"""
        return self.__representation

    @staticmethod
    def __hide_all(value: str) -> str:
        for char_ in filter(lambda it: it != ' ', value):
            value = value.replace(char_, '*')
        return value

    @classmethod
    def from_str(cls, value: str) -> bytes:
        if cls.__representation & Representation.ASCII:
            return cls(value.encode("cp1251"))
        else:
            return cls.fromhex(value)

    def __str__(self):
        if Representation.ASCII in self.__representation:
            value = self.decode("cp1251", "replace")
        else:
            value = self.hex()
        if Representation.HIDDEN in self.__representation:
            return self.__hide_all(value)
        else:
            return value


try:
    secret = config["VIEW"]["Secret"]
    value = Secret()
    if secret["ascii"]:
        value.representation = Representation.ASCII
    if secret["hidden"]:
        value.representation = Representation.HIDDEN | value.representation
    logger.error(F"install {Secret.__name__}: {Secret().representation.name}")
except KeyError as e:
    logger.warning(F"not set Secret-ASCII-HIDDEN: {e}")


@dataclass
class Parameters:
    """for send from CONTROL to VIEW"""
    client_id: str
    sap: enums.ClientSAP
    conformance: bitstrings.Conformance
    communication_transport: CommunicationTransport = None
    secret: Secret | None = None
    m_id: mechanism_id.MechanismIdElement = mechanism_id.NONE
    addr_size: frame.AddressLength = frame.AddressLength.AUTO
    response_timeout: int = 120
    com_profile: communication_profile.Parameters = None
    callback: Any = None
    """for return Parameters"""

    def copy(self):
        return dataclasses.replace(self)
