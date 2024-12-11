from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
import logging
from DLMS_SPODES.config_parser import get_values


conf = {
    "path": "./Themes",
    "theme": "light"
}


if toml_val := get_values("CONTROL", "themes"):
    conf.update(toml_val)
else:
    logging.warning("VIEW, ObjectList not find in config file")

if not (t_path := Path(F"{conf["path"]}/{conf["theme"]}")).exists():
    if not (themes := Path(F"{conf["path"]}")).exists():
        raise RuntimeError(F"themes folder: {themes.absolute()} not was find")
    if len(tmp := tuple(themes.iterdir())) == 0:
        raise RuntimeError("no one themes was find")
    else:
        t_path = tmp[0]  # choice first theme
        logging.warning(F"choice first theme: {t_path}")


DEFAULT = Image.new('RGB', (100, 100), 'white')
font = ImageFont.load_default(size=50)
pencil = ImageDraw.Draw(DEFAULT)
pencil.text(
    (50, 90),
    '?',
    anchor="ms",
    font=ImageFont.load_default(size=100),
    fill='red'
)


def get_image(name: str) -> Image:
    path = t_path / name
    if not path.is_file():
        logging.error(F"not find {name} image in {t_path}")
        return DEFAULT
    else:
        return Image.open(path)


activate = get_image("activate.png")
ascii_hex = get_image("ascii_hex.png")
back = get_image("back.png")
change = get_image("change.png")
connected = get_image("connected.png")
cycle = get_image("cycle.png")
delete = get_image("delete.png")
error = get_image("error.png")
exchange = get_image("exchange.png")
execute_error = get_image("execute_error.png")
fingerprint = get_image("fingerprint.png")
folder_tree = get_image("folder_tree.png")
group_select = get_image("group_check.png")
handle_stop = get_image("handle_stop.png")
key = get_image("key.png")
load_file = get_image("load_file.png")
lupe = get_image("lupe.png")
lock_view = get_image("lock_view.png")
no_access = get_image("no_access.png")
no_port = get_image("no_port.png")
no_transport = get_image("no_transport.png")
plus = get_image("plus.png")
read = get_image("read.png")
ready = get_image("ready.png")
receive = get_image("receive.png")
recv_all = get_image("recv_all.png")
relay_off = get_image("relay_off.png")
relay_on = get_image("relay_on.png")
send = get_image("send.png")
stop = get_image("stop.png")
stop_exchange = get_image("stop_exchange.png")
sync = get_image("sync.png")
target = get_image("target.png")
timeout = get_image("timeout.png")
unknown = get_image("unknown.png")
upgrade = get_image("upgrade.png")
version_error = get_image("version_error.png")
yellow_bagel = get_image("yellow_bagel.png")

dlms: dict[int, Image] = {
    1:  get_image("Data.png"),
    3:  get_image("Register.png")
}