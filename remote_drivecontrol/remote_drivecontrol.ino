int PWM2 = 5;
int DIR2 = 4;
int PWM1 = 3;
int DIR1 = 2;

bool ROVER5 = true;

int RTalonPin = 9;
int LTalonPin = 10;

int TALON_CENTER = 1500;

#include <Servo.h>

Servo RTalon
Servo LTalon

void setup() {
  if (ROVER5) {
    // put your setup code here, to run once:
    pinMode(PWM2, OUTPUT);
    pinMode(DIR2, OUTPUT);
    pinMode(PWM1, OUTPUT);
    pinMode(DIR1, OUTPUT);
  } else {
    pinMode(RTalonPin, OUTPUT);
    pinMode(LTalonPin, OUTPUT);

    RTalon.attach(RTalonPin);
    LTalon.attach(LTalonPin);
  }

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    int instructions = Serial.read();
    int right = instructions & 0b00001111;
    int left = (instructions & 0b11110000) >> 4;
    Serial.print('(');
    Serial.print(left);
    Serial.print(',');
    Serial.print(right);
    Serial.print(')');

    // convert to plus/minus (center it)
    left -= 7;
    right -= 7;


    if (ROVER5) {
      // left side
      analogWrite(PWM1, map(abs(left), 0, 5, 0, 255));
      digitalWrite(DIR1, left > 0);
      // right side
      analogWrite(PWM2, map(abs(right), 0, 5, 0, 255));
      digitalWrite(DIR2, right > 0);
    } else {
      LTalon.writeMicroseconds(map(left, -5, 5, 1300, 1700));
      RTalon.writeMicroseconds(map(right, -5, 5, 1300, 1700));
    }
  } else {
    if (ROVER5) {
      analogWrite(PWM1, 0);
      digitalWrite(DIR1, LOW);
      analogWrite(PWM2, 0);
      digitalWrite(DIR2, LOW);
    } else {
      RTalon.writeMicroseconds(TALON_CENTER);
      LTalon.writeMicroseconds(TALON_CENTER);
    }
  }
  delay(30);
}
