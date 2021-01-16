const char* ssid = WIFI_SSID;
const char* password =  WIFI_PASSWORD;

void connectWifi() {
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  
  Serial.println("Connected to the WiFi network!");

  Serial.println("Connecting to MQTT Network");
  if ((mqtt.connect()) != 0) {
    mqtt.disconnect();
    Serial.println("MQTT Failed!");
  } else {
    Serial.println("MQTT Connected!");
  }

  Serial.println("\nConnected to MQTT!");
}
