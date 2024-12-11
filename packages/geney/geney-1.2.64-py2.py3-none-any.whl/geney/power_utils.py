import subprocess
import time
from dask_jobqueue import PBSCluster, SLURMCluster
from dask.distributed import Client, wait
import os
from tqdm import tqdm
from pathlib import Path
from geney import config_setup
from geney.utils import contains, available_genes
import warnings
import gc
import pandas as pd
import argparse

print("remote this")
tqdm.pandas()
warnings.filterwarnings('ignore')


def write_executors(folder_path, script='geney.power_utils', input_file='/tamir2/nicolaslynn/data/ClinVar/clinvar_oncosplice_input.txt', output_folder='/tamir2/nicolaslynn/data/oncosplice_base/oncosplice/clinvar_benchmarking', default_logging_path='/tamir2/nicolaslynn/temp/logging'):
    executor_path = Path(folder_path)
    executor_path.mkdir(parents=True, exist_ok=True)
    print(executor_path)
    default_logging_path = Path(default_logging_path)
    job_file_content = f'#!/bin/bash\nhostname\nsource /a/home/cc/students/outside/nicolaslynn/.bashrc\ncd {str(executor_path)}\nsource /tamir2/nicolaslynn/venvs/geney_dask/bin/activate\npython -m {script} -n 750 -m 5GB -i {input_file} -r {output_folder}'
    job_file = executor_path / 'job.sh'
    with open(job_file, 'w') as f:
        _ = f.write(job_file_content)
    submit_file_content = f'qsub -q tamirQ -l nodes=1:ppn=1,cput=24:00:00,mem=25000mb,pmem=25000mb,vmem=50000mb,pvmem=50000mb -e {default_logging_path / "err"} -o {default_logging_path / "out"} {executor_path / "job.sh"}'
    submit_file = executor_path / 'submit'
    with open(submit_file, 'w') as f:
        _ = f.write(submit_file_content)
    subprocess.run(['bash', (executor_path / 'submit')])
    # time.sleep(60)
    # job_file.unlink()
    # submit_file.unlink()
    # executor_path.rmdir()
    return None

def launch_dask_cluster(memory_size="3GB", num_workers=10, queue="tamirQ",
                        walltime="24:00:00", dashboard_address=":23154",
                        log_directory="dask-logs", slurm=False, organism='hg38'):
    """
    Launch a Dask cluster using PBS.

    Parameters:
    memory_size (str): Memory for each worker.
    num_workers (int): Number of workers to scale to.
    queue (str): Queue name for PBS.
    walltime (str): Walltime for PBS.
    dashboard_address (str): Address for the Dask dashboard.
    log_directory (str): Directory for Dask logs.

    Returns:
    tuple: A tuple containing the Dask client and cluster objects.
    """
    try:
        if slurm:
            dask_cluster = SLURMCluster(
                cores=1,
                memory=memory_size,
                processes=1,
                queue=queue,
                walltime='7200',
                scheduler_options={"dashboard_address": dashboard_address},
                log_directory=log_directory,
                # job_script_prologue=[f"cd {config_setup[organism]['BASE']}"]
            )

        else:
            dask_cluster = PBSCluster(
                cores=1,
                memory=memory_size,
                processes=1,
                queue=queue,
                walltime=walltime,
                scheduler_options={"dashboard_address": dashboard_address},
                log_directory=log_directory,
                # job_script_prologue=[f"cd {config_setup[organism]['BASE']}"]
            )

        dask_cluster.scale(num_workers)
        dask_client = Client(dask_cluster)
        return dask_client, dask_cluster

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None




def process_and_save_tasks(tasks, dask_client, funct, save_loc=None, num_workers=10, save_increment=20, file_index=0):
    """
    Process a list of tasks using Dask, saving the results incrementally.
    Parameters:
    tasks (list): List of tasks to be processed.
    save_loc (str): Location to save results.
    dask_client (Client): Dask client for task submission.
    num_workers (int): Number of workers to use.
    save_increment (int): Number of iterations after which to save results.
    file_index (int): Starting index for output files.
    Returns:
    None
    """
    def save_results(results, index):
        if results:
            df = pd.concat(results)
            df.to_csv(os.path.join(save_loc, f'results_{index}.csv'))
            return []
        return results

    futures, all_results = [], []
    for i, task in tqdm(enumerate(tasks), total=len(tasks)):
        futures.append(dask_client.submit(funct, task))
        if (i + 1) % num_workers == 0:
            wait(futures)
            all_results.extend([f.result() for f in futures if f.status == 'finished' and f.result() is not None])
            futures = []

        if (i + 1) % (save_increment * num_workers) == 0:
            all_results = save_results(all_results, file_index)
            file_index += 1
            gc.collect()
    wait(futures)
    all_results.extend([f.result() for f in futures if f.status == 'finished' and f.result() is not None])
    save_results(all_results, file_index)


def restart_checkpoint(result_dir):
    """
    Reloads processed results from CSV files, extracting unique mutation IDs and the highest checkpoint.

    Parameters:
    result_dir (str): Directory containing result CSV files.

    Returns:
    list: List of unique mutation IDs processed.
    int: The highest checkpoint value from the files.
    """
    result_path = Path(result_dir)
    files = sorted(result_path.glob('*'), key=lambda x: int(x.stem.split('_')[-1]), reverse=True)

    if not files:
        return [], 0

    try:
        data = []
        latest_file = files[0]
        for file in files:
            data.append(pd.read_csv(file))
        processed_muts = pd.concat(data).mut_id.unique().tolist()
        highest_checkpoint = int(latest_file.stem.split('_')[-1])
        return processed_muts, highest_checkpoint

    except Exception as e:
        print(f"Error processing file {files}: {e}")
        return [], 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run oncosplice with dask.')
    parser.add_argument('--input_file', '-i', required=True, help='input text file')
    parser.add_argument('--results_directory', '-r', required=False, help='result directory', default=config_setup['ONCOSPLICE'])
    parser.add_argument('--num_workers', '-n', type=int, required=False, help='number of dask workers to recruit', default=10)
    parser.add_argument('--worker_size', '-m', type=str, required=False, help='dask worker memory allocation', default="3GB")
    args = parser.parse_args()

    client, cluster = launch_dask_cluster(memory_size=args.worker_size, num_workers=args.num_workers)
    muts = open(args.input_file, 'r').read().splitlines()
    processed_mutations, last_count = restart_checkpoint(args.results_directory)
    processed_mutations = sorted(list(set(processed_mutations)))
    muts = [m for m in tqdm(muts) if not contains(processed_mutations, m)]
    valid_genes = available_genes()
    muts = [m for m in muts if contains(valid_genes, m.split(':')[0])]
    print(f"Valid mutations: {len(muts)}")
    process_and_save_tasks(tasks=muts,
                           save_loc=args.results_directory,
                           dask_client=client,
                           file_index=last_count + 1,
                           num_workers=args.num_workers)
    print("Done.")

