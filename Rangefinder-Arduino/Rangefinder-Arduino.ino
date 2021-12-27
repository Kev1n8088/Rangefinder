/* Sweep
  by BARRAGAN <http://barraganstudio.com>
  This example code is in the public domain.

  modified 8 Nov 2013
  by Scott Fitzgerald
  http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo servoY;  // create servo object to control a servo
Servo servoX;
// twelve servo objects can be created on most boards



int degreeYAdjust = 36;
int degreeXAdjust = 90;

int degreeX;
int degreeY;
int oldDegreeX = 0;
int oldDegreeY = 0;

int posX = 0;
int posY = 0;


int x;
int y;
String s;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(4);
  servoY.attach(9);  // attaches the servo on pin 9 to the servo object
  servoX.attach(10);
}

void loop() {
  while (!Serial.available());
  s = Serial.readString();
  x = getValue(s, 'x', 0).toInt();
  y = getValue(s, 'x', 1).toInt();

  degreeX = degreeXAdjust + (x * -1);
  degreeY = degreeYAdjust + y;

  posX = 0;
  posY = 0;



  if (degreeY < oldDegreeY) {
    for (posY = oldDegreeY; posY >= degreeY; posY -= 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      servoY.write(posY);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15ms for the servo to reach the position
    }
  } else {
    for (posY = oldDegreeY; posY <= degreeY; posY += 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      servoY.write(posY);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15ms for the servo to reach the position
    }
  }

  if (degreeX < oldDegreeX) {
    for (posX = oldDegreeX; posX >= degreeX; posX -= 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      servoX.write(posX);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15ms for the servo to reach the position
    }
  } else {
    for (posX = oldDegreeX; posX <= degreeX; posX += 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      servoX.write(posX);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15ms for the servo to reach the position
    }
  }


  oldDegreeY = degreeY;
  oldDegreeX = degreeX;




}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = { 0, -1 };
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
