from selenium import webdriver
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup

class convertHour:
    hotelSigns = 'Check-in'
    weekDay = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    open24hours = '24 hours'
    def __init__(self,url,uuid):
        self.results = []
        self.uuid = uuid
        chrome_options = webdriver.ChromeOptions()
        # Initialize Chrome WebDriver with the specified options
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url)

        time.sleep(2)

        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        time.sleep(0.5)
        if convertHour.hotelSigns in self.soup.findAll('span', {'style': 'font-weight: 400;'})[0].text:
            self.convertHotels()
        elif convertHour.open24hours in self.soup.findAll('tr', {'class': 'y0skZc'})[0].text:
            self.convert24hours()
        else:
            self.convertRes()

    def convertHotels(self):
        span_elements = self.soup.findAll('span', {'style': 'font-weight: 400;'})
        pattern = r'(\d{1,2}:\d{2})'

        # Use re.search to find the match in the text
        try:
            openingHour = re.search(pattern, span_elements[0].text).group(1)
            time_object = datetime.strptime(openingHour, '%H:%M')
            openingHour = time_object.strftime('%I:%M')
            openingType = time_object.strftime('%p')
        except:
            openingHour = ''
            openingType = ''

        try:
            closingHour = re.search(pattern, span_elements[1].text).group(1)
            time_object = datetime.strptime(closingHour, '%H:%M')
            closingHour = time_object.strftime('%I:%M')
            closingType = time_object.strftime('%p')
        except:
            closingHour = ''
            closingType = ''

        for day in convertHour.weekDay:
            data = [self.uuid,day,openingHour,openingType,closingHour,closingType]
            self.results.append(data)

        return self.results
    def convertRes(self):
        span_elements = self.soup.findAll('tr', {'class': 'y0skZc'})

        i = 0
        while i < len(span_elements):
            if len(span_elements[i].findAll('li', class_= 'G8aQO')) == 1:
                matches = re.findall(r'(\b\d{1,2}(?::\d{2})?\b)', span_elements[i].findAll('li', class_= 'G8aQO')[0].text)
                hourTypes = re.findall(r'\b(?:AM|PM)\b', span_elements[i].findAll('li', class_= 'G8aQO')[0].text)

                if len(matches) != 0:
                    numbers = [match for match in matches]
                    # Use re.search to find the match in the text
                    try:
                        time_object = datetime.strptime(str(numbers[0]), '%H')
                    except:
                        time_object = datetime.strptime(str(numbers[0]), '%H:%M')

                    openingHour = time_object.strftime('%I:%M')
                    if len(hourTypes) == 0:
                        openingType = time_object.strftime('%p')
                    elif len(hourTypes) == 1:
                        openingType = hourTypes[0]
                    else:
                        openingType = time_object.strftime('%p')

                    try:
                        time_object = datetime.strptime(str(numbers[1]), '%H')
                    except:
                        time_object = datetime.strptime(str(numbers[1]), '%H:%M')

                    closingHour = time_object.strftime('%I:%M')
                    if len(hourTypes) == 0:
                        closingType = time_object.strftime('%p')
                    elif len(hourTypes) == 1:
                        closingType = hourTypes[0]
                    elif len(hourTypes) == 2:
                        closingType = hourTypes[1]
                    else:
                        closingType = time_object.strftime('%p')

                    day = [day for day in convertHour.weekDay if day in span_elements[i].find('td', class_= 'ylH6lf').text][0]
                    result = [self.uuid,day,openingHour,openingType,closingHour,closingType]
                else:
                    result = []

                self.results.append(result)

            elif len(span_elements[i].findAll('li', class_= 'G8aQO')) > 1:
                for tag in span_elements[i].findAll('li', class_= 'G8aQO'):
                    matches = re.findall(r'(\b\d{1,2}(?::\d{2})?\b)', tag.contents[0])
                    hourTypes = re.findall(r'\b(?:AM|PM)\b', tag.contents[0])

                    numbers = [match for match in matches]
                    try:
                        time_object = datetime.strptime(str(numbers[0]), '%H')
                    except:
                        time_object = datetime.strptime(str(numbers[0]), '%H:%M')

                    openingHour = time_object.strftime('%I:%M')
                    if len(hourTypes) == 0:
                        openingType = time_object.strftime('%p')
                    elif len(hourTypes) == 1:
                        openingType = hourTypes[0]
                    else:
                        openingType = time_object.strftime('%p')

                    try:
                        time_object = datetime.strptime(str(numbers[1]), '%H')
                    except:
                        time_object = datetime.strptime(str(numbers[1]), '%H:%M')

                    closingHour = time_object.strftime('%I:%M')
                    if len(hourTypes) == 0:
                        closingType = time_object.strftime('%p')
                    elif len(hourTypes) == 1:
                        closingType = hourTypes[0]
                    elif len(hourTypes) == 2:
                        closingType = hourTypes[1]
                    else:
                        closingType = time_object.strftime('%p')

                    day = [day for day in convertHour.weekDay if day in span_elements[i].find('td', class_= 'ylH6lf').text][0]
                    result = [self.uuid,day,openingHour,openingType,closingHour,closingType]
                    self.results.append(result)

            i += 1
        return self.results
    def convert24hours(self):
        span_elements = self.soup.findAll('tr', {'class': 'y0skZc'})
        i = 0
        while i < len(span_elements):
            openingHour = '00:01'
            openingType = 'AM'
            closingHour = '23:59'
            closingType = 'PM'

            day = [day for day in convertHour.weekDay if day in span_elements[i].find('td', class_='ylH6lf').text][0]
            result = [self.uuid, day, openingHour, openingType, closingHour, closingType]
            self.results.append(result)

            i += 1

