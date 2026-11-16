import pandas as pd
import streamlit as st

import dispersion
from gemelo import gemelo
from kpis import calcular
from nombres import ALERTAS_LEGIBLES, NOMBRES_COLUMNAS, PIES, numero, tabla_indicadores
from parametros import ESCENARIOS
from simulador import simular

SEMILLAS = (1, 2, 3)


@st.cache_data
def kpis_del_escenario(nombre):
    """Corre el escenario con 3 semillas y devuelve un renglón de indicadores por corrida."""
    esc = ESCENARIOS[nombre]
    filas = [calcular(simular(esc, s), esc) for s in SEMILLAS]
    return pd.DataFrame(filas)


@st.cache_data
def registro_de(nombre):
    """Registro de la corrida con semilla 1: un renglón por segundo, con nombres claros."""
    return simular(ESCENARIOS[nombre], 1).round(4).rename(columns=NOMBRES_COLUMNAS)


@st.cache_data
def datos_graficos():
    return dispersion.calcular_datos()


def tabla_verificacion(clave, r):
    """Casos V-01 a V-06 de la Tabla 9 [E3]; el resultado es el promedio de las 3 semillas."""
    m = r.mean(numeric_only=True)
    reaccion = m["reaccion_alerta_s"]
    casos = [
        ("V-01", "Balance de agua", "Error máximo de 0 %", m["err_balance_masa_max_%"],
         m["err_balance_masa_max_%"] < 1e-6, "%", 6),
        ("V-02", "Balance de sal", "Error máximo de 0,1 % o menos", m["err_balance_sal_max_%"],
         m["err_balance_sal_max_%"] <= 0.1, "%", 4),
        ("V-03", "Seguimiento de la presión", "95 % o más de los segundos con error de 5 % o menos",
         m["ciclos_e_TMP<=5%_%"], m["ciclos_e_TMP<=5%_%"] >= 95, "%", 1),
        ("V-04", "Llegada de los datos", "95 % o más de los datos con latencia de 5 s o menos",
         m["latencia<=5s_%"], m["latencia<=5s_%"] >= 95, "%", 1),
        ("V-05", "Datos completos", "98 % o más de los datos válidos",
         m["completitud_%"], m["completitud_%"] >= 98, "%", 1),
        ("V-06", "Reacción ante una perturbación", "Reacciona en 10 s o menos",
         reaccion, reaccion <= 10, "s", 1),
    ]
    filas = []
    for caso, nombre, criterio, valor, cumple, unidad, dec in casos:
        if valor != valor:
            resultado, estado = "No aplica", "No aplica"
        else:
            resultado = f"{numero(valor, dec)} {unidad}"
            estado = "Cumple" if cumple else "No cumple"
        filas.append({"Caso": caso, "Qué se Comprueba": nombre, "Criterio": criterio,
                      "Resultado Obtenido": resultado, "Estado": estado})
    # Estado esperado del escenario, según la Tabla 10 [E3]
    esperado = ESCENARIOS[clave]["esperado"]
    if esperado == "NORMAL":
        llegaron = (r["estado_dominante"] == "NORMAL").sum()
        criterio = "Se mantiene en estado NORMAL"
    else:
        llegaron = r["reaccion_alerta_s"].notna().sum()
        criterio = f"Llega a: {ALERTAS_LEGIBLES.get(esperado, esperado)}"
    filas.append({"Caso": "Control", "Qué se Comprueba": "Estado esperado del controlador",
                  "Criterio": criterio, "Resultado Obtenido": f"{llegaron} de {len(r)} corridas",
                  "Estado": "Cumple" if llegaron == len(r) else "No cumple"})
    return pd.DataFrame(filas)


def tabla_desvios(nombre, r):
    """Compara la planta simulada con el modelo ideal (gemelo) del escenario."""
    esc = ESCENARIOS[nombre]
    g = gemelo(esc["G"][0][1], esc["Qf"], esc["Cf"])
    m = r.mean(numeric_only=True)
    pares = [
        ("Agua Producida (m³/h)", g["qp"], m["Qp_media_m3_h"], 3),
        ("Recuperación", g["R"], m["R_media"], 3),
        ("Salinidad de la Salmuera (g/L)", g["cb"], m["Cb_media_g_L"], 1),
        ("Consumo de Energía (kWh/m³)", g["SEC"], m["SEC_kWh_m3"], 2),
        ("Presión de la Membrana (bar)", g["tmp_cmd"], m["TMP_media_bar"], 1),
    ]
    filas = []
    for variable, ideal, simulado, dec in pares:
        filas.append({"Variable": variable,
                      "Modelo Ideal": numero(ideal, dec),
                      "Planta Simulada": numero(simulado, dec),
                      "Diferencia": numero(simulado - ideal, dec),
                      "Diferencia (%)": numero((simulado - ideal) / ideal * 100, 1)})
    return pd.DataFrame(filas)


def color_estado(v):
    if v == "Cumple":
        return "color: #1B7F3B; font-weight: 700"
    if v == "No cumple":
        return "color: #B91C1C; font-weight: 700"
    return "color: #6B7280"


st.title("Reportes")

nombre = st.selectbox(
    "Escenario",
    list(ESCENARIOS),
    format_func=lambda k: f"{k}: {ESCENARIOS[k]['descripcion']}",
    key="reportes_escenario",
)
resultados = kpis_del_escenario(nombre)

st.subheader("Verificación de los Casos de Prueba")
st.dataframe(tabla_verificacion(nombre, resultados).style.map(color_estado, subset=["Estado"]),
             hide_index=True)
st.caption("Resultado promedio de 3 corridas con semillas distintas. «No aplica» significa que el caso no se prueba en este escenario.")

st.subheader("Comparación con el Modelo Ideal")
st.dataframe(tabla_desvios(nombre, resultados), hide_index=True)
st.caption("El modelo ideal usa las fórmulas de la Etapa 3. La diferencia muestra cuánto se aparta la planta simulada de él.")

st.subheader("Indicadores de la Corrida (KPIs)")
indicadores = resultados.mean(numeric_only=True).to_dict()
indicadores["estado_dominante"] = resultados["estado_dominante"].mode().iloc[0]
st.dataframe(tabla_indicadores(indicadores), hide_index=True)
st.caption("Promedio de las 3 corridas completas de 600 s. «No aplica» significa que el indicador no se mide en este escenario.")

st.subheader("Gráficos de Dispersión")
st.caption("Estos seis gráficos usan varios escenarios a la vez, no solo el elegido arriba.")
graficos = dispersion.crear(datos_graficos())
claves = list(graficos)
for fila in range(0, 6, 2):
    for columna, clave in zip(st.columns(2), claves[fila:fila + 2]):
        with columna:
            st.altair_chart(graficos[clave])
            st.caption(PIES[clave])

st.subheader("Registro de la Corrida")
registro = registro_de(nombre)
st.dataframe(registro.head(20), hide_index=True)
st.download_button("Descargar CSV", registro.to_csv(index=False).encode("utf-8-sig"),
                   file_name=f"registro_{nombre}.csv", mime="text/csv", icon=":material/download:")
st.caption("Vista previa de los primeros 20 segundos. El archivo trae los 600 segundos del escenario elegido (semilla 1).")