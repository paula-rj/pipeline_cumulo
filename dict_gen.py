import json
import os

from bs4 import BeautifulSoup

"""Este codigo genera una lista de links
para descargar cada archivo de cumulo,
y los guarda como json, 1 file per month.
"""


def url_parser(path_to_html):
    """Builds the url.
    Parameters
    ----------
    path_to_html: str or Path
        The path to the parsed html file

    Returns
    -------
    links_download: list
        Lista de str, cada uno es el link para descargar.
    """
    with open(path_to_html) as file:
        soup = BeautifulSoup(file, "html.parser")
    # Busca todos los links en el archivo html
    links = [link.get("href") for link in soup.find_all("a")]

    # Saca los 3 primeros porque no son archivos
    links_ok = links[3:]

    # Cambia 0 por 1 para poder descargar (dl debe ser =1)
    links_download = [link[:-1] + "1" for link in links_ok]

    # return ((key_name, full_dir),)
    return links_download


url_dict = {}
route = "pipeline_cumulo/htmls/"
html_list = sorted(os.listdir(route))
for html_file in html_list:
    k = html_file.rsplit(".")[0]
    links_list = url_parser(route + html_file)
    url_dict.update({k: links_list})

# 1 json file per month
with open("2016_03.json", "w") as fp:
    json.dump(url_dict, fp, indent=2)
