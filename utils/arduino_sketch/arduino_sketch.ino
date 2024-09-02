/*
 *  For use with Arduino UNO
 *
 *  This arduino sketch responds to a message sent to it over serial by sending the pin value read
 *  If the start byte is followed by 0xfd e.g. [0x02, 0xfd], then this indicates that there is
 *  a request to read the state of input pin 13.  The status of the pin will be
 *  read and written to the serial port.
 *
 */

const int GPIO_STATUS_PIN_13 = 13;
int incomingByte = 0;
int toggle_count = 0;

void setup()
{
  //Set digital pin as input
  pinMode(GPIO_STATUS_PIN_13, INPUT);
  //Initialize Serial port with 115200 baud rate
  Serial.begin(115200);
}

void loop()
{
  //Check if there is data in the serial buffer
  if(Serial.available() > 0){
    //Check for start byte (0x02)
    if(Serial.read() == 0x02){
      //delay needed between two consecutive reads
      delay(10);
      //Read the next byte for data
      incomingByte = Serial.read();
      if(incomingByte == 0xfd){
        //read the status of the GPIO PIN
        int initial_state_val = digitalRead(GPIO_STATUS_PIN_13);
        Serial.write(initial_state_val);
        delay(10);
      }
    }
  }
 }
