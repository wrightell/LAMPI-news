This part will be entirely on our EC2 instance. Django is overkill for this project but it's scalable and if you want to add more features, it should be really easy to extend the current set up.

### Step 1: Installing Django and creating Project and App
First, download django with `sudo pip3 install django==5.0.1`. Let's create a new project with `django-admin startproject newssite`. We can have multiple apps within our project, but we will only create one. Run
```
cd newssite
python3 manage.py startapp news
```
This creates our news app. The first thing we need to do is add our app to our project. Side note: "project" refers to the newssite/newsiste directory and "app" refers to newsiste/newssite/news directory. Open `settings.py` and in the INSTALLED_APPS list, add 'news'. 

### Step 2: Defining a model
Remember we will be sending an mqtt message containing an article title and it's url. So, let's create this: open `models.py` and write:
```
from django.db import models
from django.db import models

class NewsItem(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title
```
We now have a news article model for out database. To add it to our project, run:
```
python3 manage.py makemigrations
python3 manage.py migrate
```
### Step 3: Defining Our Structure
In our app create a new folder to hold the html files with `mkdir -p /templates/news/`. And in that subfolder create the html file `reading_list.html`:
```
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Reader</title>
    <link rel="stylesheet" href="{% static 'news/css/site.css' %}">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.2/mqttws31.min.js"></script>
    <script src="{% static 'news/js/page.js' %}" defer></script>
</head>
<body>
    <h1>News Reading List</h1>
    <ul id="newsList">
        {% for news_item in news_items %}
            <li id="news-item-{{ news_item.id }}">
                <a href="{{ news_item.url }}" target="_blank">{{ news_item.title }}</a>
                <button class="delete-button" data-id="{{ news_item.id }}">Delete</button>
            </li>
        {% endfor %}
    </ul>

    <script src="{% static 'news/js/page.js' %}" defer></script>
</body>
</html>
```
This just creates a page with a heading "News Reading List" and then if a list of news items is sent in with the request, it will add them to a list in the diplay. However, this file depends on several other items: static, site.css, news/css/site.css, and news/js/page,js. This is good practice in general to have these files so lets add them in our project directory. Run:
```
mkdir -p ./static/news/{css,images,js}
```
And then in css make the file site.css:
```
body {
    font-family: Arial, sans-serif;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    margin: 10px 0;
    padding: 10px;
    background-color: #f4f4f4;
    border: 1px solid #ddd;
}

a {
    text-decoration: none;
    color: #333;
}

a:hover {
    text-decoration: underline;
}
```
This just adds some better looking features for the news list items. 
And then in js, make the file page.js:
```
document.addEventListener("DOMContentLoaded", function() {
    const reconnectInterval = 3000;
    const brokerUrl = "34.207.111.28";
    const brokerPort = 50002;
    const clientId = "clientId" + new Date().getTime();
    let client = new Paho.MQTT.Client(brokerUrl, brokerPort, clientId);

    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    function initializeClient() {
        client.connect({
            onSuccess: onConnect,
            onFailure: onConnectFailure,
            useSSL: false,
        });
    }

    function onConnect() {
        console.log("Connected to WebSocket port " + brokerPort);
        client.subscribe("web/news");
    }

    function onConnectFailure(responseObject) {
        console.error("Connection failed: " + responseObject.errorMessage);
        setTimeout(initializeClient, reconnectInterval);
    }

    function onConnectionLost(responseObject) {
        if (responseObject.errorCode !== 0) {
            console.log("Connection lost:", responseObject.errorMessage);
            setTimeout(initializeClient, reconnectInterval);
        }
    }

    function onMessageArrived(message) {
        let newsItem = JSON.parse(message.payloadString);
        addNewsItem(newsItem);
    }

    function addNewsItem(newsItem) {
        if (!document.getElementById(`news-item-${newsItem.id}`)) {
            let li = document.createElement("li");
            li.id = `news-item-${newsItem.id}`;
            li.innerHTML = `<a href="${newsItem.url}" target="_blank">${newsItem.title}</a> <button class="delete-button" data-id="${newsItem.id}">Delete</button>`;
            document.getElementById("newsList").appendChild(li);
        } else {
            console.log('Duplicate message received, ignoring.');
        }
    }
    document.getElementById('newsList').addEventListener('click', function(event) {
        if (event.target.classList.contains('delete-button')) {
            deleteItem(event.target.dataset.id);
        }
    });

    function deleteItem(id) {
        fetch(`/news/delete/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: id })
        }).then(response => response.json())
          .then(data => {
              if (data.status === 'success') {
                  const item = document.getElementById(`news-item-${id}`);
                  if (item) {
                      item.remove();
                  }
              } else {
                  console.error('Delete failed:', data.message);
              }
          }).catch(error => console.error('Error:', error));
    }

    function getCSRFToken() {
        let cookies = document.cookie.split(';');
        let token = cookies.find(c => c.trim().startsWith('csrftoken='));
        return token ? token.split('=')[1] : 'unknown';
    }

    initializeClient();
});
```
There are a couple things happening here. We first create a connection to the mqtt broker so we can recieve messages. Notice however, we are reading over the 50002, therefore, go the AWS Console and add an inbound rule for this port just like we did for 50001. When a new message is recieved we parse the message and add it to the list of news articles on the page. Each article is identfied by it's id in the the database. There is a delete button associated with it which will remove the item from the page and then send a request to delete the element from the database. Then we make sure to reconnect if we ever get disconnected.   

### Step 4: Creating our Views
In the views.py we need to handle the logic for the requests between pages (in this case there is only one). Here is the file:
```
from django.http import JsonResponse, Http404
from .models import NewsItem
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.shortcuts import render

