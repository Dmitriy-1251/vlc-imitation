import colorsys
import dash
import logging
import serial
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import math
from dash import dcc as dcc
from dash import html
from dash import dash_table
from dash import ctx
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from sklearn.metrics import r2_score
from PIL import Image

try:
    arduino = serial.Serial(port='COM3', baudrate=1000000, timeout=.1)
    port_connect = 1
except Exception:
    logging.error('COM-порт не был подключен')
    port_connect = 0

CIEimg = Image.open("Files//IXytw.png")

logging.basicConfig(level=logging.ERROR)  # WARNING

# инициализация Dash
app = dash.Dash()

# вводим общие переменные
WL_min = 360
WL_max = 831
G = np.zeros((WL_max - WL_min, 3))
My_approx = np.zeros((WL_max - WL_min, 3))
SUM = pd.DataFrame(index=range(WL_max - WL_min), columns=['WL', 'LED', 'HUM'])

err_head = ['Канал', 'MSE', 'Pearson', 'R^2', 'S_H/S_LED', 'Spearman']
data_tbl = {h: ['-1', ' ', ' ', ' '] for i, h in enumerate(err_head)}
df_tbl = pd.DataFrame(data_tbl)

err_head_2 = ['', 'X', 'Y', 'Z']
data_tbl_2 = {h: ['-2', ' ', ' '] for i, h in enumerate(err_head_2)}
df_tbl_2 = pd.DataFrame(data_tbl_2)

Euclid = ['', 'XYZ', 'XY']
Euclid_tbl = {h: ['-3'] for i, h in enumerate(Euclid)}
df_tbl_Euclid = pd.DataFrame(Euclid_tbl)

port_open = 0


def pd_add_values(pd_imported_mass, header_names):
    # определяем, сколько строк нужно добавить в начале и в конце
    prefix_count = pd_imported_mass[header_names[0]][0] - WL_min
    suffix_count = WL_max - 1 - pd_imported_mass[header_names[0]][len(pd_imported_mass) - 1]

    if prefix_count > 0:
        first_row = pd_imported_mass.iloc[0]
        prefix_val = {header_names[i]: [first_row[i]] * prefix_count for i in range(len(header_names))}
        prefix_val[header_names[0]] = range(WL_min, pd_imported_mass[header_names[0]][0])
        prefix = pd.DataFrame(prefix_val)
        pd_imported_mass = pd.concat([prefix, pd_imported_mass], ignore_index=True)
        pd_imported_mass[header_names[0]] = pd_imported_mass.index + WL_min

    if suffix_count > 0:
        last_row = pd_imported_mass.iloc[len(pd_imported_mass) - 1]
        suffix_val = {header_names[i]: [0] * suffix_count for i in range(
            len(header_names))}  # suffix_val = {header_names[i]: [last_row[i]] * suffix_count for i in range(len(header_names))}
        suffix_val[header_names[0]] = range(pd_imported_mass[header_names[0]][len(pd_imported_mass) - 1] + 1,
                                            WL_max)
        suffix = pd.DataFrame(suffix_val)
        pd_imported_mass = pd.concat([pd_imported_mass, suffix], ignore_index=True)
    return pd_imported_mass


def pd_remove_values(pd_imported_mass, header_names):
    # определяем, сколько строк нужно удалить в начале и конце
    prefix_count = 0
    suffix_count = 0
    while pd_imported_mass[header_names[0]][prefix_count] < WL_min:
        prefix_count += 1
    while pd_imported_mass[header_names[0]][len(pd_imported_mass) - suffix_count - 1] >= WL_max:
        suffix_count += 1
    if prefix_count > 0 or suffix_count > 0:
        pd_imported_mass = pd_imported_mass.iloc[(prefix_count):(len(pd_imported_mass) - suffix_count)].reset_index(
            drop=True).copy()
    # print(pd_imported_mass)
    return pd_imported_mass


