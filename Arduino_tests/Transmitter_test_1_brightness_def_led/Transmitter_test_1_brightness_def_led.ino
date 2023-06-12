#include <FastLED.h>
#include <TimerMs.h>
#include <EncButton.h>

#define RED 10  // присваиваем имя RED для пина 11
#define GRN 9   // присваиваем имя GRN для пина 10
#define BLU 11  // присваиваем имя BLU для пина 9

#define NUM_LEDS_1 16
#define PIN_1 6
#define PERIOD 10

// (период, мс),
//(0 не запущен / 1 запущен),
//(режим: 0 период / 1 таймер)
TimerMs tmr(10, 1, 0);
TimerMs tmr1(10, 1, 0);
EncButton<EB_TICK, 12> enc;
CRGB leds_1[NUM_LEDS_1];
CHSV hsv;
//int i = 0;
int light = 0;

int brightness;
int color = 0;
// 0 - R; 1 - G, 2 - B, 3 - RG, 4 - RB, 5 - GB, 6 - RGB
byte R_L = 0;
byte G_L = 0;
byte B_L = 0;


void setup() {
  tmr.setPeriodMode();
  //Serial.begin(9600);
  FastLED.addLeds<WS2811, PIN_1, GRB>(leds_1, NUM_LEDS_1);
  FastLED.setBrightness(255);
  FastLED.show();
  Serial.begin(1000000);
//  for (int i = 0; i < NUM_LEDS_1; i += 1) {
//    leds_1[i] = CRGB(85, 85, 85);
//  }
//  FastLED.show();  // отправляем информацию на ленту

    pinMode(RED, OUTPUT);  // используем Pin11 для вывода
    pinMode(GRN, OUTPUT);  // используем Pin10 для вывода
    pinMode(BLU, OUTPUT);  // используем Pin9 для вывода
      light = 255;
      analogWrite(RED, light);
      analogWrite(GRN, light);
      analogWrite(BLU, light);
}

void loop() {
  // enc.tick();
  // if (enc.press()) {
  //   transmit_MSG();
  // } else {
  //   effect();
  // }
    if (Serial.available()) {
      for (brightness = 0; brightness <255; brightness+=5) {
        char str[16];
        sprintf(str, "\nTest %d", brightness);
        char *string = str;
        int string_length;
        string_length = strlen(string);
        Serial.println(str);
        transmit_MSG(string, string_length);
        //delay(200);
      }
    }
  //  if (Serial.available()) {
  //    transmit_MSG();
  //    int val = Serial.parseInt();
  //    //Serial.println(val);
  //  }


}


void transmit_MSG(char *string, int string_length) {
  //FastLED.setBrightness(255);

  for (int i = 0; i < string_length; i++) {
    send_byte(string[i]);
  }
}



void send_byte(char my_byte) {
//  FastLED.setBrightness(0);
//  FastLED.show();
    light = 0;
    analogWrite(RED, 0);
    analogWrite(GRN, 0);
    analogWrite(BLU, 0);
  delay(PERIOD);



  for (int i = 0; i < 8; i++) {
//    FastLED.setBrightness(brightness * (bitRead(my_byte, i) != 0));
//    FastLED.show();
        light = bitRead(my_byte, i) != 0;
        analogWrite(RED, brightness * light);
        analogWrite(GRN, brightness * light);
        analogWrite(BLU, brightness * light);
    delay(PERIOD);
  }


    light = 255;
    analogWrite(RED, brightness);
    analogWrite(GRN, brightness);
    analogWrite(BLU, brightness);
//  FastLED.setBrightness(brightness);
//  FastLED.show();
  delay(PERIOD);  //не обяз
}


//void effect() {
//  // for (int i = 0; i < NUM_LEDS_1; i += 1) {
//  //   leds_1[i] = CHSV(180, 255, 255);
//  // }
//  // FastLED.show();  // отправляем информацию на ленту
//  light = 255;
//  analogWrite(RED, light);
//  analogWrite(GRN, light);
//  analogWrite(BLU, light);
//}
