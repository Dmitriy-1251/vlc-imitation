import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np


def f(x):
    return x ** 2


def h(x):
    return np.sin(x)


def k(x):
    return np.cos(x)


def m(x):
    return np.tan(x)


def plot_all(XYZ_orig_data):
    x = np.arange(0, 5, 0.1)

    # разбиваем поле вывода на подграфики
    fig = make_subplots(rows=3, cols=2, specs=[
        [{"colspan": 2}, None],
        [{}, {}],
        [{"colspan": 2}, None]], subplot_titles=['Пример спектра источника',
                                                 'Спектральная чувствительность клеток человека, S, M и L типов',
                                                 'Типичный спектр излучения RGB светодиода',
                                                 'Спектр видимый человеком(исходный и имитированный светодиодом)',], vertical_spacing = 0.05
                        )
    fig.update_annotations(font_size=12,)

    # задаём ограничения для выбранного графика
    # fig.update_yaxes(range=[-0.5, 1.5], zeroline=True, zerolinewidth=2, zerolinecolor='LightPink',row=1, col=1)
    # fig.update_xaxes(range=[-0.5, 1.5], zeroline=True, zerolinewidth=2, zerolinecolor='#008000',row=1, col=1)

    # добавляем графики
    # fig.add_trace(go.Scatter(x = XYZ_orig_data[:, 0], y = XYZ_orig_data[:, 1], marker=dict(color='red'), name='CIExyz1931_2deg'), 1, 1)
    # fig.add_trace(go.Scatter(x=XYZ_orig_data[:, 0], y=XYZ_orig_data[:, 2], marker=dict(color='green'), name='CIExyz1931_2deg'), 1, 1)
    # fig.add_trace(go.Scatter(x=XYZ_orig_data[:, 0], y=XYZ_orig_data[:, 3], marker=dict(color='blue'), name='CIExyz1931_2deg'), 1, 1)
    fig.add_trace(go.Scatter(x=XYZ_orig_data[:, 0], y=XYZ_orig_data[:, 3], marker=dict(color='Black'), name='CIExyz1931_2deg'), 1,1)

    fig.add_trace(go.Scatter(x=x, y=f(x), mode='markers', name=''), 2, 1)
    fig.add_trace(go.Scatter(x=x, y=h(x), name='-'), 2, 2)
    fig.add_trace(go.Scatter(x=x, y=k(x), name='-'), 3, 1)
    fig.add_trace(go.Scatter(x=x, y=k(x), name='-'), 3, 1)

    # легенда
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5,y=-.02, xanchor="center"),
                      hovermode="x",
                      margin=dict(l=0, r=0, t=20, b=0),)
    fig.update_traces(hoverinfo="all", hovertemplate="WL: %{x}<br>Val: %{y}")


    fig.write_html('tmp.html', auto_open=True)
    # fig.show()


if __name__ == '__main__':
    # объявление переменных
    TESTING_WL = 430
    TESTING_SPECTRE = 14  # [1, 14]
    WL_min = 360
    WL_max = 831
    G = np.zeros((WL_max - WL_min, 3))
    My_approx = np.zeros((WL_max - WL_min, 3))

    # импортируем оригинального двухградусного наблюдателя 1931 года и строим на графике
    XYZ_orig_data = np.genfromtxt('../CIE_xyz_1931_2deg.csv', delimiter=',')



    # строим графики
    plot_all(XYZ_orig_data)
