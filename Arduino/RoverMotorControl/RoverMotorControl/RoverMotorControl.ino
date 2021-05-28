/* 
 * in order to run this: rosrun rosserial_python serial_node.py /dev/ttyUSB0   <-- put correct USB port
 */

#include <ros.h>
#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/Float32.h>

#include <Servo.h>
#include <AccelStepper.h>

#define MAX_PULSE 2000
#define MIN_PULSE 1000
#define OFF_PULSE 1500

#define TIMEOUT 1000

#define sgn(x) ((x) < 0 ? -1 : ((x) > 0 ? 1 : 0))

unsigned long driveTimestamp = 0;
unsigned long armTimestamp = 0;

double driveVals[4];
double armVals[5];

int d[] = {2, 3, 4, 5};
int a[] = {6, 7, 8, 9, 10};
int dir[] = {15, 11, 12, 13, 14};
int dirPin = 18;
int pulPin = 19;
int enaPin = 20;

Servo drives[4];
Servo arms[5];

AccelStepper gripper(1, pulPin, dirPin);  // object used to allow arduino to control stepper motor hooked up to X drive module on shield


ros::NodeHandle  nh;

void driveCallback( const std_msgs::Float32MultiArray& msg){
  driveVals[0] = msg.data[0];
  driveVals[1] = msg.data[0];
  driveVals[2] = msg.data[1];
  driveVals[3] = msg.data[1];

  driveTimestamp = millis();
}

void armCallback( const std_msgs::Float32MultiArray& msg){

  for(int i=0; i<5; i++){
    armVals[i] = msg.data[i];
  }

  armTimestamp = millis();
}

void gripperCallback( const std_msgs::Float32& msg){
  gripper.setSpeed(msg.data*750);
}

int convertToPulse(double in) {
  return ((in + 1.0) * 500.0) + 1000.0;
}

double convertToDuty(double in) {
  return abs(in) * 255;
}


//ISR(TIMER4_COMPA_vect) {
//  gripper.runSpeed();
//}

ros::Subscriber<std_msgs::Float32MultiArray> driveSub("driveCommands", &driveCallback );
ros::Subscriber<std_msgs::Float32MultiArray> armSub("armCommands", &armCallback );
ros::Subscriber<std_msgs::Float32> gripSub("armGripper", &gripperCallback );

void setup()
{   
  Serial.begin(57600);

  nh.initNode();
  nh.subscribe(driveSub);
  nh.subscribe(armSub);
  nh.subscribe(gripSub);

  gripper.setMaxSpeed(1000);
  gripper.setAcceleration(800);
  gripper.setSpeed(0);
  gripper.stop();

  pinMode(enaPin,OUTPUT);
  digitalWrite(enaPin,LOW);

  for (int i = 0; i < 4; i++) {
    drives[i].attach(d[i], MIN_PULSE, MAX_PULSE);
  }

  for(int i = 0; i < 5; i++){
    pinMode(a[i],OUTPUT);
    pinMode(dir[i],OUTPUT);
  }

//  cli();//stop interrupts
//
//  //set timer4 interrupt at 1Hz
//  TCCR4A = 0;// set entire TCCR1A register to 0
//  TCCR4B = 0;// same for TCCR1B
//  TCNT4  = 0;//initialize counter value to 0
//  // set compare match register for 1hz increments
//  OCR4A = 15624/8192;// = (16*10^6) / (1*1024) - 1 (must be <65536)
//  // turn on CTC mode
//  TCCR4B |= (1 << WGM12);
//  // Set CS12 and CS10 bits for 1024 prescaler
//  TCCR4B |= (1 << CS12) | (1 << CS10);  
//  // enable timer compare interrupt
//  TIMSK4 |= (1 << OCIE4A);
//  sei();

}

void loop()
{  

  if(millis() - driveTimestamp < TIMEOUT){
    for (int i = 0; i < 4; i++) {
      drives[i].writeMicroseconds(convertToPulse(driveVals[i]));
    }
  } else{
    for (int i = 0; i < 4; i++) {
      drives[i].writeMicroseconds(OFF_PULSE);
    }
  }

  if(millis() - armTimestamp < TIMEOUT){
    for (int i = 0; i < 5; i++) {
      digitalWrite(dir[i], sgn(armVals[i]) > 0 );
      analogWrite(a[i], convertToDuty(armVals[i]));
    }
  } else{
    for (int i = 0; i < 5; i++) {
      digitalWrite(dir[i], sgn(armVals[i]) > 0);
      analogWrite(a[i], convertToDuty(0));
    }
  }

  gripper.runSpeed();

  nh.spinOnce();
}
