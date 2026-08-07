/*
----------------------------------------------------
 Intelligent Robotic Arm
 Arduino Firmware

 Receives servo angles from Raspberry Pi

 Format:

 base,shoulder,elbow,wrist,gripper

 Example:

 90,120,75,60,30

----------------------------------------------------
*/

#include <Servo.h>

// -----------------------------
// Servo Objects
// -----------------------------

Servo baseServo;
Servo shoulderServo;
Servo elbowServo;
Servo wristServo;
Servo gripperServo;

// -----------------------------
// Pins
// Change according to wiring
// -----------------------------

const int BASE_PIN      = 3;
const int SHOULDER_PIN  = 5;
const int ELBOW_PIN     = 6;
const int WRIST_PIN     = 9;
const int GRIPPER_PIN   = 10;

// -----------------------------
// Current Angles
// -----------------------------

int baseAngle = 90;
int shoulderAngle = 90;
int elbowAngle = 90;
int wristAngle = 90;
int gripperAngle = 20;

// -----------------------------
// Setup
// -----------------------------

void setup()
{

    Serial.begin(115200);

    baseServo.attach(BASE_PIN);
    shoulderServo.attach(SHOULDER_PIN);
    elbowServo.attach(ELBOW_PIN);
    wristServo.attach(WRIST_PIN);
    gripperServo.attach(GRIPPER_PIN);

    baseServo.write(baseAngle);
    shoulderServo.write(shoulderAngle);
    elbowServo.write(elbowAngle);
    wristServo.write(wristAngle);
    gripperServo.write(gripperAngle);

    delay(1000);

    Serial.println("READY");
}

// -----------------------------
// Move Robot
// -----------------------------

void moveRobot(

    int base,

    int shoulder,

    int elbow,

    int wrist,

    int gripper

)
{

    // Safety check
    base = constrain(base, 0, 180);
    shoulder = constrain(shoulder, 0, 180);
    elbow = constrain(elbow, 0, 180);
    wrist = constrain(wrist, 0, 180);
    gripper = constrain(gripper, 0, 180);

    // Directly move servos
    baseServo.write(base);
    shoulderServo.write(shoulder);
    elbowServo.write(elbow);
    wristServo.write(wrist);
    gripperServo.write(gripper);

    // Update current angles
    baseAngle = base;
    shoulderAngle = shoulder;
    elbowAngle = elbow;
    wristAngle = wrist;
    gripperAngle = gripper;

}

// -----------------------------
// Read Serial
// -----------------------------

void loop()
{

    if(Serial.available())
    {

        String data = Serial.readStringUntil('\n');

        data.trim();

        if(data.length()==0)
            return;

        int values[5];

        int index = 0;

        char *token;

        char buffer[50];

        data.toCharArray(buffer,50);

        token = strtok(buffer,",");

        while(token != NULL && index < 5)
        {

            values[index++] = atoi(token);

            token = strtok(NULL,",");

        }

        if(index == 5)
        {

            moveRobot(

                values[0],

                values[1],

                values[2],

                values[3],

                values[4]

            );

            Serial.println("DONE");

        }
        else
        {

            Serial.println("ERROR");

        }

    }

}