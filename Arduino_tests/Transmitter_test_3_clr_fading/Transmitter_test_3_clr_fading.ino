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
TimerMs tmr(5, 1, 0);
TimerMs tmr1(10, 1, 0);
EncButton<EB_TICK, 12> enc;
CRGB leds_1[NUM_LEDS_1];
CHSV hsv;
//int i = 0;
int light = 0;

int brightness = 255;
int fading = 0;
int st = 0;
int color = 0;
// 0 - R; 1 - G, 2 - B, 3 - RG, 4 - RB, 5 - GB, 6 - RGB
byte R_L = 0;
byte G_L = 0;
byte B_L = 0;
byte array_LED[3] = {0, 255, 255};//HSV

void setup() {
  tmr.setPeriodMode();
  //Serial.begin(9600);
  FastLED.addLeds<WS2811, PIN_1, GRB>(leds_1, NUM_LEDS_1);
  FastLED.setBrightness(brightness);
  FastLED.show();
  Serial.begin(1000000);
  //  for (int i = 0; i < NUM_LEDS_1; i += 1) {
  //    leds_1[i] = CRGB(85, 85, 85);
  //  }
  LED_Color_change(array_LED[0], array_LED[1], array_LED[2]);
  FastLED.show();  // отправляем информацию на ленту

  //  pinMode(RED, OUTPUT);  // используем Pin11 для вывода
  //  pinMode(GRN, OUTPUT);  // используем Pin10 для вывода
  //  pinMode(BLU, OUTPUT);  // используем Pin9 для вывода
  //    light = 255;
  //    analogWrite(RED, light);
  //    analogWrite(GRN, light);
  //    analogWrite(BLU, light);
}

void loop() {

  if (Serial.available()) {

    for (fading = 0; fading < 255; fading = fading + 3) {
      for (st = 1; st < 2; st++) {
        //array_LED[2] = 85;
        //ligh_pulse();
        char str[16];
        sprintf(str, "\nTest %d", fading);
        char *string = str;
        int string_length;
        string_length = strlen(string);
        Serial.println(str);
        transmit_MSG(string, string_length);
        //delay(200);
        //array_LED[0] = 255;
        ligh_pulse();
      }
    }
  }
}


void transmit_MSG(char *string, int string_length) {
  //FastLED.setBrightness(255);

  for (int i = 0; i < string_length; i++) {
    send_byte(string[i]);
  }
}



void send_byte(char my_byte) {
  FastLED.setBrightness(0);
  FastLED.show();
  //  light = 0;
  //  analogWrite(RED, 0);
  //  analogWrite(GRN, 0);
  //  analogWrite(BLU, 0);
  delay(PERIOD);



  for (int i = 0; i < 8; i++) {
    FastLED.setBrightness(brightness * (bitRead(my_byte, i) != 0));
    FastLED.show();
    //    light = bitRead(my_byte, i) != 0;
    //    analogWrite(RED, brightness * light);
    //    analogWrite(GRN, brightness * light);
    //    analogWrite(BLU, brightness * light);
    delay(PERIOD);
  }


  //  light = 255;
  //  analogWrite(RED, brightness);
  //  analogWrite(GRN, brightness);
  //  analogWrite(BLU, brightness);
  FastLED.setBrightness(brightness);
  FastLED.show();
  delay(PERIOD);  //не обяз
}




int newH;

void ligh_pulse() {
  // Определяем случайное изменение
  int oldH = array_LED[0];
  newH = fading; //random(255-fading, 255-fading*2);


  while (array_LED[0] - newH < 0) {
    if (tmr.tick()) {
      array_LED[0] += st;
      // Применяем изменение к текущему цвету
      LED_Color_change(array_LED[0], array_LED[1], array_LED[2]);
    }
  }
//  while (array_LED[0] - oldH < 0) {
//    if (tmr.tick()) {
//      array_LED[0] += st;
//      // Применяем изменение к текущему цвету
//      LED_Color_change(array_LED[0], array_LED[1], array_LED[2]);
//    }
//  }

}

// функция изменяет цвет светодиодов
int LED_Color_change(byte color_0, byte color_1, byte color_2) {
  for (int i = 0; i < NUM_LEDS_1; i += 1) {
    leds_1[i] = CHSV(color_0, color_1, color_2);
  }
  FastLED.show(); // отправляем информацию на ленту
}
