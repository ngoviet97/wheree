import csv
import os
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd

chrome_options = webdriver.ChromeOptions()
# Initialize Chrome WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)

input_csv_file = "~/ExtractImgs/input.csv"
output_csv_file = "~/ExtractImgs/output.csv"

df = pd.read_csv(input_csv_file, nrows=1)

df2 = pd.read_csv(output_csv_file, encoding='utf-8')
df2.to_csv(output_csv_file, index=False)

output_directory = os.path.dirname(output_csv_file)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(output_csv_file, 'a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['uuid', 'img', 'img_types', 'sub_types']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header only if the file is empty
    if csv_file.tell() == 0:
        csv_writer.writeheader()

column_a_data = []
for num in range(0,len(df)):
    row = df.iloc[num]
    column_a_data.append({'uuid': row['uuid'],
                           'map_url': row['map_url']})

existing_urls = set()
for num in range(0, len(df2)):
    row = df2.iloc[num]
    existing_urls.add((row['uuid'], row['img_types'], row['sub_types']))

column_a_data = [row for row in column_a_data if (row['uuid'], 'main', 'introduction') not in existing_urls]

# Loop through randomly selected Yelp URLs
for row in column_a_data:
    i = 0
    results = []
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()

    driver.switch_to.window(driver.window_handles[0])
    driver.get(row['map_url'])
    # Enter a location in the search bar
    time.sleep(3)
    checkBanner = True
    try:
        div_element = driver.find_element(By.CSS_SELECTOR, 'button[jsaction="pane.heroHeaderImage.click"][class="aoRNLd kn2E5e NMjTrf lvtCsd "]').click()
        time.sleep(2)
    except:
        checkBanner = False
    imgs = []

    i = 0
    if checkBanner == True:
        for i in range(0,10):
            driver.switch_to.window(driver.window_handles[0])
            try:
                div_element = driver.find_element(By.CSS_SELECTOR, f'a[class*="OKAoZd "][data-photo-index="{i}"]').click()
                time.sleep(2)
                div_element = driver.find_element(By.CSS_SELECTOR,'a[jsaction="log.outbound;clickmod:log.outbound;contextmenu:log.outbound_contextmenu"]').click()
            except:
                break
            k = 0
            while k < 3:
                try:
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(2)
                    canvaElement = driver.find_elements(By.CSS_SELECTOR, 'canvas[class="MyME0d m5SR9c-KeEW5b-UzWXSb"]')
                    if len(canvaElement) > 0:
                        break

                    div_element = driver.find_elements(By.CSS_SELECTOR, 'div[class="quEhsf"][jsname="UOhYpb"]')
                    if len(div_element) == 0:
                        break

                    # Find the image element within the div
                    img_element = div_element[0].find_element(By.TAG_NAME, 'img')
                    # Get the src attribute from the image
                    src_value = img_element.get_attribute('src')
                    if len(src_value) != 0:
                        imgs.append(src_value)
                        break
                    else:
                        time.sleep(3)
                        k += 1
                except:
                    time.sleep(3)
                    i += 1
            driver.close()

    if len(imgs) == 0:
        headerImg = [row['uuid'], '','main','introduction']
    else:
        headerImg = [row['uuid'], imgs[0],'main','introduction']

    imgs = [[row['uuid'], x, 'main', f'position_{num}'] for num, x in enumerate(imgs)]

    time.sleep(2)
    checkMenu = True
    try:
        driver.switch_to.window(driver.window_handles[0])
        sortButton = driver.find_element(By.XPATH,
                                         "//div[contains(text(), 'Menu')]")
        sortButton.click()
        time.sleep(2)
    except:
        checkMenu = False
        pass

    imgMenu = []

    if checkMenu == True:
        for i in range(0,10):
            driver.switch_to.window(driver.window_handles[0])
            try:
                div_element = driver.find_element(By.CSS_SELECTOR, f'a[class*="OKAoZd "][data-photo-index="{i}"]').click()
                time.sleep(2)
                div_element = driver.find_element(By.CSS_SELECTOR,'a[jsaction="log.outbound;clickmod:log.outbound;contextmenu:log.outbound_contextmenu"]').click()

            except:
                break
            k = 0
            while k < 5:
                try:
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(2)
                    canvaElement = driver.find_elements(By.CSS_SELECTOR, 'canvas[class="MyME0d m5SR9c-KeEW5b-UzWXSb"]')
                    if len(canvaElement) > 0:
                        break

                    div_element = driver.find_elements(By.CSS_SELECTOR, 'div[class="quEhsf"][jsname="UOhYpb"]')
                    if len(div_element) == 0:
                        break

                    # Find the image element within the div
                    img_element = div_element[0].find_element(By.TAG_NAME, 'img')
                    # Get the src attribute from the image
                    src_value = img_element.get_attribute('src')
                    print(f"Img {src_value}")
                    if len(src_value) != 0:
                        imgMenu.append(src_value)
                        break
                    else:
                        time.sleep(3)
                        k += 1
                except:
                    time.sleep(3)
            driver.close()

    imgsMenu = [[row['uuid'], x, 'menu', f'menu_{num}'] for num, x in enumerate(imgMenu)]

    Images = [img for img in imgs]
    for x in imgsMenu:
        Images.append(x)
    Images.append(headerImg)

    with open(output_csv_file, 'a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['uuid', 'img', 'img_types', 'sub_types']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write each result entry to the CSV file
        for result_entry in Images:
            csv_writer.writerow({
                'uuid': row['uuid'],
                'img': result_entry[0],
                'img_types': result_entry[1],
                'sub_types': result_entry[2]
            })
