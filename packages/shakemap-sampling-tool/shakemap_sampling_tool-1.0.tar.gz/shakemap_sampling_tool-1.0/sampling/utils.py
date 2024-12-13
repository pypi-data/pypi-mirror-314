# stdlib imports
import codecs
import pathlib

SM_CONFIG = pathlib.Path.home() / ".shakemap" / "profiles.conf"


def get_row_col(geodict, lat, lon):
    ulx = geodict["xmin"]
    uly = geodict["ymax"]
    dx = geodict["dx"]
    dy = geodict["dy"]
    # check to see if we're in a scenario where the grid crosses the meridian
    if geodict["xmax"] < ulx and lon < 0:
        lon += 360

    col = (lon - ulx) / dx
    row = (uly - lat) / dy
    col = int(round(col))
    row = int(round(row))
    newlon = ulx + col * dx
    newlat = uly - row * dy
    return (row, col, newlat, newlon)


def get_products_path(eventid):
    if not SM_CONFIG.exists():
        raise FileNotFoundError(("Could not find ShakeMap " "path on local system."))

    encoding = open(SM_CONFIG, "rt").encoding
    lines = open(SM_CONFIG, "rt").readlines()
    profile = ""
    current_profile = ""
    data_path = None
    for line in lines:
        line = line.strip(codecs.BOM_UTF8.decode(encoding))
        if line.startswith("profile"):
            profile = line.split("=")[1].strip()
        if line.startswith("[["):
            current_profile = line.strip().strip("[").strip("]")
        if line.startswith("data_path") and current_profile == profile:
            data_path = line.split("=")[1].strip()
            break
    if data_path is None:
        raise FileNotFoundError(("Could not find ShakeMap " "path on local system."))
    product_folder = pathlib.Path(data_path) / eventid / "current" / "products"
    return product_folder
