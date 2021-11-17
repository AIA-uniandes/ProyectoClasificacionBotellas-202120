#include <Wire.h>
#include <Arduino.h>
#include <SoftwareSerial.h>
#include <HerkulexServo.h>

#define PIN_SW_RX 8
#define PIN_SW_TX 9
#define SERVO_ID  0xFE

SoftwareSerial   servo_serial(PIN_SW_RX, PIN_SW_TX);
HerkulexServoBus herkulex_bus(servo_serial);
HerkulexServo    servo(herkulex_bus, SERVO_ID);
int timeout;

void setup() {
  
  Wire.begin(8);                // join i2c bus with address #8
  Wire.setClock(400000);
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent); // register event
  Serial.begin(9600);           // start serial for output
   servo_serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(A3, INPUT);
  pinMode(A6, INPUT);
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    servo.setLedColor(HerkulexLed::Green);
  
  servo.enableSpeedControlMode();
  servo.setTorqueOff();
  servo.setSpeed(600);
}//7436000

void loop() {
  delay(1000);
   Serial.println("OK");         // print the character
     herkulex_bus.update();
  timeout++;
   digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  if (timeout>10){
    
  servo.setTorqueOff();
   servo.setLedColor(HerkulexLed::White);
  }   
  
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  //while (1 < Wire.available()) { // loop through all but the last
    //char c = Wire.read(); // receive byte as a character
   // Serial.print(c);         // print the character
  //}
  int x = Wire.read();    // receive byte as an integer
  Serial.println(x);         // print the integer
  timeout=0;
   digitalWrite(LED_BUILTIN, LOW);   // turn the LED on (HIGH is the voltage level)
  switch(x){

    case 0:servo.setTorqueOff();servo.setLedColor(HerkulexLed::Red); break;
    case 1:servo.setTorqueOn();servo.setSpeed(-1023);  servo.setLedColor(HerkulexLed::Blue); break;
    case 2:servo.setTorqueOn();servo.setSpeed(-800);  servo.setTorqueOn(); servo.setLedColor(HerkulexLed::Blue);break;
    case 3:servo.setTorqueOn();servo.setSpeed(-600);  servo.setTorqueOn(); servo.setLedColor(HerkulexLed::Blue);break;
    case 4:servo.setTorqueOn();servo.setSpeed(-500);  servo.setTorqueOn(); servo.setLedColor(HerkulexLed::Blue);break;
    case 5:servo.setTorqueOn();servo.setSpeed(-400);  servo.setTorqueOn(); servo.setLedColor(HerkulexLed::Blue);break;
    case 6:servo.setTorqueOn();servo.setSpeed(400);  servo.setTorqueOn();servo.setLedColor(HerkulexLed::Green); break;
    case 7:servo.setTorqueOn();servo.setSpeed(500);  servo.setTorqueOn();servo.setLedColor(HerkulexLed::Green); break;
    case 8:servo.setTorqueOn();servo.setSpeed(600);  servo.setTorqueOn(); servo.setLedColor(HerkulexLed::Green);break;
    case 9:servo.setTorqueOn();servo.setSpeed(800);  servo.setTorqueOn(); servo.setLedColor(HerkulexLed::Green);break;
    case 10:servo.setTorqueOn();servo.setSpeed(1023);  servo.setTorqueOn(); servo.setLedColor(HerkulexLed::Green);break;
    
  }
}

void requestEvent() {
  Wire.write(20); // respond with message of 6 bytes
  // as expected by master
   Serial.println('r');         // print the integer
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED on (HIGH is the voltage level)
}
