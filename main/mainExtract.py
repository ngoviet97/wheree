import csv
import os
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re
from googletrans import Translator
import uuid

translator = Translator()
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

input_csv_file = "~/path/input.csv"
output_csv_file = "~/path/output.csv"

output_directory = os.path.dirname(output_csv_file)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(output_csv_file, 'a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['uuid', 'map_url', 'latitude', 'longitude', 'name', 'price_lv', 'status', 'address', 'brand_type',
                  'phonecode', 'phone', 'embled_url']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header only if the file is empty
    if csv_file.tell() == 0:
        csv_writer.writeheader()

# Read data from column A (excluding the header)
column_a_data = []
with open(input_csv_file, 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        column_a_data.append(row[0])
existing_urls = set()
if os.path.exists(output_csv_file):
    with open(output_csv_file, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            existing_urls.add(row['map_url'])

column_a_data = [x for x in column_a_data if x[0] not in existing_urls if x[0] != '' and x[0] != 'map_url']
print(len(column_a_data))
print(len(existing_urls))
# Loop through randomly selected Yelp URLs
for row in column_a_data:  # Adjust 'k' as needed
    results = []
    driver.get(row)
    id = uuid.uuid4()
    try:
        try:
            brand_name = driver.find_element(By.CSS_SELECTOR, 'h1[class="DUwDvf lfPIob"]').text
        except:
            brand_name = None

        try:
            price_levels = driver.find_element(By.CSS_SELECTOR, 'span[aria-label="Price: Moderate"]').text
        except:
            price_levels = None

        try:
            brand_status = driver.find_element(By.CSS_SELECTOR, 'span[class="aSftqf "]').text
        except:
            brand_status = None

        try:
            address = driver.find_element(By.CSS_SELECTOR, 'button[class="CsEnBe"][data-item-id="address"]').text
            address = translator.translate(str(address), src='auto', dest='en').text
        except:
            address = None

        try:
            brand_type = driver.find_element(By.CSS_SELECTOR, "button[jsaction='pane.rating.category']").text
        except:
            try:
                brand_type = driver.find_element(By.CSS_SELECTOR, "span[class='mgr77e']").text
            except:
                brand_type = None

        try:
            brand_number = driver.find_element(By.CSS_SELECTOR,
                                               'button[class="CsEnBe"][data-tooltip="Copy phone number"]').text
            cleaned_number = ''.join(char for char in brand_number if char.isdigit())

            # Extract the first two numbers and the rest
            first_two_digits = cleaned_number[:2]
            remaining_digits = cleaned_number[2:]

        except:
            brand_number = None

        # Use a regular expression to extract coordinates
        match = re.search(r'@([-+]?\d+\.\d+),([-+]?\d+\.\d+)', row[0])

        if match:
            latitude = float(match.group(1))
            longitude = float(match.group(2))
        else:
            latitude = ''
            longitude = ''

        driver.find_elements(By.CSS_SELECTOR, 'button[class="g88MCb S9kvJb "][data-value="Share"]')[0].click()
        time.sleep(2)
        driver.find_elements(By.CSS_SELECTOR, 'button[aria-label="Embed a map"]')[0].click()
        time.sleep(1)
        html = driver.find_element(By.CSS_SELECTOR, 'input[class="yA7sBe"]').get_attribute('value')

        result_entry = {
            'uuid': id,
            'map_url': row,
            'name': brand_name,
            'price_lv': price_levels,
            'status': brand_status,
            'address': address,
            'brand_type': brand_type,
            'phonecode': first_two_digits,
            'phone': remaining_digits,
            'embled_url': html,
            'latitude': latitude,
            'longitude': longitude
        }
        results.append(result_entry)

    except:
        results = []
        result_entry = {
            'uuid': id,
            'map_url': row,
            'name': '',
            'price_lv': '',
            'status': '',
            'address': '',
            'brand_type': '',
            'phonecode': '',
            'phone': '',
            'embled_url': '',
            'latitude': '',
            'longitude': ''}

        # Append the new result to the output CSV file
    with open(output_csv_file, 'a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['uuid', 'map_url', 'latitude', 'longitude', 'name', 'price_lv', 'status', 'address', 'brand_type',
                      'phonecode', 'phone', 'embled_url']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writerow(result_entry)
