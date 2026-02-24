# -*- coding: utf-8 -*-
import os
import sys
import json
import signal
from datetime import datetime

# ==========================
# DJANGO SETUP
# ==========================
PROJECT_PATH = "/home/kundan/projectName"
sys.path.insert(0, PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectName.settings")

import django
django.setup()

# Note: You might want to create a Temperature model later
# For now, we use the existing Microphone model as requested
from pages.models import Microphone 

print("? Django connected successfully")

# ==========================
# MQTT CONFIG
# ==========================
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "temperature/data" # Updated topic name

# ==========================
# CALLBACKS
# ==========================
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("? MQTT Connected")
        client.subscribe(TOPIC)
        print("?? Subscribed to:", TOPIC)
    else:
        print("? MQTT Connection failed:", reason_code)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode().strip()
        
        # Handle JSON from ESP8266
        if payload.startswith("{"):
            data = json.loads(payload)
            # It still uses "level" from your ESP8266 code
            value = float(data.get("level", 0))
        else:
            value = float(payload)

        print(f"??? Temperature Received: {value}°C")

        # SAVE TO DATABASE
        # Saving absolute temp into the 'level' column of your model
        Microphone.objects.create(level=value)

        print(f"?? Saved to DB at {datetime.now().strftime('%H:%M:%S')}")

    except Exception as e:
        print("? Error:", e)

# ==========================
# MQTT CLIENT
# ==========================
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to broker...")
client.connect(BROKER, PORT, 60)

def shutdown(sig, frame):
    print("\n?? Stopping safely...")
    client.loop_stop()
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

print("?? Listening for Temperature data...\n")
client.loop_forever()
