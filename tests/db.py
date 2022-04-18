#!/usr/bin/env python
#
# This project will collect temperature and humidity information using a DHT22 sensor
# and send this information to a MySQL database.
#
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import datetime
import MySQLdb

# General settings
prog_name = "Sensor_logger.py"

# Settings for database connection
hostname = '127.0.0.1'
username = 'dbuser'
password = 'dbpass'
database = 'ARMS'

ldr_threshold = 1000
dht_sensor_port = 4                     # Connect the DHT sensor to port D
dht_sensor_type = Adafruit_DHT.DHT11    # DHT Sensor type
ldr_sensor_port = 7                   # Connect the Light sensor to port D
light_pin = 25


deviceID = 'Pi_Sensor'			        # Host name of the Pi

GPIO.setmode(GPIO.BCM)                  # Use the Broadcom pin numbering
GPIO.setup(led, GPIO.OUT)               # LED pin set as output
GPIO.setup(dht_sensor_port, GPIO.IN)    # DHT sensor port as input

# Routine to insert temperature records into the pidata.temps table:
def insert_record( deviceID, datetime, temp, hum):
	query = "INSERT INTO Sensors (deviceID,temperature,humidity,date_time) VALUES ({0},{1},{2},{3})".format(deviceID,temp,hum,datetime)
	args = (deviceID,temp,hum,datetime)
	try:
		conn = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
		cursor = conn.cursor()
		cursor.execute(query, args)
		conn.commit()
	except Exception as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def readLD (ldr_sensor_port):
    reading = 0
    #Output on the pin for 
    GPIO.setup(ldr_sensor_port, GPIO.OUT)
    GPIO.output(ldr_sensor_port, GPIO.LOW)
    time.sleep(0.1)
    
    #Change the pin back to input
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
		hum, temp = Adafruit_DHT.read_retry(dht_sensor_type, dht_sensor_port)
		temp = temp * 9/5.0 + 32
		now = datetime.datetime.now()
		date = now.strftime('%Y-%m-%d %H:%M:%S')
		light = readLDR(ldr_sensor_port)
		if light < ldr_threshold:
			switchOnLight(light_pin)
		else:
			switchOffLight(light_pin)
		insert_record(deviceID,str(date),format(temp,'.2f'),format(hum,'.2f'))
		time.sleep(180)

except (IOError,TypeError) as e:
	print("Exiting...")

except KeyboardInterrupt:  
    	# here you put any code you want to run before the program   
    	# exits when you press CTRL+C  
	print("Stopping...")

finally:
	print("Cleaning up...")  
	GPIO.cleanup() # this ensures a clean exit