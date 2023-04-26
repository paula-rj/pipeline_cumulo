# --------------------
# IMPORTS
# --------------------

import atexit
from io import BytesIO
import json
import os
import pathlib
import tempfile

from diskcache import Cache
from diskcache.core import ENOVAL
import sh

import pipeline

# ------------------------------------------------------------
# GLOBALS
# ------------------------------------------------------------
PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
CACHE_PATH = PATH / "data/cache"
HOME = pathlib.Path(os.path.expanduser("~"))

# CACHE_PATH = pathlib.Path(os.path.expanduser(os.path.join("~", "cache")))
cache = Cache(directory="CACHE_PATH")
cache.set("key", BytesIO(b"value"), expire=None, read=True)


@cache.memoize(typed=True, expire=None, tag="fib")
def product_parser(tmp_path, url):
    """
    Parameters:
    -----------
    tmp_path: str or Path
        temporary container where the file will be stored.
    url: str
        Retrieves link desde donde bajar.
    """
    sh.wget("-O", tmp_path, url)  # aca va tmp


# ---------------------------------------
# PROCESS
# ---------------------------------------

# input: json de cada MES
path_json = "pipeline_cumulo/links_dir/2016_02.json"
new_dir = path_json[-12:-5]  # Guarda la parte de la fecha
f = open(path_json)
links = json.load(f)

# iteracion sobre los dias -> da lista de urls de cada dia
# for day in links.keys():

# iteracion sobre la lista -> da 1 url
links_list = links["2016052"]
for url in links_list[1:]:
    # Extracts file name from full url
    date = url[90:104][3:].replace(".", "")

    # Generates temp file to store downloaded file
    _, tmp_path = tempfile.mkstemp(suffix=".nc", prefix=date, dir=None, text=False)
    atexit.register(os.remove, tmp_path)

    # If file not already in cache, downloads it
    result = cache.get(tmp_path, default=ENOVAL, retry=True)  # aca va tmp
    if result is ENOVAL:
        result = product_parser(tmp_path, url)

    # Extracts bands as np arrays
    # nc_file = pipeline.zip_to_nc(nc_file_name="A2016.001.0200.nc")
    norm_bands = pipeline.processing(tmp_path)

    # estos son h5 que se guarda en la memoria
    a = pipeline.generate_tiles(norm_bands, url[90:104])


# sh.rm(f"data/{js_keys[KEYN]}.zip")im
# cache = Cache()
# cache.set("key", BytesIO(b"value"), expire=None, read=True)
# juan
# from diskcache import FanoutCache, Cache, JSONDisk, core
# cache = Cache(directory="cache")
# def download_data(a):
#    ... return

# @cache.memoize(typed=True, expire=None, tag="fib")
# def load_image(a, k=1):
#    data = download_data(a)
#    return str(a) + "hola"


# cache.directory
# core.args_to_key(("load_image",), ("35",), {"k": 1}, True, set())
# cache.expire()
