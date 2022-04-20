#!/bin/python3.9

import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import datetime
import json, base64
import urllib.request

# General settings
ldr_threshold = 1000
dht_sensor_port = 4                     # DHT sensor to port 4
dht_sensor_type = Adafruit_DHT.DHT11    # DHT Sensor type
ldr_sensor_port = 7                     # Light sensor to port 7
light_pin = 25							# LED to port 25
deviceID = 'Sensor_Pi'			        # Host name of the Pi
tableName = 'Sensors'					# Sensor table name
api_key = 'YWhsYXdlbnRpMTIz'			# API Key

# GPIO settings
GPIO.setmode(GPIO.BCM)                  # Use the Broadcom pin numbering
GPIO.setup(light_pin, GPIO.OUT)         # LED pin set as output
GPIO.setup(dht_sensor_port, GPIO.IN)    # DHT sensor port as input

def encode(data):
	data = json.dumps(data)
	message_bytes = data.encode('ascii')
	base64_bytes = base64.b64encode(message_bytes)
	base64_message = base64_bytes.decode('ascii')
	return base64_message

def decode(base64_message):
	base64_bytes = base64_message.encode('ascii')
	message_bytes = base64.b64decode(base64_bytes)
	message = message_bytes.decode('ascii')
	return json.loads(message)

def readLD (ldr_sensor_port):
	reading = 0
	GPIO.setup(ldr_sensor_port, GPIO.OUT)
	GPIO.output(ldr_sensor_port, GPIO.LOW)
	time.sleep(0.1)
	GPIO.setup(ldr_sensor_port, GPIO.IN)

	while (GPIO.input(ldr_sensor_port) == GPIO.LOW):
		reading += 1
	return reading

def switchOnLight(PIN):
	GPIO.setup(PIN, GPIO.OUT)
	GPIO.output(PIN, True)

def switchOffLight(PIN):
	GPIO.setup(PIN, GPIO.OUT)
	GPIO.output(PIN, False)

# Main loop
try:
	while True:
		humidity, temperature = Adafruit_DHT.read_retry(dht_sensor_type, dht_sensor_port)
		temperature = temperature * 9/5.0 + 32
		now = datetime.datetime.now()
		date = now.strftime('%Y-%m-%d %H:%M:%S')
		light = readLDR(ldr_sensor_port)
		if light < ldr_threshold:
			switchOnLight(light_pin)
		else:
			switchOffLight(light_pin)
		try:
			data = [deviceID, tableName, humidity, temperature]
			data_enc = encode(data)
			url = 'http://127.0.0.1:8080/api/'+ api_key + '/update/{}'.format(data_enc)
			response = urllib.request.urlopen(url)
		except:
			time.sleep(2)
		time.sleep(180)
except (IOError,TypeError) as e:
	print("Exiting...")

finally:
	print("Cleaning up...")
	GPIO.cleanup() # this ensures a clean exit