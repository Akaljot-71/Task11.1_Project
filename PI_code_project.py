import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# GPIO pin setup for LEDs
led_pins = [2, 3, 4, 17, 27, 22, 10, 9]
row_led_pins = [5, 6]  # Pins for row indicator LEDs

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

# MQTT settings
broker = "broker.emqx.io"

# This function runs when the Raspberry Pi connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to each sensor topic
    client.subscribe("parking/sensor0")
    client.subscribe("parking/sensor1")
    client.subscribe("parking/sensor2")
    client.subscribe("parking/sensor3")
    client.subscribe("parking/sensor4")
    client.subscribe("parking/sensor5")
    client.subscribe("parking/sensor6")
    client.subscribe("parking/sensor7")

# This function runs when a message is received from the MQTT broker
def on_message(client, userdata, msg):
    sensor_id = int(msg.topic.split("sensor")[1])
    distance = int(msg.payload)
    
    # Control the corresponding LED
    if distance > 5:  # If space is free
        GPIO.output(led_pins[sensor_id], GPIO.HIGH)
    else:  # If space is occupied
        GPIO.output(led_pins[sensor_id], GPIO.LOW)
    
    # Update row indicator LEDs
    update_row_leds()

# Update row indicator LEDs based on individual LEDs
def update_row_leds():
    # Row 1
    if any(GPIO.input(pin) for pin in led_pins[:4]):
        GPIO.output(5, GPIO.HIGH)
    else:
        GPIO.output(5, GPIO.LOW)

    # Row 2
    if any(GPIO.input(pin) for pin in led_pins[4:]):
        GPIO.output(6, GPIO.HIGH)
    else:
        GPIO.output(6, GPIO.LOW)

# Create MQTT client and set up callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker, 1883, 60)

# Start the MQTT client loop
client.loop_forever()
