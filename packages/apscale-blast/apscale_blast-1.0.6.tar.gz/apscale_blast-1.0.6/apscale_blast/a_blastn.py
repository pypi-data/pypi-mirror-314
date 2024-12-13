import argparse
import os
from pathlib import Path
from Bio import SeqIO
import datetime
import subprocess
import shutil
import time
import glob
import multiprocessing
import threading
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
import pyarrow as pa
import pyarrow.parquet as pq

# Lock for thread-safe print statements
print_lock = threading.Lock()

# Ensure multiprocessing works when frozen (e.g. for executables)
multiprocessing.freeze_support()


def fasta_subset(fasta_file, subset_size):
    """
    Splits a large fasta file into smaller subsets for parallel processing.

    Args:
        fasta_file (str): Path to the input fasta file.
        subset_size (int): Number of sequences per subset file.

    Returns:
        Path: Path to the directory containing the subsets.
    """
    print('{} : Creating subset(s) from fasta file.'.format(datetime.datetime.now().strftime('%H:%M:%S')))

    subset_size = int(subset_size)
    fasta_file = Path(fasta_file)

    # Create a new directory for subsets
    subset_folder = Path(fasta_file.parent).joinpath('fasta_subsets')
    os.makedirs(subset_folder, exist_ok=True)

    # Delete existing subset files, if any
    for f in glob.glob(str(subset_folder / '*.fasta')):
        os.remove(f)

    chunk_fasta_files = []
    i, n = 1, 1

    # Splitting fasta file into chunks
    with open(fasta_file) as handle:
        for record in SeqIO.parse(handle, 'fasta'):
            chunk_fasta = '{}/subset_{}.fasta'.format(subset_folder, i)
            if chunk_fasta not in chunk_fasta_files:
                chunk_fasta_files.append(chunk_fasta)

            with open(chunk_fasta, 'a') as output_handle:
                SeqIO.write(record, output_handle, 'fasta')

            # Create new chunk after reaching subset_size
            if n == subset_size:
                n = 1
                i += 1
            else:
                n += 1

    print('{} : Created {} subset(s) from fasta file.'.format(datetime.datetime.now().strftime('%H:%M:%S'), i))
    return subset_folder


def accession2taxonomy(df_1, taxid_dict, col_names_2, db_name):
    """
    Maps accession numbers to taxonomy using a dictionary.

    Args:
        df_1 (pd.DataFrame): DataFrame containing accession data.
        taxid_dict (dict): Dictionary mapping accessions to taxonomy.
        col_names_2 (list): Column names for the output DataFrame.
        db_name (str): Name of the database.

    Returns:
        pd.DataFrame: DataFrame with taxonomy information appended.
    """
    df_2_list = []
    for row in df_1.values.tolist():
        ID_name, accession = row[0], row[1]
        evalue, similarity = row[-1], row[-2]

        taxonomy = taxid_dict.get(accession, ['NoMatch'] * 7)
        df_2_list.append([ID_name] + taxonomy + [similarity, evalue])

    df_2 = pd.DataFrame(df_2_list, columns=col_names_2)
    return df_2


def blastn_parallel(fasta_file, n_subsets, blastn_subset_folder, blastn_exe, db_folder, i, print_lock, task, max_target_seqs, masking):
    """
    Runs a single BLASTN job on a subset of the fasta file.

    Args:
        fasta_file (str): Path to the subset fasta file.
        n_subsets (int): Total number of subsets.
        blastn_subset_folder (Path): Folder to store BLASTN output.
        blastn_exe (str): Path to the BLASTN executable.
        db_folder (Path): Path to the BLASTN database.
        i (int): Subset index.
        print_lock (threading.Lock): Lock for synchronized printing.
        task (str): BLAST task (e.g., 'megablast', 'blastn').
        max_target_seqs (int): Maximum target sequences to report.
    """
    blastn_csv = blastn_subset_folder.joinpath(Path(fasta_file).stem + '_' + task + '.csv')

    # Skip if output already exists
    if os.path.isfile(blastn_csv):
        with print_lock:
            print('{}: Skipping {} (already exists).'.format(datetime.datetime.now().strftime('%H:%M:%S'),
                                                             blastn_csv.stem))
        time.sleep(1)
    elif masking == "No":
        # Run the BLASTN command
        subprocess.call([blastn_exe, '-task', task, '-db', str(db_folder), '-query', str(fasta_file),
                         '-num_threads', str(1), '-max_target_seqs', str(max_target_seqs),
                         '-dust', 'no', '-soft_masking', 'false',
                         '-outfmt', '6 delim=;; qseqid sseqid pident evalue', '-out', str(blastn_csv)])
        with print_lock:
            print('{}: Finished blastn for subset {}/{}.'.format(datetime.datetime.now().strftime('%H:%M:%S'), i + 1,
                                                                 n_subsets))
    else:
        # Run the BLASTN command
        subprocess.call([blastn_exe, '-task', task, '-db', str(db_folder), '-query', str(fasta_file),
                         '-num_threads', str(1), '-max_target_seqs', str(max_target_seqs),
                         '-outfmt', '6 delim=;; qseqid sseqid pident evalue', '-out', str(blastn_csv)])
        with print_lock:
            print('{}: Finished blastn for subset {}/{}.'.format(datetime.datetime.now().strftime('%H:%M:%S'), i + 1,
                                                                 n_subsets))



