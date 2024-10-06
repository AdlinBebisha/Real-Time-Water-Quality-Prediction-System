#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ThingSpeak.h>

const char* ssid = "POCO C31";
const char* password = "13060720";
const char* server = "api.thingspeak.com";
const char* apiKey = "8A6ZUK3I9ZWBLGUX";
const unsigned long channelNumber = 2421427;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(10);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println("");
  Serial.println("Connecting to WiFi...");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  ThingSpeak.begin(client);  // Initialize ThingSpeak client
}

void loop() {
  static String buffer = ""; // Static buffer to accumulate data
  
  if (Serial.available()) {
    char c = Serial.read(); // Read a character from serial
    
    if (c == '\n') { // If end of line is received
      if (buffer.startsWith("Temperature:")) { // Check if the received data is temperature value
        float temperature = buffer.substring(13).toFloat(); // Extract temperature value from received data
        
        // Update ThingSpeak channel with temperature value
        ThingSpeak.writeField(channelNumber, 1, temperature, apiKey);

        Serial.print("Sent to ThingSpeak (Temperature): ");
        Serial.println(temperature);
      } else if (buffer.startsWith("pH Value:")) { // Check if the received data is pH value
        float pHValue = buffer.substring(10).toFloat(); // Extract pH value from received data

        // Update ThingSpeak channel with pH value
        ThingSpeak.writeField(channelNumber, 2, pHValue, apiKey);

        Serial.print("Sent to ThingSpeak (pH): ");
        Serial.println(pHValue);
      } else if (buffer.startsWith("Turbidity Value:")) { // Check if the received data is turbidity value
        float ntuValue = buffer.substring(16).toFloat(); // Extract turbidity value from received data

        // Update ThingSpeak channel with turbidity value
        ThingSpeak.writeField(channelNumber, 3, ntuValue, apiKey);

        Serial.print("Sent to ThingSpeak (Turbidity): ");
        Serial.println(ntuValue);
      } else if (buffer.startsWith("TDS Value:")) { // Check if the received data is turbidity value
        int tdsValue = buffer.substring(11).toInt(); // Extract TDS value from received data

        // Update ThingSpeak channel with turbidity value
        ThingSpeak.writeField(channelNumber, 4, tdsValue, apiKey);

        Serial.print("Sent to ThingSpeak (TDS): ");
        Serial.println(tdsValue);
      }
      
      buffer = ""; // Clear buffer
    } else {
      buffer += c; // Append character to buffer
    }
  }
}
