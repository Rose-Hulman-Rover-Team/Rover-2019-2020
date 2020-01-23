/*
  Arlo-Test-Motor-Connections
  
  Run this sketch to verify that your Arlo goes forward.
*/

#include <ArloRobot.h>                        // Include Arlo library
#include <SoftwareSerial.h>                   // Include SoftwareSerial library

ArloRobot Arlo;                               // Declare Arlo object
SoftwareSerial ArloSerial(12, 13);            // Declare SoftwareSerial objectu
byte motorVals[2];
                                              // DHB-10 -> I/O 12, DHB-10 <- I/O 13
void setup()                                  // Setup function
{
  tone(4, 3000, 2000);                        // Piezospeaker beep
  Serial.begin(9600);                         // Start terminal serial port

  ArloSerial.begin(19200);                   
  Arlo.begin(ArloSerial);                     

  //Arlo.writeMotorPower(100, -100);               // Go forward
  //delay(3000);                                //   for three seconds
  //Arlo.writeMotorPower(50, 50);  
  //delay(3000);
  //Arlo.writeMotorPower(-50, -50);               // - - Turn left
  //delay(3000); 
  //Arlo.writeMotorPower(20, 20);  
  //delay(400);              
  //Arlo.writeMotorPower(0, 0); 
}

void loop() {
  if (Serial.available() > 0) {
    Serial.readBytes(motorVals, 2);

    while (Serial.available() > 0) {
      Serial.read();
    }

    Arlo.writeMotorPower(motorVals[0]*2-127, motorVals[1]*2-127);
  } 
}  
