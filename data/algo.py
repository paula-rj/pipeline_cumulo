# main
# for i in json_list: ...

# Cache
from io import BytesIO
import os
import pathlib

from diskcache import Cache
from diskcache.core import ENOVAL

CACHE_PATH = pathlib.Path(os.path.expanduser(os.path.join("~", "cache")))

cache = Cache()
cache.set("key", BytesIO(b"value"), expire=None, read=True)


import diskcache

from diskcache import FanoutCache, Cache, JSONDisk, core

cache = Cache(directory="cache")


def download_data(a):
    ...
    return


@cache.memoize(typed=True, expire=None, tag="fib")
def load_image(a, k=1):
    data = download_data(a)
    return str(a) + "hola"


cache.directory

core.args_to_key(("load_image",), ("35",), {"k": 1}, True, set())


cache.expire()
