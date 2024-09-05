
#include <ArduinoHttpClient.h>
#include <WiFi101.h>
#include "arduinoSecrets.h"

WiFiClient wifi;
int httpT(WiFiClient wifi, int array[]){
    HttpClient client = HttpClient(wifi, SECRET_HOST, 5000); // IP address and port of the HTTP server.
    String postData = "["+(String) array[0]+","+(String) array[0]+","+(String) array[0]+","+(String) array[0]+"]"
    // int result = client.post("/api/Machines/Receive", "Content-Type" : "application/json", "["+(String) array[0]+","+(String) array[0]+","+(String) array[0]+","+(String) array[0]+"]");
    client.beginRequest();
    client.post("/api/Machines/Receive");
    client.sendHeader("Content-Type", "application/json");
    client.sendHeader("tag", SECRET_TAG);
    client.sendHeader("password", SECRET_KEY);
    client.beginBody();
    client.print(postData);
    client.endRequest();
    int statusCode = client.responseStatusCode();
    return statusCode;
}
