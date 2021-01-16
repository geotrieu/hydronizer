#include "./connection.h" // Connection file containing connection details (SSID, PW)

const char* ssid = WIFI_SSID;
const char* password =  WIFI_PASSWORD;

void connectWifi() {
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
}
