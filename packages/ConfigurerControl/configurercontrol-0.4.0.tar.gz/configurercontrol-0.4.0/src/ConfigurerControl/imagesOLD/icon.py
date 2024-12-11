"""for keep registered tk image names"""
from typing import TypeAlias
import tkinter as tk


class Name(str):
    """for typing only"""


Icons: TypeAlias = dict[Name, tk.Image]
"""imagesOLD container"""

EXCHANGE = Name("exchange")
READY = Name("ready")
NO_TRANSPORT = Name("no_transport")
CONNECTED = Name("connected")
READ = Name("read")
NO_PORT = Name("no_port")
TIMEOUT = Name("timeout")
NO_ACCESS = Name("no_access")
ID_ERROR = Name("fingerprint")
STOP = Name("stop")
MANUAL_STOP = Name("handle_stop")
EXECUTE_ERROR = Name("execute_error")
MISSING_OBJ = Name("yellow_bagel")
VERSION_ERROR = Name("version_error")
UNKNOWN = Name("unknown")
