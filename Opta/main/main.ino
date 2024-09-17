/*

  created 28 Aug 2024
  by Keven Marques
  
  
  
*/

#include <Arduino.h>
#include <WiFi.h>
#include "arduino_secrets.h"
#include "http.h"
#include "opta_info.h"



OptaBoardInfo *info;
OptaBoardInfo *boardInfo();
WiFiClient wifi;


int status = WL_IDLE_STATUS;
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

float inputs[4];
const byte inputPins[] = {A0, A1, A2, A3};
int r = 0;
int i = 0;
int a = 0;

const float standard = 12;
const float VOLTAGE_MAX = 12;
const float RESOLUTION = 4095.0;

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
    if (analogRead(inputPins[i]) > 0 && analogRead(inputPins[i]) < 3412){
      inputs[i] = analogRead(inputPins[i]) * (VOLTAGE_MAX/RESOLUTION);
    }
    else if (analogRead(inputPins[i]) < 0){
      r = r+1;
      inputs[i] = 0;
    }else{
      r = r+1;
      inputs[i] = 100;
    }
  }
  if (r < 4){
    int result = 1;
    Serial.println(httpT(wifi, inputs));
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
      Serial.println('ola mununndo');
    //   for (i = 0; i < 4; i++){
    //     if (inputs[i] > standard){
    //       a = a+1;
    //     }
    //   }
    //   if (a == 4){
    //     digitalWrite(D0, HIGH);
    //     digitalWrite(D1, LOW);
    //   }
    //   else{
    //     digitalWrite(D0, LOW);
    //     digitalWrite(D1, HIGH);
    //   }
      
    //   Serial.println("fail!");
    }
  }
  r = 0;
  a = 0;
  delay(500); // Ping every 5s.
}