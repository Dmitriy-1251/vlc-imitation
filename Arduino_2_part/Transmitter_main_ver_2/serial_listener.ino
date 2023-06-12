//код проверки последовательного порта на приходящие данные с первой части

// переменные
String DATA = ""; // TODO строка которая принимает данные с первой части
int TMP_array_LED[3] = {0, 0, 0};

//функция, которая слушает последовательный порт и при появлении данных передает их на парсинг
void serialEvent() {
  if (Serial.available()) {
    DATA = Serial.readString(); //.toInt()
    parse_DATA(DATA);
  }
}

//функция забирает цвета RGB со строки, отправляемой первой частью
int parse_DATA (String MyS) {
  int MyP = 0;
  int MyI = 0;
  int index = 0;
  while (MyI >= 0) {
    MyI = MyS.indexOf(",", MyP);
    String s = MyS.substring(MyP, MyI);
    //    Serial.println(s+" ");
    MyP = MyI + 1;
    TMP_array_LED[index] = s.toInt();
    //Serial.println(array_LED);
    index = index + 1;
  }
  if (TMP_array_LED[0] == 300) {
    transmit_MSG();
  }
  else
  {
    array_LED[0] = TMP_array_LED[0];
    array_LED[1] = TMP_array_LED[1];
    array_LED[2] = TMP_array_LED[2];

    //разрешаем/запрещаем работу светодиодов и отправляем цвет
    enable_LED_func();
  }

}

//проверка на включение
bool enable_LED_func() {
  if (array_LED[0] == 0 && array_LED[1] == 0 && array_LED[2] == 0) {
    enable_LED = 0;
    LED_Color_change(0, 0, 0);
  }
  else {
    enable_LED = 1;
    LED_Color_change(array_LED[0], array_LED[1], array_LED[2]);
  }
}
