/*

  created 28 Aug 2024
  by Keven Marques
  
  
  
*/

#include <Arduino.h>
#include <Ethernet.h>
#include "arduino_secrets.h"
#include "http.h"

#include "opta_info.h"



OptaBoardInfo *info;
OptaBoardInfo *boardInfo();
EthernetClient ethernetClient;


// int status = WL_IDLE_STATUS;
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

float inputs[4];
const byte inputPins[] = {A0, A1, A2, A3};
int r = 0;
int i = 0;
int a = 0;
bool err = false;

int standard = 4;
const float VOLTAGE_MAX = 12;
const float RESOLUTION = 4095.0;

void setup() {
  analogReadResolution(12);
  pinMode(D0, OUTPUT);
  pinMode(D1, OUTPUT);
  Serial.begin(9600);
  info = boardInfo();
  if (info->magic = 0xB5)
  {
    // Attempt DHCP lease.
    if (Ethernet.begin(info->mac_address) == 0)
    {
      err = true;
    }
  }
  else
  {
    err = true;
  }

  // while ( status != WL_CONNECTED) {
  //   Serial.print("Attempting to connect to Network named: ");
  //   Serial.println(ssid);                   // print the network name (SSID);

  //   // Connect to WPA/WPA2 network:
  //   status = WiFi.begin(ssid, password);
  // }
  
}

void loop() {
  
  for (i = 0; i < 4; i++){
    if (analogRead(inputPins[i]) > 4 && analogRead(inputPins[i]) <= 3412){
      inputs[i] = analogRead(inputPins[i]) * (VOLTAGE_MAX/RESOLUTION);
    }
    else if (analogRead(inputPins[i]) <= 4){
      r = r+1;
      inputs[i] = 0;
    }else if (analogRead(inputPins[i]) > 3412){
      r = r+1;
      inputs[i] = 100;
    }
  }
  if (r <  2){
    int result = httpT(ethernetClient, inputs, standard);
    Serial.println(r);
    if (result == standard)
    {
      digitalWrite(LED_BUILTIN, HIGH);
      for (i = 0; i < 4; i++){
        if (inputs[i] > standard){
          a = a+1;
        }
      }
      if (a == 4){
        digitalWrite(D0, HIGH);
        digitalWrite(D1, LOW);
      }
      else{                         
        digitalWrite(D0, LOW);
        digitalWrite(D1, HIGH);
      }
      Serial.println("success!");
    }
    else if (result == -1)
    {
      
      digitalWrite(LED_BUILTIN, LOW);
      for (i = 0; i < 4; i++){
        if (inputs[i] > standard){
          a = a+1;
        }
      }
      if (a == 4){
        digitalWrite(D0, HIGH);
        digitalWrite(D1, LOW);
      }
      else{                         
        digitalWrite(D0, LOW);
        digitalWrite(D1, HIGH);
      }
      
      Serial.println("fail!");
    }
    else{
      standard = result;
      digitalWrite(LED_BUILTIN, HIGH);
      for (i = 0; i < 4; i++){
        if (inputs[i] > standard){
          a = a+1;
        }
      }
      if (a == 4){
        digitalWrite(D0, HIGH);
        digitalWrite(D1, LOW);
      }
      else{                         
        digitalWrite(D0, LOW);
        digitalWrite(D1, HIGH);
      }
      // String response = httpClient.responseBody();
      // Serial.println(response);
      Serial.println("success!");
    }
    
  }
  else{
    digitalWrite(D0, LOW);
    digitalWrite(D1, HIGH);
  }
  r = 0;
  a = 0;
  delay(1000); // Ping every 5s.
}