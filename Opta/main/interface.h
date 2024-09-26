#include <WiFi.h> // Ou <ESP8266WiFi.h> se estiver usando ESP8266
#include <WebServer.h>

const char* ssid = "Seu_SSID"; // SSID inicial
const char* password = "Sua_Senha"; // Senha inicial

WebServer server(80); // Cria o servidor na porta 80

void handleRoot() {
  String html = "<html><body><h1>Configuração Wi-Fi</h1>"
                "<form action=\"/setwifi\" method=\"POST\">"
                "SSID: <input type=\"text\" name=\"ssid\"><br>"
                "Senha: <input type=\"password\" name=\"password\"><br>"
                "<input type=\"submit\" value=\"Conectar\">"
                "</form></body></html>";
  server.send(200, "text/html", html);
}

void handleSetWiFi() {
  String newSSID = server.arg("ssid");
  String newPassword = server.arg("password");

  // Salvar as novas credenciais e tentar conectar
  WiFi.disconnect();
  WiFi.begin(newSSID.c_str(), newPassword.c_str());

  // Aguarda a conexão
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    server.send(200, "text/html", "Conectado! IP: " + WiFi.localIP().toString());
  } else {
    server.send(200, "text/html", "Falha ao conectar. Você pode tentar novamente.");
  }
}

void setup() {
  Serial.begin(115200);
  
  // Tenta conectar à rede Wi-Fi inicial
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Conectado!");
  } else {
    Serial.println("Falha ao conectar. Iniciando Access Point...");
    
    // Inicia o modo Access Point
    WiFi.softAP("ESP_AcessPoint", "senhaAP"); // Nome e senha do AP
    Serial.print("Access Point criado: ");
    Serial.println(WiFi.softAPIP()); // IP do AP
  }

  // Configura o servidor
  server.on("/", handleRoot);
  server.on("/setwifi", HTTP_POST, handleSetWiFi);
  server.begin();
}

void loop() {
  server.handleClient();
}