def check_size(pd_imported_mass, pd_name=None):
    header_names = pd_imported_mass.columns

    if len(pd_imported_mass) < WL_max - WL_min - 1:
        logging.warning(
            "Проверка " + str(pd_name) + " на недостаток данных: " + str(WL_max - WL_min - len(pd_imported_mass)))
        logging.warning("Попытка дополнить")
        pd_imported_mass = pd_add_values(pd_imported_mass, header_names)
        if len(pd_imported_mass) < WL_max - WL_min:
            logging.warning("Ошибка, проверьте  " + str(pd_name) + ": " + str(
                WL_max - WL_min - len(pd_imported_mass)))
        else:
            logging.warning("Автодополнение,  " + str(pd_name) + "  соответствует диапазону: [" + str(
                pd_imported_mass[header_names[0]][0]) + " " + str(
                pd_imported_mass[header_names[0]][len(pd_imported_mass) - 1]) + "]\n")
    if len(pd_imported_mass) > WL_max - WL_min:
        logging.warning("Проверка " + str(pd_name) + " на избыток данных: " + str(
            WL_max - WL_min - len(pd_imported_mass)))
        logging.warning("Попытка исключить")
        pd_imported_mass = pd_remove_values(pd_imported_mass, header_names)
        if len(pd_imported_mass) > WL_max - WL_min:
            logging.warning("Ошибка, проверьте  " + str(pd_name) + ": " + str(
                WL_max - WL_min - len(pd_imported_mass)))
        else:
            logging.warning("Автодополнение,  " + str(pd_name) + "  соответствует диапазону: [" + str(
                pd_imported_mass[header_names[0]][0]) + " " + str(
                pd_imported_mass[header_names[0]][len(pd_imported_mass) - 1]) + "]\n")
    if len(pd_imported_mass) == WL_max - WL_min:
        logging.info("Данные " + str(pd_name) + " соответствуют диапазону: [" + str(
            pd_imported_mass[header_names[0]][0]) + " " + str(
            pd_imported_mass[header_names[0]][len(pd_imported_mass) - 1]) + "]\n")

    pd_imported_mass = pd_imported_mass.replace(to_replace=np.nan, value=0)
    logging.debug(pd_imported_mass[0:5])  # 450:471
    logging.debug(pd_imported_mass[466:472])
    return pd_imported_mass


# загружаем данные
XYZ_orig_data = pd.read_csv('Files//CIE_xyz_1931_2deg.csv', delimiter=',', names=['WL', 'X', 'Y', 'Z'])
XYZ_orig_data = check_size(XYZ_orig_data, "XYZ_orig_data")

Human_data = pd.read_csv('Files//linss2_10e_1 (1).csv', delimiter=',', names=['WL', 'R', 'G', 'B'])
Human_data = check_size(Human_data, "Human_data")
Human = Human_data
# available_spectrum = [i for i in range(0, 15)]
# Lamp_test = pd.read_csv('Files//cri_1nm.txt', delimiter=' ', names=available_spectrum)
# Lamp_test = check_size(Lamp_test, "Lamp_test")

available_spectrum = [i for i in range(0, 251)]
Lamp_test = pd.read_csv('./data/LAMP_DATA_test_1.csv', delimiter=',', skiprows=1, names=available_spectrum)

CJMCU_data = pd.read_csv('Files//CJMCU_test.csv', delimiter=',', skiprows=1, names=['WL', 'R', 'G', 'B'])
CJMCU_data = check_size(CJMCU_data, "CJMCU_data")

Photoresistor = pd.read_csv('Files//Photoresistor_converted.csv', delimiter=',', skiprows=1, names=['WL', 'R', 'G', 'B'])
Photoresistor = check_size(Photoresistor, "Photoresistor")

available_receiver = ["Human_SML", "Cjmcu-101", "Photoresistor"]
# Lamp_test = Lamp_test.fillna(0)
# Lamp_test = check_size(Lamp_test, "Lamp_test")# отключить

LED_0_val = 11
LED_1_val = 13
LED_2_val = 22

# LED_0 = pd.read_csv('Files//YJ-SX-2835-01R-SPD.csv', delimiter=',', header=None, skiprows=1, names=[0, LED_0_val])
# LED_0 = check_size(LED_0, "LED_0")
#
# LED_1 = pd.read_csv('Files//YJ-SX-2835-02G-SPD.csv', delimiter=',', header=None, skiprows=1, names=[0, LED_1_val])
# LED_1 = check_size(LED_1, "LED_1")
#
# LED_2 = pd.read_csv('Files//YJ-SX-2835-01C-SPD.csv', delimiter=',', header=None, skiprows=1, names=[0, LED_2_val])
# LED_2 = check_size(LED_2, "LED_2")


available_LED = [i for i in range(0, 29)]
LED_All = pd.read_csv('./data/LED_ALL.csv', delimiter=',', skiprows=1, names=available_LED)
LED_All = check_size(LED_All, "LED_All")
LED_0 = LED_All.iloc[:, [0, LED_0_val]]
LED_1 = LED_All.iloc[:, [0, LED_1_val]]
LED_2 = LED_All.iloc[:, [0, LED_2_val]]

Blue_light_570_converted = pd.read_csv('Files//Blue_light_570_converted.csv', delimiter=',', skiprows=1, names=[0, 1])
Blue_light_570_converted = check_size(Blue_light_570_converted, "Blue_light_570_converted")
LED_2 = Blue_light_570_converted.iloc[:, [0, 1]]
LED_2_val = 1

