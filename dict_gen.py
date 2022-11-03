import numpy as np
import json 
import datetime

"""Este codigo genera un json con lista de
keys: YYYYddd
url: full url para descargar de cumulo 
      LAS CARPETAS DE CADA DIA
"""

def url_parser(dtime):
    """Builds the url.
    Parameters
    ----------
    year: int
    month: int
    day: int

    Returns
    -------
    tuple
    key_name: yyyyddd carpeta donde se van a guardar los archivos
    full dir
    """
 
    date_directory = dtime.strftime("%Y/%m/%j")
    cumulo_dir = f"CUMULO/{date_directory}/daylight"
    key_name = dtime.strftime("%Y%j")
    full_dir = f"https://www.dropbox.com/sh/6gca7f0mb3b0ikz/AAD6gEBP2WrQS1-VQvkA3DZ1a/{cumulo_dir}?dl=1"
    return ((key_name, full_dir),)

url_dict = {}
years_avail = (2008,2009,2016)
days = np.arange(1,366).tolist()
for year in years_avail:
  for day in days:
    dt = datetime.datetime.strptime(f"{year} {day}", "%Y %j")
    url_dict.update((url_parser(dt)))


with open('data.json', 'w') as fp:
    json.dump(url_dict, fp, indent=2)