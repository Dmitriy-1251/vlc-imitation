import pandas as pd
import json
from io import StringIO
# Открываем файл и загружаем в переменную data
with open('2689.json', 'r') as file:
    data = json.load(file)

# Получаем строку со значениями и сохраняем в переменную spectraldata
spectraldata = data['spectraldata']

# Преобразуем строку в pandas dataframe
df = pd.read_csv(StringIO(spectraldata), sep=',')

# Создаем новый dataframe, в котором будут храниться новые значения
df_new = pd.DataFrame(columns=['wavelength', 'relativeIntensity'])

# Проходимся по каждому значению из исходного dataframe и добавляем новые значения
for i in range(len(df)-1):
    wv1 = df.iloc[i]['wavelength']
    ri1 = df.iloc[i]['relativeIntensity']
    wv2 = df.iloc[i+1]['wavelength']
    ri2 = df.iloc[i+1]['relativeIntensity']
    step = (ri2 - ri1)/((wv2-wv1)*2)
    for j in range(int(((wv2-wv1)*2))):
        wv = wv1+ ((wv2-wv1)/10)*j
        ri = ri1+ step*j
        df_new = df_new.append({'wavelength': wv, 'relativeIntensity': ri}, ignore_index=True)

# Соединяем старый и новый dataframe в один и преобразуем его в строку
spectraldata_new = df_new.to_csv(index=False)

# Заменяем старую строку в исходном словаре новой строкой с новыми значениями
data['spectraldata'] = spectraldata_new

# Сохраняем измененный словарь в новый файл json
with open('2689_new.json', 'w') as file:
    json.dump(data, file)