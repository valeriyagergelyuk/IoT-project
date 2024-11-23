//This is for esp
#include <WiFi.h>
#include <PubSubClient.h>
//for rfid
#include <SPI.h>
#include <MFRC522.h>

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

//RFID pins
#define SS_PIN 6 // SDA Pin on RC522
#define RST_PIN 4 // RST Pin on RC522

MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(115200);
  setup_wifi();

  SPI.begin(); 
  rfid.PCD_Init(); 
  
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

string checkRfid(){
  if (!rfid.PICC_IsNewCardPresent()) {
    return;
  }
  if (!rfid.PICC_ReadCardSerial()) {
    return;
  }

  string tag_id = "";

  for (byte i = 0; i < rfid.uid.size; i++) {
    string ind_no = rfid.uid.uidByte[i] < 0x10 ? " 0" : " "; 
    std::string s {std::to_string(HEX_bufferMessage[rfid.uid.uidByte[i]])};
    tag_id += s;
  }

  rfid.PICC_HaltA();
  return tag_id;
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

  string tag_id = checkRfid();
  if(tag_id != ""){
    client.publish("IoTlab/RFID", tag_id);  
  }
  
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
