import requests
import random

class reverseLocations:
    def __init__(self):
        self.apiList = []
        file_path = '/Users/MAC/PycharmProjects/GGMaps/geoCoding/api.txt'
        with open(file_path, 'r') as file:
            file_contents = file.readlines()
            self.apiList = file_contents
            self.apiList = [x.replace("\n", "") for x in self.apiList]
    def reverse(self,latitude=None,longitude=None):
        api = random.choice(self.apiList)
        # Make the request
        url = f"https://api-bdc.net/data/reverse-geocode?latitude={latitude}&longitude={longitude}&localityLanguage=en&key={str(api)}"
        #url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={row['Latitude']}&longitude={row['Longitude']}&localityLanguage=en"
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Extract the required information
            try:
                country = data['countryCode']
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
        else:
            country = ''
            county = ''
            city = ''
            district = ''

        return country,county,city,district

