#include <FastLED.h>

#define RED 10  // присваиваем имя RED для пина 11
#define GRN 9   // присваиваем имя GRN для пина 10
#define BLU 11  // присваиваем имя BLU для пина 9

#define NUM_LEDS_1 16
CRGB leds_1[NUM_LEDS_1];
//#define PERIOD 10
int brightness = 255;
byte R_L = 0;
byte G_L = 0;
byte B_L = 0;
int light = 0;

class LEDTester {
  private:
    int PERIOD;
  public:
    void setPeriod(int newPeriod) {
      PERIOD = newPeriod;
    }
    void runTest(int LED_color, int LED_type) {
      char str[16];
      for (int i = 0; i < 4; i++) {
        switch (LED_type) {

          case 0:
            switch (LED_color) {
              case 0: // RGB_FL
                sprintf(str, "\nTest_RGB_FL %d", i);
                break;
              case 1: // RED_FL
                sprintf(str, "\nTest_RED_FL %d", i);
                break;
              case 2: // GRE_FL
                sprintf(str, "\nTest_GRE_FL %d", i);
                break;
              case 3: // BLU_FL
                sprintf(str, "\nTest_BLU_FL %d", i);
                break;
            }
            break;
          case 1:
            switch (LED_color) {
              case 0: // RGB_DF
                sprintf(str, "\nTest_RGB_DF %d", i);
                break;
              case 1: // RED_DF
                sprintf(str, "\nTest_RED_DF %d", i);
                break;
              case 2: // GRE_DF
                sprintf(str, "\nTest_GRE_DF %d", i);
                break;
              case 3: // BLU_DF
                sprintf(str, "\nTest_BLU_DF %d", i);
                break;
            }
            break;
        }
        char *string = str;
        int string_length = strlen(string);
        Serial.println(str);
        transmit_MSG(string, string_length, LED_color, LED_type);
      }
    }
    void transmit_MSG(char *string, int string_length, int LED_color, int LED_type) {
      //FastLED.setBrightness(255);

      for (int i = 0; i < string_length; i++) {
        send_byte(string[i], LED_color, LED_type);
      }
      FastLED.setBrightness(0);
      FastLED.show();
      analogWrite(RED, 0);
      analogWrite(GRN, 0);
      analogWrite(BLU, 0);
    }


    void send_byte(char my_byte, int LED_color, int LED_type) {
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
};
