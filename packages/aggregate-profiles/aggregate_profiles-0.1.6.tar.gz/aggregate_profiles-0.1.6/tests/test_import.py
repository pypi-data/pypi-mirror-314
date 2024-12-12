import os
from glob import glob 
from time import time

def print_tree(directory, prefix=""):
    """Recursively print a directory tree."""
    # List all files and directories in the given directory
    entries = sorted(os.listdir(directory))
    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = index == len(entries) - 1
        # Determine the prefix for the current entry
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{entry}")
        # If the entry is a directory, recurse into it
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(path, new_prefix)

# Run the function on the current directory or specify your package root
print("Package Tree:")
print_tree("/app")


# imports
from ..aggregate_profiles.aggregate_profiles import aggregate

# ----------------- speed test new approach -----------------
files = sorted(glob('/runtime/run/*.nc'))

prof_axis = 'profile'  # Replace with the desired profile axis
force_rm_dims = ["N_HISTORY", "N_CALIB"]


start = time()
aggregated_data = aggregate(files[0:10], prof_axis, force_rm_dims, id_source=True, meta_file=None)
end = time()
print(f"                    open_mfdataset duration : {(end-start)/60} minutes")

print("done")
