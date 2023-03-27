import os
import requests
import constants
import pandas as pd
import urllib.parse as ul
import json

class WebCache:
    def __init__(self):
        self.csv = None
    
    def get(self, url: str, txtFile: object, outputFile: str):
        '''Get data from aitopics API
        
        Arguments:
        url -> API endpoint,
        filename -> File (.txt) to loop through. File should have list of cdid's separated by \\n
        
        Result:
        Saves the returned JSON data into a CSV file named 'dataset.csv'
        with 4 headers ['pagetext', 'cdid', 'source', 'title']
        '''
        getUrl = url
        fileName = txtFile
        
        with open(fileName, 'r') as f:
            counter = 1
            for line in f:
                payload = { "q":f"cdid:{line}", "fields": "title,pagetext,cdid,source"}
                encodedPayload = ul.urlencode(payload)       
                headers = {
                    'Authorization': constants.key,
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Cookie': constants.cookie
                }
                print(f'Sending request #{counter}')
                response = requests.request("POST", getUrl, headers=headers, data=encodedPayload)
                data = json.loads(response.text)
                
                df = pd.DataFrame(data)
                
                if (os.path.exists(outputFile)):
                    df.to_csv(outputFile, mode='a', index=False, header=False, sep=',')
                else:
                    df.to_csv(outputFile, index=False, header=['title', 'pagetext', 'cdid', 'source'], sep=',')
                counter += 1
                
    def cleanCSV(self, csvFile):
        '''
        
        '''
        data = pd.read_csv(csvFile)
        df = pd.DataFrame(data)
        
        # Grab pagetext column and put into list
        pagetext = data['pagetext'].tolist()
        
        # Iterate list and strip characters out
        for i in range(len(pagetext)):
            strippedText = pagetext[i].strip('[\'"1::]')
            df['pagetext'][i] = strippedText
            
        df.to_csv(csvFile, index=False, header=['title', 'pagetext', 'cdid', 'source'], sep=',')
        
    def concat(self, input_: object):
        data = pd.read_csv(input_)
        df1 = pd.DataFrame(data)
        df2 = pd.DataFrame()
        df2['text'] = df1['title'] + ', ' + df1['pagetext'] + ', ' + df1['cdid'] + ', ' + df1['source']
        df2.to_csv(input_, index=False, header=['text'])

grabber = WebCache()
grabber.get('https://dev.i2kconnect.com/i2kweb/webapi/search', 'cdids.txt', 'i2k_new.csv')
grabber.cleanCSV('i2k_new.csv')
grabber.concat('i2k_new.csv')

# Base url to send requests to
# url = "https://dev.i2kconnect.com/i2kweb/webapi/search"

# counter = 1 # Just so i can keep track of how far along in requests we are
# with open('newcd.txt', 'r') as f:
#     for line in f:
#         payload = { "q":f"cdid:{line}", "fields": "pagetext,cdid,source,title"}
#         encodedPayload = ul.urlencode(payload)        
#         headers = {
#             'Authorization': constants.key,
#             'Content-Type': 'application/x-www-form-urlencoded',
#             'Cookie': ''
#         }
#         print(f'Sending request #{counter}')
#         response = requests.request("POST", url, headers=headers, data=encodedPayload)
#         data = response.json()
#         df = pd.DataFrame(data)
#         if (os.path.exists('newData.csv')):
#             df.to_csv('newData.csv',mode='a', index=False, header=False, sep=',')
#         else:
#             df.to_csv('newData.csv', index=False, header=['pagetext','cdid','source','title'], sep=',')
#         counter += 1