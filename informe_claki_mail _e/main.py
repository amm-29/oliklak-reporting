from scripts.utils import *
from report_generator import *
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from mailing_informe import send_mail
from mega import Mega
import os
import math


def report_creation(data, cod_school, start, end, sum_hist, logo_file):
    total_recogidas_array = total_recogidas_tipo(data, start, end, cod_school)
    (informe, cod_school, date_report) = report_generator_code(
        data, start, end, total_recogidas_array, cod_school, sum_hist, logo_file)
    print("Reporte de {} generado con éxito".format(cod_school))

    return informe, cod_school, date_report


def hist_data(df, cod_school, end):

    hist_recogidas = df[(df['cod'] == cod_school)
                        & (df['fecha'] <= end)].groupby('cod')['recogidos'].sum()\
        .values.tolist()

    return hist_recogidas[0]


def report_uploading(m, informe):

    new_folder = "/Users/alejandro/MEGA/work/Oliklak/informes/reports/{}".format(
        date_report)
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    file = '{}/informe_claki_{}_{}.html'.format(
        new_folder, cod_school, date_report)
    informe.save(file)
    link = m.export("informe_claki_{}_{}.html".format(cod_school, date_report))

    return link


if __name__ == "__main__":
    engine = create_engine(
        'mysql+pymysql://ro2wuvla_python:Zeldalink42255@lhcp2008.webapps.net/ro2wuvla_oliclak')
    (recogida, puntos) = query_db(engine)
    df = filter_data(recogida, puntos, "E")
    df_mails = pd.read_excel("./data/test.xlsx", converters={"CÓDIGO": str})
    df_mails = df_mails[df_mails['Tipo Punto'] == "E"][["CÓDIGO", "Correo_1",
                                                        "Correo_2"]]
    df_logos = pd.read_excel("./data/logos_excel.xlsx")
    df_logos = df_logos[df_logos['LOGO INFORME'].notnull()].drop_duplicates(subset=[
                                                                                    'CÓDIGO'])

    cod_school = df.cod.unique().tolist()

    mega = Mega()
    m = mega.login("alejandrobcn95@protonmail.com", "Zeldalink22955")

    cod_school_temp = ['08690E001']
    start = '2021-01-01'
    end = pd.to_datetime(start) + relativedelta(months=+10)

    for i in cod_school_temp:
        sum_hist = hist_data(df, i, end)
        try:
            logo_file = df_logos[df_logos['CÓDIGO']
                                 == i]['LOGO INFORME'].values[0]
        except IndexError:
            logo_file = 'no_logo_school.png'

        (informe, cod_school, date_report) = report_creation(df, i, start, end,
                                                             sum_hist, logo_file)
        link = report_uploading(m, informe)
        name_school = df[df['cod'] == cod_school]['Nombre'].values[0]

        if pd.isnull(df_mails[df_mails['CÓDIGO'] == cod_school]['Correo_2'].values[0]):
            email_to = df_mails[df_mails['CÓDIGO']
                                == cod_school]['Correo_1'].values[0]
            send_mail(link, name_school, date_report, email_to)
        else:
            emails = [df_mails[df_mails['CÓDIGO'] == cod_school]['Correo_1'].values[0],
                      df_mails[df_mails['CÓDIGO'] == cod_school]['Correo_2'].values[0]]
            print(emails)
            for i in emails:
                send_mail(link, name_school, date_report, i)


# "08750E001"
