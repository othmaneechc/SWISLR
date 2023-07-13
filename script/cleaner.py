import argparse
import os

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser, PDFSyntaxError

parser = argparse.ArgumentParser(description='Script to process keywords.')
parser.add_argument('-f', '--folder', nargs='+', help='folder', default="combined_data")

args = parser.parse_args()
combined_folder = args.folder[0]

# Step 1: Get file list
combined_files = [file for file in os.listdir(combined_folder) if file.endswith(".pdf")]

# Step 2: Iterate over files and retrieve information
num_files = len(combined_files)
corrupted_files = []

for file in combined_files:
    file_path = os.path.join(combined_folder, file)
    
    try:
        with open(file_path, "rb") as file_obj:
            parser = PDFParser(file_obj)
            document = PDFDocument(parser)
            num_pages = len(document.catalog)
            # Add any additional information you need to retrieve from the PDF files
            # For example, you can extract metadata, text content, etc.
            
        # Print any additional information you retrieved
            
    except (PDFSyntaxError, FileNotFoundError):
        corrupted_files.append(file)
        os.remove(file_path)  # Delete the corrupted file

# Print the summary
print("\nSummary:")
print("Number of files:", num_files)
print("Number of corrupted files:", len(corrupted_files))
print("Corrupted files:", corrupted_files)
