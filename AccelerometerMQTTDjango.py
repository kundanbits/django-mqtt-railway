# -*- coding: utf-8 -*-

import os
import sys
import json
import math
import signal

# ==========================
# DJANGO SETUP
# ==========================
sys.path.insert(0, "/home/kundan/projectName/projectName")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectName.settings")

import django
django.setup()

from pages.models import Accelerometer

print("Django connected successfully")

# ==========================
# MQTT
# ==========================
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_DATA = "accelerometer/data"
TOPIC_LED = "accelerometer/led"

VIBRATION_THRESHOLD = 1.5
DB_SAVE_INTERVAL = 10  # Save every 10 samples

sample_counter = 0


# ==========================
# MQTT CALLBACKS
# ==========================
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT broker:", reason_code)
    client.subscribe(TOPIC_DATA)


def on_message(client, userdata, msg):
    global sample_counter

    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        x = float(data.get("x", 0))
        y = float(data.get("y", 0))
        z = float(data.get("z", 0))

        sample_counter += 1

        # Save to DB every N samples
        if sample_counter % DB_SAVE_INTERVAL == 0:
            Accelerometer.objects.create(x=x, y=y, z=z)

        magnitude = math.sqrt(x**2 + y**2 + z**2)

        if magnitude > VIBRATION_THRESHOLD:
            client.publish(TOPIC_LED, "ON")
        else:
            client.publish(TOPIC_LED, "OFF")

    except Exception as e:
        print("Error:", e)


# ==========================
# MQTT CLIENT SETUP
# ==========================
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to MQTT broker...")
client.connect(BROKER, PORT, 60)


# ==========================
# CLEAN SHUTDOWN
# ==========================
def shutdown(sig, frame):
    print("\nShutting down safely...")
    client.loop_stop()
    client.disconnect()
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown)

# ==========================
# START MQTT LOOP
# ==========================
client.loop_forever()
