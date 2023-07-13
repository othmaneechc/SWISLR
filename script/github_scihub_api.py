import argparse
import concurrent.futures

import pandas as pd
from scidownl import scihub_download
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Script to process keywords.')
parser.add_argument('-f', '--file', nargs='+', help='file', default='output_files/output.csv')
parser.add_argument('-d', '--directory', nargs='+', help='directory', default='papers')

args = parser.parse_args()
file = args.file[0]
dir = args.directory[0]

df = pd.read_csv(file)

def download_papers(paper):
    name = paper.replace('/', ':')
    scihub_download(paper, paper_type="doi", out=f"./{dir}/{name}.pdf")

source = list(df['DOI'])
source = [doi for doi in source if pd.notna(doi)]

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Submit tasks to the executor
    futures = [executor.submit(download_papers, paper) for paper in source]

    # Iterate over completed futures to check progress
    for _ in tqdm(concurrent.futures.as_completed(futures), total=len(source)):
        pass

    import os

folder_path = f"{dir}"  # Replace "papers" with your folder path

# Get the list of files in the folder
file_list = os.listdir(folder_path)

# Count the number of files
num_files = len(file_list)

print(f"\nThe number of files in the folder '{folder_path}' is: {num_files} out of {len(source)} initial DOIs\n")