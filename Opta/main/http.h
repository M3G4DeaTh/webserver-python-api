
#include <ArduinoHttpClient.h>
#include <WiFi.h>
#include "arduino_secrets.h"
int statusCode = 404;
String response = "Connection Refused";
int httpT(WiFiClient wifi, float array[]){
  HttpClient client = HttpClient(wifi, SECRET_HOST, 5000); // IP address and port of the HTTP server.
  String payload = "["+(String) array[0]+","+(String) array[1]+","+(String) array[2]+","+(String) array[3]+"]";
  int payloadLength = payload.length();
  // int result = client.post("/api/Machines/Receive", "Content-Type" : "application/json", "["+(String) array[0]+","+(String) array[0]+","+(String) array[0]+","+(String) array[0]+"]");
  if(client.available() and statusCode == 1){ //Change when the Host is ready
    client.beginRequest();
    client.post("/api/Machines/Receive");
    client.sendHeader("Content-Type", "application/json");
    client.sendHeader("Content-Length", payloadLength);
    client.sendHeader("tag", SECRET_TAG);
    client.sendHeader("password", SECRET_KEY);
    client.beginBody();
    client.print(payload);
    client.endRequest();
    int statusCode = client.responseStatusCode();
    String response = client.responseBody();
    if (statusCode == 200){
      return response.toInt();
    }
    else{
      return -1;
    }
  }else{
    return -1;
  }
  
  
  int i = 0;
  
}
