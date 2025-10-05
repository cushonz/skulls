#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Stepper.h>

#define CE_PIN 9
#define CSN_PIN 10
//#define width 106.68 // cm
#define width 25.4
float currAngle = 0;

RF24 radio(CE_PIN, CSN_PIN);

const byte address[6] = "00001";

#define LED_PIN 13  // Built-in LED

const int stepsPerRevolution = 2048;
Stepper myStepper(stepsPerRevolution, 8, 6, 7, 5);

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

void commandStepper(int degrees){
  int steps = (stepsPerRevolution / 360) * degrees; // Convert degrees to steps
  myStepper.step(steps);
}

float calculateAngle(float distance){
  float angle = atan(distance/(width/2)); // Calculate angle in radian
  angle = angle * (180.0 / 3.14159); // Convert to degrees
  return angle;
}

void loop() {
  if (radio.available()) {
    char text[32] = {0};
    radio.read(&text, sizeof(text));  // Read incoming message

    float distance = atof(text);      // Convert received string to float
    float degrees = calculateAngle(distance);

    float angleDiff = degrees - currAngle;

    if (abs(angleDiff) > 1) {  // Add a small threshold to avoid jitter
      commandStepper(angleDiff);  
      currAngle = degrees;       // Update the *absolute* current angle
    }

    Serial.print("Received: ");
    Serial.println(text);
    Serial.print("Target angle: ");
    Serial.println(degrees);
  }
}
