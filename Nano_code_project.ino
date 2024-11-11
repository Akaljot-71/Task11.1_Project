#include <WiFiNINA.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "AKAL";
const char* password = "akaljotsingh";

// MQTT server
const char* mqtt_server = "broker.emqx.io";

// WiFi and MQTT clients
WiFiClient wifiClient;
PubSubClient client(wifiClient);

// Sensor pins
const int trigPins[8] = {2, 4, 6, 8, 10, 12, A0, A2};
const int echoPins[8] = {3, 5, 7, 9, 11, 13, A1, A3};
int duration;
int distances[8];

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  // Initialize sensor pins
  for (int i = 0; i < 8; i++) {
    pinMode(trigPins[i], OUTPUT);
    pinMode(echoPins[i], INPUT);
  }

  // Connect to WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  // Setup MQTT
  client.setServer(mqtt_server, 1883);
  while (!client.connected()) {
    if (client.connect("ArduinoClient")) {
      Serial.println("MQTT connected");
    } else {
      delay(5000);
    }
  }
}

void loop() {
  // Reconnect if MQTT connection is lost
  if (!client.connected()) {
    while (!client.connected()) {
      if (client.connect("ArduinoClient")) {
        Serial.println("Reconnected to MQTT broker");
      } else {
        delay(5000);
      }
    }
  }
  client.loop();
  
  // Sensor readings
  for (int i = 0; i < 8; i++) {
    digitalWrite(trigPins[i], LOW);
    digitalWrite(trigPins[i], HIGH);
    digitalWrite(trigPins[i], LOW);
    duration = pulseIn(echoPins[i], HIGH);
    distances[i] = duration * 0.017;
  }

  // Publish sensor data
  for (int i = 0; i < 8; i++) {
    String topic = "parking/sensor" + String(i);
    String payload = String(distances[i]);
    client.publish(topic.c_str(), payload.c_str());
  }

  delay(100);
}
