import concurrent.futures

import pandas as pd
from scidownl import scihub_download
from tqdm import tqdm


def download_papers(paper):
    name = paper.replace('/', ':')
    scihub_download(paper, paper_type="doi", out=f"./papers/{name}.pdf")

df = pd.read_csv('output.csv')
source = list(df['DOI'])
source = [doi for doi in source if pd.notna(doi)]

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Submit tasks to the executor
    futures = [executor.submit(download_papers, paper) for paper in source]

    # Iterate over completed futures to check progress
    for _ in tqdm(concurrent.futures.as_completed(futures), total=len(source)):
        pass

    import os

folder_path = "papers"  # Replace "papers" with your folder path

# Get the list of files in the folder
file_list = os.listdir(folder_path)

# Count the number of files
num_files = len(file_list)

print(f"\nThe number of files in the folder '{folder_path}' is: {num_files} out of {len(source)} initial DOIs\n")