# определение содержимого страницы
app.layout = html.Div(children=[

    html.H4(id='text', children='Загрузка..',
            style={'width': '600px', 'height': '5px', 'display': 'inline-block', 'marginLeft': '10px',
                   'marginTop': '0px'}),
    html.Div([
        html.H4(id='errors1', children='Источник излучения:',
                style={'width': '175px', 'height': '0px', 'display': 'inline-block', 'marginLeft': '10px',
                       'marginTop': '11px'}),
        dcc.Dropdown(
            id='spectrum_example',
            options=[{'label': lbl_spec, 'value': i_spec} for i_spec, lbl_spec in enumerate(available_spectrum)],
            value=1,
            style={'width': '80px', 'height': '40px', 'display': 'inline-block'},
        ),
        html.H4(id='errors', children='Приёмник излучения:',
                style={'width': '175px', 'height': '0px', 'display': 'inline-block', 'marginLeft': '10px',
                       'marginTop': '12px'}),
        dcc.Dropdown(
            id='receiver_dp',
            options=[{'label': lbl_rec, 'value': i_rec} for i_rec, lbl_rec in enumerate(available_receiver)],
            value=0,
            style={'width': '160px', 'height': '40px', 'display': 'inline-block'},
        ),
        dcc.Checklist(
            id='Arduino-checkbox',
            options=[{'label': 'Arduino', 'value': 'C'}],
            style={'width': '100px', 'height': '0px', 'display': 'inline-block', 'marginLeft': '20px',
                   'marginTop': '11px'}
        ),
        html.Button('Передать данные', id='trnsm_data',
                    style={'width': '160px', 'height': '30px', 'marginTop': '6px'}),
        html.Div(id='container-button-timestamp')
    ], style={'width': '100%', 'display': 'flex'}),

    # html.Div(id='output'),

    html.Div([
        dcc.Graph(
            id='our-graph',
            style={'width': '100vh', 'height': '90vh'},
        ),
        html.Div(children=[
            dcc.Graph(
                id='sum-graph',
                style={'width': '100vh', 'height': '28vh'},
            ),
            # html.H3(id='text', children='Загрузка..'),
            html.Div([
                dcc.Graph(
                    id='CIE_graph',
                    style={'width': '60vh', 'height': '60vh'},
                ),

                html.Div([
                    html.H4(id='Errors_1', children='1) Ошибка при аппроксимации:'),
                    html.P(id='Errors_1_text',
                           children='Принимаем равной нулю, т.к. для преобразования используются исходные значения функций преобразования цветов, предоставленные CIE',
                           style={"width": "40vh"}),
                    html.H4(id='Errors_2', children='2) Ошибка RGB в XYZ:', style={'marginBottom': '1vh'}),
                    dash_table.DataTable(
                        id='err_tbl_2',
                        columns=[{"name": i, "id": i} for i in df_tbl_2.columns],
                        data=df_tbl_2.to_dict('records'),
                        editable=True,
                        style_data={'width': '60px', 'height': '15px', 'text-align': 'center', 'fontSize': 16},
                        style_header={'text-align': 'center', }
                        # 'display': 'inline-block', 'margin-left': '600px','margin-top': '13px'
                    ),
                    dash_table.DataTable(
                        id='err_tbl_3',
                        columns=[{"name": i, "id": i} for i in df_tbl_Euclid.columns],
                        data=df_tbl_Euclid.to_dict('records'),
                        editable=True,
                        style_data={'width': '60px', 'height': '15px', 'text-align': 'center', 'fontSize': 16},
                        style_header={'text-align': 'center', },
                        style_table={'margin-top': '7px'},
                        # 'display': 'inline-block', 'margin-left': '600px','margin-top': '13px'
                    ),
                    html.H4(id='Errors', children='3) Ошибка исходный и имитированный спектр:',
                            style={'marginBottom': '1vh'}),
                    dash_table.DataTable(
                        id='err_tbl',
                        columns=[{"name": i, "id": i} for i in df_tbl.columns],
                        data=df_tbl.to_dict('records'),
                        editable=True,
                        style_data={'width': '60px', 'height': '15px', 'text-align': 'center', 'fontSize': 16},
                        style_header={'text-align': 'center', }
                        # 'display': 'inline-block', 'margin-left': '600px','margin-top': '13px'
                    )]),

            ], style={'width': '100%', 'display': 'flex'})
        ])
    ], style={'width': '100%', 'display': 'flex'}),
])

