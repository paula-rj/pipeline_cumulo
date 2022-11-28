import json
import os
from zipfile import ZipFile
from io import BytesIO
import pathlib

import dateutil.parser

# import h5py
from diskcache import Cache
from diskcache.core import ENOVAL
import netCDF4 as nc
import numpy as np
import sh
import ipdb

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

CACHE_PATH = PATH / "data/cache"


# for i in list json
with open("urls.json") as json_file:
    json_load = json.load(json_file)

# downloads the product
# Cachea files
cache = Cache(directory="CACHE_PATH")


@cache.memoize(typed=True, expire=None, tag="fib")
def product_parser(date_key="2016001"):
    dropbox_dir = json_load[date_key]
    sh.wget("-O", f"data/{date_key}.zip", dropbox_dir)


# cache.set('key', BytesIO(b'value'), expire=None, read=True)
result = cache.get("/data/2016001.zip", default=ENOVAL, retry=True)

if result is ENOVAL:
    result = product_parser()  # esto


# for...itera sobre todos los files
# extracts files from zip and opens as netcdf
def zip_to_nc(
    zip_file="daylight?dl=0&subfolder_nav_tracking=1.zip",
    nc_file_name="A2016.001.2330.nc",
):
    with ZipFile(zip_file, "r") as zip:
        data = zip.read(nc_file_name)
        ds = nc.Dataset(nc_file_name, mode="r", memory=data)
        return ds


def processing(nc_file):
    """Extracts bands form netcdf
    and get them ready"""
    band_dict = {
        "b1": "ev_250_aggr1km_refsb_1",  # vis
        "b2": "ev_250_aggr1km_refsb_2",  # vis
        "b22": "ev_1km_emissive_22",  # 3.9
        "b26": "ev_1km_refsb_26",  # rari
        "b29": "ev_1km_emissive_29",
        "b34": "ev_1km_emissive_34",
    }

    list_bands = []
    # extraact bands and get them ready
    for key in band_dict:
        band = nc_file.variables[band_dict.get(key)][:].data
        band_ok = band.reshape([1354, 2030])
        list_bands.append(band_ok)

    all_bands = np.stack(list_bands, -1)
    list_norm_bands = []

    for i in range(6):
        norm_band = (all_bands[:, :, i] - all_bands[:, :, i].min()) / (
            all_bands[:, :, i].max() - all_bands[:, :, i].min()
        )
        list_norm_bands.append(norm_band)

    norm_bands = np.stack(list_norm_bands, -1)

    return norm_bands


def generate_tiles(bands_matrix):
    h_tiles_list = []
    pixel_list_height = np.arange(0, 1354, 128)
    pixel_list_lenght = np.arange(0, 2030, 128)
    conth = 0
    while conth + 1 <= len(pixel_list_height):
        height_tile = bands_matrix[
            pixel_list_height[conth] : pixel_list_height[conth + 1], :, :
        ]
        conth = conth + 1
        h_tiles_list.append(height_tile)
    return h_tiles_list

    # contl = 0
    # while contl+1<=len(pixel_list_lenght):
    #    lenght_tile = bands_matrix[:, pixel_list_lenght[contl]:pixel_list_lenght[contl+1], :]
    #    contl = contl + 1

    # with h5py.File("mytestfile.hdf5", "w") as f:
    #    dset = f.create_dataset("dataset_1", data = norm_bands)
