import numpy as np
import math
import matplotlib.pyplot as plt
from scipy. stats import norm
import matplotlib as mpl
import warnings as wr
from sklearn.metrics import mean_squared_error
from sklearn.metrics import max_error
from matplotlib.patches import Rectangle

# Importing Libraries
import serial
import time
#arduino = serial.Serial(port='COM3', baudrate=2000000, timeout=.1)


def XYZMultiLobeFit1931_X(wavelen):
    dParam1 = (wavelen - 442.0) * (0.0624 if (wavelen < 442.0) else 0.0374)
    dParam2 = (wavelen - 599.8) * (0.0264 if (wavelen < 599.8) else 0.0323)
    dParam3 = (wavelen - 501.1) * (0.0490 if (wavelen < 501.1) else 0.0382)
    return 0.362 * math.exp(-0.5 * dParam1 * dParam1) + 1.056 * math.exp(-0.5 * dParam2 * dParam2) - 0.065 * math.exp(
        -0.5 * dParam3 * dParam3)


def XYZMultiLobeFit1931_Y(wavelen):
    dParam1 = (wavelen - 568.8) * (0.0213 if (wavelen < 568.8) else 0.0247)
    dParam2 = (wavelen - 530.9) * (0.0613 if (wavelen < 530.9) else 0.0322)
    return 0.821 * math.exp(-0.5 * dParam1 * dParam1) + 0.286 * math.exp(-0.5 * dParam2 * dParam2)


def XYZMultiLobeFit1931_Z(wavelen):
    dParam1 = (wavelen - 437.0) * (0.0845 if (wavelen < 437.0) else 0.0278)
    dParam2 = (wavelen - 459.0) * (0.0385 if (wavelen < 459.0) else 0.0725)
    return 1.217 * math.exp(-0.5 * dParam1 * dParam1) + 0.681 * math.exp(-0.5 * dParam2 * dParam2)

def XYZ_My_approx(wavelen):
    a = 1.0621499167932749
    x = wavelen
    x0 = 596.451688074109
    s = 47.53639992824365

    a1 = 0.13763320684843405
    x1 = wavelen
    x01 = 430.778713687185
    s1 = 14.54463117734572

    a2 = 0.3200105894892027
    x2 = wavelen
    x02 = 451.99999999999994
    s2 = 24.831725943384523
    CIE_X = a*np.exp(-((x-x0)/s)**2) + a1*np.exp(-((x1-x01)/s1)**2) + a2*np.exp(-((x2-x02)/s2)**2)

    Y_params = [1.01905504e+00, 5.59067717e+02, 5.91643457e+01, 5.81917422e-03, 4.40762790e+02, 1.12427186e+01]
    CIE_Y = Y_params[0] * np.exp(-((wavelen - Y_params[1]) / Y_params[2]) ** 2) + Y_params[3] * np.exp(-((wavelen - Y_params[4]) / Y_params[5]) ** 2)

    Z_params = [  1.66747628, 454.83950835,  31.14972175,   0.52869655, 433.95783091,  13.65315252]
    CIE_Z = Z_params[0] * np.exp(-((wavelen - Z_params[1]) / Z_params[2]) ** 2) + Z_params[3] * np.exp(-((wavelen - Z_params[4]) / Z_params[5]) ** 2)
    return CIE_X, CIE_Y, CIE_Z

def adj(i, C):
    if C < 0:
        #wr.warn("Complex value! Wavelength = " + str(i) + " (" + str(C) + " < 0)")
        return 0
    elif abs(C) <= 0.0031308:
        return 12.92 * C
    else:
        return 1.055 * pow(C, 0.41666) - 0.055


def XYZ_to_RGB(i, X, Y, Z):
    R = 3.2404542 * X - 1.5371385 * Y - 0.4985314 * Z
    G = -0.9692660 * X + 1.8760108 * Y + 0.0415560 * Z
    B = 0.0556434 * X - 0.2040259 * Y + 1.0572252 * Z
    if i == -1:
        # обнуляем потери
        if R < 0:
            R = 0
        if G < 0:
            G = 0
        if B < 0:
            B = 0
        # нормализуем значения RGB
        R_norm = R / (R + G + B)
        G_norm = G / (R + G + B)
        B_norm = B / (R + G + B)

        # корректируем яркость
        R_norm, G_norm, B_norm = adj(i, R_norm), adj(i, G_norm), adj(i, B_norm)

        # возвращаем значения для нормализации в преобразовании спектра в цвет
        return R_norm, G_norm, B_norm
    else:
        # корректируем яркость значений для всего диапазона
        R, G, B = adj(i, R), adj(i, G), adj(i, B)
    return R, G, B


