#%%%%%%%%%%%%%%%
# Imports
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np
import scipy

#%%%%%%%%%%%%%%%
# Abrimos banda visible 1
data = nc.Dataset("data/A001.nc")
band = data.variables["ev_250_aggr1km_refsb_1"][:]
band1 = band.reshape((1354, 2030))

plt.imshow(band1, cmap="gray")
#%%%%%%%%%%%%%%%%%%%%%%%%%
# Hacemos diferencia
dif = band1[:, 1:] - band1[:, :-1]

plt.imshow(dif, cmap="gray", vmin=-1, vmax=1)
plt.title("Diferencia, vmax = 1")

plt.imshow(dif, cmap="gray", vmin=np.min(dif), vmax=np.max(dif))
plt.title("Diferencia, vmax = su max")

#%%%%%%%
# Un recorte de la diferencia
rec = dif[:128, :128]

plt.imshow(rec, cmap="gray", vmin=-1, vmax=1)
plt.title("Recorte dif con vmax 1")

# plt.imshow(rec, cmap="gray", vmin = np.min(dif), vmax=np.max(dif))
# plt.title("Recorte dif con vmax = su max")

#%%%%%%%%%%%%%%%
# Aplicamos Fourier sobre una fila
fila = band1[100, :]
suma = np.sum(band1, axis=1)
print(suma.shape)
dif_suma = suma[1:] - suma[:-1]
fdif = np.fft.fft(dif_suma)
plt.plot(fdif)
plt.title("Fourier de diferencia sobre suma total")
#%%%%%%%%%%%%%%%%
# Armamos un filtro y le pasamos
ker = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])

filtered = scipy.signal.correlate2d(dif, ker)
# %%
plt.imshow(filtered[:128, :128], cmap="gray", vmin=-1, vmax=1)
plt.title("Recorte de filtrado")
# %%
