import multiprocessing
import sys
import os

def exec_mlproc_function(target, func, *args):
    """ execute function over targer thru multiple processes, store result in a list """
    output_list = []
    
    nb_workers_avail = multiprocessing.cpu_count()
    print(nb_workers_avail)        
    
    # process pool
    with multiprocessing.Pool(nb_workers_avail-2) as pool:
        # EXECUTE asynchronously the application of 
        results = [pool.apply_async(func, (targ,*args)) for targ in target]
        # results = [pool.imap(func, (targ,*args)) for targ in target]

        # Get the results
        for result in results:
            output_list.append(result.get())


    return output_list
    
# --------------------------------------------------------

def exec_mlproc_tempdir(target, func, temp_dir, nb_workers, *args):
    """ execute function over target thru multiple processes, storage of files in temp_folder """

    print("             Start Multi processing ")
    # process pool
    with multiprocessing.Pool(nb_workers) as pool:
        # EXECUTE asynchronously the application of 
        
        results = [pool.apply_async(func, (targ, temp_dir, *args)) for targ in target]
        
        for result in results:
            result.wait()
    