def XYZ_to_RGB_2(i, X, Y, Z):
    R = 1.909 * X - 0.532 * Y - 0.288 * Z
    G = -0.985 * X + 1.997 * Y - 0.028 * Z
    B = 0.058 * X - 0.119 * Y + 0.902 * Z
    R, G, B = adj(i, R), adj(i, G), adj(i, B)
    return R, G, B


def RGB_norm(Colors):
    Colors = (Colors - np.min(Colors)) / (np.max(Colors) - np.min(Colors))
    return Colors
def get_nearest_value(iterable, value):
    index, val = min(enumerate(iterable), key=lambda x: abs(x[1] - value))
    return val, index


def test_all(flag, XYZ_approx,WL):
    # определяем и выводим тестируемый спектр
    x = np.arange(360, 831, 1)
    #test_spectrum = RGB_norm(norm.pdf(x, WL, 20))
    test_spectrum = Lamp_test[:, TESTING_SPECTRE] #1 - теплый розовый 12 - синий 2 - желтый
    #test_spectrum = RGB_norm(test_spectrum)
    if flag !=-1:
        ax_3.plot(x, test_spectrum, label=('Спектр '+ str(TESTING_SPECTRE)))
    #print(test_spectrum)
    # берём веса спектра, умножаем на табличные веса чтобы получить значение влияния канала на общий спектр
    X = np.sum(test_spectrum * XYZ_approx[:, 0])
    Y = np.sum(test_spectrum * XYZ_approx[:, 1])
    Z = np.sum(test_spectrum * XYZ_approx[:, 2])
    # print(X)
    # print(Y)
    # print(Z)
    # # сопоставляем XYZ и рассчитанные ранее функции
    # X_val, X_index = get_nearest_value(XYZ_approx[:, 0], X)
    # Y_val, Y_index = get_nearest_value(XYZ_approx[:, 1], Y)
    # Z_val, Z_index = get_nearest_value(XYZ_approx[:, 2], Z)
    # print(X_val, X_index)
    # print(Y_val, Y_index)
    # print(Z_val, Z_index)

    # преобразуем в RGB с корректировками и нормализацией внутри внешней функции
    R_norm, G_norm, B_norm = XYZ_to_RGB(-1, X, Y, Z)

    if flag != -1:
        #print(WL)
        print(R_norm, G_norm, B_norm)
    return R_norm, G_norm, B_norm


def write_read(x):
    time.sleep(2)
    arduino.write(bytes(x, 'utf-8'))
    #data = arduino.readline()
    return 0#data


