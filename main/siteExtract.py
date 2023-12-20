from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

API_KEY = 'AIzaSyDh2wcKMt4HYjr-4QNEMvkBpdGwvyag8as'
from unidecode import unidecode

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

class extractData:
    def __init__(self,url,location,keyword):
        self.url = url
        self.location = location
        self.keyword = keyword
    def extract_fb_data(self):
        fb_url = self.url.replace("https://m.", "https://")
        driver.get(fb_url)
        page_source = driver.page_source
        time.sleep(2)
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            name_element = driver.find_element(By.TAG_NAME, 'h1')

            # Get the text content of the element
            fan_page_name = name_element.text
            location_element = soup.select_one(f'span:contains("{self.location}")')

            # Extract the location text
            fan_page_location = location_element.get_text().replace("\n", "") if location_element else None
            fan_page_location = ','.join(fan_page_location.split(',')[:2]).strip()
            return unidecode(fan_page_name), unidecode(fan_page_location)
        except:
            return None, None
    def extract_yelp_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')

            h1_element = soup.find('h1')
            h1_text = h1_element.get_text() if h1_element else "N/A"

            address_element = soup.find_all('p', class_='css-qyp8bo', attrs={'data-font-weight': 'semibold'})
            try:
                if len(address_element) > 0:
                    address_element = [x for x in address_element if "Verified" not in str(x)][0]
                    address = address_element.get_text()

                    return h1_text, address
                else:
                    return self.url.replace("https://yelp.com/biz/", "").replace("-", " "), None
            except:
                return self.url.replace("https://yelp.com/biz/", "").replace("-", " "), None

        else:
            return yelp_url.replace("https://yelp.com/biz/", "").replace("-", " "), None
    def extract_booking_data(self):
        driver.get(self.url)
        try:
            name_element = driver.find_element(By.CSS_SELECTOR, 'h2[class="d2fee87262 pp-header__title"]')
            # Get the text content of the element
            fan_page_name = name_element.text
            try:
                location_element = driver.find_element(By.CSS_SELECTOR,
                                                       'span[class*="hp_address_subtitle"]')
                fan_page_location = location_element.text
                parts = fan_page_location.split(',')

                return fan_page_name, ','.join(parts[:2]).strip()

            except:
                return fan_page_name, None
        except:
            return None, None
    def extract_trip_data(self):
        driver.get(self.url)
        time.sleep(2)
        fan_page_location = None
        textAttraction = ['Shopping in', 'things to do in']
        mainTag = [{'main': 'button',
                    'secondary': 'class',
                    'attribute': 'UikNM _G B- _S _T c G_ y wSSLS wnNQG raEkE'},
                   {'main': 'span',
                    'secondary': 'class',
                    'attribute': 'oAPmj _S '},
                   {'main': 'span',
                    'secondary': 'class',
                    'attribute': 'fHvkI PTrfg'},
                   {'main': 'span',
                    'secondary': 'class',
                    'attribute': 'street-address'},
                   {'main': 'span',
                    'secondary': 'class',
                    'attribute': 'fOjRx _S'},
                   {'main': 'a',
                    'secondary': 'href',
                    'attribute': '#MAPVIEW'}

                   ]
        nameTag = [{'main': 'div',
                    'secondary': 'id',
                    'attribute': 'heading'},
                   {'main': 'h1',
                    'secondary': 'id',
                    'attribute': 'heading'},
                   {'main': 'h1',
                    'secondary': 'data-test-target',
                    'attribute': 'top-info-header'},
                   {'main': 'h1',
                    'secondary': 'class',
                    'attribute': 'biGQs _P fiohW eIegw'},
                   {'main': 'h1',
                    'secondary': 'class',
                    'attribute': 'QdLfr b d Pn'},
                   {'main': 'h1',
                    'secondary': 'class',
                    'attribute': 'biGQs _P rRtyp'},
                   {'main': 'h1',
                    'secondary': 'class',
                    'attribute': 'HjBfq'},
                   {'main': 'h1',
                    'secondary': 'class',
                    'attribute': 'mainH1', }
                   ]

        try:
            for tag in nameTag:
                try:
                    h1_element = driver.find_element(By.CSS_SELECTOR,
                                                     f'{tag["main"]}[{tag["secondary"]}="{tag["attribute"]}"]')
                    fan_page_name = ','.join(h1_element.text.split(',')[:2]).strip()
                except:
                    soup = BeautifulSoup(driver.page_source, 'html.parser')

                    # Find the <h1> element by its attributes
                    h1_element = soup.find('h1')

                    # Extract the text from the <h1> element
                    fan_page_name = h1_element.text
        except:
            fan_page_name = None

        if 'Attraction_Review' in self.url:
            if fan_page_name != None:
                try:
                    location_element = driver.find_element(By.CSS_SELECTOR,
                                                           'button[class="UikNM _G B- _S _T c G_ y wSSLS wnNQG raEkE"][type="button"]')
                    word_before_in = ','.join(location_element.text.split(',')[:2]).strip()
                except:
                    for valueText in textAttraction:
                        textFind = [value.text for value in
                                    driver.find_elements(By.XPATH, f"//*[contains(text(), '{valueText}')]")]
                        textFind = [value for value in textFind if len(value) > 10]
                        if len(textFind) > 0:
                            parts = textFind[0].split(' in ')
                            if len(parts) > 1:
                                word_before_in = parts[1]
                            else:
                                word_before_in = None
                        else:
                            word_before_in = None
                return fan_page_name, word_before_in, None
            else:
                return fan_page_name, None, None

        else:
            for tag in mainTag:
                try:
                    location_element = driver.find_element(By.CSS_SELECTOR,
                                                           f'{tag["main"]}[{tag["secondary"]}="{tag["attribute"]}"]')
                    fan_page_location = ','.join(location_element.text.split(',')[:2]).strip()
                except:
                    pass

            if fan_page_location == None:
                try:
                    location_element = driver.find_element(By.CSS_SELECTOR,
                                                           'a[class="YnKZo Ci Wc _S C FPPgD"][href*="https://maps"]')
                    fan_page_location = ','.join(location_element.text.split(',')[:2]).strip()
                except:
                    fan_page_location = None

        return fan_page_name, fan_page_location
    def extractBusinessSite(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')

            h1_element = soup.find('h1')
            h1_text = h1_element.get_text() if h1_element else "N/A"

            address_element = [element.text for element in soup.findAll('address', class_='qhkvMe')]
            parts = address_element[0].split(",")
            return h1_text, ', '.join(parts[:1]).strip()
        else:
            return None, None
    def extract_agoda_data(self):
        driver.get(self.url)
        try:
            name_element = driver.find_element(By.CSS_SELECTOR, 'p[data-selenium="hotel-header-name"]')
            # Get the text content of the element
            fan_page_name = name_element.text
            try:
                location_element = driver.find_element(By.CSS_SELECTOR,
                                                       'span[data-selenium="hotel-address-map"]')
                fan_page_location = location_element.text
                parts = fan_page_location.split(',')

                return fan_page_name, ','.join(parts[:2]).strip()

            except:
                return fan_page_name, None
        except:
            return None, None
    def extract_hotels_data(self):
        driver.get(self.url)
        try:
            name_element = driver.find_element(By.CSS_SELECTOR, 'h2[class="margin-0"]')
            # Get the text content of the element
            fan_page_name = name_element.text
            try:
                location_element = driver.find_element(By.CSS_SELECTOR,
                                                       'span[itemprop="streetAddress"]')
                fan_page_location = location_element.text
                parts = fan_page_location.split(',')

                return [part.strip() for part in fan_page_name.split('|')][0].strip(), ','.join(parts[:2]).strip()

            except:
                return fan_page_name, None
        except:
            return None, None
    def extract_hotels_com_data(self):
        driver.get(self.url)
        try:
            fan_page_name = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1[class="uitk-heading uitk-heading-3"]')))
            # Get the text content of the element
            fan_page_name = fan_page_name.text
            try:
                location_element = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-stid="content-hotel-address"]')))
                fan_page_location = location_element.text
                parts = fan_page_location.split(',')

                return fan_page_name, ','.join(parts[:2]).strip(),self.keyword

            except:
                return fan_page_name,self.keyword
        except:
            # Split the URL by '/'

            parts = self.url.split('/')
            value = parts[len(parts) - 2]
            fan_page_name = value.replace('-', ' ')
            fan_page_name = fan_page_name.replace('united states of america','')
            fan_page_name = fan_page_name.replace('united kingdom','')

            return fan_page_name, self.keyword
    def extract_expedia_com_data(self):
        driver.get(self.url)
        try:
            name_element = driver.find_element(By.CSS_SELECTOR, 'h1[class="uitk-heading uitk-heading-3"]')
            # Get the text content of the element
            fan_page_name = name_element.text
            try:
                location_element = driver.find_element(By.CSS_SELECTOR,
                                                       'div[itemprop="address"]')
                fan_page_location = location_element.text
                parts = fan_page_location.split(',')

                return fan_page_name, ','.join(parts[:2]).strip()

            except:
                return fan_page_name, None
        except:
            return None, None

def detection(URL,LOCATIONs,Keyword):
    detectValue = extractData(URL,LOCATIONs,Keyword)
    if 'facebook.com' in URL:
        h1_text, address = detectValue.extract_fb_data()
        return h1_text, address
    elif 'yelp.com' in URL:
        h1_text, address = detectValue.extract_yelp_data()
        return h1_text, address
    elif 'booking.com' in URL:
        h1_text, address = detectValue.extract_booking_data()
        return h1_text, address
    elif 'tripadvisor' in URL:
        h1_text, address = detectValue.extract_trip_data()
        return h1_text, address
    elif 'business.site' in URL:
        h1_text, address = detectValue.extractBusinessSite()
        return h1_text, address
    elif 'agoda.com' in URL:
        h1_text, address = detectValue.extract_agoda_data()
        return h1_text, address
    elif '-hotel.com' in URL:
        h1_text, address = detectValue.extract_hotels_data()
        return h1_text, address
    elif 'hotels.com' in URL:
        h1_text, keyword = detectValue.extract_hotels_com_data()
        return h1_text, keyword
    elif 'expedia.com' in URL:
        h1_text, address = detectValue.extract_expedia_com_data()
        return h1_text, address
    else:
        pass
