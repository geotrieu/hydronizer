#include <SPI.h>
#include <MFRC522.h>
 
#define RST_PIN 22
#define SS_PIN 21
 
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::StatusCode status;

String input;

byte buffer[18];  // Buffer (16+2 Bytes: Data + CRC)
byte size = sizeof(buffer);

uint8_t pageAddr = 0x06; // Write to page 6

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println(F("Please enter a 16-digit code to write to the card"));
}

void loop() {
  if (Serial.available()){
    input = Serial.readStringUntil('\n');
    input.getBytes(buffer, input.length());
    Serial.println(F("Please insert card."));
    while (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
      delay(50);
    }

    // Keep trying to write data if it fails
    while (!writeData()) {
      delay(50);
    }
    
    Serial.println(F("MIFARE_Ultralight_Write() OK "));
    Serial.println();
  
    mfrc522.PICC_HaltA();
  }
}

bool writeData() {
  for (int i=0; i < 4; i++) {
    // Write the 16-bit data to four pages of memory, containing 4 bytes each (4*4=16)
    status = (MFRC522::StatusCode) mfrc522.MIFARE_Ultralight_Write(pageAddr+i, &buffer[i*4], 4);
    if (status != MFRC522::STATUS_OK) {
      Serial.print(F("MIFARE_Read() failed: "));
      Serial.println(mfrc522.GetStatusCodeName(status));
      return false;
    }
  }
  return true;
}
