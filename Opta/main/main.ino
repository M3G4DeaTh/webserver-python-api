

/*

  created 28 Aug 2024
  by Keven Marques
  
  
  
*/
#include <Arduino.h>
#include <WiFi.h>
#include "arduino_secrets.h"
#include "http.h"
#include <Arduino_UnifiedStorage.h>
#include "opta_info.h"


OptaBoardInfo *info;
OptaBoardInfo *boardInfo();
WiFiClient wifi;
USBStorage storage;            // Create an instance for interacting with USB storage

int status = WL_IDLE_STATUS;
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

float inputs[4];
const byte inputPins[] = { A0, A1, A2, A3 };
int r = 0;
int i = 0;
int a = 0;
int re = 6;
bool err = false;

const float VOLTAGE_MAX = 6;
const float RESOLUTION = 4095.0;

// Caminho do arquivo no USB
const char* wifi_config_file = "/wifi_config.txt";

// Função para ler o SSID e a senha do arquivo de configuração no armazenamento USB
bool readWifiConfig(String &ssidU, String &passwordU) {
  // Inicializa o USBStorage
  if (!storage.begin()) {
    Serial.println("Falha ao inicializar o armazenamento USB.");
    return false;
  }

  Folder dir = storage.getRootFolder();
  std::vector<UFile> files = dir.getFiles();
  // Abre o arquivo para leitura
  UFile file = file.getPath();
  file.seek(0);
  char data;
  // Ler as primeiras linhas do arquivo (espera-se que contenha "SSID:SENHA")
  while (file.available()) {
    data = file.read();
    Serial.write(data);
  }
  String NewData = String(data);
  int delimiterIndex = NewData.indexOf(':');

  if (delimiterIndex > 0) {
    ssidU = NewData.substring(0, delimiterIndex);
    passwordU = NewData.substring(delimiterIndex + 1);
    file.close();
    return true;
  } else {
    Serial.println("Formato inválido no arquivo de configuração.");
    file.close();
    return false;
  }
}

void setup() {
  analogReadResolution(12);
  pinMode(D0, OUTPUT);
  pinMode(D1, OUTPUT);
  Serial.begin(9600);
  info = boardInfo();

  // if (info->magic = 0xB5)
  // {
  //   // Attempt DHCP lease.
  //   Ethernet.begin(info->mac_address, ip)
  // }
  // else
  // {
  //   err = true;
  // }
  if (info->magic = 0xB5) {
    WiFi.begin(ssid, password);
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
      delay(500);
      Serial.print(".");
      attempts++;
    }

    // Variáveis para armazenar SSID e senha lidos do armazenamento
    String ssidU, passwordU;

    // Ler a configuração do arquivo no armazenamento
    if (readWifiConfig(ssidU, passwordU)) {
      // Verifica se o SSID no arquivo é diferente do SSID pré-configurado
      if (ssidU != ssid) {
        Serial.println("SSID diferente! Mudando Wi-Fi...");
        digitalWrite(LED_BUILTIN, HIGH);
        digitalWrite(LED_BUILTIN, LOW);
        // Desconecta do Wi-Fi atual
        WiFi.disconnect();
        delay(1000);

        // Conecta ao novo Wi-Fi
        WiFi.begin(ssidU.c_str(), passwordU.c_str());

        // Verifica o status da nova conexão
        Serial.print("Conectando ao novo Wi-Fi");
        int attempts = 0;
        while (WiFi.status() != WL_CONNECTED && attempts < 20) {
          delay(500);
          Serial.print(".");
          attempts++;
        }
        Serial.println("\nConectado ao novo Wi-Fi!");
      } else {
        digitalWrite(LED_BUILTIN, HIGH);
        Serial.println("SSID é o mesmo, nenhuma alteração necessária.");
      }
    } else {
      Serial.println("Erro ao ler a configuração de Wi-Fi.");
    }
   
  } else {
    err = true;
  }
}

void loop() {

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
    int result = httpT(wifi, inputs);
    Serial.println(r);
    re = 2;
    if (result == re) {
      digitalWrite(LED_BUILTIN, HIGH);
      for (i = 0; i < 4; i++) {
        if (inputs[i] > re) {
          a = a + 1;
        }
      }
      if (a == 4) {
        digitalWrite(D0, HIGH);
        digitalWrite(D1, LOW);
      } else {
        digitalWrite(D0, LOW);
        digitalWrite(D1, HIGH);
      }
      Serial.println("success!");
    } else if (result == -1) {

      digitalWrite(LED_BUILTIN, LOW);
      for (i = 0; i < 4; i++) {
        if (inputs[i] > re) {
          a = a + 1;
        }
      }
      if (a == 4) {
        digitalWrite(D0, HIGH);
        digitalWrite(D1, LOW);
      } else {
        digitalWrite(D0, LOW);
        digitalWrite(D1, HIGH);
      }

      Serial.println("fail!");
    } else {
      
      digitalWrite(LED_BUILTIN, HIGH);
      for (i = 0; i < 4; i++) {
        if (inputs[i] > result) {
          a = a + 1;
        }
      }
      if (a == 4) {
        digitalWrite(D0, HIGH);
        digitalWrite(D1, LOW);
      } else {
        digitalWrite(D0, LOW);
        digitalWrite(D1, HIGH);
      }
      // String response = httpClient.responseBody();
      // Serial.println(response);
      Serial.println("success!");
    }

  } else {
    digitalWrite(D0, LOW);
    digitalWrite(D1, HIGH);
  }
  r = 0;
  a = 0;
  delay(1000);  // Ping every 5s.
}