@ app.callback(
    Output('trnsm_data', 'children'),
    Input('trnsm_data', 'n_clicks'), Input('Arduino-checkbox', 'value'))


def trnsm_data_ino(n_clicks, checkbox):
    if port_connect:
        global arduino
        if checkbox == ['C']:
            msg = "Готов к передаче"
            if 'trnsm_data' == ctx.triggered_id:
                arduino.write(bytes("300,0,0", 'utf-8'))
                msg = "Передано (" + str(n_clicks) + ")"
        else:
            msg = "Чекбокс отключен"
    else:
        msg = "Не подключено"
    return html.Div(msg)


def arduino_func(R_norm, G_norm, B_norm, checkbox):
    global arduino
    if checkbox == ['C']:
        hsv = colorsys.rgb_to_hsv(*(R_norm, G_norm, B_norm))
        arduino.write(
            bytes(str(round(hsv[0] * 255)) + "," + str(round(hsv[1] * 255)) + "," + str(round(hsv[2] * 255)), 'utf-8'))
    else:
        arduino.write(bytes("0,0,0", 'utf-8'))
    return 0


@app.callback(
    [Output('our-graph', 'figure'), Output('text', 'children'), Output('err_tbl', 'data'),
     Output('sum-graph', 'figure'), Output('CIE_graph', 'figure'), Output('err_tbl_2', 'data'),
     Output('err_tbl_3', 'data')],
    # Output('errors', 'children'),
    [Input('spectrum_example', 'value'), Input('Arduino-checkbox', 'value'), Input('receiver_dp', 'value')])
def update_spectrum(spectrum_val, checkbox, receiver_val):
    R_norm, G_norm, B_norm, X_ch, Y_ch, Z_ch = color_convert(XYZ_orig_data, Lamp_test, spectrum_val)  # spectrum_val
    # print(receiver_val)
    if port_connect:
        arduino_func(R_norm, G_norm, B_norm, checkbox)

    new_df_2, x_graph, y_graph, x_graph_rgb, y_graph_rgb, new_df_tbl_Euclid = RGB_XYZ_convert_error(R_norm, G_norm, B_norm, X_ch, Y_ch,
                                                                                 Z_ch)
    if receiver_val == 0:
        Human = Human_data
    elif receiver_val == 1:
        Human = CJMCU_data
    else:
        Human = Photoresistor

    # if receiver_val:
    #     Human = CJMCU_data
    # else:
    #     Human = Human_data
    Human_view, LED_emitted = result_spectrum(R_norm, G_norm, B_norm, Human, LED_0, LED_1, LED_2)
    fig, fig_sum, CIE_graph = plot_all(spectrum_val, R_norm, G_norm, B_norm, Human_view, LED_emitted, x_graph, y_graph,
                                       x_graph_rgb, y_graph_rgb, Human)
    link = 'https://lspdd.org/app/en/lamps/' + str(2469 + spectrum_val - 1)
    text = ['Ссылка на спектр ', dcc.Link(link, href=link)]
    # stats = 0
    # stats = error_count(Human_view, LED_emitted)

    new_df = error_count(Human_view, LED_emitted)  # pd.DataFrame(data_tbl)
    # new_df['col2'] = new_df['col2'] * 10

    return fig, text, new_df.to_dict('records'), fig_sum, CIE_graph, new_df_2.to_dict('records'), new_df_tbl_Euclid.to_dict(
        'records')


