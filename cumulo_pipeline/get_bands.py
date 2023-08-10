#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT (https://tldrlegal.com/license/mit-license)
# Copyright (c) 2023, Paula Romero Jure et al.
# All rights reserved.
# ==============================================================================
import os

import h5py

import netCDF4 as nc

import numpy as np


def study_file(store_dir_nc, path_to_save):
    """Gets 4 bands from a .nc CUMULO file and returns it as hdf5."""
    file_list = os.listdir(store_dir_nc)
    band_dict = {
        "b2": "ev_250_aggr1km_refsb_2",  # vis
        "b22": "ev_1km_emissive_22",  # 3.9
        "b26": "ev_1km_refsb_26",  # rari
        "b34": "ev_1km_emissive_34",
    }

    for file_name in file_list:
        list_bands = []
        # extract bands and get them ready
        ds = nc.Dataset(
            f"{store_dir_nc}/{file_name}"
        )  # si viene del zip esto no es necesario
        for key in band_dict:
            band = ds.variables[band_dict.get(key)][:].data
            band_ok = band.reshape((1354, 2030))
            list_bands.append(band_ok)

        all_bands = np.stack(list_bands, -1)

        with h5py.File(
            f"{path_to_save}/{file_name[:-3]}.hdf5",  # Va a donde se guarden
            "w",
        ) as f:
            f.create_dataset("bands", data=all_bands)
