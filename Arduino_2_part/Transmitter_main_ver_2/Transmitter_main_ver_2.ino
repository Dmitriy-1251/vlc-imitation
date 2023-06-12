#include <FastLED.h>
#include <TimerMs.h>
#include <EncButton.h>

// переменные
#define NUM_LEDS_2 16              // указываем количество светодиодов на ленте
#define PIN_2 6                    // указываем адресный пин для подключения ленты
#define PERIOD 3                // время между передачей каждого бита
CRGB leds_2[NUM_LEDS_2];           // создаём новую ленту
TimerMs tmr(10, 1, 0);             // задаём таймер для опроса кнопки (период, мс), (0 не запущен / 1 запущен),(режим: 0 период / 1 таймер)
TimerMs tmr_trnsm1(10, 1, 0);  
TimerMs tmr_trnsm2(10, 1, 0);  
TimerMs tmr_trnsm3(10, 1, 0);  
EncButton<EB_TICK , 12> enc;       // TODO вешаем кнопку на 12 пин для активации передачи данных
const char *string = "\nТест 1\nТест 2\nТест 3"; // TODO передаваемые данные
int string_length;                 // переменная для подсчёта символов в строке

byte array_LED[3] = {80, 0, 255}; // переменные для трёх цветов
bool enable_LED = 1;               // разрешение работы
byte swith_effect = 0;

//TODO первичная инициализация устройства
void setup() {
  Serial.begin(1000000); // TODO для парсинга
  Serial.setTimeout(0.1);// TODO для парсинга

  // добавляем светодиоды в ленту и задаём их яркость
  FastLED.addLeds <WS2811, PIN_2, GRB>(leds_2, NUM_LEDS_2); //.setCorrection(TypicalLEDStrip)
  FastLED.setBrightness(60);// TODO устанавливаем яркость в максимум
  LED_Color_change(0,0,0);// обнулем переменные при первом включении

  tmr.setPeriodMode(); // задаём таймеру режим периода
  tmr_trnsm1.setPeriodMode();
  tmr_trnsm2.setPeriodMode();
  tmr_trnsm3.setPeriodMode();
  string_length = strlen(string); // вычисляем количество символов в передаваемой строке данных
}

//главный цикл работы устройства
void loop() {
  enc.tick(); //обновляем кнопку
  //проверяем что пришло разрешение работы от первой части
  if (enable_LED) {
    //проверяем что не нажата кнопка передачи данных
    if (enc.press()) {
      //передаём сообщение при нажатой кнопке
      transmit_MSG();
    } else {
      //дежурный эффект при нормальной работе
      effect();
    }
  }

}