def plot_all(spectrum_val, R, G, B, Human_view, LED_emitted, x_graph, y_graph, x_graph_rgb, y_graph_rgb, Human):
    CIE_graph = make_subplots(rows=1, cols=2, specs=[
        [{"colspan": 2}, None]], subplot_titles=[
        'Диаграмма цветности CIE с указанием ошибки при преобразовании XYZ в RGB'], vertical_spacing=0.05)
    CIE_graph.update_layout(
        margin=dict(l=0, r=10, t=20, b=0),
        xaxis1=dict(range=[-0.1, 0.9]),
        yaxis1=dict(range=[-0.1, 0.9])
    )
    CIE_graph.update_annotations(font_size=12)
    # CIE_graph = go.Figure(
    #     go.Scatter(x=[0, 0.8, 0.8, 0], y=[0, 0, 0.8, 0.8, ],line=dict(width=0),showlegend=False))
    CIE_graph.add_shape(type="rect",
                        x0=-0.1, y0=-0.1, x1=0.9, y1=0.9,
                        line=dict(width=0),
                        )
    CIE_graph.add_layout_image(
        dict(
            source=CIEimg,
            xref="x",
            yref="y",
            x=-0.1,
            y=0.9,
            sizex=1,
            sizey=1,
            sizing="stretch",
            # opacity=0.8,
            layer="below", )
    )
    CIE_graph.add_trace(go.Scatter(x=[x_graph], y=[y_graph], mode='markers', showlegend=False,
                                   marker=dict(color='White', size=14, line=dict(width=1, color='Black'))))
    CIE_graph.add_trace(go.Scatter(x=[x_graph_rgb], y=[y_graph_rgb], mode='markers', showlegend=False,
                                   marker=dict(color='Black', size=7, line=dict(width=1, color='White'))))

    CIE_graph.add_annotation(
        text=' ' + str(round(x_graph, 3)) + ' ' + str(round(y_graph, 3)), x=(x_graph + 0.09), y=y_graph,
        bgcolor='white', bordercolor='black',
        borderwidth=1,
        font=dict(size=14, color='black'), showarrow=False)

    df_tbl_Euclid.iloc[0, 2] = '' + str(round(math.dist([x_graph, y_graph], [x_graph_rgb, y_graph_rgb]), 5))



    fig_sum = make_subplots(rows=1, cols=2, specs=[
        [{"colspan": 2}, None]], subplot_titles=[
        'Суммарный спектр, видимый человеком: исходный (черный) и имитированный светодиодом (цвет имитации)'],
                            vertical_spacing=0.05)
    fig_sum.update_annotations(font_size=12)
    fig_sum.update_layout(
        margin=dict(l=0, r=0.05, t=20, b=0),
        xaxis1=dict(range=[WL_min, WL_max]),
        yaxis1=dict(range=[0, 2]))
    SUM['LED'] = LED_emitted['B'] + LED_emitted['G'] + LED_emitted['R']
    SUM['HUM'] = Human_view['B'] + Human_view['G'] + Human_view['R']
    fig_sum.add_trace(
        go.Scatter(x=Lamp_test[0], y=SUM['LED'], fill="tozeroy", fillcolor='rgba(0, 50, 120, 0.3)',
                   line=dict(color='#3e3e3e', width=3), showlegend=False, name='LED'), 1, 1)

    fig_sum.add_trace(
        go.Scatter(x=Lamp_test[0], y=SUM['HUM'], fill='tonexty', line=dict(color=f'rgb({R}, {G}, {B})', width=3),
                   showlegend=False, fillpattern=dict(fgcolor=f'rgb({R}, {G}, {B})', shape="|"),
                   name='Human'), 1, 1)

    # fig_sum.add_trace(
    #     go.Scatter(x=Lamp_test[0], y=Lamp_test[spectrum_val], marker=dict(color='Red'), showlegend=False, name='Specrum'), 1, 1)

    # разбиваем поле вывода на подграфики
    fig = make_subplots(rows=3, cols=6, specs=[
        [{"colspan": 6}, None, None, None, None, None],
        [{"colspan": 3}, None, None, {"colspan": 3}, None, None],
        [{"colspan": 2}, None, {"colspan": 2}, None, {"colspan": 2}, None]],
                        subplot_titles=['Cпектр излучения источника',
                                        'Спектральная чувствительность клеток человека S-, M- и L-типа',
                                        'Пример спектра излучения RGB светодиодов',
                                        '',
                                        'Спектр, видимый человеком по каналам: исходный(—) и имитированный светодиодом(- -)', ],
                        vertical_spacing=0.05
                        )
    fig.update_annotations(font_size=12)

    # легенда
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, y=-.02, xanchor="center"),
                      hovermode="x",
                      margin=dict(l=0, r=0, t=20, b=0),
                      # xaxis1=dict(range=[WL_min, WL_max]),
                      # yaxis1=dict(range=[0, 1]),
                      xaxis2=dict(range=[WL_min, WL_max]),
                      yaxis2=dict(range=[-0.1, 1]),
                      xaxis3=dict(range=[WL_min, WL_max]),
                      yaxis3=dict(range=[0, 1]),
                      xaxis4=dict(range=[WL_min, WL_max]),
                      yaxis4=dict(range=[0, 1]),
                      xaxis5=dict(range=[WL_min, WL_max]),
                      yaxis5=dict(range=[0, 1]),
                      xaxis6=dict(range=[WL_min, WL_max]),
                      yaxis6=dict(range=[0, 1]))
    fig.update_traces(hoverinfo="all", hovertemplate="WL: %{x}<br>Val: %{y}")

    # for i in range(WL_min, WL_max, 8):
    #     fig.add_trace(go.Scatter(x=[i, i], y=[-0.1, 0], mode='lines', showlegend=False, hoverinfo='skip',
    #                              line=dict(color="Black", width=7)), 2, 1)

    # добавляем графики
    fig.add_trace(
        go.Scatter(x=Lamp_test[0], y=Lamp_test[spectrum_val], fill='tozeroy', line=dict(color='Grey', width=3),
                   fillpattern=dict(fgcolor='#969696', shape="|"), showlegend=False), 1, 1)

    fig.add_trace(
        go.Scatter(x=Human['WL'], y=Human['R'], line=dict(color='#EF553B', width=3), name='S'), 2, 1)

    fig.add_trace(
        go.Scatter(x=Human['WL'], y=Human['G'], line=dict(color='#2CA02C', width=3), name='M'), 2, 1)
    fig.add_trace(
        go.Scatter(x=Human['WL'], y=Human['B'], line=dict(color='#3366CC', width=3), name='L'), 2, 1)

    fig.add_trace(
        go.Scatter(x=LED_0[0], y=LED_0[LED_0_val], line=dict(color='#EF553B', width=3), name='LED_0'), 2, 4)
    fig.add_trace(
        go.Scatter(x=LED_1[0], y=LED_1[LED_1_val], line=dict(color='#2CA02C', width=3), name='LED_1'), 2, 4)
    fig.add_trace(
        go.Scatter(x=LED_2[0], y=LED_2[LED_2_val], line=dict(color='#3366CC', width=3), name='LED_2'), 2, 4)

    fig.add_trace(
        go.Scatter(x=Human_view['WL'], y=Human_view['R'], line=dict(color='#993726', width=2, dash='dash'),
                   name='Human_view'), 3, 5)
    fig.add_trace(
        go.Scatter(x=Human_view['WL'], y=Human_view['G'], line=dict(color='#1c661c', width=2, dash='dash'),
                   name='Human_view'), 3, 3)
    fig.add_trace(
        go.Scatter(x=Human_view['WL'], y=Human_view['B'], line=dict(color='#1a3366', width=2, dash='dash'),
                   name='Human_view'), 3, 1)

    fig.add_trace(
        go.Scatter(x=Human_view['WL'], y=LED_emitted['R'], line=dict(color='#EF553B', width=3), name='LED_emitted'), 3,
        5)
    fig.add_trace(
        go.Scatter(x=Human_view['WL'], y=LED_emitted['G'], line=dict(color='#2CA02C', width=3), name='LED_emitted'), 3,
        3)
    fig.add_trace(
        go.Scatter(x=Human_view['WL'], y=LED_emitted['B'], line=dict(color='#3366CC', width=3), name='LED_emitted'), 3,
        1)

    fig.add_trace(
        go.Scatter(x=[700, 800, 800, 700], y=[0.6, 0.6, 0.8, 0.8], fill='toself', fillcolor=f'rgb({R}, {G}, {B})',
                   mode='none', hoverinfo='skip', showlegend=False), 2, 1)
    fig.add_trace(
        go.Scatter(x=[700, 733, 733, 700], y=[0.8, 0.8, 0.9, 0.9], fill='toself', fillcolor=f'rgb({R}, 0, 0)',
                   mode='none', hoverinfo='skip', showlegend=False), 2, 1)
    fig.add_trace(
        go.Scatter(x=[733, 766, 766, 733], y=[0.8, 0.8, 0.9, 0.9], fill='toself', fillcolor=f'rgb(0, {G}, 0)',
                   mode='none', hoverinfo='skip', showlegend=False), 2, 1)
    fig.add_trace(
        go.Scatter(x=[766, 800, 800, 766], y=[0.8, 0.8, 0.9, 0.9], fill='toself', fillcolor=f'rgb(0, 0, {B})',
                   mode='none', hoverinfo='skip', showlegend=False), 2, 1)
    rgb = (R, G, B)
    # print(rgb) #print!
    hsv = colorsys.rgb_to_hsv(*rgb)
    # print(hsv)

    fig.add_trace(
        go.Scatter(x=[700, 800, 800, 700], y=[0.2, 0.2, 0.4, 0.4], fill='toself',
                   fillcolor=f'hsv({hsv[0] * 360}, {hsv[1] * 100}, {100})',
                   mode='none', hoverinfo='skip', showlegend=False), 2, 1)

    fig.add_annotation(
        text='RGB: ' + str(round(R * 255, 1)) + ' ' + str(round(G * 255, 1)) + ' ' + str(round(B * 255, 1)), x=750,
        y=0.57,
        font=dict(size=14, color='black'), showarrow=False, row=2, col=1)
    fig.add_annotation(text='HSV: ' + str(round(hsv[0] * 360, 1)) + ' ' + str(round(hsv[1] * 100, 1)) + ' 100', x=750,
                       y=0.17,
                       font=dict(size=14, color='black'), showarrow=False, row=2, col=1)
    # fig.add_annotation(text='HSV: '+str(round(hsv[0] * 360, 1)) + ' ' + str(round(hsv[1] * 100, 1)) + ' 100', x=750, y=0.37,
    #                    font=dict(size=14, color='black'), showarrow=False, row=2, col=1)

    return fig, fig_sum, CIE_graph


