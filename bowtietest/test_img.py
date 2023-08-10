#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT (https://tldrlegal.com/license/mit-license)
# Copyright (c) 2023, Paula Romero Jure et al.
# All rights reserved.
#==============================================================================
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Function
# -----------------------------------------------------------------------------

def test_rep_x_col(
    band, scan_by="col", rmin=1, rmax=10, frec_min=5, factor=2, graph=1
):
    """
        This test tries to identify in images if there is pixel repetitions (by columns).
        To a tile of an image, desplacemnts.
        
        A tile of an image is shifted successively between rmin and rmax (in columns) and 
        subtracted from the original to emphasise repetitions (black stripes). 
        A sum is performed on a coordinate (row) and 
        a Fourier transform is performed on this sequence.
        
        If there is a frequency that stands out notably over the others 
        (exceeding a threshold) it is concluded that there is a repetition.
        

    Parameters
    ----------
        band: ndarray
            2D array normalized to [0,1]
        scan_by: str
            scan direction to look for repetitions 
            Values are 'col' or 'row'
        rmin: int 
            minimum shift value (>= 0)
        rmax: int
            maximum shift value (>= 1)
        frec_min: int 
            minimum frequency from which the one with 
            major spectral component is calculated (>= 1)
        factor: float
            the factor of std deviations to calulate the threshold  (>=0)
        graph: int
            if 1, plots the test, if 0 does not plot
            
    Returns
    -------
        test: int
            0 means no errors, 1 means image with repetitions, 
            2 means nearly uniform image 
            
    """
    # Validation of the input data
    if (
        str(type(band)) != "<class 'numpy.ndarray'>"
        or type(scan_by) != str
        or type(rmin) != int
        or type(rmax) != int
        or type(frec_min) != int
        or type(factor) != int
        or type(graph) != str
    ):
        raise TypeError(f"Verify data type {type(band)}, {type(scan_by)}, \
            {type(rmin)}, {type(rmax)}, {type(factor)}, {type(frec_min)}, \
            {type(graph)}")
        return

    dim = band.shape
    if np.min(dim) < 50 + 2 * rmax or np.max(dim) > 300 + 2 * rmax:
        raise ValueError(f"Image dimensions out of range {np.min(dim)}, {50 + 2 * rmax}, {np.max(dim)}, {300 + 2 * rmax}")
        return

    if band.min() < 0 or band.max() > 1:
        raise ValueError(f"Image is not normalized min(img) = {band.min()}, max(img) = {band.max()}")
        return

    if (
        (scan_by != "row" and scan_by != "col")
        or rmin < 0
        or rmax <= rmin
        or frec_min < 1
        or factor < 1
        or (graph != 1 and graph != "n")
    ):
        raise ValueError(f"{scan_by}, {rmin}, {rmax}, {graph}")
        return

    if scan_by == "row":
        band_aux = band.T
    else:
        band_aux = band

    # Minimum frequency of detection: Number of rows - rmax
    ncol0 = band_aux.shape[0] - rmax

    sum_dif = np.zeros([ncol0 - rmax, rmax - rmin])
    Msum_dif = np.ones_like(sum_dif)

    # Calculates the differences between the original image and the one
    # displaced by columns 
    # Sums the differences by row

    for j in range(rmin, rmax):  
        dif = abs(
            band_aux[j : ncol0 - rmax + j, :] - band_aux[: ncol0 - rmax, :]
        )
        sum_dif[:, j - rmin] = dif.sum(axis=1)  # ke

    umbral0 = sum_dif.mean() - sum_dif.std()
    Msum_dif[sum_dif < umbral0] = 0
    Msum_dif = np.copy(sum_dif)

    # Looking for repetition frequencies through FFT
    FMsum_dif = np.zeros_like(Msum_dif, dtype="complex")

    max_val_frec = 0
    max_des = 0
    frec_max = 0
    for j in range(rmin, rmax):
        FMsum_dif[:, j - rmin] = np.fft.fft(Msum_dif[:, j - rmin])  # Fourier
        if abs(FMsum_dif[frec_min : ncol0 // 2, j - rmin]).max() > max_val_frec:
            frec_max = (
                np.argmax(abs(FMsum_dif[frec_min : ncol0 // 2, j - rmin]))
                + frec_min
            )
            max_val_frec = abs(FMsum_dif[frec_max, j - rmin])
            max_des = j

    # Result
    val = np.copy(abs(FMsum_dif[frec_min:, max_des - rmin]))
    umbral = val.mean() + factor * val.std()
    if (val - umbral).max() > 0 and frec_max > frec_min:
        test = 1
    elif max_val_frec == 0:
        test = 2
    else:
        test = 0

    print(
        f"Test = {test}, Desplazamiento que maximiza = {max_des}, Frecuencia maxima = {frec_max}, valor = {max_val_frec}"
    )

    # Plots
    if graph == 1:
        if max_des < rmax - rmin:
            j = max_des - rmin
        else:
            j = Msum_dif.shape[1] - 2
        if max_des == 0:
            j = rmin
        # print(max_des, rmax, rmin, j, Msum_dif.shape)

        plt.figure(figsize=[5, 5])
        plt.subplot(121)
        plt.title("Original image")
        plt.imshow(band_aux[: ncol0 - rmax, :], cmap="gray")

        plt.subplot(122)
        plt.imshow(
            abs(band_aux[j : ncol0 - rmax + j, :] - band_aux[: ncol0 - rmax, :]),
            cmap="gray",
        )
        plt.title("Diferential image")

        plt.show()

        plt.figure(figsize=[5, 2])
        plt.subplot(121)
        plt.plot(Msum_dif[1:, j])
        plt.ylabel("Differences")
        plt.xlabel("Column")
        plt.title("Accumulated differences")
        plt.subplot(122)
        plt.plot(abs(FMsum_dif[1:, j]))
        plt.title("Fourier components")
        # plt.ylabel('Component value')
        plt.xlabel("Transformed column")
        plt.show()

    return test, int(ncol0 / frec_max)