def blastn_v2(blastn_exe, query_fasta, blastn_database, project_folder, n_cores, task, subset_size, max_target_seqs, masking):
    """
    Improved BLASTN function that utilizes multithreading for faster performance.

    Args:
        blastn_exe (str): Path to the BLASTN executable.
        query_fasta (str): Path to the input fasta file.
        blastn_database (str): Path to the BLASTN database.
        project_folder (str): Path to the project directory for saving output.
        n_cores (int): Number of cores to use for parallel processing.
        task (str): BLAST task (e.g., 'megablast', 'blastn').
        subset_size (int): Size of fasta file subsets.
        max_target_seqs (int): Maximum target sequences to report.
    """
    # Split fasta file into subsets
    subset_folder = fasta_subset(query_fasta, subset_size)

    project_folder = Path(project_folder)
    fasta_files = sorted(glob.glob(str(subset_folder) + '/*.fasta'))
    n_subsets = len(fasta_files)

    # Map task names to valid BLAST task identifiers
    task_mapping = {
        'Highly similar sequences (megablast)': 'megablast',
        'More dissimilar sequences (discontiguous megablast)': 'dc-megablast',
        'Somewhat similar sequences (blastn)': 'blastn'
    }
    task = task_mapping.get(task, task)

    filename = Path(query_fasta).stem.replace('.', '_').replace(' ', '_')

    print('{}: Starting {} for \'{}\''.format(datetime.datetime.now().strftime('%H:%M:%S'), task, filename))
    print('{}: Your database: {}'.format(datetime.datetime.now().strftime('%H:%M:%S'), Path(blastn_database).stem))

    db_folder = Path(blastn_database).joinpath('db')

    # Create a folder for subset BLASTN results
    blastn_subset_folder = project_folder.joinpath('subsets')
    os.makedirs(blastn_subset_folder, exist_ok=True)

    # Run BLASTN in parallel across all subsets
    Parallel(n_jobs=n_cores, backend='threading')(delayed(blastn_parallel)(
        fasta_file, n_subsets, blastn_subset_folder, blastn_exe, db_folder, i, print_lock, task, max_target_seqs, masking
    ) for i, fasta_file in enumerate(fasta_files))

    # Write log file with database and task information
    with open(project_folder.joinpath('log.txt'), 'w') as f:
        f.write('Your database: {}\n'.format(Path(blastn_database).stem))
        f.write('Your task: {}\n'.format(task))

    # Write OTU report
    with open(project_folder.joinpath('IDs.txt'), 'w') as f:
        for record in SeqIO.parse(query_fasta, "fasta"):
            f.write(record.id + '\n')

    print('{}: Finished {} for \'{}\''.format(datetime.datetime.now().strftime('%H:%M:%S'), task, filename))

    # Merge BLASTN results (CSV files) into a single Parquet file with Snappy compression
    csv_files = glob.glob('{}/*.csv'.format(str(blastn_subset_folder)))
    col_names = ['unique ID', 'Sequence ID', 'Similarity', 'evalue']
    df = pd.concat(
        (pd.read_csv(f, header=None, sep=';;', names=col_names, engine='python').fillna('NAN') for f in csv_files))

    table = pa.Table.from_pandas(df)
    pq.write_table(table, project_folder.joinpath('{}.parquet.snappy'.format(filename)), compression='snappy')

    # Remove temporary subset fasta folder
    shutil.rmtree(subset_folder)


def main(blastn_exe, query_fasta, blastn_database, project_folder, n_cores, task, subset_size, max_target_seqs, masking):
    """
    Main entry point for the script.
    """

    # Run the BLASTn filter
    blastn_v2(blastn_exe, query_fasta, blastn_database, project_folder, n_cores, task, subset_size, max_target_seqs, masking)

if __name__ == '__main__':
    main()