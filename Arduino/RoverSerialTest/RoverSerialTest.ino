
#include <Servo.h>

#define MAX_PULSE 2000
#define MIN_PULSE 1000
#define OFF_PULSE 1500

//union MotorOutput{
//byte tempBytes[4];
////int tempInts[4];
//};

//union MotorOutput motorVals;
byte motorVals[4];
//        FR
int m[] = {3, 5, 6, 9};
Servo motors[4];

byte message = 0;

Servo motor;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //  TCCR0B = TCCR0B & B11111000 | B00000100;
  //  TCCR1B = TCCR1B & B11111000 | B00000100;
  //  TCCR2B = TCCR2B & B11111000 | B00000101;

  for (int i = 0; i <= 3; i++) {
    motor.attach(m[i], MIN_PULSE, MAX_PULSE);
  }
}

void loop() {

  if (Serial.available() > 0) {

    //    message = Serial.read();
    //
    //    if(message == 254){
    //      for(int i=0; i<=3; i++){
    //        while(!Serial.available()){}
    //        motorvals[i] = Serial.read();
    //      }
    //    }
    //    Serial.print("Here ");
    //    Serial.print(Serial.available());
    //    Serial.print(" ");
    long x = micros();
    Serial.readBytes(motorVals, 4);

    //    Serial.print((micros() - x));
    while (Serial.available() > 0) {
      Serial.read();
    }
    //    Serial.print(" ");
    //    Serial.print((micros() - x));
    //        Serial.print(" ");

    //    Serial.print("temps");
    //        Serial.print(" ");

    //        for (int i = 0; i <= 7; i++) {
    //      Serial.print(motorVals.tempBytes[i]);
    //          Serial.print(" ");
    //
    //    }
    //    Serial.print(" ");
    for (int i = 0; i <= 3; i++) {
      //      motors[i].writeMicroseconds(motorVals.tempInts[i]);
      //      Serial.print(motorVals[i]);
      //          Serial.print(" ");
      //          Serial.print(convertToPulse(motorVals[i]));
      convertToPulse(motorVals[i]);
      //          Serial.print(" ");

    }
    //        Serial.println();
Serial.println((micros() - x));
  }

  //  for(int i=0; i<=3; i++){
  //    analogWrite(m[i], motorvals[i]);
  //  }
  //  Serial.println("HERE");
  //  motor.writeMicroseconds(2000);
  //
  //  //  analogWrite(m[3],254);
  //  delay(2000);
  //  //  analogWrite(m[3], 1);
  //  motor.writeMicroseconds(1500);
  //  delay(2000);
  //  //  analogWrite(m[3], 127);
  //  motor.writeMicroseconds(1000);
  //  digitalWrite(13, HIGH);
  //  delay(2000);
  //  digitalWrite(13, LOW);
  //  motor.writeMicroseconds(1500);
  //  delay(2000);

}

int convertToPulse(byte in) {
  return map(in, 0, 255, 1000, 2000);
}

