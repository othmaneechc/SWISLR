import argparse
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

import nltk
import numpy as np
import pandas as pd
import requests
import spacy
from tqdm import tqdm

# Get the keywords
parser = argparse.ArgumentParser(description='Script to process keywords.')
parser.add_argument('-w', '--keywords', nargs='+', help='Keywords', default=['salinization', 'flooding'])
parser.add_argument('-k', '--api_key', help='API key')

args = parser.parse_args()
keywords = args.keywords

# Get the keywords
my_input = ' AND '.join(keywords)

# Set your API Key
if args.api_key is None:
    print("\nPlease provide an API key using the -k or --api_key option.\n")
    exit()

key = args.api_key
# key = 'a4dfe1b4f9535e6e41587a40f9ba9877'

# Create a session for making requests
session = requests.Session()
session.headers['X-ELS-APIKey'] = key
session.headers['X-ELS-ResourceVersion'] = 'XOCS'
session.headers['Accept'] = 'application/json'

def scopus_search(my_input: str) -> list:
    api_resource = "https://api.elsevier.com/content/search/scopus?"
    search_param = f'query=title-abs-key({my_input})'  # for example

    # Set the desired number of results per page
    results_per_page = 25

    # Send the first request to get the total number of results
    first_page_request = session.get(api_resource + search_param + f"&count={results_per_page}&start=0")
    first_page = json.loads(first_page_request.content.decode("utf-8"))

    total_results = int(first_page['search-results']['opensearch:totalResults'])
    total_pages = (total_results // results_per_page) + 1

    # List to store all articles
    articles_list = []

    print(f"Scrapping Data Pages from Scopus using {my_input}...")
    # Iterate over all pages
    with ThreadPoolExecutor() as executor:
        for page_number in tqdm(range(total_pages)):
            start_index = page_number * results_per_page
            page_request = session.get(api_resource + search_param + f"&count={results_per_page}&start={start_index}")
            page = json.loads(page_request.content.decode("utf-8"))
            try:
                articles_list.extend(page['search-results']['entry'])
            except:
                continue

        print(f"Number of articles: {len(articles_list)}")
        return articles_list

def article_info(articles_list: list) -> set:
    print(f"\nGetting article titles...")

    article_title = []
    article_doi = []
    article_eid = []
    article_ID = []
    article_pii = []
    article_url = []
    article_creator = []
    article_pub = []
    article_coverDate = []
    article_number_citations = []
    

    global outliers
    outliers = {}
    # Access individual articles
    with ThreadPoolExecutor() as executor:
        for article in tqdm(range(len(articles_list))):
            try:
                article_pii.append(articles_list[article].get("pii"))
                article_title.append(articles_list[article].get("dc:title"))
                article_doi.append(articles_list[article].get("prism:doi"))
                article_eid.append(articles_list[article].get("eid"))
                article_ID.append(articles_list[article].get("dc:identifier"))
                article_url.append(articles_list[article].get("prism:url"))
                article_creator.append(articles_list[article].get("dc:creator"))
                article_pub.append(articles_list[article].get("prism:publicationName"))
                article_coverDate.append(articles_list[article].get("prism:coverDate"))
                article_number_citations.append(articles_list[article].get("citedby-count"))

            except:
                article_pii.append(None)
                article_doi.append(None)
                article_title.append(articles_list[article].get("dc:title"))
                article_eid.append(articles_list[article].get("eid"))
                article_ID.append(articles_list[article].get("dc:identifier"))
                article_url.append(articles_list[article].get("prism:url"))
                article_creator.append(None)
                article_pub.append(articles_list[article].get("prism:publicationName"))
                article_coverDate.append(articles_list[article].get("prism:coverDate"))
                article_number_citations.append(articles_list[article].get("citedby-count"))


        return (
            article_title, article_doi, article_eid, article_ID,
            article_pii, article_url, article_creator,
            article_pub, article_coverDate, article_number_citations
        )

affiliation = []
area = []
author_count = []

def scopus_id_abstract_retriever(scopus_id: str) -> str:
    api_endpoint = f"https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}"

    # Make the request to retrieve the abstract
    response = session.get(api_endpoint)
    data = json.loads(response.content.decode("utf-8"))
    # Extract the abstract from the response
    try:
        abstract = data["abstracts-retrieval-response"]["coredata"]["dc:description"]
        try: affiliation.append(data["abstracts-retrieval-response"]["affiliation"]["affilname"])
        except:
            try: affiliation.append(data["abstracts-retrieval-response"]["affiliation"])
            except: affiliation.append(None)
        # Study Area
        try:
            result = data["abstracts-retrieval-response"]["subject-areas"]["subject-area"]
            subjects = [subject["$"] for subject in result]
            area.append(" & ".join(subjects))
        except:
            area.append(None)
        # Authors
        try: author_count.append(len(data["abstracts-retrieval-response"]["authors"]['author']))
        except: author_count.append(None)

    except:
        abstract = "NA"
        try: affiliation.append(data["abstracts-retrieval-response"]["affiliation"]["affilname"])
        except:
            try: affiliation.append(data["abstracts-retrieval-response"]["affiliation"])
            except: affiliation.append(None)
        # Study Area
        try:
            result = data["abstracts-retrieval-response"]["subject-areas"]["subject-area"]
            subjects = [subject["$"] for subject in result]
            area.append(" & ".join(subjects))
        except:
            area.append(None)
        # Authors
        try: author_count.append(len(data["abstracts-retrieval-response"]["authors"]['author']))
        except: author_count.append(None)
        
    # Return the abstract
    return abstract

def location_finder(text: str) -> dict:
    # Load the pre-trained model
    nlp = spacy.load("en_core_web_sm")

    # Sample text
    sample_text = text

    # Process the text
    doc = nlp(sample_text)

    # Find location words and their locations
    locations = [entity.text for entity in doc.ents if entity.label_ == "GPE" or entity.label_ == "LOC"]

    # Sorting locations by frequency
    my_dict = dict(Counter(locations))
    sorted_dict = dict(sorted(my_dict.items(), key=lambda x: x[1], reverse=True))
    first_five_elements = dict(list(sorted_dict.items())[:5])

    return first_five_elements

def contains_country(value):
        for country in countries:
            if country in value:
                return True
        return False

# Function to check if a row should be deleted
def should_delete_row(row):
        for column in columns_to_check:
            value = str(row[column])
            if contains_country(value) and "USA" not in value and "U.S." not in value and "United States" not in value:
                return False
        return True

if __name__ == "__main__":
    # Perform the search and retrieve article info
    my_set = article_info(scopus_search(my_input))

    # Create an empty list to store the output dictionary keys
    list_of_lists = []

    # Loop over the IDs and find locations
    print(f'\nGetting locations from {len(my_set[3])} abstracts...')
    with ThreadPoolExecutor() as executor:
        for n, scopus_id in tqdm(enumerate(my_set[3])):
            output_dict = location_finder(scopus_id_abstract_retriever(scopus_id))
            list_of_lists.append(list(output_dict.keys()))
            
    print(f"\nMaking Dataframe...")
            
    # Extract first and second elements
    first_elements = [inner_list[0] if len(inner_list) > 0 else None for inner_list in list_of_lists]
    second_elements = [inner_list[1] if len(inner_list) > 1 else None for inner_list in list_of_lists]
    third_elements = [inner_list[2] if len(inner_list) > 2 else None for inner_list in list_of_lists]
    fourth_elements = [inner_list[3] if len(inner_list) > 3 else None for inner_list in list_of_lists]

    # Make DataFrame
    df = pd.DataFrame({
        "Paper Title": my_set[0],
        "Scopus ID" : my_set[3],
        "DOI": my_set[1],
        "URL": my_set[5],
        "Lead Author": my_set[6],
        "Affiliation": affiliation,
        "Author count": author_count,
        "Area of Study": area,
        "Publication": my_set[7],
        "Cover Date": my_set[8],
        "Number of citations": my_set[9],
        "first_location" : first_elements,
        "second_location" : second_elements,
        "third_location" : third_elements,
        "fourth_location": fourth_elements})

    # Saving file

    affiliation_series = df['Affiliation']

    modified_series = affiliation_series.apply(lambda x: x[0]['affilname'] if isinstance(x, list) and len(x) > 0 else x)

    df['Affiliation'] = modified_series

    df.to_csv("output_files/output.csv")

    # print("\nNow excluding useless papers...")

    # from country_list import countries_for_language

    # # countries_for_language returns a list of tuples now, might be changed to an OrderedDict
    # countries = dict(countries_for_language('en'))
    # del countries["US"]

    # # List of countries
    # countries = list(countries.values())
    # countries.append("Africa")

    # # Columns to check
    # columns_to_check = df.columns[-4:]

    # # Check if the last four columns are empty
    # last_four_columns_empty = df.iloc[:, -4:].isnull().all(axis=1)
    # # Delete rows where the last four columns are empty
    # df = df[~last_four_columns_empty]

    # # Delete rows that meet the criteria
    # df = df[df.apply(should_delete_row, axis=1) == True]
    # df.to_csv('output_files/excluded.csv')

    print("DONE!")