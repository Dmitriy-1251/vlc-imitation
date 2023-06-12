import pandas as pd
import json
import os
import numpy as np
# создаем пустой список для хранения данных из файлов json
data = []

pd.set_option('display.max_colwidth', 500)

# перебираем все файлы с расширением "json" в папке "data"
for file in os.listdir("data"):
    if file.endswith(".json"):
        # читаем данные из файла json в новую переменную
        with open(os.path.join("data", file)) as f:
            json_data = json.load(f)
        # добавляем данные из файла в список
        data.append(json_data)

# создаем DataFrame из списка данных
df = pd.DataFrame(data)
df = df.iloc[:, [1, 2, 17]]
# print(df) # выводим первые 5 строк DataFrame
prefix = df.iloc[:, [0]] #0,1

df[['spectrum_name', 'spectrum_data']] = df['spectraldata'].str.split(pat='\n', n=1, expand=True)
df = df.iloc[:, [0, 4]]

# Разбиваем строку по разделителю \r\n
data = df['spectrum_data'].str.split('\r\n')

# Применяем функцию pd.Series() к каждой строке
data = data.apply(lambda x: pd.Series(x))

# Удаляем последний столбец, который будет содержать только символы \n
data = data.iloc[:, :-1]

data.columns = [col.split(",")[0] for col in data.iloc[0]]
df = data

# удаляем символы до запятой в каждой ячейке
df = df.astype(str).applymap(lambda x: x.split(',')[1] if ',' in x else x)
df = df.filter(regex='^(?!.*\.50)')


df_transposed = df.transpose()
df_transposed = df_transposed.iloc[87:558, :]
df = df_transposed

# df.iloc[:, 0] = df.iloc[:, 0].astype(float).round().astype(int)

# сдвиг всех столбцов вправо
df = df.shift(axis=1)
df = df.shift(axis=1)
# # изменение значения первого столбца
df.iloc[:, 1] = df.index.values

# сбросить значения индексов столбцов
df.columns = range(df.shape[1])
df.index = range(df.shape[0])
# # изменение значения первого столбца
df.iloc[:, 0] = df.index.values



from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

df.replace('', np.nan, inplace=True)

df = df.astype(float)
df = df.fillna(0)
# Нормализуем данные в каждом столбце, начиная со второго столбца:
df.iloc[:, 2:] = scaler.fit_transform(df.iloc[:, 2:])

print(df)
# df = df.fillna(0)
df.to_csv (r'./data/LAMP_DATA_test_1.csv', index=False) #