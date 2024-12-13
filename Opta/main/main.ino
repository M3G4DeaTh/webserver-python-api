/**
  Opta USB data logging and API sending
  Name: main.ino

  @author Keven Marques
  @version 2.1 10/11/24
*/

#include "Arduino_UnifiedStorage.h"
#include <WiFi.h>
#include "arduino_secrets.h"
#include "http.h"
#include <Arduino.h>

// Constants for analog input pins and LED pins
const int analog_pins[] = { A0, A1, A2, A3 };
const int led_pins[] = { LED_D0, LED_D1, LED_D2, LED_D3 };

// Standard Wifi SSid and password
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

// Define constants for voltage, resolution, and divider.
const float VOLTAGE_MAX   = 6.0;      // Maximum voltage that can be read
const float RESOLUTION    = 4095.0;   // 12-bit resolution
const float DIVIDER       = 0.3;      // Voltage divider

//New password and SSID
String data = "olamundo";
String ssidU, passwordU;

//Wifi initializer
int status = WL_IDLE_STATUS;
bool changeWifi = true;
WiFiClient wifi;

// Sensor variables
float inputs[4];
const byte inputPins[] = { A0, A1, A2, A3 };
int r = 0;
int i = 0;
int a = 0;
int standard = 0.04;
int result = 0;
bool err = false;

// Timing control variables
unsigned long previousMillis = 0;
const long interval = 1000;

// Knight Rider LED pattern variables
int ledDirection = 1;
int currentLed = 0;

// USB storage and folder instances
USBStorage usbStorage;
Folder backupFolder = Folder();
Folder wifiFolder = Folder();
Folder standardFolder = Folder();
// Folder hostFolder = Folder();
bool usbIntialized = false;
volatile bool usbAvailable = false;

/**
  Function to handle USB connection callback.
  Sets the USB available flag and removes the connection callback.

  @param none
  @return none
*/
void connectionCallback() {
    usbAvailable = true;
    Arduino_UnifiedStorage::debugPrint("- USB device connected!");
    usbStorage.removeOnConnectCallback();
}

/**
  Function to handle USB disconnection callback.
  Resets the USB available flag and reinstalls the connection callback.

  @param none
  @return none
*/
void disconnectionCallback() {
    usbAvailable = false;
    Arduino_UnifiedStorage::debugPrint("- USB device disconnected!");
    usbStorage.onConnect(connectionCallback);
}

/**
  Function to handle Knight Rider LED pattern.
  Displays a LED sequence on Opta's user LEDs to indicate waiting for USB connection.

  @param none
  @return none
*/
void knightRiderPattern() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(led_pins[i], LOW);
  }

  digitalWrite(led_pins[currentLed], HIGH);
  delay(100);
  currentLed += ledDirection;

  if (currentLed == 3) {
    ledDirection = -1;
  } else if (currentLed == 0) {
    ledDirection = 1;
  } 
}


/**
  Function to blink all user LEDs a specified number of times.
  Indicates the start or end of a process like data logging.

  @param times Number of times to blink the LEDs
  @return none
*/
void blinkAllLeds(int times) {
  for (int i = 0; i < times; i++) {
    for (int j = 0; j < 4; j++) {
      digitalWrite(led_pins[j], HIGH);
    }
    delay(500);
    for (int j = 0; j < 4; j++) {
      digitalWrite(led_pins[j], LOW);
    }
    delay(500);
  }
}

