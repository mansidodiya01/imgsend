#include <SPI.h>
#include <LoRa.h>

#define SS 10    // LoRa module NSS pin
#define RST 9    // LoRa module RESET pin
#define DIO0 2   // LoRa module DIO0 pin

void setup() {
    Serial.begin(115200);  // Communication with Raspberry Pi
    while (!Serial);

    LoRa.setPins(SS, RST, DIO0);
    if (!LoRa.begin(433E6)) {  // Set LoRa frequency to 433 MHz
        Serial.println("LoRa initialization failed!");
        while (1);
    }
    Serial.println("LoRa initialized.");
}

void loop() {
    if (Serial.available()) {
        // Read text from Raspberry Pi
        String text = Serial.readStringUntil('\n');

        // Send text via LoRa
        LoRa.beginPacket();
        LoRa.print(text);
        LoRa.endPacket();

        Serial.println("Sent via LoRa: " + text);
    }
}