@ensure_csrf_cookie
def reading_list(request):
    news_items = NewsItem.objects.all()
    return render(request, 'news/reading_list.html',{'news_items':news_items})

def delete_news_item(request, pk):
    if request.method == 'POST':
        try:
            news_item = get_object_or_404(NewsItem, pk=pk)
            news_item.delete()
            return JsonResponse({'status': 'success'})
        except NewsItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
```
For the reading_list page, we query all the news item objects in the database and pass them into the request to for the page to load them. We also need to create a view for the delete button when it gets triggered we can update the database. 

### Step 5: Handling Navigation
This part is also easy because we only have one page on our app. We first need a `urls.py` in our app though. So create that file and add:
```
from django.urls import path
from . import views

urlpatterns = [
    path('reading-list/', views.reading_list, name='reading_list'),
    path('delete/<int:pk>/', views.delete_news_item, name='delete_news_item'),
]
```
We have now just created a path so that when someone goes to the site  http://"EC2-IP"/reading-list/" they get directed to the file we created. The same applies to the logic of the delete button as described above, but this is not visible to the user. In order to link our app urls to the project urls we mush navigate to the project  `urls.py` file and add the following to the urlpatterns list: `path('news/', include('news.urls')),`

### Step 6: Communication Between Pi and Website
Instead of sending mqtt messages straight from the pi to the javascript, we have an intermediate step. This is better for security reasons and allows us to do some pre-processing on the database side before showing it to the user. Therefore I created a script called `mqtt-daemon.py` to handle this which looks like:
```
import json
import paho.mqtt.client as mqtt
import django
import os
import logging

logging.basicConfig(level=logging.INFO, filename='mqtt-daemon.log', format='%(asctime)s:%(levelname)s:%(message)s')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newssite.settings")
django.setup()

from news.models import NewsItem

def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code " + str(rc))
    client.subscribe("devices/+/news/")

def on_message(client, userdata, msg):
    logging.info(f"Message received-> {msg.topic}: {str(msg.payload)}")
    try:
        decoded_payload = msg.payload.decode('utf-8')
        data = json.loads(decoded_payload)
        logging.info("JSON loaded successfully")

        news_item, created = NewsItem.objects.get_or_create(
            title=data['title'], 
            defaults={'url': data['url']}
        )

        if created:
            logging.info(f"Created a new NewsItem: {news_item.title}")
        else:
            logging.info(f"NewsItem already exists: {news_item.title}")

        client_payload = json.dumps({'id': news_item.id, 'title': news_item.title, 'url': news_item.url})
        client.publish("web/news", payload=client_payload)

    except Exception as e:
        logging.error("Error processing message: %s", str(e), exc_info=True)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("34.207.111.28", 50001, 60)
client.loop_forever()
```
I created logging to make sure messages were getting received and processed correctly. When we get a message from the pi, we decode the data and create a new news item for the data base. We then get the id, and create a new mqtt message with this included to pass to the webbrowser. The reason this is necessary is so that a user cannot add the same article multiple times and when we delete articles on the webpage, we can link the id to the database entry. 

This script needs to continually run so a supervisor script was created. Just like we did for the kivy on the pi:
```
sudo apt-get install supervisor
```
And create the file `sudo nano /etc/supervisor/conf.d/mqtt-daemon.conf` with 
```
[program:mqtt-daemon]
command=/usr/bin/python3 /home/ubuntu/LAMPI-news/Web/newssite/mqtt-daemon.py
directory=/home/ubuntu/LAMPI-news/Web/newssite/
autostart=true
autorestart=true
stderr_logfile=/var/log/mqtt-daemon.err.log
stdout_logfile=/var/log/mqtt-daemon.out.log
user=ubuntu
environment=DJANGO_SETTINGS_MODULE="newssite.settings"
```
### Step 7: Deploy the Website
We are going to use Nginx and uwsgi to host the website. To do this we need to install both. First we need to change permissions to our home directory with `chmod +rx /home/ubuntu`. It is not good to host sites from the home directory, but, alas. To get nginx run `sudp apt-get install -y nginx`. We need to open the http port so go to the AWS console and add another inbound rule, but this time with Type HTTP. 





