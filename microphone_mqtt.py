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

from pages.models import Microphone

print("? Django connected successfully")


# ==========================
# MQTT CONFIG
# ==========================
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "microphone/data"


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


def on_disconnect(client, userdata, reason_code, properties=None):
    print("?? MQTT disconnected. Reconnecting...")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode().strip()
        print("RAW:", payload)

        # ---- HANDLE JSON OR NUMBER ----
        if payload.startswith("{"):
            data = json.loads(payload)
            level = float(data.get("level", 0))
        else:
            level = float(payload)

        print("?? Level:", level)

        # ---- SAVE TO DATABASE ----
        Microphone.objects.create(level=level)

        print("?? Saved to DB at", datetime.now().strftime("%H:%M:%S"))

    except Exception as e:
        print("? Error:", e)


# ==========================
# MQTT CLIENT
# ==========================
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

print("Connecting to broker...")
client.connect(BROKER, PORT, 60)


# ==========================
# SAFE EXIT
# ==========================
def shutdown(sig, frame):
    print("\n?? Stopping safely...")
    client.loop_stop()
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)


# ==========================
# START LOOP
# ==========================
print("?? Listening for microphone data...\n")
client.loop_forever()