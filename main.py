# --------------------
# IMPORTS
# --------------------

from io import BytesIO
import os
import pathlib

from diskcache import Cache
from diskcache.core import ENOVAL
import sh

from pipeline_cumulo import pipeline

# -------------------------------
# GLOBALS
# ------------------------------------------------------------
PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
CACHE_PATH = PATH / "data/cache"
HOME = pathlib.Path(os.path.expanduser("~"))

# CACHE_PATH = pathlib.Path(os.path.expanduser(os.path.join("~", "cache")))
cache = Cache(directory="CACHE_PATH")
cache.set("key", BytesIO(b"value"), expire=None, read=True)

# Temporary container
# _, tmp_path = tempfile.mkstemp()
# atexit.register(os.remove, tmp_path)


@cache.memoize(typed=True, expire=None, tag="fib")
def product_parser(url):
    """
    Parameters:
    -----------
    key_num: url
        Retrieves link desde donde bajar
    """
    sh.wget("-O", f"pipeline_cumulo/data/{url[90:107]}", url)  # aca va tmp


# ---------------------------------------
# PROCESS
# ---------------------------------------

# for i in htmls dir
path_html = "pipeline_cumulo/htmls/2009001.html"
new_dir = path_html[22:-5]  # Guarda la parte de la fecha
links_list = pipeline.url_parser(path_html)


# for i in links_list[i]:
i = 0
link = links_list[i]
date = link[90:104][3:].replace(".", "")
result = cache.get(f"pipeline_cumulo/data/", default=ENOVAL, retry=True)  # aca va tmp
if result is ENOVAL:
    result = product_parser(link)


# nc_file = pipeline.zip_to_nc(nc_file_name="A2016.001.0200.nc")
norm_bands = pipeline.processing(f"pipeline_cumulo/data/{link[90:107]}")

a = pipeline.generate_tiles(
    norm_bands, new_dir, date
)  # -> estos son h5 que se guarda en la memoria o ftp


# sh.rm(f"data/{js_keys[KEYN]}.zip")


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
