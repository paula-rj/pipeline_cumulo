import os

import bonobo
import dateutil.parser
import h5py
import netCDF4 as nc
import numpy as np
import sh



def product_parser():
    a = 2016
    sh.wget("https://www.dropbox.com/sh/i3s9q2v2jjyk2it/AACq0CgQOsRQQuGjhmPNrjafa/2016/01/001/daylight/A2016.001.0610.nc?dl=1", 
        O = f"/content/A{a}.001.0610.nc")

def extract_bands():
    band_dict = {
    'b1': 'ev_250_aggr1km_refsb_1', #vis
    'b2': 'ev_250_aggr1km_refsb_2', #vis
    'b22': 'ev_1km_emissive_22', #3.9
    'b26': 'ev_1km_refsb_26', #rari
    'b29': 'ev_1km_emissive_29',
    'b34': 'ev_1km_emissive_34'
    }
    
    ncvar = nc.Dataset("/content/drive/MyDrive/cumulo_cosas/A2016.366.1355.nc")
    for key in band_dict:
        band = ncvar.variables[band_dict.get(key)][:].data 
        band_ok = band.reshape([1354, 2030])
       

    for i in range(6):
        norm_bands = (all_bands[:,:,i] - all_bands[:,:,i].min() ) \
            / (all_bands[:,:,i].max() - all_bands[:,:,i].min() )