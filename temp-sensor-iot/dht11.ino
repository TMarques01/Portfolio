#include "DHT.h"

#define DHTPIN 8       // Pino ligado ao sensor
#define DHTTYPE DHT11  // Tipo de sensor

// Pinos PWM do LED RGB
#define RED_PIN    9
#define GREEN_PIN  10
#define BLUE_PIN   11

#define LDR_PIN A0

#define BUTTON_PIN 12

DHT dht(DHTPIN, DHTTYPE);

int ledPins[6] = {2, 3, 4, 5, 6, 7}; // Pinos dos LEDs (bit 0 a bit 5)

void setup() {
  Serial.begin(9600);
  dht.begin();

  // Define todos os pinos dos LEDs como saída
  for (int i = 0; i < 6; i++) {
    pinMode(ledPins[i], OUTPUT);
  }

  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);

}

void loop() {

  int ldrValue = analogRead(LDR_PIN);         // 0 (muita luz) a 1023 (muito escuro)

  if (ldrValue < 1000) {

    delay(5000);

    float temp = dht.readTemperature();
    float hum = dht.readHumidity();

    if (isnan(temp) || isnan(hum)) {
      Serial.println("Erro ao ler o DHT11.");
      return;
    }

    // Serial.println("______________________________");
    // Serial.print("Temperatura: "); Serial.println(temp);
    // Serial.print("Humidade: "); Serial.println(hum);
    Serial.print(temp);Serial.print(",");Serial.println(hum);

    // Atualizar LEDs binários da temperatura
    int tempInt = (int)temp - 2;
    for (int i = 0; i < 6; i++) {
      digitalWrite(ledPins[i], (tempInt >> i) & 1);
    }

    // ---------- COR DO LED RGB BASEADA NA HUMIDADE ----------
    int r = 0, g = 0, b = 0;

    if (hum < 40) {
      // 0 a 40 → transição de vermelho (255,0,0) para verde (0,255,0)
      float factor = hum / 40.0;
      r = 255 * (1 - factor);
      g = 255 * factor;
    } else if (hum <= 60) {
      // Faixa ideal: verde puro
      r = 0;
      g = 255;
      b = 0;
    } else if (hum <= 80) {
      // 60 a 80 → transição de verde (0,255,0) para azul (0,0,255)
      float factor = (hum - 60) / 20.0;
      g = 255 * (1 - factor);
      b = 255 * factor;
    } else {
      // Acima de 80 → azul puro
      r = 0;
      g = 0;
      b = 255;
    }

    // ---------- AJUSTE DE INTENSIDADE COM BASE NO LDR ----------
    float intensityFactor = 1.0 - (ldrValue / 1023.0);  // Normalizado entre 0.0 a 1.0

    r *= intensityFactor;
    g *= intensityFactor;
    b *= intensityFactor;

    // ---------- APLICAR AO LED RGB ----------
    analogWrite(RED_PIN,    255 - r);
    analogWrite(GREEN_PIN,  255 - g);
    analogWrite(BLUE_PIN,   255 - b);

    // Debug (opcional)
    
    // Serial.print("LDR: ");          Serial.println(ldrValue);
    // Serial.print("RGB: "); Serial.print(r); Serial.print(", ");
    // Serial.print(g); Serial.print(", "); Serial.println(b);
    
  
  } else { // Está escuro, desliga tudo

    for (int i = 0; i < 6; i++) {
      digitalWrite(ledPins[i], LOW);
    }

    analogWrite(RED_PIN, 255);
    analogWrite(GREEN_PIN, 255);
    analogWrite(BLUE_PIN, 255);

    delay(1000);
  }
}