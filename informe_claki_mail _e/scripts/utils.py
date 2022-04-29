import pandas as pd
from babel.dates import format_date, format_datetime, format_time
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go


def query_db(engine):
    recogida = pd.read_sql('SELECT * FROM transport', engine)
    puntos = pd.read_sql('SELECT * FROM puntos', engine)

    return recogida, puntos


def filter_data(recogida, puntos, tipo_punto):

    recogida['fecha'] = pd.to_datetime(recogida['fecha'], errors='coerce')
    recogida = recogida.rename(columns={'codpun': 'cod'})

    puntos = puntos.rename(columns={'codpun': 'cod'})

    df = pd.merge(puntos[['cod', 'Nombre', 'Direccion']],
                  recogida, on='cod', how='inner')
    df = df[df['tipo'] == tipo_punto]
    # df_filter = df[(df['fecha'] > start) & (df['fecha'] <= end)]
    return df


def current_course_plot(df, cod_school, start, end, history=False):

    df_school = df[(df['fecha'] > start) & (df['fecha'] <= end)]
    df_school = df_school[df_school['cod']
                          == cod_school].sort_values('fecha', ascending=True)

    df_school['fecha'] = pd.to_datetime(df_school['fecha'], format="%d-%m-%Y")

    dates = df_school['fecha'].tolist()

    dates_month = [format_date(i, locale='es_ES') for i in dates]

    recogidas = df_school['recogidos'].tolist()

    if not history:
        df_school['MA'] = df_school.recogidos.rolling(3).mean()
        periods = 3
    else:
        df_school['MA'] = df_school.recogidos.rolling(6).mean()
        periods = 6

    try:
        name_school = df_school.Nombre.unique().tolist()[0]
    except IndexError:
        name_school = "Vacío"

    fig = go.Figure()

    if not history:
        color = 'rgb(184, 247, 212)'
    else:
        color = 'rgb(23, 190, 207)'

    fig.add_trace(go.Scatter(x=dates, y=recogidas,
                             mode='lines',
                             line_color='grey',
                             fill='tozeroy',
                             fillcolor=color,
                             name="recollides"
                             ))

    fig.add_trace(go.Scatter(x=dates, y=df_school['MA'], line=dict(color='black', width=2),
                             name='mitja mòvil {} períodes'.format(periods)))

    '''fig.update_layout(
        title='Recollides curs vigent',
        yaxis_title='Clakis recollits',
        xaxis=dict(
            tickmode='array',
            tickvals=dates,
            ticktext=dates_month
        ))'''

    fig.update_layout(legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                        ))

    df_school['fecha'] = dates_month

    # fig.write_image('../images/recollides_mes_{}_{}.png'.format(cod_school, end))
    return fig, df_school, name_school, recogidas


def all_courses_plot(df):
    # df_school = df[(df['fecha'] > start) & (df['fecha'] <= end)]

    name_school = df.Nombre.unique().tolist()

    recollides_integer = df['recogidos'].values.tolist()

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.fecha, y=recollides_integer,
                             mode='lines',
                             line_color='grey',
                             fill='tozeroy',
                             fillcolor='rgb(184, 247, 212)'
                             ))
    fig.update_layout(legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                        ))
    # fig.write_image('../images/recollides_totals_{}_{}.png'.format(cod_school, timestamp))
    return fig, name_school, recollides_integer
