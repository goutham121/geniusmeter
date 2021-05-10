int Read_Voltage  = A1;
int Read_Current  = A0;
float Voltage = 0.0;
float Current = 0.0;
float Power = 0.0;

void setup() {
  Serial.begin(9600);
  
}

void loop() {
 Voltage = analogRead(Read_Voltage);
 Current = analogRead(Read_Current);

 Voltage = Voltage * (5.0/1023.0) * 6.46;
 Current = Current * (5.0/1023.0) * 0.239;

 Serial.println(Voltage);
 Serial.println(Current);

 Power = Voltage * Current;

 Serial.println(Power);
  delay(1000);
}
