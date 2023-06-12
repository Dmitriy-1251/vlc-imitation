import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
import numpy as np


def Gauss(x, a, x0, s):
    return a*np.exp(-((x-x0)/s)**2)

def nGauss(x, *p):
    n = len(p)//3
    res = 0
    for i in range(n):
        res += Gauss(x, p[i*3], p[i*3+1], p[i*3+2])
    return res

def plotAllGauss(X, p):
    n = len(p)//3
    for i in range(n):
        #i+=1
        plt.plot(X, Gauss(X,p[i*3],p[i*3+1],p[i*3+2]), 'b', linewidth=2)


# начальные приближения для трёх гауссианов
ip0= [0.01, 590, 10,     0.34, 441, 10,     0.33, 450, 10]
# верхняя граница
top_limits = [20, 600, 100,     0.36, 443, 100,     0.338, 452, 100]
# нижняя граница
bottom_limits = [0, 0, 0,     0, 0, 0,     0, 0, 0]

XYZ_orig_data = np.genfromtxt('../CIE_xyz_1931_2deg.csv', delimiter=',')

X = XYZ_orig_data[:, 0]
Y = XYZ_orig_data[:, 1]
plt.plot(X, Y, 'r+', markersize=3)

# интерполяция экспериментальных данных
p, cov = curve_fit(nGauss, X, Y, p0=ip0, bounds=(bottom_limits, top_limits))
print("Параметры гауссианов: ")

for pl in p:
    print(pl,",", end = " ")

# погрешность вычислений
print("Станд. отклонение: ", np.std(Y-nGauss(X, *p)))
slope, ic, r_value, p_value, std_err = \
stats.linregress(Y, nGauss(X, *p))
print("Квадрат коэффициента корреляции: ", r_value**2)

# вывод графиков
plt.ylabel('Интенсивность, отн. ед.')
plt.xlabel('Энергия, эВ')
plt.text(2.8,0.021,'R$^2$='+'%.4f' % r_value**2)
plotAllGauss(X, p)
plt.plot(X, nGauss(X, *p), 'g')
plt.savefig('result.png')
plt.show()