def adj(i, C):
    if i == -1:
        if C < 0:
            logging.warning("Complex value! Wavelength = " + str(i) + " (" + str(C) + " < 0)")
            return 0
        elif abs(C) <= 0.0031308:
            return 12.92 * C
        else:
            return 1.055 * pow(C, 0.41666) - 0.055
    elif i == 1:
        if abs(C) <= 0.04045:
            return C / 12.92
        else:
            return (pow((C + 0.055), 2.4)) / 1.13715


def XYZ_to_RGB(i, X, Y, Z):
    R = 3.2410 * X - 1.5374 * Y - 0.4986 * Z
    G = -0.9692 * X + 1.8760 * Y + 0.0416 * Z
    B = 0.0556 * X - 0.2040 * Y + 1.0570 * Z

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

        if (R + G + B) == 0:
            R_norm = 0
            G_norm = 0
            B_norm = 0

        # корректируем яркость
        R_norm, G_norm, B_norm = adj(i, R_norm), adj(i, G_norm), adj(i, B_norm)

        # возвращаем значения для нормализации в преобразовании спектра в цвет
        return R_norm, G_norm, B_norm, X, Y, Z
    else:
        # корректируем яркость значений для всего диапазона
        R, G, B = adj(i, R), adj(i, G), adj(i, B)
    return R, G, B, X, Y, Z


