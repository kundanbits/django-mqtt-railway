import json
import requests
import paho.mqtt.client as mqtt

# Django API endpoint
DJANGO_URL = "http://127.0.0.1:8000/api/sensor/"

# MQTT settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "accelerometer/data"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        # Post X-axis value to Django
        requests.post(DJANGO_URL, data={"value": data["x"]})
        print(f"Posted to Django: {data}")
    except Exception as e:
        print(f"Error: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 60)
client.loop_forever()
