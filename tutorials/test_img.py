# %%
import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
import shutil


# %%
def test_rep_x_fil(
    band_aux, row_col="col", rmin=1, rmax=10, frec_min=5, grafico=0
):
    """
        A una subimagen se le realizan desplazamiento sucesivos en columnas y
        se resta con la original para determinar si repetición de columnas
    Inputs:
        band aux = array 2 D normalizado a [0,1]
        rmin = valor mínimo de desplazamiento
        rmax = valor máximo de desplazamiento
        grafico = 1 grafica, otro valor no
    Output:
        test =
            0 imagen sin error
            1 imagen con repeticiones verticales
            2 imagen con rayas horizontales o uniforme
        frec_max = frecuencia de repeticion
    """

    # Frecuencia mínima de detección
    # Number of rows - rmax
    nfil0 = band_aux.shape[0] - rmax
    ncol0 = band_aux.shape[1] - rmax
    if row_col == "col":
        sum_dif = np.zeros([ncol0 - rmax, rmax - rmin])
        Msum_dif = np.ones_like(sum_dif)
        # Cálculo de las diferencias entre imagen original y desplazada en columna
        # Suma por fila de las diferencias
        for j in range(rmin, rmax):
            dif = abs(
                band_aux[:, j : ncol0 - rmax + j] - band_aux[:, : ncol0 - rmax]
            )
            sum_dif[:, j - rmin] = dif.sum(axis=0)
    elif row_col == "row":
        sum_dif = np.zeros([nfil0 - rmax, rmax - rmin])
        Msum_dif = np.ones_like(sum_dif)
        # Cálculo de las diferencias entre imagen original y desplazada en filas
        # Suma por fila de las diferencias
        for j in range(rmin, rmax):  # como ? si son iguales rmin y rmax
            dif = abs(
                band_aux[j : nfil0 - rmax + j, :] - band_aux[: nfil0 - rmax, :]
            )
            sum_dif[:, j - rmin] = dif.sum(axis=1)  # ke

    umbral0 = sum_dif.mean() - sum_dif.std()
    Msum_dif[sum_dif < umbral0] = 0
    Msum_dif = np.copy(sum_dif)

    # Búsqueda de las frecuencias de repetición mediante FFT
    FMsum_dif = np.zeros_like(Msum_dif, dtype="complex")

    max_val_frec = 0
    max_des = 0
    frec_max = 0
    for j in range(rmin, rmax):
        FMsum_dif[:, j - rmin] = np.fft.fft(Msum_dif[:, j - rmin])  # Fourier
        if abs(FMsum_dif[frec_min : nfil0 // 2, j - rmin]).max() > max_val_frec:
            frec_max = (
                np.argmax(abs(FMsum_dif[frec_min : nfil0 // 2, j - rmin]))
                + frec_min
            )
            max_val_frec = abs(FMsum_dif[frec_max, j - rmin])
            max_des = j

    # Resultado del TEST

    val = np.copy(abs(FMsum_dif[frec_min:, max_des - rmin]))
    umbral = val.mean() + 2 * val.std()
    if (val - umbral).max() > 0 and frec_max > frec_min:
        test = 1
    elif max_val_frec == 0:
        test = 2
    else:
        test = 0

    print(
        f"Test = {test}, Desplazamiento que maximiza = {max_des}, Frecuencia maxima = {frec_max}, valor = {max_val_frec}"
    )

    # Graficos
    if grafico == 1:
        if max_des < rmax - rmin:
            j = max_des - rmin
        else:
            j = Msum_dif.shape[1] - 2
        if max_des == 0:
            j = rmin
        # print(max_des, rmax, rmin, j, Msum_dif.shape)

        plt.figure(figsize=[5, 5])
        plt.subplot(121)
        plt.imshow(band_aux[: nfil0 - rmax, :], cmap="gray")

        plt.subplot(122)
        plt.imshow(
            abs(band_aux[j : nfil0 - rmax + j, :] - band_aux[: nfil0 - rmax, :]),
            cmap="gray",
        )

        plt.show()

        plt.figure(figsize=[5, 2])
        plt.subplot(121)
        plt.plot(Msum_dif[1:, j])
        plt.subplot(122)
        plt.plot(abs(FMsum_dif[1:, j]))
        plt.show()

    return test, frec_max


files = os.listdir("../data/")
files.remove("cache")

test_list = []
for i in range(len(files)):
    fullpath = os.path.join("../data/", files[i])
    f = h5py.File(fullpath, "r")
    band_aux = f["bands"][:][:, :, 0]
    testok, _ = test_rep_x_fil(band_aux, rmin=1, rmax=10, frec_min=5, grafico=0)
    # if testok == 0:
    #    copypath = os.path.join("../data/filtered", files[i])
    #    shutil.copy(fullpath, copypath)

# %%
fullpath = os.path.join("../data/filtered", files[i])
f = h5py.File("../data/filtered/A2009.001.1605_tile004.hdf5", "r")
band_aux = f["bands"][:][:, :, 0]
test_rep_x_fil(band_aux, rmin=1, rmax=10, frec_min=5, grafico=1)

# %%
