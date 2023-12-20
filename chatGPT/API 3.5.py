from openai import OpenAI
import pandas as pd
import csv
import random

inputCSV = '~/path/csvfiles/inputsample.csv'
outputCSV = '~/path/output.csv'

df = pd.read_csv(inputCSV)
print(df.columns)

with open(outputCSV, 'a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['uuid', 'main', 'photos','menu']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header only if the file is empty
    if csv_file.tell() == 0:
        csv_writer.writeheader()

column_a_data = []
for num in range(0,len(df)):
    row = df.iloc[num]
    column_a_data.append([{'name': row['name'],
                           'uuid': row['uuid'],
                           'address': row['address'],
                           'brandtype': row['brand_type'],
                           'reviews': row['reviews'],
                           'openinghours': row['opening_hours'],
                           'price' : row['price_lv']
    }])

apiList = []
file_path = '~/path/apis.txt'
with open(file_path, 'r') as file:
    file_contents = file.readlines()
    apiList = file_contents
    apiList = [x.replace("\n","") for x in apiList]

def main(name,address,brandtype,reviews,openinghours,price):
  prompt = (f'Write an introduction:\n Brand Name: {name} \n Brand type: {brandtype} \n Information: {reviews[0:2000]} Address: {address} \n Opening Hours: {openinghours} \n Price Level: {price}')

  action = 'Focus on the introduction about the brand in third-person and STOP WRITING about guests or someone talk about them, avoiding negative side. REMEMBER TO ONLY write in within 130-160 words in third-person.'

  return prompt + action
def photos(name,reviews):
  prompt = (f'Write short description about the PHOTOS and the VIEWS, the Landscape AROUND the:\n Brand Name: {name}\n Information: {reviews}')

  action = 'Focus only on positive side of photos and Views, Landscape around, Dont write about anything else. REMEMBER TO ONLY write in within 130-160 words in third-person.'

  return prompt + action
def menu(name,reviews,price):
  prompt = (f'Introduce about 130 words to introdruce people about the menu and food, drink of the:\n Brand Name: {name} \n  Information: {reviews} Price Level: {price} in third-person')

  action = 'Avoiding Negative side of reviews and focus only on the menu, Food, drink. Dont write about anything else'

  return prompt + action

for row in column_a_data:
    api = random.choice(apiList)
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=api,
    )
    try:
        row = row[0]
        mainContent = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{main(str(row['name']),str(row['address']),str(row['brandtype']),str(row['reviews'])[0:1500],str(row['openinghours']),str(row['price']))}",
                }
            ],
            model="gpt-3.5-turbo",
        )
        mainContentResult = mainContent.choices[0].message.content

        photosContent = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{photos(row['name'],row['reviews'][1500:])}",
                }
            ],
            model="gpt-3.5-turbo",
        )
        photosContentResult = photosContent.choices[0].message.content

        menuContent = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{menu(row['name'],row['reviews'][0:2000],row['price'])}",
                }
            ],
            model="gpt-3.5-turbo",
        )
        menuContentResult = menuContent.choices[0].message.content

        print(row['link'])
        results = []
        result_entry = {
            'uuid': row['uuid'],
            'main': mainContentResult,
            'photos': photosContentResult,
            'menu': menuContentResult,

        }
    except:
        result_entry = {
            'uuid': row['uuid'],
            'main': '',
            'photos': '',
            'menu':''}

    results.append(result_entry)
    with open(outputCSV, 'a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['uuid', 'main','photos','menu']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writerow(result_entry)
