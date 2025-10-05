#include <Stepper.h>
const int stepsPerRevolution = 2048;

// Try one of the following lines — test one, then switch if needed
Stepper myStepper(stepsPerRevolution, 8, 6, 7, 5);
// Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);
// Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {
  myStepper.setSpeed(10);
}

void loop() {
  myStepper.step(stepsPerRevolution / 4);   // 90° CW
  delay(1000);
  myStepper.step(-stepsPerRevolution / 4);  // 90° CCW
  delay(1000);
}
