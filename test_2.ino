float zeroPowerCurrent = 0.05;
float ct = A0;
float voltTransformer = A1;
float power;
float wattHour = 0;
void setup() {
Serial.begin(9600);
pinMode(ct,INPUT);
pinMode(voltTransformer,INPUT);
}
float getCurrent()
{ 
  float currentError = 0.0301933437;
  float rVPP;   
  float nCurrThruResistorPP; 
  float nCurrThruResistorRMS; 
  float nCurrentThruWire;     
  float result1;
  int readValue1;           
  int maxValue1 = 0;      
   uint32_t start_time = millis();
   while((millis()-start_time) < 1000) 
   {
       readValue1 = analogRead(ct);
       if (readValue1> maxValue1) 
       {
          maxValue1 = readValue1;
       }
   }
   rVPP = (maxValue1 * 5.0)/1024.0;
   nCurrThruResistorPP = (rVPP/200.0) * 1000.0;
   nCurrThruResistorRMS = nCurrThruResistorPP * 0.707;
   nCurrentThruWire = nCurrThruResistorRMS * 1000;
   Serial.print("Volts Peak : ");
   Serial.println(rVPP,3);
   Serial.print("Current Through Resistor (Peak) : ");
   Serial.print(nCurrThruResistorPP,3);
   Serial.println(" mA Peak to Peak"); 
   Serial.print("Current Through Resistor (RMS) : ");
   Serial.print(nCurrThruResistorRMS,3);
   Serial.println(" mA RMS");
   Serial.print("Current Through Wire : ");
   Serial.print(nCurrentThruWire,3);
   Serial.println(" mA RMS");
   Serial.println();
   return (nCurrentThruWire/1000) + currentError;   
 } 
 
float getVoltage()
{ 
  float zeroOffset = 0;
  float calibrateVoltage = 238; 
  float readValue1,maxValue1,result;    
   uint32_t start_time = millis();
   digitalWrite(led, HIGH);
   while((millis()-start_time) < 1000) //sample for 1 Sec
   {
       readValue1 = analogRead(voltTransformer);
       // see if you have a new maxValue
       if (readValue1> maxValue1) 
       {
           maxValue1 = readValue1;
       }
   }
   
   // Convert the digital data to a voltage
  result = (maxValue1 * calibrateVoltage)/1024.0;
  return result - zeroOffset;

}

void loop() {
  // put your main code here, to run repeatedly:
float volt = getVoltage();
Serial.print("AC Voltage: ");
Serial.println(volt);
float current = getCurrent();
if (current>zeroPowerCurrent)
{
  float power = volt * current;
  Serial.print("Power: ");
  Serial.println(power);
  Serial.println();
}

else 
{
  Serial.print("Power: 0 ");
  Serial.println();
}

wattHour = wattHour + (power * (2.13/60/60));..

Serial.print("Wh: ");
Serial.println(wattHour,3);
Serial.println(); 

}
