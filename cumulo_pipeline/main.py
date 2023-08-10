#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT (https://tldrlegal.com/license/mit-license)
# Copyright (c) 2023, Paula Romero Jure et al.
# All rights reserved.
# ==============================================================================
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

import numpy as np

import sh

import pipeline

r"""Modulo de automatizacion para descargar, recortar, testear img de CUMULO"""
# ------------------------------------------------------------
# GLOBALS
# ------------------------------------------------------------
PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
CACHE_PATH = PATH / "data/cache"
HOME = pathlib.Path(os.path.expanduser("~"))
PATH_FOR_HDF5 = pathlib.Path(os.path.abspath(os.path.dirname(__file__))) / "data"
LINKS_DIR = (
    pathlib.Path(os.path.abspath(os.path.dirname(__file__))) / "links_dir"
)

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


# ------------------------------------------------------------------------------
# PROCESS
# ------------------------------------------------------------------------------
links_by_month = os.listdir(LINKS_DIR)
# loop sobre json de cada MES
for path_json in links_by_month:
    new_dir = path_json[-12:-5]  # Guarda la parte de la fecha
    f = open(path_json)
    links = json.load(f)

    # iteracion sobre los dias -> da lista de urls de cada dia
    for day in links.keys():
        # iteracion sobre la lista -> da 1 url
        links_list = links[day]
        for url in links_list[1:]:
            # Extracts file name from full url
            date = url[90:104][3:].replace(".", "")

            # Generates temp file to store downloaded file
            _, tmp_path = tempfile.mkstemp(
                suffix=".nc", prefix=date, dir=None, text=False
            )
            atexit.register(os.remove, tmp_path)

            # If file not already in cache, downloads it
            result = cache.get(
                tmp_path, default=ENOVAL, retry=True
            )  # aca va tmp
            if result is ENOVAL:
                result = product_parser(tmp_path, url)

            # Extracts bands as np arrays
            # nc_file = pipeline.zip_to_nc(nc_file_name="A2016.001.0200.nc")
            norm_bands = pipeline.processing(tmp_path)

            # estos son h5 que se guarda en la memoria
            a = pipeline.generate_tiles(
                norm_bands, url[90:104], path_to_save=PATH_FOR_HDF5
            )

        files = os.listdir(PATH_FOR_HDF5)
        files.remove("cache")

        # Tests whether tiles are ok
        test_list = []
        for i in range(len(files)):
            test_list.append(pipeline.test_int(f"{PATH_FOR_HDF5}/{files[i]}"))

        print(len(test_list))

        arr = np.array(test_list)
        mal = np.argwhere(arr == 0)

        print(len(mal))

        for j in mal[:]:
            os.remove(f"{PATH_FOR_HDF5}/{files[j[0]]}")

    f.close()
