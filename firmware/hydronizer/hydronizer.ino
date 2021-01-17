#include "WiFi.h"
#include "./connection.h" // Connection file containing connection details (SSID, PW)

const char* mqttServer = MQTT_SERVER;
const int mqttPort = 1883;        
#define MQTTUSERNAME ""
const char* mqttPassword = "";

#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h> 
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "Adafruit_MQTT.h" 
#include "Adafruit_MQTT_Client.h"
 
#define RST_PIN 5
#define SS_PIN 4

#define MINUTE_RESET 30

#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(128, 64, &Wire, OLED_RESET);
 
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::StatusCode status;

WiFiClient client; 
Adafruit_MQTT_Client mqtt(&client, mqttServer, mqttPort, MQTTUSERNAME, mqttPassword);
Adafruit_MQTT_Publish mqtt_reports = Adafruit_MQTT_Publish(&mqtt, MQTTUSERNAME "hydronizer/reports");

byte buffer[18];
byte size = sizeof(buffer);

int timer = 0;
int counter = 1;

uint8_t pageAddr = 0x06;  // Read from page 6  

void setup() {
  Serial.begin(115200);
  
  SPI.begin();
  mfrc522.PCD_Init();

  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  // Show initial display buffer contents on the screen --
  // the library initializes this with an Adafruit splash screen.
  display.display();
  delay(1000);

  display.clearDisplay();
  display.display();

  connectWifi();
  
  Serial.println(F("Read data from MIFARE"));
}

void loop() {
  if (!mqtt.connected())  // Reconnect if connection is lost
  {
    connectWifi();
  }
  
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
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
  
    int weight = 500;
    
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
      resetTimer();
      mqtt_reports.publish(resultChar);
    }
  
    mfrc522.PICC_HaltA();
  }
  oledDrawText(getTimer());
  if (counter >= 10) {
    if (timer > 0) timer--;
    counter = 1;
  } else {
    counter++;
  }
  delay(100);
}

void resetTimer() {
  timer = MINUTE_RESET * 60;
}

String getTimer() {
  if (timer < 0) timer = 0;
  int minutes = timer/60;

  int seconds = timer % 60;

  String timeSeconds = seconds < 10 ? "0" : "";
  timeSeconds += String(seconds);

  String ret = String(minutes);
  ret += ":";
  ret += String(timeSeconds);
  return ret;
}

void oledDrawText(String text) {
  display.clearDisplay();
  display.setTextSize(4);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.cp437(true);

  for(int i=0; i<text.length(); i++) {
    display.write(text[i]);
  }
  display.display();
}
