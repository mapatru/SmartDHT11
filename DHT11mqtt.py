import os
import time
import sys
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import json


THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'

# Data capture and upload interval in seconds.
INTERVAL=2

dhtDevice = adafruit_dht.DHT11(board.D4)

sensor_data = {'temperature': 0, 'humidity': 0, 'led':'OFF'}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 120 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 120)

client.loop_start()

try:
    while True:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        sensor_data['temperature'] = temperature_c
        sensor_data['humidity'] = humidity
        sensor_data['led'] = 'OFF'
        
        
        if temperature_c < 23:
            sensor_data['led'] = 'ON'
            

        # Sending humidity, temperature and led state data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
            
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
