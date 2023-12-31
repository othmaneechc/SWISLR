# SWISLR

This repository contains all of the code used by team 25 for Duke University Data plus 2023: Assessing Climate Change Risk of Rural Coastal Plain Communities. 

Our goal was to create a dataset containing all the research happening in the US related to SWISLR that was then mapped using ArcGIS. We found many ways to gather the data and unfortunately, we realized (a bit late) that it is usually easier to download the data we need manually from journal databases (Web of Science, Scopus...) than use their APIs. 

Here are a few ways to collect data, and things you need to know before using this code. 

- Downloading PDF files, PDF mining, then extracting data with SpaCy/ChatGPT.
- Analysing Abstracts (Very easy to download as CSV from most journal databases) and extracting data with SpaCy/ChatGPT.
- The Scopus API can be useful if you want to get data for a large number of keyword combinations.
- The code might need a few edits depending on your computer's local environment.
- Here is the link to the map: https://dukeuniv.maps.arcgis.com/apps/mapviewer/index.html?webmap=46722778e4cb468bb9d2431784d8d204

## Pre-Requirements

To install the necessary dependencies, run the following command: 

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

`scihub_api.py` tends not to work due to the lack of working proxies. That is, if you have access to working proxies, then you can edit the code and run it.

### Documentation for Command-line Arguments:

The `file` argument allows you to specify the path(s) to the CSV file(s) to be processed. You can provide one or more file paths as input. If no file path is provided, the script assumes the file path as `output_files/output.csv`. The CSV file should have a "DOI" column.

Examples: 

`python github_scihub_api.py -f input_files/data.csv`
`python scihub_api.py -f input_files/data.csv`

The `directory` argument allows you to specify the directory where the downloaded papers will be saved. You can provide one or more directory paths as input. If no directory path is provided, the script assumes the directory as `papers`.

Example: 

`python scihub_api.py -f input_files/data.csv -d download_directory`

## PDF Location Analysis

This script processes a folder containing PDF files and tries to find the most common location words. It outputs all the data in a CSV file called `pdf_location_analysis.py.`

### Documentation for Command-line Arguments:

The `folder` argument allows you to specify the path to the folder containing the PDF files. Provide a single folder path as input.

Example: 

`python pdf_location_analysis.py -p pdf_folder`

## Geolocation (Longitude & Latitude)

This script takes a CSV and tries to find location fields ("location", "address", "city", "county", "state", "country") and tries to find Longitude/Latitude information to add them as additional fields. It searches Nominatum using these fields in the query and Nominatum then returns Longitude/Latitude information to the best it can. Prolonged use can result in errors occurring (likely due to IP blocking), so using this script several times may be necessary. Once started, the script will prompt the user to provide a name for the output file.

Example:

`python AddressToLatLong.py sheets.csv`

`Enter Name for New Generated File: sheetsLongLat`