def color_convert(XYZ_orig_data, Lamp_test, spectrum_val):
    # определяем тестируемый спектр
    test_spectrum = Lamp_test[spectrum_val]
    logging.debug(Lamp_test)
    logging.debug(Lamp_test[spectrum_val])
    # берём веса спектра, умножаем на табличные веса чтобы получить значение влияния канала на общий спектр
    X = (test_spectrum * XYZ_orig_data.iloc[:, 1]).sum()
    Y = (test_spectrum * XYZ_orig_data.iloc[:, 2]).sum()
    Z = (test_spectrum * XYZ_orig_data.iloc[:, 3]).sum()
    logging.debug(X)
    logging.debug(Y)
    logging.debug(Z)
    # преобразуем в RGB с корректировками и нормализацией внутри внешней функции
    return XYZ_to_RGB(-1, X, Y, Z)


def result_spectrum(R, G, B, Human, LED_0, LED_1, LED_2):
    # создаем DataFrame для Human_view и LED_emitted
    Human_view = pd.DataFrame(index=range(WL_max - WL_min), columns=['WL', 'R', 'G', 'B'])
    LED_emitted = pd.DataFrame(index=range(WL_max - WL_min), columns=['WL', 'R', 'G', 'B'])

    # заполняем первую колонку значениями длин волн
    Human_view['WL'] = range(WL_min, WL_max)
    LED_emitted['WL'] = range(WL_min, WL_max)

    # находим поэлементно результат для всех значений спектра видимых человеком
    for i in range(WL_min, WL_max, 1):
        Human_view.loc[i - WL_min, "R"] = R * Human.loc[i - WL_min, "R"]
        Human_view.loc[i - WL_min, "G"] = G * Human.loc[i - WL_min, "G"]
        Human_view.loc[i - WL_min, "B"] = B * Human.loc[i - WL_min, "B"]

    # находим поэлементно результат для всех значений спектра излучаемых светодиодом
    for i in range(WL_min, WL_max, 1):
        LED_emitted.loc[i - WL_min, "R"] = R * LED_0.loc[i - WL_min, LED_0_val]
        LED_emitted.loc[i - WL_min, "G"] = G * LED_1.loc[i - WL_min, LED_1_val]
        LED_emitted.loc[i - WL_min, "B"] = B * LED_2.loc[i - WL_min, LED_2_val]

    return Human_view, LED_emitted


def RGB_to_XYZ(R, G, B):

    X = 0.4127 * R + 0.3586 * G + 0.1808 * B
    Y = 0.2132 * R + 0.7172 * G + 0.0724 * B
    Z = 0.0195 * R + 0.1197 * G + 0.9517 * B

    return X, Y, Z


