# %%
import atexit
import json
import os
import tempfile
import zipfile

import h5py
import matplotlib.pyplot as plt
import numpy as np

from .. import main
from .. import pipeline

# %%Download file from 1 day
PATH_FOR_HDF5 = "../data/"
path_json = "links_dir/2008_01.json"

new_dir = path_json[-12:-5]  # Guarda la parte de la fecha
f = open(path_json)
links = json.load(f)

# dias -> da lista de urls de cada dia
day = "2009001"
# lista -> da 1 url
links_list = links[day]
url = links_list[-1]

# Extracts file name from full url
date = url[90:104][3:].replace(".", "")

# Generates temp file to store downloaded file
_, tmp_path = tempfile.mkstemp(suffix=".nc", prefix=date, dir=None, text=False)
atexit.register(os.remove, tmp_path)

# If file not already in cache, downloads it
result = main.product_parser(tmp_path, url)

# Extracts bands as np arrays
# nc_file = pipeline.zip_to_nc(nc_file_name="A2016.001.0200.nc")
norm_bands = pipeline.processing(tmp_path)

# estos son h5 que se guarda en la memoria
a = pipeline.generate_tiles(norm_bands, url[90:104], "data/")

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
print(mal)

# for j in mal[:]:
#        os.remove(f"{PATH_FOR_HDF5}{files[j[0]]}")

f.close()

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
f = h5py.File("../data/A2009.001.1605_tile613.hdf5", "r")
a = f["bands"][:]
plt.imshow(a[:, :, 1], cmap="gray")
plt.show()
# for i in range(6):
#    plt.imshow(a[:, :, i], cmap="gray")
#    plt.show()


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
plt.imshow(b[:, :, 5], cmap="gray")
plt.show()
