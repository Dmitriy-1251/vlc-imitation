#define LDR_PIN A2 //A1 - Photoresistor GL55, A2 - Photodiode CJMCU-101
#define THRESHOLD 500
#define PERIOD 10

bool previous_state;
bool current_state;

// определение времени выполнения программного блока Ардуино

unsigned int  timerValue; // значение таймера


void setup() {
  pinMode(LDR_PIN, INPUT);
  Serial.begin(1000000);
  //    // установки таймера 1
  //  TCCR1A = 0;
  //  TCCR1B = 0;
}

void loop() {
  current_state = get_ldr();

  if (!current_state && previous_state)
  {
    print_byte(get_byte());
  }
  previous_state = current_state;
}

bool get_ldr()
{
  int voltage = analogRead(LDR_PIN);
  //Serial.println(voltage);
  return voltage > THRESHOLD ? true : false;
}

char get_byte() {
  char ret = 0;
  delay(1.5 * PERIOD);
  for (int i = 0; i < 8; i++)
  {
    ret = ret | get_ldr() << i;
    delay(PERIOD);
  }
  return ret;
}

void print_byte(char my_byte)
{
  char buff[2];
  sprintf(buff, "%c", my_byte);
  Serial.print(buff);
}
