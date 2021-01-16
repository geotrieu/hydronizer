#include "WiFi.h"

#include <SPI.h>
#include <MFRC522.h>
 
#define RST_PIN 22
#define SS_PIN 21
 
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::StatusCode status;

byte buffer[18];  // Buffer (16+2 Bytes: Data + CRC)
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
  //Dump a byte array to Serial
  for (byte i = 0; i < 16; i++) {
    Serial.write(buffer[i]);
  }
  Serial.println();

  mfrc522.PICC_HaltA();
 
}
