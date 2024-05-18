#include "OneWire.h"            //librerie sensore di temperatura
#include "DallasTemperature.h"

#define ONE_WIRE_BUS 2          //definizione pin del sensore di temperatura
int pin_illuminazione = 3;      //definizione pin illuminazione e piastra
int pin_piastra = 4;

OneWire oneWire(ONE_WIRE_BUS);        //dichiarazioni libreria del sensore
DallasTemperature sensors(&oneWire);

void setup() {
  pinMode(pin_illuminazione, OUTPUT);   //dichiarazione pin di uscita
  pinMode(pin_piastra, OUTPUT);

  sensors.begin();                      //inizializzazione libreria del sensore
  Serial.begin(9600);
}

void loop() {   //ciclo del programma

  sensors.requestTemperatures();            //lettura della temperatura
  int tempC = sensors.getTempCByIndex(0);   //acquisizione valori di temperatura in gradi Celsius

  if (Serial.available()) {    //se avviene una comunicazione comincia la lettura/scrittura
    int data = Serial.read();  //lettura dei dati provenienti dal programma
    if (0 <= data <= 255) {    //selezione dei dati corretti e controllo delle uscite in funzione di essi
      analogWrite(pin_illuminazione, data);
    }else if (data == 256) {
      digitalWrite(pin_piastra, LOW);
    }else if (data == 257) {
      digitalWrite(pin_piastra, HIGH);
    }

    if(tempC != -127.00) {    //invio dei valori di temperatura del sensore
      Serial.print(tempC);
    }
  }

  delay(100); //attesa di 100 ms
}