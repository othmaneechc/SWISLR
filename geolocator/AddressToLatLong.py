import csv

###Setting Up Geolocater
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="MyApp")
#location = geolocator.geocode("North Carolina")

###Read the Data
path = "10_New_Sites"
dictList = []
print("\nDo not include redundant location information, it will lower the accuracy of Nominatim\n")
with open(path + ".csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames

    ###Lowercasing all the fields and finding which fields are present
    addressFields = ["location", "addresss", "city", "county", "state", "country"]
    detectedFields = []
    for i in range(len(fieldnames)):
        fieldnames[i] = fieldnames[i].lower()
    for field in addressFields:
        if (field in fieldnames):
            detectedFields.append(field)
            if (len(detectedFields) > 3):
                break
    numDetected = len(detectedFields)
    print("Fieldnames", fieldnames)
    
    if numDetected == 0:
        print("We did not find any address fields, please make sure your data is labeled appropriately")
        exit()
    print("We found these address fields", detectedFields)
    numDetected = len(detectedFields)
    
    ###Update all the data with the new fields
    fieldnames += ['latitude', 'longitude']
    for row in reader:  
        searchQuery = []
        for field in detectedFields:
            if row[field] != "":
                searchQuery.append(row[field])
        print("Search Terms", searchQuery)
        print("\nSearching Nominatim for", " ".join(searchQuery))
        location = geolocator.geocode(" ".join(searchQuery))

        ###if no results, try first location only
        if location == None:
            print("Location not found")
            print("Instead searching for", searchQuery[0])
            location = geolocator.geocode(searchQuery[0])

        ###Searching for second location
        if (location == None)  and (numDetected > 1):
            print("Location not found")
            print("Instead searching for", searchQuery[1])
            location = geolocator.geocode(searchQuery[1])

        if location == None:
            print("Location not found\nPlease double check location data")
            continue

        row['latitude'] = location.latitude
        row['longitude'] = location.longitude
        dictList.append(row)  
#print(dictList)

###Write the Data to a new spreadsheet
with open(path + "_LatLong.csv", 'w', newline='') as csvfile:
    headers = fieldnames
    writer = csv.DictWriter(csvfile, fieldnames= headers)
    writer.writeheader()
    writer.writerows(dictList)