#from io import BytesIO

#from diskcache import Cache
#from diskcache.core import ENOVAL
#import ipdb

#CACHE_PATH = pathlib.Path(os.path.expanduser(os.path.join("~", "cache")))

#cache = Cache()
#cache.set("key", BytesIO(b"value"), expire=None, read=True)
#juan
#from diskcache import FanoutCache, Cache, JSONDisk, core
#cache = Cache(directory="cache")
#def download_data(a):
#    ... return

#@cache.memoize(typed=True, expire=None, tag="fib")
#def load_image(a, k=1):
#    data = download_data(a)
#    return str(a) + "hola"


#cache.directory

#core.args_to_key(("load_image",), ("35",), {"k": 1}, True, set())


#cache.expire()
#%%
#MA
import pipeline
import matplotlib.pyplot as plt
#for que extraiga cada archivo del zip
nc_file = pipeline.zip_to_nc() #dir_name, file_name
norm_bands = pipeline.processing(nc_file)
a = pipeline.generate_tiles(norm_bands) #-> estos son h5 que se guarda en la memoria o ftp
# delate nc_file from local ?
#plt.imshow(a[45][:,:,-3:])

