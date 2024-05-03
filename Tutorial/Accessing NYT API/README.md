### Step 1: Creating API accounts
This project utilizes the NYT API. You can get started by following the [directions](https://developer.nytimes.com/get-started) to create an account, and build an app to get the API license key. Once you sign up, create an app, this one is called LAMPI-News and I gave it access to the Article Search, Times Wire, and Top Stories APIs. 

### Step 2: Adding API keys to Environment
Since we don't want to hardcode our API keys in our code we can add them to our environment. Copy the key from your App in the NYT Developer portal. On the ec2 lampi write:
```
nano ~/.bashrc
```
add the following line to the end of the file:
```
export NYT_API_KEY="<YOUR-KEY-HERE>"
```
Save and exit the file. To make the changes, run:
```
source ~/.bashrc
```
### Step 3: Writing scripts
First, create a new python script. At the top of your file import `requests ` and `os`:
```
import requests
import os
```
The requests library allows us to send calls to the NYT api to get data. Here, I will show how to make the calls. Copy the following:
```
key = os.getenv('NYT_API_KEY')
section = 'home'

top_stories_url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={key}"
recent_stories_url = f"https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key={key}"

top_stories_response = requests.get(top_stories_url)
recent_stories_response = requests.get(recent_stories_url)

if top_stories_response.ok:
  top_stories = top_stories_response.json()['results']

if recent_stories_response.ok:
  recent_stories = recent_stories_resposnse.json()['results']
```
This code first retrieves our `key` from our environment. For the top stories we can select a section (The possible section value are: arts, automobiles, books/review, business, fashion, food, health, home, insider, magazine, movies, nyregion, obituaries, opinion, politics, realestate, science, sports, sundayreview, technology, theater, t-magazine, travel, upshot, us, and world.) Then it defines the NYT api endpoints to make requests to get the data. We use a `get` request to retrieve it. Assuming you write your key correctly in your .bashrc file and you have a stable internet connection, the response should be successful. You can view the list of json objects of the responses. 

### My Lampi code:
```
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
```
I just created an class which stores the key and has the calls I made with some extra statements. I use a pandas dataframe to filter the results of the jsons to the sections I needed. 

### Move on to (Setting Up MQTT)[../Setting%20Up%20MQTT]