def test_color_A(XYZ_approx,Fotopic,Human,Lamp_test, WL):
    R_norm, G_norm, B_norm = test_all(0,XYZ_approx,WL)
    ax_4.add_patch(Rectangle((700, 0.2), 100, 0.4, facecolor = (R_norm, G_norm, B_norm), fill=True, lw=5)) #, color=(r_srgb, g_srgb, b_srgb)
    #x = str(round(R_norm*255))+","+str(round(G_norm*255))+","+str(round(B_norm*255))
    #print(x)
    #write_read(x)

    #ax_4.add_patch(Rectangle((700, 0.2), 100, 0.2, facecolor = (R_norm * Human[WL- WL_min, 1], G_norm * Human[WL- WL_min, 2], B_norm * Human[WL- WL_min, 3]), fill=True, lw=5))
    null_mass = np.zeros((30, 2))
    null_mass_1 = np.zeros((30, 4))
    Fotopic = np.concatenate((null_mass,Fotopic), axis=0)
    Human = np.concatenate((null_mass_1, Human), axis=0)
    Human_view = np.zeros((WL_max - WL_min, 3))
    # TODO возможно заменить i в цикле на WL и убрать цикл тк она нужен только для оценки всего
    for i in range(WL_min, WL_max, 1):
        R_norm, G_norm, B_norm = test_all(-1,XYZ_approx,i) #
        ax_7.vlines(i, ymin=-0.1, ymax=0, linewidth=2, color=(R_norm, G_norm, B_norm))
        ax_7.vlines(i, ymin=-0.2, ymax=-0.1, linewidth=2, color=(R_norm*Fotopic[i - WL_min,1], G_norm*Fotopic[i - WL_min,1], B_norm*Fotopic[i - WL_min,1]))

        ax_4.vlines(i, ymin=-0.1, ymax=0, linewidth=2, color=(R_norm, G_norm, B_norm))
        ax_4.vlines(i, ymin=-0.2, ymax=-0.1, linewidth=2, color=(R_norm * Human[i - WL_min, 1], G_norm * Human[i - WL_min, 2], B_norm * Human[i - WL_min, 3]))

        ax_1.vlines(i, ymin=-0.6, ymax=-0.5, linewidth=2, color=(R_norm, G_norm, B_norm))
        ax_1.vlines(i, ymin=-0.7, ymax=-0.6, linewidth=2, color=(R_norm * Human[i - WL_min, 1], G_norm * Human[i - WL_min, 2], B_norm * Human[i - WL_min, 3]))
        ax_1.vlines(i, ymin=-0.8, ymax=-0.7, linewidth=2, color=(R_norm * Fotopic[i - WL_min, 1], G_norm * Fotopic[i - WL_min, 1], B_norm * Fotopic[i - WL_min, 1]))

        Human_view[i- WL_min, 0], Human_view[i- WL_min, 1], Human_view[i- WL_min, 2] = R_norm * Human[i - WL_min, 1], G_norm * Human[i - WL_min, 2], B_norm * Human[i - WL_min, 3]
        ax_5.vlines(i, ymin=-0.1, ymax=0, linewidth=2, color=(R_norm * Human[i - WL_min, 1], G_norm * Human[i - WL_min, 2], B_norm * Human[i - WL_min, 3]))
    ax_5.plot(range(WL_min, WL_max, 1), Human_view[:, 0], 'r-', range(WL_min, WL_max, 1), Human_view[:, 1], 'g--', range(WL_min, WL_max, 1), Human_view[:, 2], 'b.')
    return 0#X_index, Y_index, Z_index
def test_color_B(XYZ_approx,X_index, Y_index, Z_index):

    # сопоставляем XYZ и рассчитанные ранее функции
    print(X_index)
    R_val = XYZ_approx[X_index, 0]
    G_val = XYZ_approx[Y_index, 1]
    B_val = XYZ_approx[Z_index, 2]

    ax_4.add_patch(Rectangle((700, 0.1), 100, 0.5, facecolor=(R_val, G_val, B_val), fill=True,lw=5))  # , color=(r_srgb, g_srgb, b_srgb)
    return 0

