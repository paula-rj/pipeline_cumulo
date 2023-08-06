import numpy as np
import matplotlib.pyplot as plt

def test_rep_x_col(band, barrido = 'col', rmin = 1, rmax = 10, frec_min = 5, fact = 2, grafico = 'y'):
    '''
        Este test trata de identificar en imágenes de una banda si hay repetición de datos (en columnas)
        A una subimagen se le realizan desplazamientos sucesivos entre rmin y rmax (en columnas) y
        se resta con la original para enfatizar repeticiones (franjas negras). Se realiza una suma en una
        coordenada (fila) y a esta secuencia se les hace una transformada de Fourier.
        Si existe una frecuencia que se destaca notablemente sobre las otras (superando un umbral) se
        concluye que hay repetición.

    Inputs:
        band = array 2 D normalizado a [0,1]
            type = ndarray
        barrido = dirección de búsqueda de repeticiones 'col, 'raw'
            type = str
        rmin = valor mínimo de desplazamiento (>= 0)
            type = int
        rmax = valor máximo de desplazamiento (>= 1)
            type = int
        frec_min = frecuencia mínima a partir de la que se calcula la frecuencia con mayor componente
             espectral (>= 1)
            type = int
        fact = factor de desviaciones estándar para calcular el umbral  (>=0)
            type = float
        grafico = y grafica, n no grafica
            type = str
    Output:
        test =
            (0, 1, 2) imagen: sin error, con repeticiones, casi uniforme
                type = int
            periodo de repetición
                type = int
    '''
    #Verficacion de los datos de entrada

    if str(type(band))!="<class 'numpy.ndarray'>" or type(barrido)!=str or type(rmin)!=int  or type(rmax)!=int or type(frec_min)!=int  or type(fact)!=int or type(grafico)!=str:
        print(type(band), type(barrido), type(rmin), type(rmax), type(fact), type(frec_min), type(grafico))
        print("Error: en los datos de entrada, verifique los tipos")
        return

    dim = band.shape
    if np.min(dim) < 50+2*rmax  or np.max(dim) > 300+2*rmax:
        print(np.min(dim), 50+2*rmax, np.max(dim) , 300+2*rmax)
        print(f'Dimensiones de la imagen fuera de rango {dim}')
        return

    if band.min() < 0 or band.max() > 1:
        print(f'min(img) = {band.min()}, max(img) = {band.max()}')
        print(f'Imagen no normalizada')
        return

    if (barrido!='raw' and barrido!='col') or rmin<0 or rmax<=rmin or frec_min<1 or fact<1 or (grafico!='y' and grafico!='n'):
        print(barrido, rmin, rmax, grafico)
        print("Error: en los datos de entrada, verifique los valores")
        return

    if barrido == 'raw':
        band_aux = band.T
    else:
        band_aux = band

    # Frecuencia mínima de detección
    # Number of rows - rmax
    ncol0 = band_aux.shape[0] - rmax

    sum_dif = np.zeros([ncol0-rmax, rmax-rmin])
    Msum_dif = np.ones_like(sum_dif)

    #Cálculo de las diferencias entre imagen original y desplazada en columna
    #Suma por fila de las diferencias

    for j in range(rmin, rmax): #
        dif = abs(band_aux[j:ncol0-rmax+j, :] - band_aux[:ncol0-rmax, :])
        sum_dif[:, j-rmin] = dif.sum(axis=1) # ke

    umbral0 = sum_dif.mean() - sum_dif.std()
    Msum_dif[sum_dif < umbral0] = 0
    Msum_dif = np.copy(sum_dif)

    #Búsqueda de las frecuencias de repetición mediante FFT
    FMsum_dif = np.zeros_like(Msum_dif, dtype='complex')

    max_val_frec = 0
    max_des = 0
    frec_max = 0
    for j in range(rmin, rmax):
        FMsum_dif[:, j-rmin] = np.fft.fft(Msum_dif[:, j-rmin]) #Fourier
        if abs(FMsum_dif[frec_min:ncol0//2, j-rmin]).max() > max_val_frec:
            frec_max = np.argmax(abs(FMsum_dif[frec_min:ncol0//2, j-rmin]))+frec_min
            max_val_frec = abs(FMsum_dif[frec_max, j-rmin])
            max_des = j

    #Resultado del TEST

    val = np.copy(abs(FMsum_dif[frec_min:, max_des-rmin]))
    umbral = val.mean() + fact * val.std()
    if (val - umbral).max() > 0 and frec_max > frec_min:
        test = 1
    elif max_val_frec == 0:
        test = 2
    else:
        test = 0

    print(f"Test = {test}, Desplazamiento que maximiza = {max_des}, Frecuencia maxima = {frec_max}, valor = {max_val_frec}")

    #Graficos
    if grafico == 'y':
        if max_des < rmax - rmin:
            j = max_des - rmin
        else:
            j = Msum_dif.shape[1] - 2
        if max_des == 0: j = rmin
        #print(max_des, rmax, rmin, j, Msum_dif.shape)

        plt.figure(figsize=[5, 5])
        plt.subplot(121)
        plt.title('Original image')
        plt.imshow(band_aux[:ncol0-rmax, :], cmap= 'gray')

        plt.subplot(122)
        plt.imshow(abs(band_aux[j:ncol0-rmax+j, :] - band_aux[:ncol0-rmax,: ]), cmap= 'gray')
        plt.title('Diferential image')

        plt.show()

        plt.figure(figsize=[5, 2])
        plt.subplot(121)
        plt.plot(Msum_dif[1:, j])
        plt.ylabel('Differences')
        plt.xlabel('Column')
        plt.title('Accumulated differences')
        plt.subplot(122)
        plt.plot(abs(FMsum_dif[1:, j]))
        plt.title('Fourier components')
        #plt.ylabel('Component value')
        plt.xlabel('Transformed column')
        plt.show()

    return test, int(ncol0/frec_max)
