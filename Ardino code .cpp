#include <Servo.h>

Servo servoPan;   
Servo servoTilt;  

#define trigPin 2
#define echoPin 3


float getDistance() {
  float total = 0;

  for (int i = 0; i < 5; i++) {   
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH, 30000);
    float d = duration * 0.034 / 2;

    total += d;
    delay(5);
  }

  return total / 5.0;   
}


void setup() {
  servoPan.attach(9);
  servoTilt.attach(8);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  Serial.begin(9600);
}

void loop() {

  
  for (int panAngle = 0; panAngle <= 180; panAngle += 10) {

    servoPan.write(panAngle);
    delay(300);  

    
    for (int tiltAngle = 90; tiltAngle <= 150; tiltAngle += 2) {

      servoTilt.write(tiltAngle);
      delay(100);

      float d = getDistance();

      if (d > 2 && d < 400) {
        Serial.print(panAngle);
        Serial.print(",");
        Serial.print(tiltAngle);
        Serial.print(",");
        Serial.println(d);
      }
    }

    for (int tiltAngle = 150; tiltAngle >= 90; tiltAngle -= 2) {

      servoTilt.write(tiltAngle);
      delay(100);

      float d = getDistance();

      if (d > 2 && d < 400) {
        Serial.print(panAngle);
        Serial.print(",");
        Serial.print(tiltAngle);
        Serial.print(",");
        Serial.println(d);
      }
    }
  }

  while (1);
}