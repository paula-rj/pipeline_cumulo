import os
import numpy as np
import matplotlib.pyplot as plt
import h5py

# %%
files = os.listdir("data/")
files.remove("cache")
# %%
i = 101
print(files[i])
f = h5py.File(f"data/{files[i]}", "r")
# f = h5py.File(f"data/A2008.007.0135_tile115.hdf5", "r")
dset = f["bands"]

plt.imshow(dset[:, :, 1], cmap="gray")
f.close()


# %%
def test_int(path):
    rmax = 10
    nfil0, ncol0 = 128, 128  # tamaño de la imagen
    # fila  y columna inicial de la imagen de test
    f = h5py.File(f"data/{path}", "r")
    dset = f["bands"]
    Nband_aux = dset[:, :, 1]
    f.close()

    sum_dif = np.zeros([ncol0 - rmax, rmax - 1])
    Msum_dif = np.zeros_like(sum_dif)

    for j in range(1, rmax):
        dif = abs(Nband_aux[:, j : ncol0 - rmax + j] - Nband_aux[:, : ncol0 - rmax])
        sum_dif[:, j - 1] = dif.sum(axis=0)
        umbral = (sum_dif[:, j - 1].max() + 2 * sum_dif[:, j - 1].min()) / 3
        Msum_dif[sum_dif[:, j - 1] > umbral, j - 1] = 1

    FMsum_dif = np.zeros_like(Msum_dif)

    for j in range(1, rmax):
        FMsum_dif[:, j - 1] = np.fft.fft(Msum_dif[:, j - 1])

    # gap = 5 #altas frecuencias descartadas para las posiciones
    for j in range(rmax - 1):
        # for j in range(1):
        val = np.copy(abs(FMsum_dif[1:, j]))
        umbral = val.mean() + 4 * val.std()
        # pos_max = np.argwhere(val[gap:-gap] > umbral) + gap
        # val_max = val[pos_max]
        # print(j, umbral, pos_max, val_max)

    test = 0
    for j in range(rmax - 1):
        val = np.copy(abs(FMsum_dif[1:, j]))
        umbral = val.mean() + 4 * val.std()
        if (val - umbral).max() > 0:
            test += 1
    test = test // 2  # se divide por 2 pues la FFT es simétrica
    return test


# %%
test_list = []
for i in range(len(files)):
    test_list.append(test_int(files[i]))


# %%
len(test_list)
# %%
arr = np.array(test_list)
mal = np.argwhere(arr == 0)
print(mal)
print(len(mal))
# %%
for j in mal[12:]:
    os.remove(f"data/{files[j[0]]}")
# %%
for j in mal:
    print
print(f"data/{files[mal[12]]}")
# %%
