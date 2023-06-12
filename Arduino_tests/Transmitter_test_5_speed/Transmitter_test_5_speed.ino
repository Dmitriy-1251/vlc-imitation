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

int brightness = 255;
int color = 0;

byte LED_color = 0; //0 - RGB; 1 - R; 2 - G; 3 - B
byte R_L = 0;
byte G_L = 0;
byte B_L = 0;
byte LED_type = 0; //0 - Adress; 1 - Default

void setup() {
  tmr.setPeriodMode();
  //Serial.begin(9600);
  FastLED.addLeds<WS2811, PIN_1, GRB>(leds_1, NUM_LEDS_1);
  FastLED.setBrightness(255);
  FastLED.show();
  Serial.begin(1000000);


  pinMode(RED, OUTPUT);
  pinMode(GRN, OUTPUT);
  pinMode(BLU, OUTPUT);
  light = 255;
  analogWrite(RED, light);
  analogWrite(GRN, light);
  analogWrite(BLU, light);
  for (int i = 0; i < NUM_LEDS_1; i += 1) {
    leds_1[i] = CRGB(85, 85, 85);
  }
  FastLED.show();
  FastLED.setBrightness(0);
  FastLED.show();
  analogWrite(RED, 0);
  analogWrite(GRN, 0);
  analogWrite(BLU, 0);
}

void loop() {

  if (Serial.available()) {
    for (int i  = 0; i < 4; i += 1) {
      char str[16];
      sprintf(str, "\nTest_RGB_FL %d", i);
      char *string = str;
      int string_length;
      string_length = strlen(string);
      Serial.println(str);
      LED_color = 0;
      LED_type = 0;
      transmit_MSG(string, string_length);
      FastLED.setBrightness(0);
      FastLED.show();
    }
    for (int i  = 0; i < 4; i += 1) {
      char str[16];
      sprintf(str, "\nTest_RGB_DF %d", i);
      char *string = str;
      int string_length;
      string_length = strlen(string);
      Serial.println(str);
      LED_color = 0;
      LED_type = 1;
      transmit_MSG(string, string_length);
      analogWrite(RED, 0);
      analogWrite(GRN, 0);
      analogWrite(BLU, 0);
    }
    for (int i  = 0; i < 4; i += 1) {
      char str[16];
      sprintf(str, "\nTest_RED_FL %d", i);
      char *string = str;
      int string_length;
      string_length = strlen(string);
      Serial.println(str);
      LED_color = 1;
      LED_type = 0;
      transmit_MSG(string, string_length);
      FastLED.setBrightness(0);
      FastLED.show();
    }
    for (int i  = 0; i < 4; i += 1) {
      char str[16];
      sprintf(str, "\nTest_RED_DF %d", i);
      char *string = str;
      int string_length;
      string_length = strlen(string);
      Serial.println(str);
      LED_color = 1;
      LED_type = 1;
      transmit_MSG(string, string_length);
      analogWrite(RED, 0);
      analogWrite(GRN, 0);
      analogWrite(BLU, 0);
    }
    for (int i  = 0; i < 4; i += 1) {
      char str[16];
      sprintf(str, "\nTest_GRE_FL %d", i);
      char *string = str;
      int string_length;
      string_length = strlen(string);
      Serial.println(str);
      LED_color = 2;
      LED_type = 0;
      transmit_MSG(string, string_length);
      FastLED.setBrightness(0);
      FastLED.show();
    }
    for (int i  = 0; i < 4; i += 1) {
      char str[16];
      sprintf(str, "\nTest_GRE_DF %d", i);
      char *string = str;
      int string_length;
      string_length = strlen(string);
      Serial.println(str);
      LED_color = 2;
      LED_type = 1;
      transmit_MSG(string, string_length);
      analogWrite(RED, 0);
      analogWrite(GRN, 0);
      analogWrite(BLU, 0);
    }
    for (int i  = 0; i < 4; i += 1) {
      char str[16];
      sprintf(str, "\nTest_BLU_FL %d", i);
      char *string = str;
      int string_length;
      string_length = strlen(string);
      Serial.println(str);
      LED_color = 3;
      LED_type = 0;
      transmit_MSG(string, string_length);
      FastLED.setBrightness(0);
      FastLED.show();
    }
    for (int i  = 0; i < 4; i += 1) {
      char str[16];
      sprintf(str, "\nTest_BLU_DF %d", i);
      char *string = str;
      int string_length;
      string_length = strlen(string);
      Serial.println(str);
      LED_color = 3;
      LED_type = 1;
      transmit_MSG(string, string_length);
      analogWrite(RED, 0);
      analogWrite(GRN, 0);
      analogWrite(BLU, 0);
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
  if (LED_type == 0) {
    if (LED_color == 0) {
      for (int i = 0; i < NUM_LEDS_1; i += 1) {
        leds_1[i] = CRGB(85, 85, 85);
      }
    } else if (LED_color == 1) {
      for (int i = 0; i < NUM_LEDS_1; i += 1) {
        leds_1[i] = CRGB(255, 0, 0);
      }
    } else if (LED_color == 2) {
      for (int i = 0; i < NUM_LEDS_1; i += 1) {
        leds_1[i] = CRGB(0, 255, 0);
      }
    } else if (LED_color == 3) {
      for (int i = 0; i < NUM_LEDS_1; i += 1) {
        leds_1[i] = CRGB(0, 0, 255);
      }
    }
    FastLED.setBrightness(0);
    FastLED.show();
    delay(PERIOD);
    for (int i = 0; i < 8; i++) {
      FastLED.setBrightness(brightness * (bitRead(my_byte, i) != 0));
      FastLED.show();
      delay(PERIOD);
    }
    FastLED.setBrightness(brightness);
    FastLED.show();
    delay(PERIOD);  //не обяз

  }
  else {
    if (LED_color == 0) {
      R_L = 255;
      G_L = 255;
      B_L = 255;
    } else if (LED_color == 1) {
      R_L = 0;
      G_L = 255;
      B_L = 0;
    } else if (LED_color == 2) {
      R_L = 255;
      G_L = 0;
      B_L = 0;
    } else if (LED_color == 3) {
      R_L = 0;
      G_L = 0;
      B_L = 255;
    }
    light = 0;
    analogWrite(RED, 0);
    analogWrite(GRN, 0);
    analogWrite(BLU, 0);
    delay(PERIOD);
    for (int i = 0; i < 8; i++) {

      light = bitRead(my_byte, i) != 0;
      analogWrite(RED, R_L * light);
      analogWrite(GRN, G_L * light);
      analogWrite(BLU, B_L * light);
      delay(PERIOD);
    }
    light = 255;
    analogWrite(RED, R_L);
    analogWrite(GRN, G_L);
    analogWrite(BLU, B_L);

    delay(PERIOD);  //не обяз
  }

}
