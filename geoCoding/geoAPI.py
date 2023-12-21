import pandas as pd
import requests
import os
import csv
import random

# Read the CSV file into a DataFrame
df = pd.read_csv('~/path/input.csv')
fileout = '~/path/output.csv'

output_directory = os.path.dirname(fileout)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(fileout, 'a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['uuid', 'addresslv1', 'addresslv2', 'addresslv3', 'addresslv4']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header only if the file is empty
    if csv_file.tell() == 0:
        csv_writer.writeheader()

existing_urls = set()
if os.path.exists(fileout):
    with open(fileout, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            existing_urls.add(row['uuid'])

dfOut = pd.read_csv(fileout)

apiList = []
file_path = '~/geoCoding/api.txt'
with open(file_path, 'r') as file:
    file_contents = file.readlines()
    apiList = file_contents
    apiList = [x.replace("\n","") for x in apiList]

column_a_data = []
print(df.columns)

for num in range(0,len(df)):
    row = df.iloc[num]
    column_a_data.append([{'uuid': row['uuid'],
                           'Latitude': str(row['Latitude']),
                           'Longitude': str(row['Longitude'])
    }])

column_a_data = [row for row in column_a_data if row[0]['name'] not in existing_urls if row[0]['name'] != '' and row[0]['uuid'] != 'uuid']
# Iterate over rows
print(len(column_a_data))
for row in column_a_data:
    num = column_a_data.index(row)
    row = row[0]
    api = random.choice(apiList)

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
            'uuid': row['uuid'],
            'addresslv1': country,
            'addresslv2': county,
            'addresslv3': city,
            'addresslv4': district
        }

        # Print the extracted information
        print(f"Processed row {num + 1}")

    else:
        result_entry = {
            'uuid': row['uuid'],
            'addresslv1': '',
            'addresslv2': '',
            'addresslv3': '',
            'addresslv4': ''
        }
        print(f"Error: {response.status_code} for row {num + 1}")

    results = []
    results.append(result_entry)
    with open(fileout, 'a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['uuid', 'addresslv1', 'addresslv2', 'addresslv3', 'addresslv4']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writerow(result_entry)
