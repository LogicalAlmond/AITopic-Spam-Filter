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
            
            if (os.path.exists(OUTPUT_FILE)):
                raw_data_df.to_csv(OUTPUT_FILE, mode='a', index=False, header=False, sep=',')
            else:
                raw_data_df.to_csv(OUTPUT_FILE, index=False, header=['title', 'pagetext', 'source', 'cdid'], sep=',')

         
    def clean_raw_data(self, raw_csv_file):
        OUTPUT_FILE = 'interim_data.csv'
        OUTPUT_DIR = 'data/interim'
        CWD = os.getcwd()
        
        raw_data = pd.read_csv(raw_csv_file)
        raw_data_df = pd.DataFrame(raw_data)
        
        if (CWD != os.path.join(os.getcwd(), OUTPUT_DIR)):
            os.chdir(os.path.join(os.getcwd(), OUTPUT_DIR))
            print(os.getcwd())

        columns = ['pagetext']
        for col in columns:
            text = raw_data[col].tolist()
            for i in range(len(text)):
                cleaned_text = text[i].strip('[\'"1::]')
                raw_data_df[col][i] = cleaned_text

        raw_data_df.to_csv(OUTPUT_FILE, index=False, header=['title', 'pagetext', 'source', 'cdid'], sep=',')
        
    
    def concat(self, input_: str):
        data = pd.read_csv(input_)
        df1 = pd.DataFrame(data)
        df2 = pd.DataFrame()
        df2['text'] = df1['title'] + ' ' + df1['pagetext'] + ' ' + df1['source']
        df2.to_csv(input_, index=False, header=['text'])
        
        
grab = WebCache()
grab.clean_raw_data('data/raw/raw_data.csv')