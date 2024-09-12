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

float inputs[4];
const byte inputPins[] = {A0, A1, A2, A3};
int r = 0;
void setup() {
  analogReadResolution(12);
  pinMode(D0, OUTPUT);
  pinMode(D1, OUTPUT);
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
  for (i = 0; i < 4; i++){
    if (analogRead(inputPins[i]) > 0){
      
      inputs[i] = analogRead(inputPins[i]);
    }
    else if (analogRead(inputPins[i]) < 0){
      r = r+1;
      inputs[i] = 0;
    }
  }
  if (r < 4){
    result = http.httpT(wifi, inputs);
    if (result == 0)
    {
      digitalWrite(D0, HIGH);
      digitalWrite(D1, LOW);
      // String response = httpClient.responseBody();
      // Serial.println(response);
      Serial.println("success!");
    }
    else
    {
      digitalWrite(D0, LOW);
      digitalWrite(D1, HIGH);
      Serial.println("fail!");
    }
  }
  r = 0;
  delay(500); // Ping every 5s.
}