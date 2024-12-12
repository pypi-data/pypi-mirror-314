# module of profiles aggregation
# this module allows the aggregation of oceanographic profiles

import pandas as pd
import xarray as xr
import warnings
import tempfile
import numpy as np
import os
from datetime import datetime
from dateutil import parser
import dask.array as da
import multiprocessing
from glob import glob
from time import time
from .read_and_write import read_and_store_dimensions
from typing import Dict, Any
from .multiprocess import exec_mlproc_tempdir
from .utils import open_and_expand, open_and_store, id_source_function, include_meta



def aggregate(files: list[str], prof_axis: str, force_del_dim: list[str] = None, 
                id_source: bool = False, 
                meta_file: str = None,
                meta_convention: list[str] = ["LAUNCH_DATE", "PLATFORM_TYPE", "PI_NAME"],
                ) -> xr.Dataset:
    """
    Aggregate datasets from multiple files.

    Parameters
    ----------
    files : list of str
        List of file paths to be aggregated.
    prof_axis : str
        The dimension along which to concatenate the datasets.
    force_del_dim : list of str, optional
        List of dimensions to force removal from aggregation.

    Returns
    -------
    xr.Dataset
        An aggregated xarray dataset containing the concatenated data.

    Raises
    ------
    MemoryError
        If there is not enough space to aggregate the dataset.
    """
    
    # sort files by order and extract times start and end : 
    files = sorted(files)
    first_ds = xr.open_dataset(files[0])
    last_ds = xr.open_dataset(files[-1])
    
    try:
        time_start = first_ds.attrs["time_coverage_start"]
    except KeyError:
        time_start = None
    try:
        time_end = last_ds.attrs["time_coverage_end"]
    except KeyError:
        time_end = None
        
    # Fonction pour parser la date et la formater
    def format_date(date_str):
        if date_str:
            # Utilise dateutil.parser.parse pour détecter automatiquement le format
            date_obj = parser.parse(date_str)
            return date_obj.strftime("%Y-%m-%dT%H:%M:%S")
        return None

    # Appliquer la fonction de formatage sur les dates de début et de fin
    if time_start:
        time_start = format_date(time_start)

    if time_end:
        time_end = format_date(time_end)



        
    # keeping the loop because it is quite the same as the map function and it avoid memory error
    start = time()
    c=0 
    df_dims = pd.DataFrame()
    for file in files : 
        df_dims = pd.concat([read_and_store_dimensions(file), df_dims]).reset_index().drop("index", axis=1)
        c+=1
        
    # if prof_axis not in files dimensions trigger warning 
    if prof_axis not in df_dims.columns:
        warnings.warn("Warning : concatenation axis is not in files dimensions, concatenation alog this new axis ")

    # check if any dimension is not shared by all files 
    nansum = df_dims[df_dims.columns.difference(['filepath', 'filename', 'estimated_compx8', 'estimated_size_Mb'])].isna().sum()
    undesirable_dimensions = nansum[nansum !=0].to_dict()

    # if any dim not shared by all, remove from shared dims and max levels : 
    cols_to_exclude = list(undesirable_dimensions.keys())
    [cols_to_exclude.append(x) for x in ['filepath', 'filename', 'estimated_compx8', 'estimated_size_Mb']]
    
    if force_del_dim:
        for dim in force_del_dim:
            undesirable_dimensions[dim] = 22 # arbitrary value

    
    # compute max_n_levels : sizes max of each dimension shared by all files 
    max_n_levels = df_dims[df_dims.columns.difference(cols_to_exclude)].max().to_dict()
    
    # expand each file
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f'Temporary directory created at: {temp_dir}')
        statvfs = os.statvfs(temp_dir)
        avail = statvfs.f_frsize * statvfs.f_bavail /(1024**2)/1000
                
        # number of workers avail
        nb_workers_avail = multiprocessing.cpu_count()

        # biggest file size
        fs_max = df_dims["estimated_compx8"].max()
        
        # theoretical number of files open in the same time
        # Getting usage of virtual_memory in GB 
        # print('RAM total (GB):', psutil.virtual_memory().total / (1024 ** 3))     
        # print('RAM available (GB):', psutil.virtual_memory().available / (1024 ** 3))     
        # print('         This not woerks and display the RAM of the host. Setting RAM limit to 12Gb for now')

        ram_avail = 12 * 1024 # in Mb
        nb_workers = np.floor(ram_avail / fs_max)

        if nb_workers > nb_workers_avail : 
            nbw = nb_workers_avail -2 # -2 for security
        else : 
            nbw = nb_workers -2 # -2 for security
            
        # final space used by the tmp dir
        final_space = df_dims["estimated_compx8"].sum()/1000
        
        # is it enough space ? (10% de marge sur l'estimation de compression 8:1, on est larges)
        if avail-(final_space*1.1) <= 0 : 
            raise MemoryError("Not enough space to aggregate this dataset => exit(). Please consider chunk this aggregation")


        #                           % % % % % % store files version multiprocessing % % % % % % 
        _ = exec_mlproc_tempdir(files, open_and_store, temp_dir, nbw, max_n_levels, prof_axis, undesirable_dimensions)
        
        # gather files to concatenate
        files2concat = sorted(glob(f"{temp_dir}/*"))
        # print(files2concat)
        end = time()
        print(f" files creation in tmp = {end-start} seconds")
        
        aggregated_dataset = xr.open_mfdataset(files2concat, combine='nested', concat_dim=prof_axis).load()
        
        # on peut trouver une pichenette sur le nombre de fichiers, si le nombre de fichiers est supérieur à 100 et que la taille dépasse XMb
        # , on divise le processus en paquets de 100 puis on réassemble. 
        # Enfin, si oin estime que le load du fichier va pêter la mémoire (ça n'arrivera pas si on ne traite que des fichiers harmonisés) 
        # on retourne le dossier tampon avec les ficheirs aggregés ? pas clair cette stratégie, 
        
        
        # aggregated_dataset = xr.open_mfdataset(files2concat, combine='nested', concat_dim=prof_axis, chunks='auto')
        # aggregated_dataset = xr.open_mfdataset(files2concat, combine='nested', concat_dim=prof_axis).load()#, chunks='auto')
    
        
        # replace time coverage start and time coverage end attributes
        try : 
            aggregated_dataset.attrs["time_coverage_start"] = time_start
        except:
            pass
        
        try:
            aggregated_dataset.attrs["time_coverage_end"] = time_end
        except:
            pass
        
 
        # # ----------------------------- % % % % % % version for loop % % % % % % -----------------------------
        # c = 0
        # res_computed = []
        # for f in files : 
        #     start_f = time()
        #     res_computed.append(1)
        #     # res_computed.append(open_and_expand(f, max_n_levels, prof_axis, undesirable_dimensions))
        #     if c ==0 : 
        #         aggregated_dataset = open_and_expand(f, max_n_levels, prof_axis, undesirable_dimensions)
        #     else : 
        #         aggregated_dataset = xr.concat([aggregated_dataset, open_and_expand(f, max_n_levels, prof_axis, undesirable_dimensions)], dim=prof_axis)
        #     # open_and_expand(f, max_n_levels, prof_axis, undesirable_dimensions)
        #     end_f = time()
        #     print(f"file : {len(res_computed)}/{len(files)} - {end_f - start_f} ")
        #     # aggregated_dataset = xr.concat(res_computed, dim=prof_axis)
        #     c += 1
        # # ----------------------------- % % % % % % version for loop % % % % % % -----------------------------
        
        if meta_file:
            include_meta(meta_file, aggregated_dataset, convention=meta_convention)
        
        if id_source :
            aggregated_dataset = id_source_function(aggregated_dataset, files)

    return aggregated_dataset


