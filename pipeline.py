import json
import os
from zipfile import ZipFile

import dateutil.parser
import h5py
import netCDF4 as nc
import numpy as np
import sh


# for i in list json
with open("data.json") as json_file:
    json_load = json.load(json_file)

# downloads the product directory
def product_parser(date_key="2008001"):
    dropbox_dir = json_load[date_key]
    sh.wget(dropbox_dir, -O, f"/data/{date_key}.zip")


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
    tiles_list = []
    pixel_list_height = np.arange(0, 1354, 128)
    pixel_list_lenght = np.arange(0, 2030, 128)
    lcycle = iter(pixel_list_height)
    for i in pixel_list_height:
        if i == 0:
            nex = next(lcycle)
            htile = bands_matrix[i : next(lcycle), :, :]
        elif i == 1280:
            break
        else:
            htile = bands_matrix[i : next(lcycle), :, :]

    return htile

    # with h5py.File("mytestfile.hdf5", "w") as f:
    #    dset = f.create_dataset("dataset_1", data = norm_bands)
