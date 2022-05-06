import RPi.GPIO as io
import paho.mqtt.client as mqtt

io.setwarnings(False)
io.setmode(io.BCM)

#define driver pins
IN1 = 2
IN2 = 3
IN3 = 14
IN4 = 18
#setup driver pins
io.setup(IN1,io.OUT)#IN1
io.setup(IN2,io.OUT)#IN2
io.setup(IN3,io.OUT)#IN3
io.setup(IN4,io.OUT)#IN4

def forward():
    io.output(IN1,1)
    io.output(IN2,0)
    io.output(IN3,1)
    io.output(IN4,0)
    
#this function moves the robot backward
def backward():
    io.output(IN1,0)
    io.output(IN2,1)
    io.output(IN3,0)
    io.output(IN4,1)
    
#this function stops the robot
def stopfcn():
    io.output(IN1,0)
    io.output(IN2,0)
    io.output(IN3,0)
    io.output(IN4,0)
    
#this function moves the robot right
def right():
    io.output(IN1,1)
    io.output(IN2,0)
    io.output(IN3,0)
    io.output(IN4,0)
    
#this function moves the robot left
def left():
    io.output(IN1,0)
    io.output(IN2,0)
    io.output(IN3,1)
    io.output(IN4,0)


MQTT_SERVER = "localhost" #specify the broker address, it can be IP of raspberry pi or simply localhost
MQTT_PATH = "testTopic"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '" + message.topic)
    if message.payload == b'5':
        forward()
    elif message.payload == b'0':
        stopfcn()
    elif message.payload == b'4':
        backward()
    elif message.payload == b'1':
        left()
    elif message.payload == b'2':
        right()
    else:
        stopfcn()

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_SERVER, 1883, 60)
    # Connect to the MQTT server and process messages in a background thread.
    mqtt_client.loop_forever()

if __name__ == '__main__':
    main()
