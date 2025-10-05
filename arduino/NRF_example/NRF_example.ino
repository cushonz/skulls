#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Stepper.h>

#define CE_PIN 9
#define CSN_PIN 10

RF24 radio(CE_PIN, CSN_PIN);

const byte address[6] = "00001";

#define LED_PIN 13  // Built-in LED

const int stepsPerRevolution = 2048;
Stepper myStepper(stepsPerRevolution, 8, 7, 6, 5);

void setup() {
    myStepper.setSpeed(10);
  pinMode(LED_PIN, OUTPUT);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_LOW);
  radio.startListening();

  Serial.begin(9600);  // Optional: for debugging
  Serial.println("Receiver ready...");
}

void loop() {
  if (radio.available()) {
    char text[32] = {0};
    radio.read(&text, sizeof(text));  // Read incoming message

    float distance = atof(text);  // Convert received string to float
    float arc = 7; // hard code actual dist from center of walk way
    arctan(distance/arc);

    Serial.print("Received: ");
    Serial.println(text);  // Optional: print received message
    Serial.println("Distance: " + String(distance) + "+5=" + String(distance + 5));  // Print distance and scaled value

  }
}