/**
  Function to handle the writing of data to USB storage.
  Manages USB initialization, mounting, and writing of sensor data to file.

  @param none
  @return none
*/
void writeToUSB() {
  if (usbAvailable && !usbIntialized) {
    usbStorage.begin();
    Folder usbRoot = usbStorage.getRootFolder();
    String folderName = "backup_data";
    String folderWifi = "wifi_data";
    String folderStandard = "standard_data";
    // String folderHost = "host_data";
    backupFolder = usbRoot.createSubfolder(folderName);
    wifiFolder = usbRoot.createSubfolder(folderWifi);
    standardFolder = usbRoot.createSubfolder(folderStandard);
    // hostFolder = usbRoot.createSubfolder(folderHost);
    Arduino_UnifiedStorage::debugPrint("- Backup folder created: " + backupFolder.getPathAsString());
    Arduino_UnifiedStorage::debugPrint("- Wifi folder created: " + wifiFolder.getPathAsString());
    Arduino_UnifiedStorage::debugPrint("- Standard folder created: " + standardFolder.getPathAsString());
    // Arduino_UnifiedStorage::debugPrint("- Host folder created: " + hostFolder.getPathAsString());
    usbStorage.unmount();
    usbIntialized = true;
  } else if (usbAvailable && usbIntialized) {
    if (!usbStorage.isMounted()) {
      if (usbStorage.begin()) {
        if (changeWifi){
          wifiUpdate();
        }
        standardUpdate();
        performUpdate();
      }
    } else if (usbStorage.isMounted()) {
      if (changeWifi){
        wifiUpdate();
      }
      standardUpdate();
      performUpdate();
    }
  }
}

/**
  Function to perform data update on USB storage.
  Writes analog sensor data in a formatted string to a text file.

  @param none
  @return none
*/
void performUpdate() {
  UFile backupFile = backupFolder.createFile("analog_inputs_data.txt", FileMode::APPEND);
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    String buffer = "";
    for (int i = 0; i < 4; i++) {
      int value = analogRead(analog_pins[i]);

      // Convert the terminal value to its corresponding voltage. 
      float voltage = value * (VOLTAGE_MAX / RESOLUTION);
      if (i > 0) {
        buffer += "; ";
      }
      buffer += "A" + String(i) + ": " + String(voltage);
    }
    buffer += "\n";
    backupFile.write(buffer);
    Arduino_UnifiedStorage::debugPrint("- Data written to file: " + buffer);
  }
  backupFile.close();
  usbStorage.unmount();
  Arduino_UnifiedStorage::debugPrint("- File closed and USB storage unmounted!");
}

/**
  Function to check if all the sensor's pressured.
  Read the sensor's info send it to the API and checking if matches the pressure value.

  @param none
  @return none
*/
void sensorsCheck(int standard){
  // converting the value and checking if its not in the max or minimum resolution
  for (i = 0; i < 4; i++) {
    if (analogRead(inputPins[i]) > 4 && analogRead(inputPins[i]) <= 4095) {
      inputs[i] = analogRead(inputPins[i]) * (VOLTAGE_MAX / RESOLUTION);
    } else if (analogRead(inputPins[i]) <= 4) {
      r = r + 1;
      inputs[i] = 0;
    } else if (analogRead(inputPins[i]) > 4095) {
      r = r + 1;
      inputs[i] = 100;
    }
  }
  if (r < 2) {
    // check if wifi is connected to send data to API
    if (WiFi.status() == WL_CONNECTED){
      int result = httpT(wifi, inputs);
    }
    else{
      int result = -1;
    }
    // standard pressure
    // checking if is the same that API
    if (result == r){
      // checking all the 4 sensors
      for (i = 0; i < 4; i++) {
        if (inputs[i] > standard) {
          a = a + 1;
          Serial.println(inputs[i]);
        }
      }
      if (a > 2) {
        digitalWrite(D0, HIGH);
        digitalWrite(D1, LOW);
      } else {
        digitalWrite(D0, LOW);
        digitalWrite(D1, HIGH);
      }
    } 
    // if the API was not found
    else if (result == -1) {
      // checking all the 4 sensors
      for (i = 0; i < 4; i++) {
        if (inputs[i] > standard) {
          Serial.println(inputs[i]);
          a = a + 1;
        }
      }
      if (a > 2) {
        digitalWrite(D0, HIGH);
        digitalWrite(D1, LOW);
      } else {
        digitalWrite(D0, LOW);
        digitalWrite(D1, HIGH);
      }
    } 
    // if was founded then the CLP will use the API standard
    else {
      // checking all the 4 sensors
      for (i = 0; i < 4; i++) {
        if (inputs[i] > result) {
          a = a + 1;
        }
      }
      if (a > 2) {
        digitalWrite(D0, HIGH);
        digitalWrite(D1, LOW);
      } else {
        digitalWrite(D0, LOW);
        digitalWrite(D1, HIGH);
      }
    }

  } else {
    digitalWrite(D0, LOW);
    digitalWrite(D1, HIGH);
  }
  r = 0;
  a = 0;
}


