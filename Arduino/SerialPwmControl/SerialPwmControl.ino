
#include <Servo.h>

#define MAX_PULSE 2000
#define MIN_PULSE 1000
#define OFF_PULSE 1500

byte motorVals[4];

//        FR
int m[] = {3, 5, 6, 9};
Servo motors[4];

void setup() {

  Serial.begin(9600);

        Serial.println("HERE");

  for (int i = 0; i <= 3; i++) {
    motors[i].attach(m[i], MIN_PULSE, MAX_PULSE);
  }
}

void loop() {

  if (Serial.available() > 0) {

    Serial.readBytes(motorVals, 4);

    while (Serial.available() > 0) {
      Serial.read();
    }

    for (int i = 0; i <= 3; i++) {
//        Serial.print(i);
//        Serial.print(" ");
//        Serial.print(motorVals[i]);
//        Serial.print(" ");
        motors[i].writeMicroseconds(convertToPulse(motorVals[i]));
    }
    Serial.println();
  }
}

int convertToPulse(byte in) {
  return map(in, 0, 255, 1000, 2000);
}

