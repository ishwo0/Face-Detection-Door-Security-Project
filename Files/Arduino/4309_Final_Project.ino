/*
 The LCD pinout guide:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)
*/

#include <LiquidCrystal.h>

// LCD interface pins with aruduino pin numbers
const int rs = 12;
const int en = 11;
const int d4 = 5;
const int d5 = 4;
const int d6 = 3;
const int d7 = 2;
// initialize LCD
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// LEDS
const int greenLED = 6;
const int blueLED = 7;
const int yellowLED = 8;
const int redLED = 9;

// Btn pin and state
const int btnPin = 10;
int btnState = 0;

void setup() {
  Serial.begin(9600);    // Initialize the USB UART Serial Connection

  // Set up LED pins as outputs
  pinMode(greenLED, OUTPUT);
  pinMode(blueLED, OUTPUT);
  pinMode(yellowLED, OUTPUT);
  pinMode(redLED, OUTPUT);

  // Set up button pin as input
  pinMode(btnPin, INPUT);

  // set up the LCD's number of columns and rows: 16 columns, 2 rows
  lcd.begin(16, 2);

  // flash hello world for 2 seconds
  lcd.clear();
  lcd.print("hello, world!");
  delay(2000);
  lcd.clear();
}

void loop() {
  btnState = digitalRead(btnPin);

  // wait until something is there to receive
  if (Serial.available() > 0) {
    // save the received message from the python code
    String message = Serial.readString(); 

    // check what the message is
    if (message == "Known Face OK") {
      // if there was a known face and we are not in after hours
      digitalWrite(greenLED, HIGH); // turn on green led
      lcd.print("Access Granted."); // display access on LCD
      delay(3000);                  // wait 3 seconds
      digitalWrite(greenLED, LOW);  // turn off green led
      lcd.clear();                  // clear LCD

    }
    else if (message == "Known Face AFTER HOURS") {
      // if there was a known face but we are in after hours
      digitalWrite(blueLED, HIGH);            // turn on blue led
      lcd.print("Access Denied: AFTER HRS");  // display access on LCD
      delay(3000);                            // wait 3 seconds
      digitalWrite(blueLED, LOW);             // turn off blue led
      lcd.clear();                            // clear LCD
    }
    else if (message == "Unknown Face OK") {
      // if there was an unknown face and we are not in after hours
      digitalWrite(yellowLED, HIGH);  // turn on yellow led
      lcd.print("Access Denied.");   // display access on LCD
      delay(3000);                    // wait 3 seconds
      digitalWrite(yellowLED, LOW);   // turn off yellow led
      lcd.clear();                    // clear LCD
    }
    else if (message == "Unknown Face AFTER HOURS") {
      // if there was an unknown face and we are in after hours
      digitalWrite(redLED, HIGH);                 // turn on red led
      lcd.print("Access Denied: AFTER HRS");      // display access on LCD
      delay(3000);                                // wait 3 seconds
      digitalWrite(redLED, LOW);                  // turn off red led
      lcd.clear();                                // clear LCD
    }

  }

  if (btnState == HIGH) {
    // turn red LED on
    digitalWrite(redLED, HIGH);                 // turn on red led
    lcd.print("ERROR");                         // display access on LCD
    delay(3000);                                // wait 3 seconds
    digitalWrite(redLED, LOW);                  // turn off red led
    lcd.clear();                                // clear LCD
  }

}