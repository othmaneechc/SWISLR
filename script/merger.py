import os
import shutil

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser

data1_folder = "data1"
data2_folder = "data2"
output_folder = "combined_data"

# Step 1: Get file lists
data1_files = [file for file in os.listdir(data1_folder) if file.endswith(".pdf")]
data2_files = [file for file in os.listdir(data2_folder) if file.endswith(".pdf")]

# Step 2: Determine shared files
shared_files = set(data1_files).intersection(data2_files)
num_shared_files = len(shared_files)

# Step 3: Count total files in each folder
num_files_data1 = len(data1_files)
num_files_data2 = len(data2_files)

# Step 4: Identify and count corrupted files
def is_pdf_corrupted(file_path):
    try:
        with open(file_path, "rb") as file:
            parser = PDFParser(file)
            document = PDFDocument(parser)
            _ = len(document.catalog)  # Accessing the catalog to check for corruption
        return False
    except:
        return True

num_corrupted_data1 = sum(is_pdf_corrupted(os.path.join(data1_folder, file)) for file in data1_files)
num_corrupted_data2 = sum(is_pdf_corrupted(os.path.join(data2_folder, file)) for file in data2_files)

# Print the results
print("Number of shared files:", num_shared_files)
print(f"Number of files in {data1_folder}:", num_files_data1)
print(f"Number of files in {data2_folder}:", num_files_data2)
print("Number of corrupted files in data1:", num_corrupted_data1)
print("Number of corrupted files in data2:", num_corrupted_data2)


# Step 1: Get file lists
data1_files = [file for file in os.listdir(data1_folder) if file.endswith(".pdf")]
data2_files = [file for file in os.listdir(data2_folder) if file.endswith(".pdf")]

# Combine the file lists and remove duplicates
combined_files = set(data1_files + data2_files)

# Step 2: Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Step 3: Copy files to the output folder
for file in combined_files:
    source_path_data1 = os.path.join(data1_folder, file)
    source_path_data2 = os.path.join(data2_folder, file)
    output_path = os.path.join(output_folder, file)
    
    # Prioritize files from data1 if there are duplicates
    if file in data1_files:
        shutil.copy2(source_path_data1, output_path)
    else:
        shutil.copy2(source_path_data2, output_path)

# Print the success message
print("Files from data1 and data2 copied to the output folder without duplicates.")
print("Output folder path:", output_folder)

