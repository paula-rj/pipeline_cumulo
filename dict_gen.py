from bs4 import BeautifulSoup

"""Este codigo genera una lista de links
para descargar cada archivo de cumulo.
url: full url para descargar de cumulo 
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
    links_ok = links[:-3]

    # Cambia 0 por 1 para poder descargar (dl debe ser =1)
    links_download = [link[:-1] + "1" for link in links_ok]

    # return ((key_name, full_dir),)
    return links_download


# url_dict = {}
# years_avail = (2016,)
# days = np.arange(1, 366).tolist()
# for year in years_avail:
#    for day in days:
#        dt = datetime.datetime.strptime(f"{year} {day}", "%Y %j")
#        url_dict.update((url_parser(dt)))
# with open("urls.json", "w") as fp:
#    json.dump(url_dict, fp, indent=2)
