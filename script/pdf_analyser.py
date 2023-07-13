import argparse
import concurrent.futures
import glob
import json
import re
from collections import Counter
from functools import partial
from io import StringIO
from multiprocessing import Pool

import nltk
import numpy as np
import pandas as pd
import spacy
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from tqdm import tqdm


def get_pdf_file_content(path_to_pdf):
    # Set parameters
    out_text = StringIO()
    text_converter = TextConverter(PDFResourceManager(caching=True), out_text, laparams=LAParams())
    interpreter = PDFPageInterpreter(PDFResourceManager(caching=True), text_converter)

    fp = open(path_to_pdf, 'rb')

    # Set the maximum number of pages to read
    max_pages = 7

    # Use tqdm to create a progress bar
    # with tqdm(total=max_pages, desc="Extracting") as pbar:
    for index, page in enumerate(PDFPage.get_pages(fp, pagenos=set())):
        interpreter.process_page(page)
        # pbar.update(1)

        # Check if the maximum number of pages has been reached
        if index + 1 >= max_pages:
            break

    text = out_text.getvalue()

    fp.close()
    text_converter.close()
    out_text.close()

    return text

def replace_newlines(text):
    # Replace newlines in the middle of a sentence with spaces
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

    # Remove newlines at the end of a sentence
    text = re.sub(r'\n$', '', text)

    return text

def most_recurrent_locations(text: str, number_elements) -> dict:
    # Load the pre-trained model
    nlp = spacy.load("en_core_web_sm")

    # Replace newlines in the text
    sample_text = replace_newlines(text)

    # Process the text
    doc = nlp(sample_text)

    # Find location words and their locations
    locations = [entity.text for entity in doc.ents if entity.label_ == "GPE" or entity.label_ == "LOC"]

    # Disregard strings that contain specific words
    disregarded_words = ['USA', 'United States', 'United States of America', 'North America', 'UNITED STATES', 'al.', 'US', "U.S.", 'the United States']
    locations = [location for location in locations if not any(word in location for word in disregarded_words)]

    # Count the frequency of each location
    location_counts = Counter(locations)

    # Sorting locations by frequency
    sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)

    # Create a dictionary with 7 item (frequency) format
    first_elements = {f"{item} ({count})": count for item, count in sorted_locations[:number_elements]}

    return first_elements


def get_pdf_file_names(path):
    pdf_files = glob.glob(path)
    return pdf_files

# Define a function to process a single file
def process_pdf_file(file):
    content = get_pdf_file_content(file)
    output_dict = most_recurrent_locations(content, 7)
    return file, list(output_dict.keys())

def df_maker(path, filename):
    # Remove "PDF Papers (20)" from the strings in pdf_files
    filename = [file.replace(path.split("/")[0] + "/", "") for file in filename]
    filename = [file.replace(".pdf", "") for file in filename]
    filename = [file.replace(":", "/") for file in filename]

    # Extract the columns from list_of_lists
    col1 = [item[0] if len(item) > 0 else '' for item in list_of_lists]
    col2 = [item[1] if len(item) > 1 else '' for item in list_of_lists]
    col3 = [item[2] if len(item) > 2 else '' for item in list_of_lists]
    col4 = [item[3] if len(item) > 3 else '' for item in list_of_lists]
    col5 = [item[4] if len(item) > 4 else '' for item in list_of_lists]
    col6 = [item[5] if len(item) > 5 else '' for item in list_of_lists]
    col7 = [item[6] if len(item) > 6 else '' for item in list_of_lists]

    # Create the dataframe
    data = {
        'DOI': filename,
        'Col1': col1,
        'Col2': col2,
        'Col3': col3,
        'Col4': col4,
        'Col5': col5,
        'Col6': col6,
        'Col7': col7
    }
    return pd.DataFrame(data)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Folder Name')
    parser.add_argument('-f', '--folder', nargs='+', help='Folder', default="combined_data")

    args = parser.parse_args()
    keywords = args.folder[0]

    path = keywords + "/*.pdf"
    pdf_files = get_pdf_file_names(path)
    list_of_lists = []

    filename = []
    # Create a ThreadPoolExecutor with the maximum number of worker threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the file processing tasks to the executor
        future_results = [executor.submit(process_pdf_file, file) for file in pdf_files]

        # Use tqdm to track the progress of the tasks
        for future in tqdm(concurrent.futures.as_completed(future_results), total=len(future_results)):
            # Retrieve the result from the completed task and append it to the list
            list_of_lists.append(future.result()[1])
            filename.append(future.result()[0])

    # Find the maximum number of elements in the lists
    max_list_length = max(len(lst) for lst in list_of_lists)

    # Add empty strings to lists lacking elements
    for lst in list_of_lists:
        while len(lst) < max_list_length:
            lst.append('')

    # Now all the lists inside list_of_lists have the same number of elements

    df_maker(path, filename).to_csv('output_files/primary_pdf_analysis.csv')