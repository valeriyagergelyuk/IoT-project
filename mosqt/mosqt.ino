//This is for esp
#include <WiFi.h>
#include <PubSubClient.h>
// Replace the next variables with your SSID/Password combination
const char* ssid = "Crackers";
const char* password = "ChrisDuck";
// Add your MQTT Broker IP address, example:
const char* mqtt_server = "192.168.167.140";
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
int islightReallyTrue = 0;
int islightReallyFalse = 0;
// LED Pin
const int ledPin = 5;
const int photoResistorPin = 39;

void setup() {
  Serial.begin(115200);
  setup_wifi();

  client.setServer(mqtt_server, 1883);
  pinMode(ledPin, OUTPUT);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("vanieriot")) {
      Serial.println("connected");
      //client.subscribe("room/light");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  if (!client.loop()) {
    client.connect("vanieriot");
  }
  int lightValue = analogRead(photoResistorPin);
  String lightValueStr = String(lightValue);

  if (atoi(lightValueStr.c_str()) <= 400) {
    islightReallyFalse = 0;
    islightReallyTrue++;
    Serial.println("Light On: " + String(islightReallyTrue));

    if (islightReallyTrue == 4) {
      islightReallyTrue = 3;
    }

    if (islightReallyTrue == 3) {
      digitalWrite(ledPin, HIGH);
      client.publish("IoTlab/EPS32", lightValueStr.c_str());
      Serial.println(lightValueStr.c_str());
    }
  } else {
    islightReallyTrue = 0;
    islightReallyFalse++;
    Serial.println("Light off: " + String(islightReallyFalse));

    if (islightReallyFalse == 4) {
      islightReallyFalse = 3;
    }

    if (islightReallyFalse == 3) {
      digitalWrite(ledPin, LOW);
      client.publish("IoTlab/EPS32", lightValueStr.c_str());
      Serial.println(lightValueStr.c_str());
    }
  }
  delay(1000);
}