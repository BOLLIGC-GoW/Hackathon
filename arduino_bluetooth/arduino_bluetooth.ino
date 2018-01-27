#include <SoftwareSerial.h>


char val; // variable to receive data from the serial port
int ledpinR = 7; // LED connected to pin 48 (on-board LED)
int ledpinG = 12; 
int ledpinY = 9; 
void setup() {
  pinMode(ledpinR, OUTPUT);  // pin 48 (on-board LED) as OUTPUT
  pinMode(ledpinG, OUTPUT);  // pin 48 (on-board LED) as OUTPUT
  pinMode(ledpinY, OUTPUT);  // pin 48 (on-board LED) as OUTPUT
  Serial.begin(9600);       // start serial communication at 9600bps
}
void loop() {
  if( Serial.available() )       // if data is available to read
  {
    val = Serial.read();         // read it and store it in 'val'
  
  if( val == 'R' )               // if 'H' was received
  {
    digitalWrite(ledpinR, HIGH);  // turn ON the LED
    digitalWrite(ledpinG, LOW);
    digitalWrite(ledpinY, LOW);
  } 
  else if(val == 'G')
{
  
    digitalWrite(ledpinR, LOW);  // turn ON the LED
    digitalWrite(ledpinG, HIGH);
    digitalWrite(ledpinY, LOW);
}
 else if(val == 'Y')
{
  
    digitalWrite(ledpinR, LOW);  // turn ON the LED
    digitalWrite(ledpinG, LOW);
    digitalWrite(ledpinY, HIGH);
}
  else { 
    digitalWrite(ledpinR, HIGH);   // otherwise turn it OFF
    digitalWrite(ledpinG, HIGH);
    digitalWrite(ledpinY, HIGH);
  }
  delay(1000);                    // wait 100ms for next reading
}
}