if __name__ == "__main__":
    # Example usage (assuming files and prof_axis are defined)
    # files = ['/runtime/data/6901580/profiles/BD6901580_032.nc', '/runtime/data/6901580/profiles/D6901580_050.nc']  # Replace with actual file paths
    
    # files = glob('/runtime/data/6901583/profiles/B*.nc')
    # [files.append(elem) for elem in glob('/runtime/data/6901583/profiles/D*.nc')]
    # [files.append(elem) for elem in glob('/runtime/data/6901583/profiles/R*.nc')]
    # print(len(files))

    # prof_axis = 'N_PROF'  # Replace with the desired profile axis
    # force_rm_dims = ["N_HISTORY", "N_CALIB"]
    
    # start_total = time()
    
    # start = time()
    # aggregated_data = aggregate(files[0:100], prof_axis, force_rm_dims, id_source=True, meta_file="/runtime/data/6901583/6901583_meta.nc")
    # end = time()
    # print(f"                    open_mfdataset duration : {(end-start)/60} minutes")
    
    # # start = time()
    # # aggregated_data = aggregated_data.load()
    # # end = time()
    # # print(f"                    .load() duration : {(end-start)/60} minutes")
    
    
    # print(aggregated_data)
    
    # end_total = time()
    # print(f"                    Computation time : {(end_total-start_total)/60} minutes")
    # print("the end")
    
    # ----------------- speed test new approach -----------------
    files = glob('/runtime/run/*.nc')
    
    prof_axis = 'profile'  # Replace with the desired profile axis
    force_del_dim = ["N_HISTORY", "N_CALIB"]
    
    start = time()
    aggregated_data = aggregate(files[0:10], prof_axis, force_del_dim, id_source=True, meta_file=None)
    end = time()
    print(f"                    open_mfdataset duration : {(end-start)/60} minutes")
    