#include <OneWire.h>
#include <DallasTemperature.h>
#include <SoftwareSerial.h>
#include <LiquidCrystal.h>

#define SENSOR_PIN A0 // Analog pin connected to the pH sensor
#define ONE_WIRE_BUS 4 // Pin for DS18B20 data line
#define TURBIDITY_SENSOR_PIN A1 // Analog pin connected to the turbidity sensor
#define TDS_SENSOR_PIN A2 // Analog pin connected to the TDS sensor

SoftwareSerial espSerial(2, 3); // RX, TX
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void adjustBacklight(byte brightness) {
  analogWrite(6, brightness); // Pin 6 for backlight control, adjust pin according to your setup
}

void setup() {
  Serial.begin(9600);
  espSerial.begin(115200);
  lcd.begin(16, 2);
  lcd.command(B00001100); // Turn off cursor
  adjustBacklight(50); // Adjust backlight brightness here (0-255), lower value reduces brightness
  sensors.begin(); // Initialize temperature sensors
}

void loop() {
  readPHSensor();
  readTemperatureSensor();
  readTurbiditySensor();
  readTDSSensor();
  delay(5000); // Delay before reading the sensors again
}

void readPHSensor() {
  int sensorValue = analogRead(SENSOR_PIN); // Read analog value from pH sensor
  float voltage = sensorValue*(5.0/1024.0);
  float pHValue = 2.5 * voltage + 0.00;
  //float pHValue = map(sensorValue, 0, 1023, 0, 14); // Map analog value to pH range (0-14)
  
  Serial.print("pH Value: ");
  Serial.println(pHValue);

  espSerial.print("pH Value: ");
  espSerial.println(pHValue);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("pH:");
  lcd.print(pHValue);

  delay(15000); 
}

void readTemperatureSensor() {
  sensors.requestTemperatures();
  float temperatureC = sensors.getTempCByIndex(0); // Get temperature in Celsius
  
  Serial.print("Temperature: ");
  Serial.println(temperatureC);

  // Send data to ESP-12E
  espSerial.print("Temperature: ");
  espSerial.println(temperatureC);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temp:");
  lcd.print(temperatureC);

  delay(18000);
}

void readTurbiditySensor() {
  int turbidityValue = analogRead(TURBIDITY_SENSOR_PIN); // Read turbidity value
  float ntuValue = map(turbidityValue, 0, 1023, 0, 500);

  Serial.print("Turbidity Value: ");
  Serial.println(ntuValue);

  // Send data to ESP-12E
  espSerial.print("Turbidity Value: ");
  espSerial.println(ntuValue);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Turbidity:");
  lcd.print(ntuValue);

  delay(18000);
}

void readTDSSensor() {
  int tdsValue = analogRead(TDS_SENSOR_PIN); // Read TDS value
  Serial.print("TDS Value: ");
  Serial.println(tdsValue);

  // Send data to ESP-12E
  espSerial.print("TDS Value: ");
  espSerial.println(tdsValue);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("TDS:");
  lcd.print(tdsValue);

  delay(18000);
}
