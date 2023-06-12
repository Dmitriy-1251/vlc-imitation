//код передачи данных

// переменные



void transmit_MSG() {
  //FastLED.setBrightness(255);
  for (int i = 0; i < string_length; i++)
  {
    send_byte(string[i]);
  }
  FastLED.setBrightness(60);
}


void send_byte(char my_byte) {
  //if (tmr_trnsm1.tick()) {
  //if (tmr_trnsm2.tick()) {
  FastLED.setBrightness(0);
  FastLED.show();
  // }
  delay(PERIOD);

  uint8_t bin;

  for (int i = 0; i < 8; i++) {
    //if (tmr_trnsm3.tick()) {
    int led_state = bitRead(my_byte, i);
    FastLED.setBrightness(255 * (led_state != 0));
    FastLED.show();
    // }
    delay(PERIOD);
  }

  FastLED.setBrightness(255);
  FastLED.show();

  delay(PERIOD);
}