def RGB_XYZ_convert_error(R_norm, G_norm, B_norm, X_ch, Y_ch, Z_ch):
    # восстанавливаем нелинейность коррекции
    R, G, B = adj(1, R_norm), adj(1, G_norm), adj(1, B_norm)

    # нормализуем исходные XYZ
    X = X_ch / (X_ch + Y_ch + Z_ch)
    Y = Y_ch / (X_ch + Y_ch + Z_ch)
    Z = Z_ch / (X_ch + Y_ch + Z_ch)
    if (X_ch + Y_ch + Z_ch) == 0:
        X = 0
        Y = 0
        Z = 0

    # преобразуем RGB в XYZ с помощью матрицы
    X_cmp, Y_cmp, Z_cmp = RGB_to_XYZ(R, G, B)

    x_graph = X_ch / (X_ch + Y_ch + Z_ch)
    y_graph = Y_ch / (X_ch + Y_ch + Z_ch)
    x_graph_rgb = X_cmp / (X_cmp + Y_cmp + Z_cmp)
    y_graph_rgb = Y_cmp / (X_cmp + Y_cmp + Z_cmp)

    err_2 = ['Исходные координаты', 'Преобразованные в RGB', 'Разность']

    for ch_num, channel in enumerate(err_2):
        df_tbl_2.iloc[ch_num, 0] = channel
    df_tbl_2.iloc[0, 1] = str(round(X, 5))
    df_tbl_2.iloc[0, 2] = str(round(Y, 5))
    df_tbl_2.iloc[0, 3] = str(round(Z, 5))

    df_tbl_2.iloc[1, 1] = str(round(X_cmp, 5))
    df_tbl_2.iloc[1, 2] = str(round(Y_cmp, 5))
    df_tbl_2.iloc[1, 3] = str(round(Z_cmp, 5))

    df_tbl_2.iloc[2, 1] = str(round(X - X_cmp, 5))
    df_tbl_2.iloc[2, 2] = str(round(Y - Y_cmp, 5))
    df_tbl_2.iloc[2, 3] = str(round(Z - Z_cmp, 5))
    df_tbl_Euclid.iloc[0, 1] = str(round(math.dist([X, Y, Z], [X_cmp, Y_cmp, Z_cmp]), 5))
    df_tbl_Euclid.iloc[0, 0] = 'Евклидово расстояние'

    return df_tbl_2, x_graph, y_graph, x_graph_rgb, y_graph_rgb, df_tbl_Euclid


def error_count(Human_view, LED_emitted):
    ch = ['R', 'G', 'B']
    Human_view = Human_view.astype(float)
    LED_emitted = LED_emitted.astype(float)
    for ch_num, channel in enumerate(ch):
        corr_coef, p_value_pears = pearsonr(Human_view[channel], LED_emitted[channel])
        corr_sp, p_value_sp = spearmanr(Human_view[channel], LED_emitted[channel])

        df_tbl.iloc[ch_num, 0] = channel
        df_tbl.iloc[ch_num, 1] = round(mean_squared_error(Human_view[channel], LED_emitted[channel]), 5)
        df_tbl.iloc[ch_num, 2] = round(corr_coef, 5)  # pearson
        df_tbl.iloc[ch_num, 3] = round(r2_score(Human_view[channel], LED_emitted[channel]), 5)
        df_tbl.iloc[ch_num, 4] = round(((np.trapz(Human_view[channel], x=Human_view['WL'])) / (
            np.trapz(LED_emitted[channel], x=LED_emitted['WL']))), 5)
        df_tbl.iloc[ch_num, 5] = round(corr_sp, 5)

    # считаем для всех каналов
    corr_coef, p_value_pears = pearsonr(Human_view['R'] + Human_view['G'] + Human_view['B'],
                                        LED_emitted['R'] + LED_emitted['G'] + LED_emitted['B'])
    corr_sp, p_value_sp = spearmanr(Human_view['R'] + Human_view['G'] + Human_view['B'],
                                    LED_emitted['R'] + LED_emitted['G'] + LED_emitted['B'])
    df_tbl.iloc[3, 0] = 'Общий'
    df_tbl.iloc[3, 1] = round(mean_squared_error(Human_view, LED_emitted), 5)
    df_tbl.iloc[3, 2] = round(corr_coef, 5)  # pearson
    df_tbl.iloc[3, 3] = round(r2_score(Human_view, LED_emitted), 5)
    df_tbl.iloc[3, 4] = round(((np.trapz(Human_view['R'] + Human_view['G'] + Human_view['B'], x=Human_view['WL'])) / (
        np.trapz(LED_emitted['R'] + LED_emitted['G'] + LED_emitted['B'], x=LED_emitted['WL']))), 5)
    df_tbl.iloc[3, 5] = round(corr_sp, 5)

    return df_tbl


if __name__ == '__main__':
    app.run_server(debug=False)  # NB! Arduino работает только в Release режиме
