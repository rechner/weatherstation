
void setup() {
  randomSeed(analogRead(0));
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect.  Needed for Leonardo only
  }
}

long getTemperature() {
  return random(-20, 34);
}

long getHumidity() {
  return random(100);
}

long getWindSpeed() {
  return random(60);
}

float getWindDirection() {
  return (random(360) / 360.0);
}

float getBarometer() {
  return 101.3 - (random(1000) / 100.0);
}

boolean getRain() {
  return ((random(100) / 100) > 90 ? true : false);
}

float getLight() {
  return (random(100) / 100.0);
}

void loop() {
  Serial.print("{ \"temperature\" : ");
  Serial.print(getTemperature());
  Serial.print(", \"relative_humidity\" : ");
  Serial.print(getHumidity());
  Serial.print(", \"wind_speed\" : ");
  Serial.print(getWindSpeed());
  Serial.print(", \"wind_direction\" : ");
  Serial.print(getWindDirection());
  Serial.print(", \"rain_sensor\" : ");
  Serial.print(getRain());
  Serial.print(", \"barometer\" : ");
  Serial.print(getBarometer());
  Serial.print(", \"light\" : ");
  Serial.print(getLight());
  Serial.print(" }\n");
  delay(1000);
}
