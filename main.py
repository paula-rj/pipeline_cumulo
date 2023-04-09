# ------------------
# IMPORTS
# ------------------
from io import BytesIO
import os
import json
import pathlib

from diskcache import Cache
from diskcache.core import ENOVAL
import sh

import pipeline

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
CACHE_PATH = PATH / "data/cache"
# CACHE_PATH = pathlib.Path(os.path.expanduser(os.path.join("~", "cache")))
KEYN = 1

cache = Cache(directory="CACHE_PATH")
cache.set("key", BytesIO(b"value"), expire=None, read=True)

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


# for i in list json
with open("urls.json") as json_file:
    json_load = json.load(json_file)
    js_keys = list(json_load.keys())


@cache.memoize(typed=True, expire=None, tag="fib")
def product_parser(key_num=KEYN):
    """
    Parameters:
    -----------
    key_num: int
    number of key in list of  json keys
    la idea es iterar sobre esa lista
    """
    date_key = js_keys[key_num]
    dropbox_dir = "https://www.dropbox.com/sh/i3s9q2v2jjyk2it/AACQ1-eFbBvdwX6jBXzEAkXba/2016/01/001/daylight?dl=1"  # json_load[date_key]
    sh.wget("-O", f"data/{date_key}.zip", dropbox_dir)


result = cache.get(f"data/{js_keys[KEYN]}.zip", default=ENOVAL, retry=True)
if result is ENOVAL:
    result = product_parser()  # esto

# for file in zip: ... que extraiga cada archivo del zip
# name = file.name
nc_file = pipeline.zip_to_nc(nc_file_name="A2016.001.0200.nc")
norm_bands = pipeline.processing(nc_file)
a = pipeline.generate_tiles(
    norm_bands
)  # -> estos son h5 que se guarda en la memoria o ftp

# sh.rm(f"data/{js_keys[KEYN]}.zip")
