import RPi.GPIO as GPIO
import dht22
import time
import paho.mqtt.client as mqtt

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize DHT22 sensor
sensor = dht22.DHT22(pin=4)

# GPIO pins for actuators
light_relay_pin = 17
fan_relay_pin = 18

# Set up MQTT parameters
mqtt_broker = "your_mqtt_broker_address"
mqtt_port = 1883
mqtt_topic_temp = "room/temperature"
mqtt_topic_motion = "room/motion"
mqtt_topic_light = "room/light"

# Set up GPIO pins
GPIO.setup(light_relay_pin, GPIO.OUT)
GPIO.setup(fan_relay_pin, GPIO.OUT)

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic_temp)
    client.subscribe(mqtt_topic_motion)

# MQTT on_message callback
def on_message(client, userdata, msg):
    if msg.topic == mqtt_topic_temp:
        process_temperature(float(msg.payload))
    elif msg.topic == mqtt_topic_motion:
        process_motion(int(msg.payload))

# Function to control lights based on motion
def process_motion(motion_status):
    if motion_status == 1:
        GPIO.output(light_relay_pin, GPIO.HIGH)  # Turn on lights
    else:
        GPIO.output(light_relay_pin, GPIO.LOW)   # Turn off lights

# Function to adjust temperature control
def process_temperature(temperature):
    # Add logic to control temperature (e.g., turn on fan or AC based on temperature)

# Set up MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

# Start MQTT loop
client.loop_start()

try:
    while True:
        # Read temperature from DHT22 sensor
        result = sensor.read()
        if result.is_valid():
            temperature = result.temperature
            # Publish temperature to MQTT broker
            client.publish(mqtt_topic_temp, temperature)
        time.sleep(5)  # Adjust the sleep duration based on your requirements

except KeyboardInterrupt:
    print("Program terminated by user.")
    GPIO.cleanup()
    client.disconnect()
