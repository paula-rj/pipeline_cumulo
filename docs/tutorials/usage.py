# %% Imports
import atexit
import json
import os
import tempfile
import zipfile
import sh
import h5py
import matplotlib.pyplot as plt
import numpy as np

# %%
import sys
from pathlib import Path  # if you haven't already done so

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))


import pipeline

# %%Download file from 1 day
PATH_FOR_HDF5 = "../data/"
# Elije el json del mes
path_json = "../links_dir/2008_01.json"
# Guarda la parte de la fecha
new_dir = path_json[-12:-5]
f = open(path_json)
links = json.load(f)
# dias -> da lista de urls de cada dia
days = list(links.keys())
print(len(days))

# %% lista de urls de cada dia

di = 5
links_list = links[days[di]]
print(len(links_list))
# %%
# k = 70
for k in range(95, 105, 1):
    url = links_list[k]
    print(url)
    result = sh.wget("-O", f"../ncfiles/{url[90:107]}", url)

# %%
# SAVES AS NC
# %%
# Extracts file name from full url
date = url[90:104][3:].replace(".", "")
# %%Downloading
# Generates temp file to store downloaded file
_, tmp_path = tempfile.mkstemp(suffix=".nc", prefix=date, dir=None, text=False)
atexit.register(os.remove, tmp_path)

# If file not already in cache, downloads it
result = sh.wget("-O", tmp_path, url)

# Extracts bands as np arrays
# nc_file = pipeline.zip_to_nc(nc_file_name="A2016.001.0200.nc")
norm_bands = pipeline.processing(tmp_path)

# estos son h5 que se guarda en la memoria
a = pipeline.generate_tiles(norm_bands, url[90:104], PATH_FOR_HDF5)
# %%Testing
files = os.listdir(PATH_FOR_HDF5)
files.remove("cache")

# Tests whether tiles are ok
test_list = []
for i in range(len(files)):
    test_list.append(pipeline.test_int(f"{PATH_FOR_HDF5}/{files[i]}"))

print(len(test_list))
print(test_list)

arr = np.array(test_list)
mal = np.argwhere(arr == 0)

print(len(mal))
print(mal)

f.close()
# %%
a_json = {"id": url[90:104][3:], "files_names": files, "test": test_list}

with open(f"{days[di]}.json", "w") as final:
    json.dump(a_json, final)
# %% Plot
dir_to_hdf5 = f"{PATH_FOR_HDF5}/{files[100]}"
f = h5py.File(dir_to_hdf5, "r")
img = f["bands"][:]

for i in range(6):
    plt.imshow(img[:, :, i], cmap="gray")
    plt.show()

# ONly one
# plt.imshow(img[:, :, 1], cmap="gray")
# plt.show()

# %%
# for file in zip: ... que extraiga cada archivo del zip
# name = file.name
nc_file = pipeline.zip_to_nc(nc_file_name="A2016.001.0200.nc")  # dir_name, file_name
norm_bands = pipeline.processing(nc_file)
a = pipeline.generate_tiles(
    norm_bands, "A2016.001.0200.nc"
)  # -> estos son h5 que se guarda en la memoria o ftp
# delate nc_file from local ?
# plt.imshow(a[45][:,:,-3:])

# %%
print(a[:, :, 1])
# %%
raw = pipeline.zip_to_nc()
raw.variables.keys()
# %%

lon = np.array(raw.variables["longitude"][:].data)
lonr = np.reshape(lon, [1354, 2030])
print(lonr[0, 0])
# %%
lat = np.array(raw.variables["longitude"][:].data)
lat = np.reshape(lon, [1354, 2030])
print(lonr[0, 0])
# %%
with zipfile.ZipFile("data/sample2016001.zip", "r") as zip:
    data = zip.open("2016.001.1510_tile59.hdf5")
    hf = h5py.File(data, "r")
b = hf["bands"][:]

# %%
#%% TEST

# files = os.listdir("/media/paula/DAYE 1/cumulo/")

# test_list = []
# for i in range(len(files)):
#     fullpath = os.path.join("/media/paula/DAYE 1/cumulo", files[i])
#     f = h5py.File(fullpath, "r")
#     band_aux = f["bands"][:][:, :, 0]
#     testok, _ = test_rep_x_fil(band_aux, rmin=1, rmax=10, frec_min=5, grafico=0)
#     if testok == 0:
#         copypath = os.path.join("/media/paula/DAYE 1/cumulook", files[i])
#         shutil.copy(fullpath, copypath)