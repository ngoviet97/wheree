from openai import OpenAI
import pandas as pd
import csv
import random

apiList = []
file_path = '~/chatGPT/apis.txt'
with open(file_path, 'r') as file:
    file_contents = file.readlines()
    apiList = file_contents
    apiList = [x.replace("\n","") for x in apiList]

class gptContent:
    def __init__(self):
        api = random.choice(apiList)
        print(api)
        self.client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=api,
        )

    def command(self,prompt):
        mainContent = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}",
                }
            ],
            model="gpt-3.5-turbo",
        )
        return mainContent.choices[0].message.content
