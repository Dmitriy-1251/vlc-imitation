//описание возможных эффектов в режиме ожидания передачи данных

// переменные
byte newH;

void effect() {
  switch (swith_effect) {
    case 0: ligh_ON();
      break;
    case 1: ligh_pulse();
      break;
    default: Serial.println("def");
      break;
  }
}

void ligh_ON() {
  if (tmr.tick()) {
    LED_Color_change(array_LED[0], array_LED[1], array_LED[2]);
  }
}

//пульсирующая яркость(нужно переписить с нормальным допуском)
void ligh_pulse() {
  // Определяем случайное изменение
  newH = random(160, 255);

  while (array_LED[2] - newH > 0) {
    if (tmr.tick()) {
      array_LED[2] -= 1;
      // Применяем изменение к текущему цвету
      LED_Color_change(array_LED[0], array_LED[1], array_LED[2]);
    }
  }

  while (array_LED[2] - newH < 0) {
    if (tmr.tick()) {
      array_LED[2] += 1;
      // Применяем изменение к текущему цвету
      LED_Color_change(array_LED[0], array_LED[1], array_LED[2]);
    }
  }
}

// функция изменяет цвет светодиодов
int LED_Color_change(byte color_0, byte color_1, byte color_2) {
  for (int i = 0; i < NUM_LEDS_2; i += 1) {
    leds_2[i] = CHSV(color_0, color_1, color_2);
  }
  FastLED.show(); // отправляем информацию на ленту
}
