import csv
import os
from extractReviews import extractReviews
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re
import uuid
from geoAPI import reverseLocations
from gptContent import gptContent
import string
from collections import Counter
from bs4 import BeautifulSoup

def remove_punctuation(input_string):
    punctuation = ['.']
    for punc in punctuation:
        # Use translate to remove punctuation
        input_string = input_string.replace(punc,"")

    return input_string

chrome_options = webdriver.ChromeOptions()
def removePunc(input_string):
    translator = str.maketrans('', '', string.punctuation)
    result_string = input_string.translate(translator)
    return result_string

def convertWords(string):
    exclude = {'the', 'was', 'is', 'are', 'and', 'you', 'our', 'they', 'us', 'in', 'on', 'at', 'we', 'a', 'an', 'but',
               'be', 'of', 'when', 'were', 'with', 'i', 'to', 'so', 'not', 'did', 'had', 'off', 'no', 'this', 'for',
               'me', 'what', 'it','breakfast','very','if','have','good','nice','that','there','its','...','just','one','my','lot','also','as','from','would'}

    word_list = [word.lower() for word in removePunc(string).split() if word.lower() not in exclude]
    # Count occurrences of each word
    word_counts = Counter(word_list)
    # Find the top 5 most common words
    most_common_words = word_counts.most_common(10)
    return most_common_words

results = []
subfile = '~/main/catesub.csv'
catefile = '~/main/category.csv'
catedf = pd.read_csv(catefile)
subdf = pd.read_csv(subfile)

driver = webdriver.Chrome(options=chrome_options)

input_csv_file = "~/path/input.csv"
output_csv_file = "~/path/output.csv"

output_directory = os.path.dirname(output_csv_file)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(output_csv_file, 'a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['uuid', 'embled_url', 'map_url', 'latitude', 'longitude', 'price_lv', 'eng_name', 'phone_code',
                  'phone',
                  'addresslv1', 'addresslv2', 'addresslv3', 'addresslv4', 'addresslv5', 'category', 'subcate1',
                  'subcate2', 'subcate3']
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
    time.sleep(5)
    try:
        time.sleep(5)
        try:
            brand_name = driver.find_element(By.CSS_SELECTOR, 'h1[class="DUwDvf lfPIob"]').text
        except:
            brand_name = None

        try:
            price_levels = driver.find_element(By.CSS_SELECTOR, 'span[aria-label="Price: Moderate"]').text
        except:
            price_levels = None

        try:
            address = driver.find_element(By.CSS_SELECTOR, 'button[class="CsEnBe"][data-tooltip="Copy address"]').text
            try:
                from googletrans import Translator

                translator = Translator()
                address = translator.translate(str(address), src='auto', dest='en').text
            except:
                pass
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
        match = re.search(r'@([-+]?\d+\.\d+),([-+]?\d+\.\d+)', row)

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
        driver.find_elements(By.CSS_SELECTOR, 'button[aria-label="Close"]')[0].click()

        time.sleep(2)
        i = 0
        while i < 2:
            reviews = " ".join(extractReviews(driver).mostCommon(numReviews=10))
            if reviews != '':
                break
            else:
                time.sleep(1)
                pass

        country, county, city, district = reverseLocations().reverse(latitude=latitude, longitude=longitude)

        ###Categories the brand by chatGPT API 3.5:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        try:
            div_element = soup.find('div', class_='m6QErb WNBkOb', role='main')
            categoryGg = div_element.get_text(strip=True)
        except:
            categoryGg = None
        ###Categories the brand by chatGPT API 3.5:
        reviews = row[1]
        driver.get(row)
        categories = catedf['category'].tolist()
        i = 0
        wordsKey = convertWords(str(reviews))

        while i < 2:
            if categoryGg != '':
                prompt = f'Based on the recommended category from Google: {categoryGg}  then choose the most appropriate category from {categories}. Returns result in a format string: "category" '
            else:
                prompt = f'Based on the URL of the brand: {row[0]} and those keywords {wordsKey} then choose the most appropriate category from {categories}. Returns result in a format string: "category" '

            result = gptContent().command(prompt)
            try:
                category = re.search(r'"([^"]*)"', result).group(1)
                category = remove_punctuation(category)
            except:
                category = result
                pass

            if any(cate == category for cate in categories):
                break
            else:
                category = ''
                i += 1

        i = 0
        while i < 2:

            subcate_List = subdf.loc[subdf['category'] == category, 'sub_category'].unique().tolist()
            prompt = f'Read the reviews:  {reviews[0:2000]}. Choose no more than 3 and at least 2 and most exactly, appropriate subcategories from the {subcate_List}. ONLY TAKE SUBCATEGORIES FROM THE LIST. Returns result in a format list "subcate1","subcate2","subcate3" '
            resultSub = gptContent().command(prompt)
            sub_GPT = re.findall(r'\d+\.\s+(\w+)', resultSub)

            if len(sub_GPT) == 0:
                sub_GPT = re.findall(r'"(.*?)"', resultSub)

            sub_category = [x for x in sub_GPT if x in subcate_List]
            if len(sub_category) > 0:
                try:
                    cate1 = sub_category[0]
                except:
                    cate1 = ''
                try:
                    cate2 = sub_category[1]
                except:
                    cate2 = ''
                try:
                    cate3 = sub_category[2]
                except:
                    cate3 = ''

                break
            else:
                i += 1

        result_entry = {
            'uuid': uuid,
            'embled_url': html,
            'map_url': row['map_url'],
            'latitude': latitude,
            'longitude': longitude,
            'price_lv': price_levels,
            'eng_name': brand_name,
            'phone_code': first_two_digits,
            'phone': remaining_digits,
            'addresslv1': country,
            'addresslv2': county,
            'addresslv3': city,
            'addresslv4': district,
            'addresslv5': address,
            'category': category,
            'subcate1':cate1,
            'subcate2':cate2,
            'subcate3':cate3
        }
        results.append(result_entry)

    except:
        results = []
        result_entry = {
            'uuid': uuid,
            'embled_url': '',
            'map_url': row['map_url'],
            'latitude': '',
            'longitude': '',
            'price_lv': '',
            'eng_name': '',
            'phone_code': '',
            'phone': '',
            'addresslv1': '',
            'addresslv2': '',
            'addresslv3': '',
            'addresslv4': '',
            'addresslv5': '',
            'category': '',
            'subcate1':'',
            'subcate2':'',
            'subcate3':''
}

        # Append the new result to the output CSV file
    with open(output_csv_file, 'a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['uuid', 'embled_url', 'map_url', 'latitude', 'longitude', 'price_lv', 'eng_name', 'phone_code', 'phone',
                       'addresslv1', 'addresslv2', 'addresslv3', 'addresslv4', 'addresslv5','category','subcate1','subcate2','subcate3']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writerow(result_entry)
