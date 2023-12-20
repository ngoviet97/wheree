import pandas as pd
import requests
import os
import csv
import random

# Read the CSV file into a DataFrame
df = pd.read_csv('~/path/samplefile/inputsample.csv')
fileout = '~/path/output.csv'

output_directory = os.path.dirname(fileout)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(fileout, 'a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['yelp_link', 'country', 'county', 'city', 'district']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header only if the file is empty
    if csv_file.tell() == 0:
        csv_writer.writeheader()

existing_urls = set()
if os.path.exists(fileout):
    with open(fileout, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            existing_urls.add(row['yelp_link'])

dfOut = pd.read_csv(fileout)

apilist = ['bdc_a3aa745fc7cf407d9fa4c278ef94dbcf']

column_a_data = []
print(df.columns)

for num in range(0,len(df)):
    row = df.iloc[num]
    column_a_data.append([{'name': row['yelp_link'],
                           'Latitude': str(row['latitude']),
                           'Longitude': str(row['longitude'])
    }])

column_a_data = [row for row in column_a_data if row[0]['name'] not in existing_urls if row[0]['name'] != '' and row[0]['name'] != 'yelp_link']
# Iterate over rows
print(len(column_a_data))
for row in column_a_data:
    num = column_a_data.index(row)
    row = row[0]
    api = random.choice(apilist)

    # Make the request
    url = f"https://api-bdc.net/data/reverse-geocode?latitude={row['Latitude']}&longitude={row['Longitude']}&localityLanguage=en&key={str(api)}"
    #url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={row['Latitude']}&longitude={row['Longitude']}&localityLanguage=en"
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the required information
        try:
            country = data['countryName']
        except:
            country = ''
        try:
            county = data['principalSubdivision']
        except:
            county = ''
        try:
            city = data['city']
        except:
            city = ''
        try:
            district = data['locality']
        except:
            district = ''

        result_entry = {
            'yelp_link': row['name'],
            'country': country,
            'county': county,
            'city': city,
            'district': district
        }

        # Print the extracted information
        print(f"Processed row {num + 1}")

    else:
        result_entry = {
            'yelp_link': row['name'],
            'country': '',
            'county': '',
            'city': '',
            'district': ''
        }
        print(f"Error: {response.status_code} for row {num + 1}")

    results = []
    results.append(result_entry)
    with open(fileout, 'a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['yelp_link', 'country', 'county','city','district']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writerow(result_entry)
