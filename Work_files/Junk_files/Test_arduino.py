# Importing Libraries
import serial
import time
arduino = serial.Serial(port='COM3', baudrate=2000000, timeout=.01)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    # time.sleep(0.01)
    # print(arduino.readline())
    # print(arduino.readline())
    # print(arduino.readline())
    # print(arduino.readline())
    #data = arduino.readline()
    arduino.close()
    return 0#data
while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    #print(value) # printing the value
