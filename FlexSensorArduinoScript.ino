int flex = A0;
int data[200];

void setup() {
  Serial.begin(9600);
  pinMode(flex, INPUT);
  Serial.flush();
}

void loop() {
//  Serial.flush();
  while (!Serial.available()) {} // wait for data to arrive
  while (Serial.available()) {
    Serial.read();
  }
  for (int i = 0; i < 200; i++) {
    data[i] = analogRead(flex); 
    Serial.println(data[i]-925);
  }
//  Serial.println("STARTING");
  Serial.end();
  Serial.begin(9600);
//  Serial.println("ENDING");

//Serial.println(analogRead(flex)-925);

delay(10);

  
} 
