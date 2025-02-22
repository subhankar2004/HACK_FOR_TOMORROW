#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// WiFi Credentials
// WiFi Credentials
#define WIFI_SSID "M35"
#define WIFI_PASSWORD "11111111"

// Firebase Credentials
#define FIREBASE_HOST "https://resqnet-171e6-default-rtdb.firebaseio.com/"
#define FIREBASE_AUTH "AIzaSyDseZriypzJzrz-Iy8jAxDmsB6vVLhxLbI"

// Initialize Firebase
FirebaseData firebaseData;
FirebaseConfig config;
FirebaseAuth auth;

// LCD Setup
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Pin Assignments
const int buzzerPin = D5;
const int gasAnalog = A0;
const int gasDigital = D4;
const int vibrationPin = D3;
const int flamePin = D6;

// Threshold Values
const int GAS_THRESHOLD = 300;
const int BUZZER_DURATION = 1000;

// Function to beep buzzer
void beepBuzzer(int duration) {
  digitalWrite(buzzerPin, HIGH);
  delay(duration);
  digitalWrite(buzzerPin, LOW);
  delay(200);
}

void setup() {
  Serial.begin(115200);

  // Initialize WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nWiFi Connected!");

  // Set Firebase credentials
  config.host = FIREBASE_HOST;
  config.signer.tokens.legacy_token = FIREBASE_AUTH;

  // Initialize Firebase
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  // Pin Modes
  pinMode(buzzerPin, OUTPUT);
  pinMode(gasDigital, INPUT);
  pinMode(vibrationPin, INPUT_PULLUP);
  pinMode(flamePin, INPUT_PULLUP);
  digitalWrite(buzzerPin, LOW);

  // LCD Setup
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(".....ResQNet......");
  delay(2000);
  //lcd.clear();
}

void loop() {
  int gasSensorAnalog = analogRead(gasAnalog);
  int gasSensorDigital = digitalRead(gasDigital);
  int vibrationState = digitalRead(vibrationPin);
  int flameState = digitalRead(flamePin);

  // Display real-time gas sensor reading
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Gas Level: ");
  lcd.print(gasSensorAnalog);

  Serial.print("Gas Level: ");
  Serial.print(gasSensorAnalog);
  Serial.print("\tVibration: ");
  Serial.print(vibrationState);
  Serial.print("\tFlame: ");
  Serial.println(flameState);

  // Send sensor data to Firebase
  Firebase.setInt(firebaseData, "/sensorData/smokeLevel", gasSensorAnalog);
  Firebase.setBool(firebaseData, "/sensorData/flameDetected", flameState == LOW);
  Firebase.setBool(firebaseData, "/sensorData/vibration", vibrationState == LOW);
  Firebase.setInt(firebaseData, "/sensorData/timestamp", millis());

  // Check for alerts
  if (gasSensorAnalog > GAS_THRESHOLD) {
    Serial.println("⚠ Smoke Detected!");
    lcd.setCursor(0, 1);
    lcd.print("Smoke Alert!");
    beepBuzzer(BUZZER_DURATION);
  }

  if (vibrationState == LOW) {
    Serial.println("⚠ Earthquake Detected!");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Earthquake Alert!");
    beepBuzzer(BUZZER_DURATION);
  }

  if (flameState == LOW) {
    Serial.println("⚠ Fire Detected!");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Fire Alert!");
    beepBuzzer(BUZZER_DURATION);
  }

delay(500);
}