if __name__ == '__main__':
    # объявление переменных
    TESTING_WL = 430
    TESTING_SPECTRE = 12 # [1, 14]
    WL_min = 360
    WL_max = 831
    G = np.zeros((WL_max - WL_min, 3))
    My_approx = np.zeros((WL_max - WL_min, 3))
    # настройки плоттера
    fig = plt.figure(figsize=(18, 9))
    fig.subplots_adjust(**{"left": 0.03, "bottom": 0.03, "right": .99, "top": .97, "wspace": .08, "hspace": .2})
    ax_1 = fig.add_subplot(2, 2, 1)
    plt.title("Референсные значения XYZ + вычисленные XYZ по аппроксимации", size = 10)
    ax_2 = fig.add_subplot(4, 2, 5)
    plt.title("Ошибка м/у референсным XYZ и аппрокcимацией", size = 10)
    ax_3 = fig.add_subplot(3, 2, 2)
    plt.title("Пример спектра источника", size = 10)
    plt.ylim(0, 1)
    ax_4 = fig.add_subplot(3, 4, 7)
    plt.title("Спектральная чувствительность клеток человека, S, M и L типов", size = 7)
    ax_5 = fig.add_subplot(3, 2, 6)
    plt.title("Спектр источника, видимый человеком", size=10)
    plt.ylim(-0.1, 1)
    ax_6 = fig.add_subplot(4, 2, 7)
    plt.title("Ошибка м/у референсным XYZ и моей аппрокcимацией", size=10)
    ax_7 = fig.add_subplot(3, 4, 8)
    plt.title("Функция чувствительности зрения человека", size = 9)

    ax_1.grid(True)
    ax_2.grid(True)


    #импортируем оригинального двухградусного наблюдателя 1931 года и строим на графике
    XYZ_orig_data = np.genfromtxt('Files//CIE_xyz_1931_2deg.csv', delimiter=',')
    ax_1.plot(XYZ_orig_data[:,0], XYZ_orig_data[:,1], 'm-', XYZ_orig_data[:,0], XYZ_orig_data[:,2], 'y--', XYZ_orig_data[:,0], XYZ_orig_data[:,3], 'c.', label='CIExyz1931_2deg')

    # преобразуем значение длины волны в XYZ на всём диапазоне
    for i in range(WL_min, WL_max, 1):
        G[i - WL_min, 0], G[i - WL_min, 1], G[i - WL_min, 2] = XYZMultiLobeFit1931_X(i), XYZMultiLobeFit1931_Y(
            i), XYZMultiLobeFit1931_Z(i)

    for i in range(WL_min, WL_max, 1):
        My_approx[i - WL_min, 0], My_approx[i - WL_min, 1], My_approx[i - WL_min, 2] = XYZ_My_approx(i)

    # импортируем функцию восприятия яркости человеком и строим на графике
    Fotopic = np.genfromtxt('Work_files//linCIE2008v2e_1.csv', delimiter=',')
    ax_7.plot(Fotopic[:, 0], Fotopic[:, 1], 'k-', label='Fotopic')

    # реакция рецепторов человека
    Human = np.genfromtxt('Files//linss2_10e_1 (1).csv', delimiter=',', filling_values=0)
    ax_4.plot(Human[:, 0], Human[:, 1], 'r-', Human[:, 0], Human[:, 2], 'g--',
              Human[:, 0], Human[:, 3], 'b.',label='LMS-cones')

    # забираем тестовые значения лампочек
    Lamp_test = np.genfromtxt('Work_files//cri_1nm — копия.txt', delimiter=' ', filling_values=0)
    #ax_5.plot(Lamp_test[:, 0], Lamp_test[:, 5], label='test')

    #запускаем тестируемую функцию, пока не изменились значения в G
    test_color_A(G, Fotopic, Human, Lamp_test, TESTING_WL) #X_index, Y_index, Z_index =








    # строим три графика преобразованных кривых
    ax_1.plot(range(WL_min, WL_max, 1), My_approx[:, 0], 'k-', range(WL_min, WL_max, 1), My_approx[:, 1], 'k--',range(WL_min, WL_max, 1), My_approx[:, 2], 'k.', linewidth=1, label='Моя аппрокс') # мой
    ax_1.plot(range(WL_min, WL_max, 1), G[:, 0], 'r-', range(WL_min, WL_max, 1), G[:, 1], 'g--', range(WL_min, WL_max, 1), G[:, 2], 'b.', label='Найденная аппрокс(CMF)') # их

    #считаем ошибку между референсными и подсчитанными и строим график ошибки
    XYZ_orig_data = np.delete(XYZ_orig_data, 0, 1)
    diff = G - XYZ_orig_data

    print("max squared error CIE и NW X: " + str(max_error(G[:, 0], XYZ_orig_data[:, 0])))
    print("max squared error CIE и NW Y: " + str(max_error(G[:, 1], XYZ_orig_data[:, 1])))
    print("max squared error CIE и NW Z: " + str(max_error(G[:, 2], XYZ_orig_data[:, 2])))
    print("mean_squared_error CIE и NW X: " + str(mean_squared_error(G[:, 0], XYZ_orig_data[:, 0])))
    print("mean_squared_error CIE и NW Y: " + str(mean_squared_error(G[:, 1], XYZ_orig_data[:, 1])))
    print("mean_squared_error CIE и NW Z: " + str(mean_squared_error(G[:, 2], XYZ_orig_data[:, 2])))
    ax_2.plot(range(WL_min, WL_max, 1), diff[:, 0], 'r-', range(WL_min, WL_max, 1), diff[:, 1], 'g-',
              range(WL_min, WL_max, 1), diff[:, 2], 'b-', label='Ошибка CMF-CIExyz')

    diff_my = My_approx - XYZ_orig_data
    ax_6.plot(range(WL_min, WL_max, 1), diff_my[:, 0], 'r-', range(WL_min, WL_max, 1), diff_my[:, 1], 'g-', range(WL_min, WL_max, 1), diff_my[:, 2], 'b-',label='Ошибка Моя-CIExyz')

    print("max squared error  CIE и Я X:" + str(max_error(My_approx[:, 0], XYZ_orig_data[:, 0])))
    print("max squared error  CIE и Я Y:" + str(max_error(My_approx[:, 1], XYZ_orig_data[:, 1])))
    print("max squared error  CIE и Я Z:" + str(max_error(My_approx[:, 2], XYZ_orig_data[:, 2])))
    print("mean_squared_error  CIE и Я X:" + str(mean_squared_error(My_approx[:, 0], XYZ_orig_data[:, 0])))
    print("mean_squared_error  CIE и Я Y:" + str(mean_squared_error(My_approx[:, 1], XYZ_orig_data[:, 1])))
    print("mean_squared_error  CIE и Я Z:" + str(mean_squared_error(My_approx[:, 2], XYZ_orig_data[:, 2])))
    # преобразуем значения XYZ в RGB на всём диапазоне
    for i in range(WL_min, WL_max, 1):
        G[i - WL_min, 0], G[i - WL_min, 1], G[i - WL_min, 2] = XYZ_to_RGB(i, G[i - WL_min, 0], G[i - WL_min, 1], G[i - WL_min, 2]) #спектр по их аппроксимации
        XYZ_orig_data[i - WL_min, 0], XYZ_orig_data[i - WL_min, 1], XYZ_orig_data[i - WL_min, 2] = XYZ_to_RGB(i, XYZ_orig_data[i - WL_min, 0], XYZ_orig_data[i - WL_min, 1], XYZ_orig_data[i - WL_min, 2]) #спектр CIE
        My_approx[i - WL_min, 0], My_approx[i - WL_min, 1], My_approx[i - WL_min, 2] = XYZ_to_RGB(i, My_approx[i - WL_min, 0], My_approx[i - WL_min, 1], My_approx[i - WL_min, 2])  # спектр по моей аппроксимации

    # нормализация массива по каналам
    G[:, 0], G[:, 1], G[:, 2] = RGB_norm(G[:, 0]), RGB_norm(G[:, 1]), RGB_norm(G[:, 2])#спектр по их аппроксимации
    XYZ_orig_data[:, 0], XYZ_orig_data[:, 1], XYZ_orig_data[:, 2] = RGB_norm(XYZ_orig_data[:, 0]), RGB_norm(XYZ_orig_data[:, 1]), RGB_norm(XYZ_orig_data[:, 2]) #спектр CIE
    My_approx[:, 0], My_approx[:, 1], My_approx[:, 2] = RGB_norm(My_approx[:, 0]), RGB_norm(My_approx[:, 1]), RGB_norm(My_approx[:, 2]) # спектр по моей аппроксимации

    # test_color_B(G,X_index, Y_index, Z_index)

    # рисуем преобразованный спектр
    for i in range(WL_min, WL_max, 1):
        ax_1.vlines(i, ymin=-0.1, ymax=0, linewidth=2, color=(G[i - WL_min, 0], G[i - WL_min, 1], G[i - WL_min, 2])) #спектр по их аппроксимации
        ax_1.vlines(i, ymin=-0.3, ymax=-0.2, linewidth=2, color=(XYZ_orig_data[i - WL_min, 0], XYZ_orig_data[i - WL_min, 1], XYZ_orig_data[i - WL_min, 2]))  #спектр CIE
        ax_1.vlines(i, ymin=-0.1, ymax=-0.2, linewidth=2, color=(abs(G[i - WL_min, 0] - XYZ_orig_data[i - WL_min, 0]), abs(G[i - WL_min, 1] - XYZ_orig_data[i - WL_min, 1]), abs(G[i - WL_min, 2] - XYZ_orig_data[i - WL_min, 2])))# разность спектров их и оригинал
        ax_1.vlines(i, ymin=-0.5, ymax=-0.4, linewidth=2, color=(My_approx[i - WL_min, 0], My_approx[i - WL_min, 1], My_approx[i - WL_min, 2]))  # спектр по моей аппроксимации
        ax_1.vlines(i, ymin=-0.4, ymax=-0.3, linewidth=2, color=(
        abs(My_approx[i - WL_min, 0] - XYZ_orig_data[i - WL_min, 0]), abs(My_approx[i - WL_min, 1] - XYZ_orig_data[i - WL_min, 1]),
        abs(My_approx[i - WL_min, 2] - XYZ_orig_data[i - WL_min, 2])))  # разность спектров моего и оригинал

    ax_1.legend(loc=1, prop={'size': 6})#
    ax_2.legend()
    ax_3.legend()
    ax_4.legend()
    #ax_5.legend()
    ax_6.legend()
    ax_7.legend()
    plt.show()


