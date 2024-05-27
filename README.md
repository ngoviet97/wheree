# wheree - Create, Manage and Extract Data

wheSCA is a approriate library which provides developers ability to scrape raw data from multiple sources and make it structured in DBMS. 

## Before Start:

Those tools are required to run, you must install it by pip3 on terminal. You must update for the latest version!!
For most of the tool, you should read the documentations first at the link.

- **[selenium](https://www.selenium.dev/)**: Selenium is an open source umbrella project for a range of tools and libraries aimed at supporting browser automation. It provides a playback tool for authoring functional tests across most modern web browsers, without the need to learn a test scripting language
````
pip install opencv-python
````
- [pytesseract](https://pypi.org/project/pytesseract/): Python-tesseract is an optical character recognition (OCR) tool for python. That is, it will recognize and “read” the text embedded in images. Follow instruction below to install:

1. Install brew: 
````
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
````
2. Install Tesseract on Mac:
````
brew install tesseract
````
3. Install library:
````
pip install pytesseract
pip install Pillow
````
- [UUID](https://docs.python.org/3/library/uuid.html): This module provides immutable UUID objects (the UUID class) and the functions uuid1(), uuid3(), uuid4(), uuid5() for generating version 1, 3, 4, and 5 UUIDs as specified in RFC 4122.
````
pip install uuid
````


- [csv](https://docs.python.org/3/library/csv.html): The csv module implements classes to read and write tabular data in CSV format
````
pip install python-csv
````

- [pandas](https://pandas.pydata.org/): pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language
````
pip install pandas
````

- [requests](https://pypi.org/project/requests/): Requests is an HTTP client library for the Python programming language. Requests is one of the most downloaded Python libraries, with over 300 million monthly downloads
````
pip install requests
````

- [bs4](https://pypi.org/project/beautifulsoup4/): Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.
````
pip install bs4
````

- [googletrans](https://pypi.org/project/googletrans/): Googletrans is a free and unlimited python library that implemented Google Translate API. This uses the Google Translate Ajax API to make calls to such methods as detect and translate.
````
pip install googletrans
````

- [openai](https://openai.com/blog/openai-api): OpenAI offers text embedding models that take as input a text string and produce as output an embedding vector.
Find your APIs here: https://platform.openai.com/api-keys
Here is language models and price you should consider before running: https://openai.com/pricing. For most of the time, GPT-3.5-turbo-1106 must be best choice.
<img width="1427" alt="Screenshot 2023-12-20 at 11 05 38" src="https://github.com/ngoviet97/wheree/assets/46282671/f3691747-c77b-4616-b9b0-222421c14c13">

````
pip install openapi
````


**Besides, you must notice some of api solutions below:
**

- https://www.bigdatacloud.com/reverse-geocoding: Transform latitude/longitude coordinates into precise locations using BigDataCloud's cutting-edge Reverse Geocoding API. Discover the world's quickest 'Reverse Geocoding to City' service, now with a generous FREE tier. Dive into unparalleled accuracy and comprehensive global coverage, only at BigDataCloud.
Head to: https://www.bigdatacloud.com/account to find your API KEY.
They offer 50.000 requests for free every months on Reverse Geocoding Api Package.
<img width="1000" alt="Screenshot 2023-12-20 at 11 08 00" src="https://github.com/ngoviet97/wheree/assets/46282671/ee8a826d-21ad-4f3d-9033-f3d2681e59f4">

## Installation:
Overall, the goals of the library is to scrapt and extract data from Google Maps URL, then formating the extracted paramaters into raw datasets. After that, proceeding with the raw datasets and returning results as formatted databases. It's essential to evaluate the results before executing any processes. 

<img width="577" alt="Screenshot 2024-05-27 at 08 16 07" src="https://github.com/ngoviet97/wheree/assets/46282671/4826a67d-d2f8-48cd-84a5-5beff4602bdd">

The raw datasets contains:
- Main Dataset: Basic information about a brand. 
- Review Dataset: Reviews related to the brand. 
- Image Dataset: Images associated with the brand.


| Tables | uuid  |brand_name  |phone  |hour  |embled_url  |address  |price_lv  |brand_type  |map_url  | reviews | image|booking_url
| ------------- | -----:| ----:| ---------:| ----:| ----------:| -------:| --------:| ----------:| -------:| -------:| -----:| -----:
| main_dataset  |  ✅    |✅    |✅         |✅    |✅         |✅       |✅       |✅           |✅       |❌      |❌|❌
| review_dataset|  ✅    |❌  |❌ |❌  |❌ |❌ |❌ |❌ |❌ |✅ |❌ |❌  
| image_dataset |  ✅   |❌  |❌ |❌  |❌ |❌ |❌ |❌ |❌ |❌ |✅  |❌  
| link_dataset |  ✅   |❌  |❌ |❌  |❌ |❌ |❌ |❌ |❌ |❌ |❌  |✅  
| hour_dataset |  ✅   |❌  |❌ |✅  |❌ |❌ |❌ |❌ |❌ |❌ |❌  |❌  

****1. Data transaction flows:

<img width="622" alt="Screenshot 2024-05-20 at 10 02 05" src="https://github.com/ngoviet97/wheree/assets/46282671/b254159a-aa38-4baa-80ba-0db7882d3c9b">

**CONDITION 1:** **The CONDITION ONE** consists of 2 attributes which defined as _integers_ and must be _larger than 0_:
- Rating (int)
- Number of reviews (int)

If the URL is **qualified**, extract chosen data type to create a raw data file including:
- uuid: ID of the brand
- name: Brand name
- phonecode: Mobile phone
- hour: Opening hours
- embled_url: embled url for the map
- address: Address of the brand
- price_lv: Price level
- brand_type: Type of the brand
- map_url: Google Map's URL of the brand

From the map_url, extract Latitude and Longitude of the brand as format: xx.xxxxxxx,xx.xxxxxxx
- latitude: a coordinate that specifies the north–south position
- longitude: Longitude is a geographic coordinate that specifies the east–west position

****2. Reverse locations to particular levels:
- level0: zipcode or postcode of the location
- level1: The country name of the brand
- level2: The county name of the brand
- level3: The city name of the brand
- level4: The district of the brand

****3. Image extraction:
- banner: The banner of the brand.
- imgs: Total images of the brand.
- menuimgs: In case of restaurant, menu images is required.

## License:

wheSCA is licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0.
