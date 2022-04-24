import time
import RPi.GPIO as GPIO
import Adafruit_DHT
import psutil
import datetime
import json, base64
import urllib.request
# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
	if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
		proc.kill()

GPIO.setmode(GPIO.BCM) 

deviceID = 'Sensors'			        # Host name of the Pi
tableName = 'Sensor_Pi'					# Sensor table name
api_key = 'YWhsYXdlbnRpMTIz'			# API Key

ldr_threshold = 25000
DHT11_GPIO = 23
LIGHT_GPIO = 25
LDR_GPIO = 18

GPIO.setup(DHT11_GPIO, GPIO.OUT)
GPIO.setup(LDR_GPIO, GPIO.OUT)

DHT11 = Adafruit_DHT.DHT11

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

def readLDR(ldr_sensor_port):
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
try:
	while True:
		try:
			humidity,temperature = Adafruit_DHT.read_retry(DHT11,DHT11_GPIO)
			now = datetime.datetime.now()
			light = readLDR(LDR_GPIO)
			print('Temperature={0:0.1f}°C Humidity={1:0.1f}%\ Light={2}'.format(temperature, humidity, light))

			if light < ldr_threshold:
				switchOnLight(LIGHT_GPIO)
			else:
				switchOffLight(LIGHT_GPIO)

			data = [deviceID, tableName, temperature, 0, humidity, light]
			data_enc = encode(data)
			url = 'http://127.0.0.1:8080/api/'+ api_key + '/update/{}'.format(data_enc)
			response = urllib.request.urlopen(url)
			time.sleep(1.5)
		except RuntimeError as error:
			print(error.args[0])
			time.sleep(2.0)
			continue
		except Exception as error:
			raise error
			time.sleep(2.0)
finally:
		print("Cleaning up ...")
		GPIO.cleanup()
	