import os
import warnings
import xarray as xr
import pandas as pd


def read_and_store_dimensions(file):
    """  """
    with xr.open_dataset(file, decode_times=False) as ds: # decode=False to avoid temporal data loading
        dims = dict(ds.sizes)
        dims["filename"] = os.path.basename(file)
        dims["filepath"] = file
        dims["estimated_compx8"] = file_size(file)*8
        dims["estimated_size_Mb"] = estimate_memory(ds)
        return pd.DataFrame(dims, index=[0])
    

def estimate_memory(ds):
    total_memory = 0
    for var_name, variable in ds.data_vars.items():
        # compute each variable size
        size = variable.size * variable.dtype.itemsize  # taille en octets
        total_memory += size

    return total_memory/(1024^2) # in Mo 

def file_size(file):
    size = os.path.getsize(file)  # Get size in Mbytes
    return size / (1024 ** 2)

def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        print(it)
        for entry in it:
            if entry is not dir:
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total