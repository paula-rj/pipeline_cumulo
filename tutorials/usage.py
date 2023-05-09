#%%
import numpy as np
import h5py
import zipfile
import matplotlib.pyplot as plt

import pipeline

#%%
# for file in zip: ... que extraiga cada archivo del zip
# name = file.name
nc_file = pipeline.zip_to_nc(
    nc_file_name="A2016.001.0200.nc"
)  # dir_name, file_name
norm_bands = pipeline.processing(nc_file)
a = pipeline.generate_tiles(
    norm_bands, "A2016.001.0200.nc"
)  # -> estos son h5 que se guarda en la memoria o ftp
# delate nc_file from local ?
# plt.imshow(a[45][:,:,-3:])

#%%
f = h5py.File("data/2016001/2016.001.0200_tile05.hdf5", "r")
a = f["bands"][:]
plt.imshow(a[:, :, 5], cmap="gray")
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
#%%
with zipfile.ZipFile("data/sample2016001.zip", "r") as zip:
    data = zip.open("2016.001.1510_tile59.hdf5")
    hf = h5py.File(data, "r")
b = hf["bands"][:]

#%%
plt.imshow(b[:, :, 5], cmap="gray")
plt.show()
# %%
