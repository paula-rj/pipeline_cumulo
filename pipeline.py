# ---------------------
# IMPORTS
# ---------------------
from zipfile import ZipFile

import h5py
import netCDF4 as nc
import numpy as np


# extracts files from zip and opens as netcdf
def zip_to_nc(
    nc_file_name,
    zip_file="data/2016001.zip",
):
    """Extracts one file from a zip
    Parameters:
    -----------
    zip_file: str or Path
        Path to zip file where the files are stored
    nc_file_name: str
        Name of netcdf file to extract

    Returns:
    --------
    ds: netcdf.Dataset
        Dataset from the extracted file

    Notes:
    ------
    Si no uso este porque descargo file by file
    agregas nc.Dataset en norm_bands
    """
    with ZipFile(zip_file, "r") as zip:
        data = zip.read(nc_file_name)
        ds = nc.Dataset(nc_file_name, mode="r", memory=data)
        return ds


def processing(ds_ncfile):
    """Extracts bands form netcdf and get them ready.
    Retrieves numpy array with 6 bands.

    Parameters:
    -----------
        nc_file: netCDF file from CUMULO dataset

    Returns:
    --------
    norm_bands: np array
        6 bands normalized in a 1354x2030x6 array"""

    band_dict = {
        "b1": "ev_250_aggr1km_refsb_1",  # vis
        "b2": "ev_250_aggr1km_refsb_2",  # vis
        "b22": "ev_1km_emissive_22",  # 3.9
        "b26": "ev_1km_refsb_26",  # rari
        "b29": "ev_1km_emissive_29",
        "b34": "ev_1km_emissive_34",
    }

    list_bands = []
    # extract bands and get them ready
    ds = nc.Dataset(ds_ncfile)  # si viene del zip esto no es necesario
    for key in band_dict:
        band = ds.variables[band_dict.get(key)][:].data
        band_ok = band.reshape((1354, 2030))
        list_bands.append(band_ok)

    all_bands = np.stack(list_bands, -1)
    list_norm_bands = []

    for i in range(6):
        norm_band = (
            (all_bands[:, :, i] - all_bands[:, :, i].min())
            / (all_bands[:, :, i].max() - all_bands[:, :, i].min())
            * 255
        ).astype("uint8")
        list_norm_bands.append(norm_band)

    norm_bands = np.stack(list_norm_bands, -1)

    return norm_bands


def generate_tiles(bands_matrix, file_name):
    """Generates tiles by trimming the image in tiles of
    size 128x128.

    Parameters:
    ----------
    bands_matrix:
        the bands as np arrays.
    file_name: str
        the file name

    Returns
    -------
    l_tiles_list: list
        List of tiles names.

    """
    h_tiles_list = []
    pixel_list_height = np.arange(0, 1354, 128)
    conth = 0
    while conth + 1 < len(pixel_list_height):
        height_tile = bands_matrix[
            pixel_list_height[conth] : pixel_list_height[conth + 1], :, :
        ]
        conth = conth + 1
        h_tiles_list.append(height_tile)

    l_tiles_list = []
    pixel_list_lenght = np.arange(0, 2030, 128)
    conth = 0
    for height_tile in h_tiles_list:
        contl = 0
        while contl + 1 < len(pixel_list_lenght):
            lenght_tile = height_tile[
                :, pixel_list_lenght[contl] : pixel_list_lenght[contl + 1], :
            ]
            contl = contl + 1
            l_tiles_list.append(lenght_tile)

            if contl < 10:
                contl_str = f"0{contl}"
            else:
                contl_str = str(contl)

            with h5py.File(
                f"pipeline_cumulo/data/{file_name}_tile{conth}{contl_str}.hdf5",  # acca va disco
                "w",
            ) as f:
                f.create_dataset("bands", data=lenght_tile)
        conth = conth + 1

    return l_tiles_list
