#include <FlashIAPBlockDevice.h>
#include "FlashIAPLimits.h"

using namespace mbed;

FlashIAPBlockDevice *blockDevice;

const int SENTINEL_VALUE = 0xDEADBEEF; // Valor sentinela conhecido

struct FlashData {
  int sentinel;
  int count;
  int count2;
  int count3;
};

void saveDataToFlash(FlashData data) {
  blockDevice->init();
  const auto eraseBlockSize = blockDevice->get_erase_size();
  const auto programBlockSize = blockDevice->get_program_size();
  const auto dataSize = programBlockSize;

  blockDevice->erase(0, eraseBlockSize);
  blockDevice->program(&data, 0, dataSize);
  blockDevice->deinit();
}

FlashData readDataFromFlash() {
  blockDevice->init();
  FlashData data = {0, 0, 0, 'nothing'};
  blockDevice->read(&data, 0, sizeof(data));
  blockDevice->deinit();

  if (data.sentinel == SENTINEL_VALUE) {
    return data;
  } else {
    return {SENTINEL_VALUE, 0, 100, 200}; // Valores padrão se a memória não foi inicializada corretamente
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("FlashIAPBlockDevice Test");
  Serial.println("------------------------");

  // Obtém os limites da flash interna do microcontrolador
  auto [flashSize, startAddress, iapSize] = getFlashIAPLimits();

  Serial.print("Flash Size: ");
  Serial.print(flashSize / 1024.0 / 1024.0);
  Serial.println(" MB");
  Serial.print("FlashIAP Start Address: 0x");
  Serial.println(startAddress, HEX);
  Serial.print("FlashIAP Size: ");
  Serial.print(iapSize / 1024.0 / 1024.0);
  Serial.println(" MB");

  // Cria um dispositivo de bloco no espaço disponível da flash
  blockDevice = new FlashIAPBlockDevice(startAddress, iapSize);

  // Lê os dados armazenados na memória Flash
  FlashData data = readDataFromFlash();
  Serial.println("Iniciando contagem a partir de: " + String(data.count));
  Serial.println("Iniciando contagem2 a partir de: " + String(data.count2));
  Serial.println("Iniciando contagem3 a partir de: " + String(data.count3));
}

void loop() {
  delay(2000);

  // Incrementa as contagens
  FlashData data = readDataFromFlash();
  data.count++;
  data.count2++;
  data.count3++;

  Serial.println("Contagem: " + String(data.count));
  Serial.println("Contagem2: " + String(data.count2));
  Serial.println("Contagem3: " + String(data.count3));

  saveDataToFlash(data);
}