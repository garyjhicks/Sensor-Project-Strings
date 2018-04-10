int ledPin = 13;
bool lightStatus = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

  int value = analogRead(A0);
  //Serial.print("Voltage: ");
  Serial.println(value);

  int value2 = analogRead(A1);
  Serial.println(value2);

  if ((Serial.available() > 0) && (Serial.available() < 2)) {
    if (lightStatus == false) {
      digitalWrite(ledPin, HIGH);
      lightStatus = true;
    }
    else{
      digitalWrite(ledPin, LOW);
      lightStatus = false;
    }

    //digitalWrite(ledPin, HIGH);
  }
  else if (Serial.available() == 2) {
    digitalWrite(ledPin, LOW);
    lightStatus = false;
    Serial.read();
    Serial.read();
  }


  delay(1000);

}
