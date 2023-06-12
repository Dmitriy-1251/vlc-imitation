import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
import numpy as np

def Gauss(x, a, x0, s):
    return a*np.exp(-((x-x0)/s)**2)

def DoubleGauss(x, a1, x01, s1,  a2, x02, s2):
    return Gauss(x, a1, x01, s1) + Gauss(x, a2, x02, s2)



XYZ_orig_data = np.genfromtxt('../CIE_xyz_1931_2deg.csv', delimiter=',')

X = XYZ_orig_data[:, 0]
Y = XYZ_orig_data[:, 3]


# вектор начальных приближений
# 1 - нормировка по высоте
# 2 - положение максимума
# 3 - величина, пропорциональная полуширине
ip0= [0.01, 590, 10,     0.01, 420, 10] # [0.01, 590, 10,     0.01, 420, 10] #[0.01, 590, 10,     0.01, 420, 10]

# расчёт
p, cov = curve_fit(DoubleGauss, X, Y, p0=ip0, bounds=(0, [20, 600, 100,     20, 460, 100])) #[20, 600, 100,     20, 460, 100] #[20, 600, 100,     20, 460, 100]
print("Параметры гауссианов: ",p)
YY = DoubleGauss(X, *p)


# оценка погрешности аппроксимации и достоверности модели
print("Стандартное отклонение: ", np.std(Y-YY))
slope, ic, r_value, p_value, std_err = stats.linregress(Y, YY)
print("Квадрат коэффициента корреляции: ", r_value**2)


plt.plot(X, Y, 'r-', label='CIE 1931 исходный', linewidth=1)
plt.ylabel('Интенсивность')
plt.xlabel('Длины волн')
plt.plot(X, Gauss(X,p[0],p[1],p[2]),'b', linewidth=2, label='Гауссиан 1',)
plt.plot(X, Gauss(X,p[3],p[4],p[5]),'b', linewidth=2, label='Гауссиан 2',)
plt.plot(X, YY, 'g', label='Результат', linewidth=2)
plt.savefig('result.png')
plt.legend()
plt.show()
