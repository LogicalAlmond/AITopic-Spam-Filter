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


    def clean_raw_data(self, raw_csv_file):
        OUTPUT_FILE = 'interim_data.csv'
        OUTPUT_DIR = 'data/interim'
        CWD = os.getcwd()
        
        raw_data = pd.read_csv(raw_csv_file)
        raw_data_df = pd.DataFrame(raw_data)
        
        if (CWD != os.path.join(os.getcwd(), OUTPUT_DIR)):
            os.chdir(os.path.join(os.getcwd(), OUTPUT_DIR))

        columns = ['pagetext']
        for col in columns:
            text = raw_data[col].tolist()
            for i in range(len(text)):
                cleaned_text = text[i].strip('[\'"1::]')
                raw_data_df[col][i] = cleaned_text

        raw_data_df.to_csv(OUTPUT_FILE, index=False, header=['title', 'pagetext', 'source', 'cdid'], sep=',')
        
    
    def transform_data(self, interim_csv_file):
        OUTPUT_FILE = 'processed_data.csv'
        OUTPUT_DIR = 'data/processed'
        CWD = os.getcwd()
        
        interim_data = pd.read_csv(interim_csv_file)
        interim_data_df = pd.DataFrame(interim_data)
        
        if (CWD != os.path.join(os.getcwd(), OUTPUT_DIR)):
            os.chdir(os.path.join(os.getcwd(), OUTPUT_DIR))
        
        processed_data = pd.DataFrame()
        processed_data['text'] = interim_data_df['title'] + ' ' + interim_data_df['pagetext'] + ' ' + interim_data_df['source']
        processed_data.to_csv(OUTPUT_FILE, index=False, header=['text'])
        
    
    def parse_cdid(self, interim_csv_file):
        OUTPUT_FILE = 'cdid.csv'
        OUTPUT_DIR = 'data/cdid'
        CWD = os.getcwd()
        
        interim_data = pd.read_csv(interim_csv_file)
        interim_data_df = pd.DataFrame(interim_data)
        
        if (CWD != os.path.join(os.getcwd(), OUTPUT_DIR)):
            os.chdir(os.path.join(os.getcwd(), OUTPUT_DIR))
        
        cdid = interim_data_df['cdid']
        cdid.to_csv(OUTPUT_FILE, index=False, header=['cdid'])
        
grab_data = WebCache()
grab_data.parse_cdid('data/interim/interim_data.csv')