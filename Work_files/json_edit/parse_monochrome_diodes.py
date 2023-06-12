import pandas as pd
import json
import os
import numpy as np


LED_2 = pd.read_csv('led_spd_350_700 (3).csv', delimiter=',')
LED_2 = LED_2.transpose()
LED_2 = LED_2.shift(axis=1)
LED_2.iloc[:, 0] = LED_2.index.values
LED_2.index = range(LED_2.shape[0])

# создание нового dataframe с удвоенным числом строк
new_index = pd.Index(range(LED_2.shape[0]*2-1), name='index')
new_df = pd.DataFrame(columns=LED_2.columns, index=new_index)

# копирование значений из исходного dataframe в новый
new_df.loc[LED_2.index*2] = LED_2.values



# преобразование столбцов в числовой формат и интерполяция
numeric_df = LED_2.apply(pd.to_numeric, errors='coerce')
new_df = new_df.apply(pd.to_numeric, errors='coerce')

numeric_columns = numeric_df.columns
numeric_df[numeric_columns] = numeric_df[numeric_columns].interpolate()
new_df[numeric_columns] = new_df[numeric_columns].interpolate()

print(new_df)
new_df[0] = new_df[0].astype(int)

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

# Нормализуем данные в каждом столбце, начиная со второго столбца:
new_df.iloc[:, 1:] = scaler.fit_transform(new_df.iloc[:, 1:])


new_df.to_csv (r'./data/LED_ALL.csv', index=False)