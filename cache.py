import os
import requests
import constants
import pandas as pd
import urllib.parse as ul
import json

class WebCache:
    def __init__(self):
        pass
    
    def download_data(self, url):
        OUTPUT_FILE = 'raw_data.csv'
        OUTPUT_DIR = 'data/raw'
        CWD = os.getcwd()
        if (CWD != os.path.join(os.getcwd(), OUTPUT_DIR)):
            os.chdir(os.path.join(os.getcwd(), OUTPUT_DIR))
            
        with open((OUTPUT_FILE), 'w'):
            payload = {'fields':'title,pagetext,source,cdid'}
            encodedPayload = ul.urlencode(payload)
            headers = {
                'Authorization': constants.key,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': constants.cookie
            }
            print('Downloading data...')
            response = requests.request("POST", url, headers=headers, data=encodedPayload)
            raw_data = json.loads(response.text)
            
            raw_data_df = pd.DataFrame(raw_data)
            raw_data_df.to_csv(OUTPUT_FILE, index=False, header=['title', 'pagetext', 'source', 'cdid'], sep=',')


    def cleanCSV(self, csvFile: str):
        data = pd.read_csv(csvFile)
        df = pd.DataFrame(data)
        
        # Grab pagetext column and put into list
        pagetext = data['pagetext'].tolist()
        
        # Iterate list and strip characters out
        for i in range(len(pagetext)):
            strippedText = pagetext[i].strip('[\'"1::]')
            df['pagetext'][i] = strippedText
                        
        df.to_csv(csvFile, index=False, header=['title', 'pagetext', 'source'], sep=',')
        
    
    def concat(self, input_: str):
        data = pd.read_csv(input_)
        df1 = pd.DataFrame(data)
        df2 = pd.DataFrame()
        df2['text'] = df1['title'] + ' ' + df1['pagetext'] + ' ' + df1['source']
        df2.to_csv(input_, index=False, header=['text'])