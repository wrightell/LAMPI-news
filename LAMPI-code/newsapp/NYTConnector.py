#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import os
import json
import pandas as pd


class NYTConnector():
    def __init__(self):
        self.key = os.getenv('NYT_API_KEY')
        
    def get_top_stories(self, section='home'):
        print(f"finding: {section}")
        url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={self.key}"
        response = requests.get(url)
        if response.ok:
            df = pd.DataFrame(response.json()['results'])
            cols = ['section','title','abstract','url','item_type']
            return df
        else:
            print(f"{response.status_code}: {response.reason}")
            return None
    
    def get_recent_stories(self):
        url = f"https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key={self.key}"
        print('finding recent')
        response = requests.get(url)
        if response.ok:
            df = pd.DataFrame(response.json()['results'])
            cols = ['section','title','abstract','url','item_type']
            return df[cols]
        else:
            print(f"{response.status_code}: {response.reason}")
            return None
    

        