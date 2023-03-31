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
#fila = band1[100, :]
dif_img = band1[1:] - band1[:-1]
suma = np.sum(dif_img, axis=0)

print(suma.shape)

dif_suma = suma[1:] - suma[:-1]

fdif = np.fft.fft(suma)

plt.plot(np.abs(fdif))
plt.title("Fourier de diferencia sobre suma total")
#%%%%%%%%%%%%%%%%
import statistics as st
std =np.std(abs(fdif[1:]))
media =np.mean(abs(fdif[1:]))

print(media, std)

af_fil = np.zeros(len(fdif))
af_fil[1:] = abs(fdif[1:])
af_fil[af_fil < media+ 2*std] = 0
af_fil[af_fil >= media+ 2*std] = 1

posmax = np.argwhere(af_fil == 1)
posmax = np.reshape(posmax, [len(posmax)])

difpos = posmax[1:]- posmax[:-1]

moda = st.mode(difpos)

masc = np.zeros_like(difpos)
masc[difpos == moda] = 1

if masc.sum() / len(difpos) > .5:
    print('--------------------------------------------')
    print('--La imagen tiene ruido periodico-----------')
    print('--------------------------------------------')

print(masc.sum() , len(difpos), masc.sum() / len(difpos))


plt.plot(af_fil)






#%%%
# Armamos un filtro y le pasamos
ker = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])

filtered = scipy.signal.correlate2d(dif, ker)
# %%
plt.imshow(filtered[:128, :128], cmap="gray", vmin=-1, vmax=1)
plt.title("Recorte de filtrado")
# %%%%%%%%%%%%%%%%%%%%%%%%%%
suma_filt = np.sum(filtered, axis=0)
plt.plot(suma_filt)

print(suma_filt.shape)
#%%%%%
fft_suma_filt = np.fft.fft(suma_filt)
plt.plot(np.abs(fft_suma_filt))

# %%
af = np.fft.fft(suma)

plt.plot(abs(af[1:]))
# %%
