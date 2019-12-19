
byte motorvals[4];

int m[] = {3, 5, 6, 9};

byte message = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  for(int i=0; i<=3; i++){
    pinMode(m[i], OUTPUT);
  }
}

void loop() {
  
  if(Serial.available()>0){
    
//    message = Serial.read();
//    
//    if(message == 255){
//      for(int i=0; i<=3; i++){
//        while(!Serial.available()){}
//        motorvals[i] = Serial.read();
//      }
//    }

    Serial.readBytes(motorvals, 4);
  }

  for(int i=0; i<=3; i++){
    analogWrite(m[i], motorvals[i]);
  }
  
}
