#include "WiFi.h"
#include "./connection.h" // Connection file containing connection details (SSID, PW)

const char* mqttServer = MQTT_SERVER;
const int mqttPort = 1883;        
#define MQTTUSERNAME ""
const char* mqttPassword = "";

#include <SPI.h>
#include <MFRC522.h>
#include "Adafruit_MQTT.h" 
#include "Adafruit_MQTT_Client.h"
 
#define RST_PIN 22
#define SS_PIN 21
 
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::StatusCode status;

WiFiClient client; 
Adafruit_MQTT_Client mqtt(&client, mqttServer, mqttPort, MQTTUSERNAME, mqttPassword);
Adafruit_MQTT_Publish mqtt_reports = Adafruit_MQTT_Publish(&mqtt, MQTTUSERNAME "hydronizer/reports");

byte buffer[18];
byte size = sizeof(buffer);

uint8_t pageAddr = 0x06;  // Read from page 6  

void setup() {
  Serial.begin(115200);
  
  SPI.begin();
  mfrc522.PCD_Init();

  connectWifi();
  
  Serial.println(F("Read data from MIFARE"));
}

void loop() {
  if (!mqtt.connected())  // Reconnect if connection is lost
  {
    connectWifi();
  }
  
  while (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    delay(50);
  }

  Serial.println(F("Reading data ... "));
  // Read Data
  status = (MFRC522::StatusCode) mfrc522.MIFARE_Read(pageAddr, buffer, &size);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("MIFARE_Read() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  Serial.print(F("Readed data: "));
  char hydro_id[17];
  for (int i = 0; i < 16; i++) {
    hydro_id[i] = (char) buffer[i];
    Serial.print(hydro_id[i]);
  }
  hydro_id[16] = '\0';
  Serial.println();

  int weight = random(300,500);
  
  if (mqtt.connected()) {
    Serial.println(hydro_id);
    String result = "{\"id\":\"";
    result += hydro_id;
    result += "\",\"weight\":";
    result += weight;
    result += "}";
    char resultChar[result.length()];
    result.toCharArray(resultChar, result.length() + 1);
    Serial.println(resultChar);
    mqtt_reports.publish(resultChar);
  }

  mfrc522.PICC_HaltA();
 
}
