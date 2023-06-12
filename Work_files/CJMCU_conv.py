import pandas as pd
import json
import os
import numpy as np
from scipy import interpolate

LED_2 = pd.read_csv('Photoresistor.txt', delimiter=',')
x = np.linspace(start=0, stop=57, num=58)
y = LED_2['y'].values
f = interpolate.interp1d(x, y, kind='linear')  # Создание интерполяционной функции
x_new = np.linspace(start=0, stop=57, num=459)
y_new = f(x_new)
LED_2_interpolated = pd.DataFrame({'x': x_new, 'y': y_new})  # Создание нового DataFrame


# генерируем значения от 200 до 1100 с шагом в 1
new_x = range(350, 809)

# заменяем значения в столбце x
LED_2_interpolated['x'] = new_x
LED_2_interpolated = LED_2_interpolated.astype(float)
min_y = LED_2_interpolated['y'].min()
max_y = LED_2_interpolated['y'].max()

# нормируем значения в столбце "y"
LED_2_interpolated['y'] = (LED_2_interpolated['y'] - min_y) / (max_y - min_y)




LED_2_interpolated = LED_2_interpolated.assign(z=LED_2_interpolated['y'], w=LED_2_interpolated['y'])
LED_2_interpolated.loc[:, 'z'] = LED_2_interpolated['y']
LED_2_interpolated.loc[:, 'w'] = LED_2_interpolated['y']


LED_2_interpolated = LED_2_interpolated.apply(pd.to_numeric)
LED_2_interpolated['x'] = LED_2_interpolated['x'].astype(int)
LED_2_interpolated['y'] = LED_2_interpolated['y'].astype(float)
print(LED_2_interpolated.head())

LED_2_interpolated.to_csv('Photoresistor_converted.csv', index=False)
print(LED_2_interpolated)
# import matplotlib.pyplot as plt
# # построение графика
# LED_2_interpolated.plot(x='x', y='y', legend=None)
# plt.show()