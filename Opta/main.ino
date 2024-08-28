/*

  created 28 Oct 2024
  by Keven Marques
  
  
  
*/

#include <Arduino.h>
#include <WiFi101.h>
#include "arduinoSecrets.h"
#include "Http.h"
#include "opta_info.h"
 
OptaBoardInfo *info;
OptaBoardInfo *boardInfo();
WiFiClient wifi;
Http http;

int status = WL_IDLE_STATUS;
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

int inputs[4];
const byte inputPins[] = {A0, A1, A2, A3};

void setup() {
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  Serial.begin(9600);
  info = boardInfo();

  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);                   // print the network name (SSID);

    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, password);
  }
  
}

void loop() {
  for (i = 0; i <4; i++){
    if (digitalRead(inputPins[i])){
      
      inputs[i] = 1;
    }
    else if (!digitalRead(inputPins[i])){
      
      inputs[i] = 0;
    }
  }
  
  result = http.httpT(wifi, inputs);
  if (result == 0)
  {
    // String response = httpClient.responseBody();
    // Serial.println(response);
    Serial.println("success!");
  }
  else
  {
    Serial.println("fail!");
  }
  delay(500); // Ping every 5s.
}