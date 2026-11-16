import altair as alt
import pandas as pd

AZUL, VERDE, NARANJA, ROJO, GRIS = "#1E4D78", "#1B7F3B", "#C2570C", "#B91C1C", "#6B7280"
ETIQUETA = "Segundo de la Simulación"


def _marca(t):
    return alt.Chart(pd.DataFrame({"x": [t]})).mark_rule(
        strokeDash=[5, 4], color=GRIS, strokeWidth=2).encode(x="x:Q")


def _limite(valor):
    return alt.Chart(pd.DataFrame({"y": [valor]})).mark_rule(
        strokeDash=[6, 4], color=ROJO, strokeWidth=2).encode(y="y:Q")


def _acabado(grafico, titulo):
    return (
        grafico.properties(title=alt.TitleParams(titulo, fontSize=15, fontWeight="bold", anchor="start"), height=260)
        .configure_axis(labelFontSize=12, titleFontSize=13, titleFontWeight="bold")
        .configure_legend(labelFontSize=12, labelFontWeight="bold", orient="bottom", title=None)
    )


def _puntos(df, series, titulo, titulo_y, t, limite=None, ceros=False):
    datos = pd.concat([
        pd.DataFrame({"Segundo": df["t_s"], "Valor": df[col], "Serie": nombre})
        for nombre, (col, _) in series.items()
    ])
    base = alt.Chart(datos).mark_circle(size=14, opacity=0.8).encode(
        x=alt.X("Segundo:Q", title=ETIQUETA),
        y=alt.Y("Valor:Q", title=titulo_y, scale=alt.Scale(zero=ceros)),
        color=alt.Color("Serie:N", scale=alt.Scale(
            domain=list(series), range=[c for _, c in series.values()])),
    )
    capas = base + _marca(t)
    if limite is not None:
        capas = capas + _limite(limite)
    return _acabado(capas, titulo)


def _salinidad(df, t):
    producida = alt.Chart(pd.DataFrame({"Segundo": df["t_s"], "Valor": df["Cp"]})).mark_circle(
        size=14, opacity=0.8, color=VERDE).encode(
        x=alt.X("Segundo:Q", title=ETIQUETA),
        y=alt.Y("Valor:Q", title="Agua producida (g/L)", scale=alt.Scale(zero=True, domain=[0, 0.6]),
                axis=alt.Axis(titleColor=VERDE, labelColor=VERDE)))
    salmuera = alt.Chart(pd.DataFrame({"Segundo": df["t_s"], "Valor": df["Cb"]})).mark_circle(
        size=14, opacity=0.8, color=NARANJA).encode(
        x=alt.X("Segundo:Q", title=ETIQUETA),
        y=alt.Y("Valor:Q", title="Salmuera (g/L)", scale=alt.Scale(zero=False),
                axis=alt.Axis(orient="right", titleColor=NARANJA, labelColor=NARANJA)))
    izquierda = producida + _limite(0.5) + _marca(t)
    return _acabado(alt.layer(izquierda, salmuera).resolve_scale(y="independent"),
                    "Salinidad del agua producida y de la salmuera")


def _latencia(df, t):
    d = df[["t_s", "latencia_s", "dato_valido"]].dropna()
    d = d.assign(Estado=d["dato_valido"].map({1: "Dato usado", 0: "Dato descartado"}))
    base = alt.Chart(d.rename(columns={"t_s": "Segundo", "latencia_s": "Valor"})).mark_circle(
        size=18, opacity=0.8).encode(
        x=alt.X("Segundo:Q", title=ETIQUETA),
        y=alt.Y("Valor:Q", title="Tiempo de llegada (s)", scale=alt.Scale(zero=True)),
        color=alt.Color("Estado:N", scale=alt.Scale(
            domain=["Dato usado", "Dato descartado"], range=[VERDE, ROJO])))
    return _acabado(base + _limite(5.0) + _marca(t), "Tiempo de llegada de los datos")


def crear(df, t):
    return {
        "presion": _puntos(df, {"Presión ordenada": ("TMP_cmd", AZUL), "Presión medida": ("TMP_med", NARANJA)},
                           "Presión ordenada y presión medida", "Presión (bar)", t),
        "caudales": _puntos(df, {"Agua producida": ("Qp", VERDE), "Salmuera": ("Qb", NARANJA)},
                            "Agua producida y salmuera", "Caudal (m³/h)", t, ceros=True),
        "salinidad": _salinidad(df, t),
        "latencia": _latencia(df, t),
    }