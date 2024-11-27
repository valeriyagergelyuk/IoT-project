
//This is for esp
#include <WiFi.h>
#include <DHT.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>

const char* ssid = "AMANANET_016";
const char* password = "68557461";
const char* mqtt_server = "192.168.1.161";

WiFiClient espClient;
PubSubClient client(espClient);

int islightReallyTrue = 0;
int islightReallyFalse = 0;
// Led Pin
const int ledPin = 5;
// PhotoResistor Pin
const int photoResistorPin = 39;  //VN
// RFID pins
#define SS_PIN 17  // SDA Pin
#define RST_PIN 4  // RST Pin
MFRC522 rfid(SS_PIN, RST_PIN);
// DHT pin
#define DHTPIN 16
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  // WIFI
  setup_wifi();
  // RFID
  SPI.begin();
  rfid.PCD_Init();
  // DHT
  dht.begin();
  // MQTT
  client.setServer(mqtt_server, 1883);
  // LED
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
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

String checkRfid() {
  // Look for new cards
  if (!rfid.PICC_IsNewCardPresent()) {
    return "none";
  }

  // Select one of the cards
  if (!rfid.PICC_ReadCardSerial()) {
    return "none";
  }

  // get UID
  String card_uid = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (rfid.uid.uidByte[i] < 0x10) {
      card_uid += "0"; // Add leading zero for single-digit bytes
    }
    card_uid += String(rfid.uid.uidByte[i], HEX);
  }
  // Halt PICC
  rfid.PICC_HaltA();
  Serial.println(card_uid);
  return card_uid;
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  if (!client.loop()) {
    client.connect("vanieriot");
  }

  String resultTemp = dhtHandlerTemp();
  String resultHum = dhtHandlerHum();
  String tag_id = checkRfid();

  client.publish("IoTlab/dht11/hum", resultHum.c_str());
  client.publish("IoTlab/dht11/temp", resultTemp.c_str());
  client.publish("IoTlab/RFID", tag_id.c_str());

  lightSensor();
    delay(1000);
}

void lightSensor() {
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
}

String dhtHandlerTemp() {
  float t = dht.readTemperature();
  if (isnan(t)) {
    return "";
  }
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  return String(t);
}

String dhtHandlerHum() {
  float h = dht.readHumidity();
  if (isnan(h)) {
    return "";
  }
  Serial.print(F("Humidity: "));
  Serial.print(h);
  return String(h);
}
