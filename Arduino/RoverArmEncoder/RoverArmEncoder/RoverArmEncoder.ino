#include <ros.h>
#include <std_msgs/Float32MultiArray.h>

#define MAX_ENC 1316

//int e[] = {2, 18 , 19, 20, 21};
int e[] = {2, 4, 5, 6, 7};

int encOffsets[] = {0, 420, 540, 732, 100};

volatile unsigned long eTime[5];
volatile bool eHigh[5];

volatile int encoders[5];
std_msgs::Float32MultiArray enc_msg;

int pinA = 2;
int pinB = 3;
volatile int counter;
bool upper;

ros::NodeHandle  nh;

void readEnc0(){
  if(digitalRead(pinA) == digitalRead(pinB)){
    counter--;
  } else{
    counter++;
  }

  if(counter > MAX_ENC-1){
    counter -= MAX_ENC;
  } else if(counter < 0){
    counter += MAX_ENC;
  }
}

void readEnc1(){
  if(!digitalRead(e[1])){
    encoders[1] = micros() - eTime[1];
    if(encoders[1] > 1024){
      encoders[1] = 0.0;
    }

    detachInterrupt(digitalPinToInterrupt(e[1]));
    while(digitalRead(e[2])){}
    attachInterrupt(digitalPinToInterrupt(e[2]),readEnc2,CHANGE);
    
  } else{
    eTime[1] = micros();
  }
}

void readEnc2(){
  if(!digitalRead(e[2])){
    encoders[2] = micros() - eTime[2];
    if(encoders[2] > 1024){
      encoders[2] = 0.0;
    }

    detachInterrupt(digitalPinToInterrupt(e[2]));
    while(digitalRead(e[3])){}
    attachInterrupt(digitalPinToInterrupt(e[3]),readEnc3,CHANGE);
    
  } else{
    eTime[2] = micros();
  }

}

void readEnc3(){
  if(!digitalRead(e[3])){
    encoders[3] = micros() - eTime[3];
    if(encoders[3] > 1024){
      encoders[3] = 0.0;
    }

    detachInterrupt(digitalPinToInterrupt(e[3]));
    while(digitalRead(e[4])){}
    attachInterrupt(digitalPinToInterrupt(e[4]),readEnc4,CHANGE);
    
  } else{
    eTime[3] = micros();
  }
}

void readEnc4(){
  if(!digitalRead(e[4])){
    encoders[4] = micros() - eTime[4];
    if(encoders[4] > 1024){
      encoders[4] = 0.0;
    }

    detachInterrupt(digitalPinToInterrupt(e[4]));
    while(digitalRead(e[1])){}
    attachInterrupt(digitalPinToInterrupt(e[1]),readEnc1,CHANGE);
    
  } else{
    eTime[4] = micros();
  }
}

ros::Publisher encPub("armEncoders", &enc_msg);

void setup() {
  Serial.begin(57600);
  
  nh.initNode();
  nh.advertise(encPub);

  enc_msg.data = (float*)malloc(sizeof(float) * 5);
  enc_msg.data_length = 5;

  for(int i = 0; i < 5; i++){
    pinMode(e[i], INPUT);

    enc_msg.data[i] = 0.0;
  }

  pinMode(pinA,INPUT);
  pinMode(pinB,INPUT);
  counter = 0;
  upper = false;

  attachInterrupt(digitalPinToInterrupt(e[0]), readEnc0, CHANGE);
  attachInterrupt(digitalPinToInterrupt(e[1]), readEnc1, CHANGE);
}

void loop() {

  enc_msg.data[0] = map(counter, 0, 1316, 0, 1024);
  
  for(int i=1; i<5; i++){
    enc_msg.data[i] = ( (encoders[i] - encOffsets[i] + 1023) % 1023 );
  }
  encPub.publish( &enc_msg );
  delay(20);
  nh.spinOnce();

}
