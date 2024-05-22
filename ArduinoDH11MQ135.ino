
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <math.h>


// #####################################################################################################
//                                    DEO ZA TEMPERATURU
// #####################################################################################################
// pin connected to DHT11 data line
#define DATA_PIN 8

// create DHT instance
DHT_Unified dht(DATA_PIN, DHT11);
//#####################################################################################################



// #####################################################################################################
//                                    DEO ZA CO2
// #####################################################################################################
const int MQ135_PIN = A0;   // Analogni pin na koji je priključen MQ-135 senzor
const float VCC = 5.0;      // Napajanje senzora (obično 5V)
const float RL = 10.0;      // Load otpornik u kilo-ohmima
const float Ro = 100.0;     // Kalibrisani otpor senzora u čistom vazduhu (izmeriti tokom kalibracije)

const float CO2_THRESHOLD = 1000.0;  // Prag za koncentraciju CO2 u ppm

// Funkcija za izračunavanje otpornosti senzora (RS)
float calculateRS(int sensorValue) {
  float voltage = sensorValue * (VCC / 1023.0);
  float RS = (VCC - voltage) / voltage * RL;
  return RS;
} 

// Funkcija za izračunavanje koncentracije CO2 u ppm
float calculateCO2(float RS) {
  float ratio = RS / Ro;
  // Korišćenje empirijske formule iz datasheeta za CO2
  // Vrednosti B i m su uzete kao pretpostavke; treba koristiti tačne vrednosti iz datasheeta
  const float B = 0.33;   // Pretpostavljena vrednost
  const float m = -0.44;  // Pretpostavljena vrednost
  float ppm = pow(10, (log10(ratio) - B) / m);
  return ppm;
}
// #####################################################################################################





void setup() {
  Serial.begin(9600);  // Pokretanje serijske komunikacije sa brzinom od 115200 bps
  dht.begin();
}
void loop() {
  sensors_event_t event;

  int sensorValue = analogRead(MQ135_PIN);  // Očitavanje analogne vrednosti sa MQ-135
  float RS = calculateRS(sensorValue);      // Izračunavanje otpornosti senzora
  float co2_ppm = calculateCO2(RS);         // Izračunavanje koncentracije CO2 u ppm

  dht.temperature().getEvent(&event);
  float celsius = event.temperature;
  float fahrenheit = (celsius * 1.8) + 32;

  // Serial.print("Celsius: ");
  // Serial.print(celsius);
  // Serial.println("C");

  // Serial.print("Fahrenheit: ");
  // Serial.print(fahrenheit);
  // Serial.println("F");

  // Get humidity event and print its value
  dht.humidity().getEvent(&event);
  // Serial.print("Humidity: ");
  // Serial.print(event.relative_humidity);

Serial.print(celsius);
Serial.print(",");
Serial.print(event.relative_humidity);
Serial.print(",");
Serial.println(co2_ppm);

  // Serial.println("%");
  // Serial.println();
  
  // Serial.print("Analog value: ");
  // Serial.println(sensorValue);
  // Serial.print("RS: ");
  // Serial.print(RS);
  // Serial.println(" kOhm");
  // Serial.print("CO2 concentration: ");
  // Serial.print(co2_ppm);
  // Serial.println(" ppm");
  
  // // Provera da li je koncentracija CO2 veća od praga
  // if (co2_ppm > CO2_THRESHOLD) {
  //   Serial.println("WARNING: CO2 concentration is too high!");
  // }else{
  //   Serial.println("CO2 concentration is okay.");
  // }
  // Serial.println("##################################################\n\n");


  delay(3000);  // Čekanje 2 sekunde pre sledećeg očitanja
}