/**
  Function to perform wifi update on USB storage.
  Read wifi data in a formatted string inside the text file.

  @param none
  @return none
*/
void wifiUpdate() {
  UFile wifiFile = wifiFolder.createFile("wifi_config.txt", FileMode::READ);
  data = wifiFile.readAsString();
  String NewData = String(data);
  int delimiterIndex = NewData.indexOf(':');

  if (delimiterIndex > 0) {
    ssidU = NewData.substring(0, delimiterIndex);
    passwordU = NewData.substring(delimiterIndex + 1);
    if (ssidU != ssid || password != passwordU) {
      Serial.println("SSID diferente! Mudando Wi-Fi...");
      // wifi disconnect
      WiFi.disconnect();
      delay(1000);

      // Connecting to a new wifi connection
      WiFi.begin(ssidU.c_str(), passwordU.c_str());

      // Wifi'status verify
      Serial.print("Conectando ao novo Wi-Fi");
      int attempts = 0;
      while (WiFi.status() != WL_CONNECTED && attempts < 5) {
        delay(500);
        Serial.print(".");
        attempts++;
      }
      if (WiFi.status() == WL_CONNECTED){
        digitalWrite(D0, HIGH);
      }
    }
  }
  Arduino_UnifiedStorage::debugPrint("- Data written to file: ");
  
  wifiFile.close();
  usbStorage.unmount();
  Arduino_UnifiedStorage::debugPrint("- File closed and USB storage unmounted!");
}

/**
  Function to perform standard update on USB storage.
  Read standard data in a formatted string inside the text file.

  @param none
  @return none
*/
void standardUpdate() {
  UFile standardFile = standardFolder.createFile("standard_config.txt", FileMode::READ);
  data = standardFile.readAsString();
  String NewData = String(data);
  
  int standardUpdated = NewData.toInt();
  if (standardUpdated > 0){
    sensorsCheck(standardUpdated);
  }
  else{
    sensorsCheck(standard);
  }
  Arduino_UnifiedStorage::debugPrint("- Data written to file: ");
  
  standardFile.close();
  usbStorage.unmount();
  Arduino_UnifiedStorage::debugPrint("- File closed and USB storage unmounted!");
}


// Board initialization 
void setup() {
  //changewifi mode
  bool changewifi = false;
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 5) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  pinMode(D0, OUTPUT);
  pinMode(D1, OUTPUT);
  Serial.begin(115200); 
  Arduino_UnifiedStorage::debuggingModeEnabled = false;
  analogReadResolution(12);

  usbStorage = USBStorage();
  usbStorage.onConnect(connectionCallback);
  usbStorage.onDisconnect(disconnectionCallback);

  for (int i = 0; i < 4; i++) {
    pinMode(led_pins[i], OUTPUT);
    digitalWrite(led_pins[i], LOW);
  }

  pinMode(BTN_USER, INPUT_PULLUP);
  Arduino_UnifiedStorage::debugPrint("- Setup complete!");
}

// Main loop
void loop() {
  static bool dataLoggingStarted = false;

  if (usbAvailable && !dataLoggingStarted) {
    knightRiderPattern();
    dataLoggingStarted = true;
    // Turn off all the user LEDs
    for (int i = 0; i < 4; i++) {
      pinMode(led_pins[i], OUTPUT);
      digitalWrite(led_pins[i], LOW);
    }
    // Turn on LED_D0 for data logging indication
    digitalWrite(led_pins[0], HIGH); 
    Arduino_UnifiedStorage::debugPrint("- Data logging started!");
  }
  if (dataLoggingStarted) {
    writeToUSB();

    // Toggle LED_D0
    digitalWrite(led_pins[0], digitalRead(led_pins[0]) == LOW); 

  }
  if (!usbAvailable){
    sensorsCheck(standard);
  }
  
}