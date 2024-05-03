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
