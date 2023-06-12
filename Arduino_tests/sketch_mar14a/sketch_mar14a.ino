#include <FastLED.h> // подключаем библиотеку

#define NUM_LEDS_1 2 // указываем количество светодиодов на ленте
#define NUM_LEDS_2 16 // указываем количество светодиодов на ленте
#define PIN_1 5      // указываем пин для подключения ленты
#define PIN_2 6      // указываем пин для подключения ленты

CRGB leds_1[NUM_LEDS_1];
CRGB leds_2[NUM_LEDS_2];

String DATA = "100,100,100";

void setup() {

  Serial.begin(2000000);
  Serial.setTimeout(1);

  // основные настройки для адресной ленты
  FastLED.addLeds <WS2811, PIN_1, RGB>(leds_1, NUM_LEDS_1); //.setCorrection(TypicalLEDStrip)
  FastLED.setBrightness(255);
  FastLED.addLeds <WS2811, PIN_2, GRB>(leds_2, NUM_LEDS_2); //.setCorrection(TypicalLEDStrip)
  FastLED.setBrightness(255);
}

int LED_change(byte R, byte G, byte B) {  //R G B [0-255]
  for (int i = 0; i < NUM_LEDS_1; i += 1) {
    leds_1[i] = CRGB(R, G, B); //CHSV(color*C_color, 255, 255); // задаем цвет !!!!!!!исправить [0]
    //delay(10);
  }
  for (int i = 0; i < NUM_LEDS_2; i += 8) {
    leds_2[i] = CRGB(R, G, B); //CHSV(color*C_color, 255, 255); // задаем цвет !!!!!!!исправить [0]
    //delay(10);
  }
  FastLED.show(); // отправляем информацию на ленту
}

int parse_DATA (String MyS) {
  int MyP = 0;
  int MyI = 0;
  byte array_LED[3] = {0, 0, 0};
  int index = 0;
  while (MyI >= 0) {
    MyI = MyS.indexOf(",", MyP);
    String s = MyS.substring(MyP, MyI);
    Serial.println(s + " ");
    MyP = MyI + 1;
    array_LED[index] = s.toInt();
    //Serial.println(array_LED);
    index = index + 1;
  }
  LED_change(array_LED[0], array_LED[1], array_LED[2]);
}

void loop() {
  while (!Serial.available());
  DATA = Serial.readString(); //.toInt()
  parse_DATA(DATA);
  //Serial.print(DATA);
}
