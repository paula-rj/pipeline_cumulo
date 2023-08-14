# Pipeline CUMULO*


![Python: 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) 


Python package designed to retrieve files from CUMULO* dataset and to detect bowtie effect and stripping in images form MODIS and other similar sensors. 

# About CUMULO pipeline

Retrieves files from CUMULO dataset, selects 6 bands and returns tiles of size 128 x 128 x 6. Each tile is saved in HDF5 format and named following the convention:

     AYYYY.ddd.HHMM_tileijj.hdf5

    |______________||______|
     First part      Second part

The first part is the name of the file from which the tile was extracted. 

- YYYY is the year. It could be 2008,2009 or 2016.
- ddd is the day of the year. It ranges from 001 to 366.
- HH is the hour (UTC).
- MM the minutes (UTC).

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