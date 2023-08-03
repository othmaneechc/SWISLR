# SWISLR

This repository contains all of the code used by team 25 for Duke University Data plus 2023: Assessing Climate Change Risk of Rural Coastal Plain Communities

## Pre-Requirements

All the code is within the "script" folder. To install the necessary dependencies, navigate to the script directory and run the following command: 

`pip install -r requirements.txt`

## Scopus API 

To use the Scopus API, follow these steps:

1. Go to https://dev.elsevier.com/ and create an account.
2. Create an API Key.
3. Once you have your API Key, run the file abstract_requests.py.
   
### Documentation for Command-line Arguments:

The `keywords` argument allows you to specify one or more keywords for searching or filtering operations. Separate multiple keywords with spaces. The default keywords are "salinization" and "flooding".

Example:

`python abstract_requests.py -w keyword1 keyword2 keyword3`

The `api_key` argument is used to provide your API key. This key is required to access certain services or resources within the script. Provide a single value for this argument.

Example:

`python abstract_requests.py -w keyword1 keyword2 keyword3 -k a4dfe1b4f9535e6e41587a40f9ba9877`

The output data from Scopus is saved in the file `output_files/output.csv`. Remember to update your API Key after a certain number of requests

## Sci-Hub API

This repository includes two scripts that use different Sci-Hub APIs: `github_scihub_api.py` and `scihub_api.py`. These scripts process keywords, read a CSV file, and download papers based on the provided input. They also define a function called download_papers() to facilitate paper downloads.

### Documentation for Command-line Arguments:

The `file` argument allows you to specify the path(s) to the CSV file(s) to be processed. You can provide one or more file paths as input. If no file path is provided, the script assumes the file path as `output_files/output.csv`. The CSV file should have a "DOI" column.

Examples: 

`python github_scihub_api.py -f input_files/data.csv`
`python scihub_api.py -f input_files/data.csv`

The `directory` argument allows you to specify the directory where the downloaded papers will be saved. You can provide one or more directory paths as input. If no directory path is provided, the script assumes the directory as `papers`.

Example: 

`python scihub_api.py -f input_files/data.csv -d download_directory`

## PDF Cleaning

After saving PDF files from Sci-Hub, this script processes a folder containing the PDF files, retrieves information from each file, and deletes corrupted files. It utilizes the `argparse` module for command-line argument parsing and the `os` module for file and directory handling.

### Documentation for Command-line Arguments:

The `folder` argument allows you to specify the path to the folder containing the PDF files to be processed. Provide a single folder path as input. If no folder path is provided, the script assumes the folder path as "combined_data".

Example: 

`python cleaner.py -f pdf_folder`

## PDF Analysing

This script processes a folder containing PDF files and tries to find the most common location words. It outputs all the data in a CSV file called `primary_pdf_analysis.py.`

### Documentation for Command-line Arguments:

The `folder` argument allows you to specify the path to the folder containing the PDF files. Provide a single folder path as input. If no folder path is provided, the script assumes the folder path as "combined_data".

Example: 

`python pdf_analyser.py -f pdf_folder`

## Geolocation

This script takes a csv and tries to find location fields ("location", "address", "city", "county", "state", "country") and tries to find Longitude/Latitude information to add them as additional fields. It searches Nominatum using these fields in the query and Nominatum then returns Longitude/Latitude information to the best it can. Prolonged use can result in errors occurring (likely due to IP blocking), so using this script several times may be necessary. Once started, the script will prompt the user to provide a name for the output file.

Example:

`python AddressToLatLong.py sheets.csv`

`Enter Name for New Generated File: sheetsLongLat`




