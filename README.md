# Pipeline CUMULO*

Retrieves files from CUMULO dataset, selects 6 bands and returns tiles of size 128 x 128 x 6. Each tile is saved in HDF5 format and named following the convention:

 **AYYYY.ddd.HHMM_tileijj.hdf5**
|_______________| |______|
First part         Second part

The first part is the name of the file from which the tile was extracted. 
The second part is an indicator of the part of the image from where the file was extracted.

- i represents the rows and is an int  number between 0 and 9.
- jj represents the columns and is a number between 00 and 15. 


            
              0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
              ----------------------------------------------------------------
            0
              ----------------------------------------------------------------
            1
              ----------------------------------------------------------------   
            2
              ----------------------------------------------------------------
            3
              ----------------------------------------------------------------
            4
              ----------------------------------------------------------------
            5
              ----------------------------------------------------------------
            6
              ----------------------------------------------------------------
            7
              ----------------------------------------------------------------
            8
              ----------------------------------------------------------------
            9
              ----------------------------------------------------------------


*Zantedeschi, V., Falasca, F., Douglas, A., Strange, R., & Kusner, M. J. (2019). Cumulo: A Dataset for Learning Cloud Classes. ArXiv. [/abs/1911.04227](https://arxiv.org/abs/1911.04227)