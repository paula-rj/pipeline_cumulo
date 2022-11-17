import json
import os
from zipfile import ZipFile
from io import BytesIO
import pathlib

# import bonobo
import dateutil.parser

# import h5py
from diskcache import Cache
from diskcache.core import ENOVAL
import netCDF4 as nc
import numpy as np
import sh
import ipdb

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

CACHE_PATH = PATH/ "data/cache" 


# for i in list json
with open("urls.json") as json_file:
    json_load = json.load(json_file)

# downloads the product
#Cachea files
cache = Cache(directory="CACHE_PATH")

@cache.memoize(typed=True, expire=None, tag='fib')
def product_parser(date_key="2016001"):
    dropbox_dir = json_load[date_key]
    sh.wget("-O", f"data/{date_key}.zip", dropbox_dir)


#cache.set('key', BytesIO(b'value'), expire=None, read=True)
result = cache.get("/data/2016001.zip", default = ENOVAL, retry=True)

if result is ENOVAL:
    result = product_parser() #esto 


# for...itera sobre todos los files
# extracts files from zip and opens as netcdf
def zip_to_nc(nc_file_name = "A2016.001.1505.nc"):
    with ZipFile("/data/2016001.zip", "r") as zip:
        data = zip.read(nc_file_name)
        ds = nc.Dataset(nc_file_name, mode="r", memory=data)
        return ds


def extract_bands(ncvar):
    band_dict = {
        "b1": "ev_250_aggr1km_refsb_1",  # vis
        "b2": "ev_250_aggr1km_refsb_2",  # vis
        "b22": "ev_1km_emissive_22",  # 3.9
        "b26": "ev_1km_refsb_26",  # rari
        "b29": "ev_1km_emissive_29",
        "b34": "ev_1km_emissive_34",
    }

    list_bands = []
    for key in band_dict:
        band = ncvar.variables[band_dict.get(key)][:].data
        band_ok = band.reshape([1354, 2030])
        list_bands.append(band_ok)

    all_bands = np.stack(list_bands, -1)

    for i in range(6):
        norm_bands = (all_bands[:, :, i] - all_bands[:, :, i].min()) / (
            all_bands[:, :, i].max() - all_bands[:, :, i].min()
        )

        return norm_bands
