import csv

###Setting Up Geolocater
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="MyApp")
#location = geolocator.geocode("North Carolina")

###Read the Data
path = "Study_Sites_Cleaned.csv"
dictList = []
with open(path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames

    ###Finding which fields are present and making them all lowercase
    addressFields = ["country", "state", "county", "city", "neighborhood", "addresss"]
    detectedFields = []
    for i in range(len(fieldnames)):
        fieldnames[i] = fieldnames[i].lower()
        if fieldnames[i] in addressFields:
            detectedFields.append(fieldnames[i])
    print("Fieldnames", fieldnames)
    print("We found these address fields", detectedFields)
    

    ###Update all the data with the new fields
    fieldnames += ['Latitude', 'Longitude']
    for row in reader:  
        searchQuery = ''
        for field in detectedFields:
            searchQuery += row[field]
        print("Searching Nominatim for", searchQuery)
        location = geolocator.geocode(searchQuery)
        row['Latitude'] = location.latitude
        row['Longitude'] = location.longitude
        dictList.append(row)  
print(dictList)

###Write the Data to a new spreadsheet
outpath = "Study_Sites_LatLong.csv"
with open(outpath, 'w', newline='') as csvfile:
    headers = fieldnames
    writer = csv.DictWriter(csvfile, fieldnames= headers)
    writer.writeheader()
    writer.writerows(dictList)


    

