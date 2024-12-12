# from . import aggregate_profiles, read_and_write, utils, multiprocesss

# Import the necessary modules and expose their content
from .aggregate_profiles import *  # Expose functions from aggregate_profiles.py
from .multiprocess import *        # Expose functions from multiprocess.py
from .read_and_write import *      # Expose functions from read_and_write.py
from .utils import *               # Expose functions from utils.py

# Define what gets exported when someone imports this package
__all__ = [
    # From aggregate_profiles.py
    "aggregate",  # Replace with actual function names
    # From multiprocess.py
    "exec_mlproc_tempdir",
    # From read_and_write.py
    "read_and_store_dimensions",
    # From utils.py
    "open_and_expand", "open_and_store", "id_source_function", "include_meta",
]