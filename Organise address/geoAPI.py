import pandas as pd
import requests
import os
import csv
import random

# Read the CSV file into a DataFrame
df = pd.read_csv('/Users/MAC/Documents/WEBIFY/Lọc Hình ảnh/Manage/brandinfo_with_coordinates.csv')
fileout = '/Users/MAC/Documents/WEBIFY/Lọc Hình ảnh/Manage/locations1.csv'

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

apilist = ['bdc_a3aa745fc7cf407d9fa4c278ef94dbcf',
'bdc_4c1e8ca868cb4eaeb1db70c84865a41f',
'bdc_4c1313a90794411eb1030b9393ceb622',
'bdc_9601a2a7a99843c4bd607b6500609c93',
'bdc_befb67c9b02642aa9fedd6a16dfc6822',
'bdc_adada2ca65ac4c4090b95954f8d6211f',
'bdc_9d6d46b237bc429195164d06a5f4dfd7',
'bdc_280397da96f84451a121a7932e1fc27c',
'bdc_35c8024f45834d3790f86f8b37a29b30',
'bdc_07c4b3329f27494d9d4b81fdd8d3b854',
'bdc_dc7a27f777694f588632eb0e42cafa8d',
'bdc_ab2132d51f0e45aa874d0ab054507d2c',
'bdc_cda872f9bf7c412d82b53bbfb2916779',
'bdc_5832c7d53aa94fc6a0e8c3249da92a54',
'bdc_b7fe95a008a6491494cde6a341674750',
'bdc_cc5fcafd8a104bac8d12f7a009aa90ef',
'bdc_c5a2764292574d2db2f977956c7481ea',
'bdc_07427821f00d4bcebd336498f7ce5acb',
'bdc_63e14e70392945f8a4ec6882ff992ef5',
'bdc_679295a6fcf145e2b0a2ba2e4b33aafd',
'bdc_89237b27163349a8893a6b29badf598e']

column_a_data = []
print(df.columns)

for num in range(0,len(df)):
    row = df.iloc[num]
    column_a_data.append([{'name': row['yelp_link'],
                           'Latitude': str(row['Latitude']),
                           'Longitude': str(row['Longitude'])
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
