from scripts.utils import *
import pandas as pd
import datapane as dp
from dateutil.relativedelta import relativedelta
from scipy.stats import percentileofscore
from datetime import datetime


def total_recogidas_tipo(df, start, end, cod_school):
    tipo_punto = df[df['cod'] == cod_school]['tipo'].values[0]

    total_recogidas_array = df[(df['fecha'] > start)
                               & (df['fecha'] <= end)
                               & (df['tipo'] == tipo_punto)].groupby('cod')['recogidos'].sum()\
        .values.tolist()

    return total_recogidas_array


def report_generator_code(df, start, end, total_recogidas_array, cod_school, sum_hist):
    (fig, table, name_school, recogidas) = current_course_plot(
        df, cod_school, start, end)

    date_report = "{}_{}".format(
        datetime.now().date().month, datetime.now().date().year)
    clakis_curs = sum(recogidas)
    l_aigua_actual_int = round((sum(recogidas) * 1.35) * 40000)

    percentile = percentileofscore(total_recogidas_array, clakis_curs)

    if len(recogidas) > 1:
        try:
            change_prev_recogida = (
                recogidas[-1] - recogidas[-2])/recogidas[-2]
        except (IndexError, ZeroDivisionError):
            change_prev_recogida = 0

        md_subtitle = """ ## ***ID del centre:*** {}
                      """.format(cod_school)

        md_subtitle_2 = """
                        ## ***Nom:*** {}
                        """.format(name_school)

        md_head_1 = """
                    ### Gràfic de les recollides de l' any actual:
                    """

        md_head_11 = """#### En aquest panell es mostra la evolució de les recollides de l' any vigent (en verd), amb una taula sobre els dies de recollida."""

        bool_change = [True if change_prev_recogida > 0 else False][0]

        informe = dp.Report(
            dp.File(file="./images/header.png"),
            dp.Text(md_subtitle),
            dp.Text(md_subtitle_2),
            dp.Text(
                "## ***Mes de recollida:*** {}".format(date_report.replace("_", "-"))),
            dp.Text(md_head_1),
            dp.Text(md_head_11),
            dp.Plot(fig),
            dp.Text("#### Mantenir la recollida sobre la línia negra significa que estem millorant respecte les últimes 3 i, per tant, progressem adequadament :) "),
            dp.Table(table[['fecha', 'recogidos']].set_index('fecha').tail(9)),
            dp.Text(" ## Estadístiques última recollida"),
            dp.Text("#### Dades rellevants sobre el darrer mes de recollida: "),
            dp.Group(
                dp.BigNumber(
                    heading="Clakis última recollida:",
                    value=f'{round(recogidas[-1]):,d}'
                ),
                dp.BigNumber(
                    heading="Litres d' oli úlima recollida:",
                    value=f'{round(recogidas[-1] * 1.35):,d}'
                ),

                dp.BigNumber(
                    heading="Comparatiu últimes dues recollides:",
                    value=recogidas[-1],
                    prev_value=recogidas[-2]
                ),
                dp.BigNumber(
                    heading="Última recollida amb respecte l' anterior (i la variació %): ",
                    value=recogidas[-1] - recogidas[-2],
                    change=round(change_prev_recogida * 100, 2),
                    is_upward_change=bool_change,
                    is_positive_intent=bool_change
                ),
                dp.BigNumber(
                    heading="Litres d' aigua salvats:",
                    value=f'{round((recogidas[-1] * 1.35) * 40000):,d}'
                ),
                dp.BigNumber(
                    heading="Equivalent Piscines Olímpiques:",
                    value=round((recogidas[-1] * 1.35) * 40000 / 2500000, 2)),
                columns=3),
            dp.Text(" ## Estadístiques anuals"),
            dp.Text(
                "#### Dades rellevants sobre les recollides acumulades durant el curs: "),
            dp.Group(
                dp.BigNumber(
                    heading="Clakis recollits aquest any:",
                    value=clakis_curs
                ),
                dp.BigNumber(
                    heading="Litres d' oli recollits:",
                    value=f'{round(clakis_curs * 1.35):,d}'
                ),
                dp.BigNumber(
                    heading="Litres d' aigua salvats:",
                    value=f'{l_aigua_actual_int:,d}'),
                dp.BigNumber(
                    heading="Equivalent Piscines Olímpiques:",
                    value=round(l_aigua_actual_int / 2500000, 2),
                ), columns=2),
            dp.Text(" ## Estadístiques globals"),
            dp.Text(
                "#### Dades rellevants sobre les recollides acumulades històricament al projecte: "),
            dp.Group(
                dp.BigNumber(
                    heading="Litres d' oli recollits des de l' inici del Projecte: ",
                    value=f'{round(sum_hist * 1.35):,d}'
                ),
                dp.BigNumber(
                    heading="Litres d' aigua salvats des de l' inici del Projecte:",
                    value=f'{round(sum_hist * 1.35 * 40000):,d}'
                )),
            dp.Text(" ## Comparatives amb altres referències"),
            dp.Text(
                "#### Es compara utilitzant el pes de l' aigua salvada en tot el curs: "),
            dp.Group(
                dp.BigNumber(
                    heading="Equivalent a nº persones (40 anys, 65 kg):",
                    value=f'{round((sum_hist * 1.35 * 40000)/65):,d}'),
                dp.BigNumber(
                    heading="Equivalent a nº vehicles (900 kg):",
                    value=f'{round((sum_hist * 1.35 * 40000) / 900):,d}'),
                dp.BigNumber(
                    heading="Equivalent a nº piscines olímpiques (2,5 M L):",
                    value=f'{round((sum_hist * 1.35 * 40000) / 2500000):,d}'),
                columns=3),
            dp.Text(
                "## ***************************************************************************************"),
            dp.Text(
                "# **El vostre centre es troba al** {}% **del rànquing dels millors!**".format(round(percentile, 2))),
            dp.Text(
                "## ***************************************************************************************"),
            dp.File(file="./images/footer.png"),
            dp.Text(".")
            )

        # informe.save(path='./reports/informe_claki_{}_{}.html'.format(cod_school, date_report), open=False)
    else:
        informe = None

    return informe, cod_school, date_report
