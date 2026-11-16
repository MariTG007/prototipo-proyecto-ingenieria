"""dispersion.py - Los seis gráficos de dispersión de la página Reportes."""
import altair as alt
import pandas as pd

from gemelo import gemelo
from kpis import calcular
from parametros import ESCENARIOS, escenario
from simulador import simular

SEMILLAS = (1, 2, 3)
AZUL, VERDE, NARANJA, ROJO, GRIS = "#1E4D78", "#1B7F3B", "#C2570C", "#B91C1C", "#6B7280"


def barrido(variable, valores):
    """Repite una corrida corta de 300 s variando solo una variable (G o Cf)."""
    filas = []
    for v in valores:
        esc = escenario(f"{variable}_{v}", "barrido",
                        [(0, v if variable == "G" else 850)],
                        Cf=v if variable == "Cf" else 35.0)
        for s in SEMILLAS:
            k = calcular(simular(esc, s, n_ciclos=300), esc)
            filas.append({"valor": v, "SEC": k["SEC_kWh_m3"], "Cp": k["Cp_media_g_L"], "R": k["R_media"]})
    return pd.DataFrame(filas)


def calcular_datos():
    """Corre todo lo necesario para los seis gráficos (tarda unos segundos)."""
    corridas, caudales = [], []
    for nombre, esc in ESCENARIOS.items():
        d = simular(esc, 1)
        corridas.append(d.iloc[::5].assign(Escenario=nombre))                  # 1 punto cada 5 s
        ideal = gemelo(esc["G"][0][1], esc["Qf"], esc["Cf"])["qp"]
        for s in SEMILLAS:
            k = calcular(simular(esc, s), esc)
            caudales.append({"Escenario": nombre, "Ideal": ideal, "Simulado": k["Qp_media_m3_h"]})
    return {
        "corridas": pd.concat(corridas),
        "caudales": pd.DataFrame(caudales),
        "barrido_G": barrido("G", range(400, 1001, 100)),
        "barrido_Cf": barrido("Cf", range(30, 41, 2)),
        "latencia": pd.concat([simular(ESCENARIOS[n], 1).assign(Escenario=n) for n in ("V01", "V06")]),
    }


def _linea(x0, y0, x1, y1, color=GRIS, punteada=False):
    datos = pd.DataFrame({"x": [x0, x1], "y": [y0, y1]})
    return alt.Chart(datos).mark_line(color=color, strokeWidth=2, strokeDash=[6, 4] if punteada else [1, 0]).encode(
        x="x:Q", y="y:Q")


def _regla(valor, color=ROJO):
    return alt.Chart(pd.DataFrame({"y": [valor]})).mark_rule(
        strokeDash=[6, 4], color=color, strokeWidth=2).encode(y="y:Q")


def _acabado(grafico, titulo):
    return (
        grafico.properties(title=alt.TitleParams(titulo, fontSize=15, fontWeight="bold", anchor="start"), height=380)
        .configure_axis(labelFontSize=12, titleFontSize=13, titleFontWeight="bold")
        .configure_legend(labelFontSize=12, labelFontWeight="bold", orient="bottom", title=None,
                          columns=5, symbolLimit=0)
    )


def _eje(titulo, minimo=None, maximo=None):
    escala = alt.Scale(domain=[minimo, maximo], zero=False) if minimo is not None else alt.Scale(zero=False)
    return alt.Axis(title=titulo), escala


def _dispersion(datos, x, y, titulo_x, titulo_y, dominio, color=None, tamano=40, colores=None):
    ejes_x, escala_x = _eje(titulo_x, *dominio[0])
    ejes_y, escala_y = _eje(titulo_y, *dominio[1])
    codigo = dict(x=alt.X(f"{x}:Q", axis=ejes_x, scale=escala_x),
                  y=alt.Y(f"{y}:Q", axis=ejes_y, scale=escala_y))
    if color:
        escala = alt.Scale(domain=list(colores), range=list(colores.values())) if colores else alt.Undefined
        codigo["color"] = alt.Color(f"{color}:N", scale=escala)
        codigo["tooltip"] = [color, x, y]
    return alt.Chart(datos).mark_circle(size=tamano, opacity=0.75, color=AZUL).encode(**codigo)


def crear(d):
    c = d["corridas"]
    seguimiento = (_dispersion(c, "TMP_cmd", "TMP_med", "Presión ordenada (bar)", "Presión medida (bar)",
                               ((44, 61), (44, 61)), "Escenario", 14)
                   + _linea(44, 44, 61, 61) + _linea(44, 44 * 1.05, 61, 61 * 1.05, punteada=True)
                   + _linea(44, 44 * 0.95, 61, 61 * 0.95, punteada=True))
    desvio = (_dispersion(d["caudales"], "Ideal", "Simulado", "Modelo ideal (m³/h)",
                          "Planta simulada (m³/h)", ((0.2, 0.45), (0.2, 0.45)), "Escenario", 60)
              + _linea(0.2, 0.2, 0.45, 0.45))
    energia = (_dispersion(d["barrido_G"], "valor", "SEC", "Irradiancia (W/m²)", "Consumo de energía (kWh/m³)",
                           ((350, 1050), (3.0, 5.0)))
               + _regla(4.5))
    sal = (_dispersion(d["barrido_Cf"], "valor", "Cp", "Salinidad del agua de mar (g/L)",
                       "Salinidad del agua producida (g/L)", ((29, 41), (0.2, 0.6)))
           + _regla(0.5))
    lat = d["latencia"].dropna(subset=["latencia_s"])[["escenario", "t_s", "latencia_s"]].rename(
        columns={"escenario": "Escenario"}).replace({"Escenario": {"V01": "Red normal (V01)", "V06": "Red degradada (V06)"}})
    latencia = (_dispersion(lat, "t_s", "latencia_s", "Segundo de la simulación", "Latencia (s)",
                            ((-10, 610), (0, 40)), "Escenario", 14,
                            colores={"Red normal (V01)": VERDE, "Red degradada (V06)": NARANJA}) + _regla(5.0))
    banda = alt.Chart(pd.DataFrame({"a": [0.25], "b": [0.40]})).mark_rect(color=VERDE, opacity=0.15).encode(
        y="a:Q", y2="b:Q")
    recuperacion = (_dispersion(d["barrido_G"], "valor", "R", "Irradiancia (W/m²)", "Recuperación",
                                ((350, 1050), (0.2, 0.45))) + banda)
    return {
        "reporte_1": _acabado(seguimiento, "Presión ordenada vs. presión medida (banda de ±5 %)"),
        "reporte_2": _acabado(desvio, "Agua producida: modelo ideal vs. planta simulada"),
        "reporte_3": _acabado(energia, "Consumo de energía por m³ según la irradiancia"),
        "reporte_4": _acabado(sal, "Salinidad del agua producida según la del agua de mar"),
        "reporte_5": _acabado(latencia, ["Latencia de los datos:", "comunicación normal vs. degradada"]),
        "reporte_6": _acabado(recuperacion, "Recuperación según la irradiancia"),
    }