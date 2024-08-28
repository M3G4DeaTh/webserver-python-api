
#include <ArduinoHttpClient.h>
#include <WiFi101.h>
#include "arduinoSecrets.h"

WiFiClient wifi;
int httpT(WiFiClient wifi, int array[]){
    HttpClient httpClient = HttpClient(wifi, SECRET_HOST, 5000); // IP address and port of the HTTP server.

    int result = httpClient.post("/api/Machines/Receive", "application/json", "["+(String) array[0]+","+(String) array[0]+","+(String) array[0]+","+(String) array[0]+"]");
    return result;
}
