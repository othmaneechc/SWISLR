import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import cycle
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Script to process keywords.')
parser.add_argument('-f', '--file', nargs='+', help='file', default='output_files/output.csv')

args = parser.parse_args()
file = args.file

df = pd.read_csv(file)
source = list(df['DOI'])
source = [doi for doi in source if pd.notna(doi)]

titles = []
citations = []
dois = []

def test_proxies(proxies):
    working_proxies = []
    session = requests.Session()

    for proxy in tqdm(proxies, desc='Testing Proxies', unit='proxy'):
        ip, port = proxy.split(':')
        http_proxy = f'http://{ip}:{port}'
        https_proxy = f'https://{ip}:{port}'
        proxies = {
            'http': http_proxy,
            'https': https_proxy
        }

        try:
            response = session.get('https://sci-hub.ru', proxies=proxies, timeout=5)
            working_proxies.append(proxy)
        except requests.exceptions.RequestException:
            pass  # Proxy connection or timeout error, ignore

    return working_proxies

def get_proxies():
    url = 'https://free-proxy-list.net/'

    response = requests.get(url)

    parser = fromstring(response.text)
    headers = [header.text_content() for header in parser.xpath('//thead/tr/th')]
    rows = parser.xpath('//tbody/tr')

    proxies = []
    for row in tqdm(rows):
        proxy = [cell.text_content() for cell in row.xpath('.//td')]
        proxies.append(proxy)

    proxies_df = pd.DataFrame(proxies, columns=headers)

    # Filter the DataFrame based on the conditions
    filtered_df = proxies_df[proxies_df['Https'] == 'yes']

    # Extract the IP address and port from the filtered DataFrame
    ip_port_list = []
    for _, row in filtered_df.iterrows():
        ip = row['IP Address']
        port = row['Port']
        ip_port = f"{ip}:{port}"
        ip_port_list.append(ip_port)

    return ip_port_list

def pdf_downloader(doi):

    doi = doi.replace(':', '/')
    base_url = "https://sci-hub.ru"
    url = f"{base_url}/{doi}"

    proxy = next(proxy_cycle)
    proxies = {
        'http': proxy,
        'https': proxy
    }

    try:
        response = requests.get(url, proxies=proxies)
        # response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

    except Exception as e:
        print(f"An exception occurred: {str(e)}")


    try:
        citation_div = soup.find('div', {'id': 'citation'})
        title = citation_div.find('i').text
        citation = citation_div.text
        titles.append(title)
        citations.append(citation)
        dois.append(doi)
    except:
        titles.append(None)
        citations.append(None)
        dois.append(doi)

    try:
        pdf_relative_url = soup.find('embed', {'type': 'application/pdf'}).get('src')
        pdf_url = urljoin(base_url, pdf_relative_url)

        pdf_response = requests.get(pdf_url, proxies=proxies)

        filename = f"data/{doi.replace('/', ':')}.pdf"

        with open(filename, "wb") as file:
            file.write(pdf_response.content)

    except Exception as e:
        return

if __name__ == "__main__":
# Get the list of proxies
    print("\nGetting list of proxies from https://free-proxy-list.net/")
    proxies = get_proxies()

    print("\nLooking for working proxies")
    working_proxies = test_proxies(proxies)
    proxy_cycle = cycle(working_proxies)

    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(pdf_downloader, doi) for doi in source]

        # Iterate over completed futures to check for any exceptions
        for future in tqdm(as_completed(futures), total=len(futures)):
            try:
                future.result()
            except Exception as e:
                print(f"An exception occurred: {str(e)}")

    import os

    folder_path = "data"  # Replace "papers" with your folder path

    # Get the list of files in the folder
    file_list = os.listdir(folder_path)

    # Count the number of files
    num_files = len(file_list)

    print(f"\nThe number of files in the folder '{folder_path}' is: {num_files} out of {len(source)} initial DOIs\n")