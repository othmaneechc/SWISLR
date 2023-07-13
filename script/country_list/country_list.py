import csv

import requests
from bs4 import BeautifulSoup

# Send a GET request to the URL
response = requests.get("https://www.iban.com/country-codes")

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the country data
table = soup.find("table", {"id": "myTable"})

# Create a list to store the country data
country_data = []

# Iterate over each row in the table
for row in table.find_all("tr")[1:]:
    # Get the columns of each row
    columns = row.find_all("td")

    # Extract the country name and code
    country_name = columns[0].text.strip()
    country_code = columns[1].text.strip()

    # Check if it is not the United States
    if country_name != "United States":
        # Append the country data to the list
        country_data.append([country_name, country_code])

# Define the CSV file path
csv_file = "country_list.csv"

# Write the country data to the CSV file
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Country", "Code"])  # Write header row
    writer.writerows(country_data)

print(f"Country list has been saved to {csv_file}.")
