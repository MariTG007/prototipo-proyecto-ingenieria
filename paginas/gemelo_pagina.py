import time
import pandas as pd
import streamlit as st
import curvas
import esquema
from nombres import ACCIONES_LEGIBLES, ALERTAS_LEGIBLES, PIES, numero
from parametros import ESCENARIOS, N_CICLOS
from simulador import simular

SEGUNDOS_POR_CUADRO = 4
PAUSA = 0.05

COLOR_ESTADO = {
    "NORMAL": "#1B7F3B",
    "ENERGY_LIMIT": "#C2570C",
    "HIGH_SALINITY": "#6D28D9",
    "SAFE_MODE": "#B91C1C",
}

ESTILO = """
<style>
.datos { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.75rem;
         margin: 0.6rem 0 1rem 0; }
.dato { display: flex; flex-direction: column; justify-content: space-between; gap: 0.6rem;
        background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 10px;
        padding: 0.8rem 0.9rem; box-shadow: 0 1px 4px rgba(15, 23, 42, 0.08); }
.dato .nombre { font-weight: 700; font-size: 0.82rem; line-height: 1.25; color: #4B5563; }
.dato .valor { font-weight: 700; font-size: 1.9rem; line-height: 1.1; color: #111827; }
.dato .valor.estado { font-size: 1.2rem; }
</style>
"""


def dato(nombre, valor, ayuda, color="#111827", estado=False):
    clase = "valor estado" if estado else "valor"
    return (
        f'<div class="dato" title="{ayuda}"><div class="nombre">{nombre}</div>'
        f'<div class="{clase}" style="color:{color}">{valor}</div></div>'
    )


@st.cache_data
def correr(nombre, semilla, personalizar, G, Qf, Cf):
    esc = dict(ESCENARIOS[nombre])
    if personalizar:
        esc.update(G=[(0, G)], Qf=Qf, Cf=Cf)
    return simular(esc, semilla=semilla)


def iniciar():
    st.session_state["reproduciendo"] = True


def detener():
    st.session_state["reproduciendo"] = False


def pausar(clave):
    st.session_state[clave] = st.session_state.get("t_actual", st.session_state[clave])
    st.session_state["reproduciendo"] = False


def reiniciar(clave, valor):
    st.session_state[clave] = valor
    st.session_state["reproduciendo"] = False


st.title("Gemelo")

with st.container(border=True):
    c1, c2, c3 = st.columns([3, 1, 2], vertical_alignment="bottom")
    nombre = c1.selectbox(
        "Escenario", list(ESCENARIOS),
        format_func=lambda k: f"{k}: {ESCENARIOS[k]['descripcion']}",
        on_change=detener,
    )
    semilla = c2.number_input("Semilla", min_value=1, max_value=999, value=1, step=1, on_change=detener)
    personalizar = c3.checkbox("Personalizar condiciones", on_change=detener)
    base = ESCENARIOS[nombre]
    G, Qf, Cf = base["G"][0][1], base["Qf"], base["Cf"]
    if personalizar:
        g1, g2, g3 = st.columns(3)
        G = g1.number_input("Irradiancia (W/m²)", 200, 1000, int(G), step=50, key=f"G_{nombre}")
        Qf = g2.number_input("Caudal de Agua de Mar (m³/h)", 0.60, 1.20, float(Qf), step=0.05, key=f"Qf_{nombre}")
        Cf = g3.number_input("Salinidad del Agua de Mar (g/L)", 30.0, 40.0, float(Cf), step=0.5, key=f"Cf_{nombre}")

df = correr(nombre, semilla, personalizar, G, Qf, Cf)

esperado = base["esperado"]
casos = df[(df["estado"] == esperado) | df["alertas"].str.contains(esperado)]
casos = casos[casos["t_s"] >= base["t_evento"]]
t_inicial = max(int(casos["t_s"].iloc[0]), 30) if esperado != "NORMAL" and len(casos) else 300

clave_t = f"segundo_{nombre}_{semilla}_{personalizar}"
st.session_state.setdefault(clave_t, t_inicial)
if "t_pendiente" in st.session_state:
    st.session_state[clave_t] = st.session_state.pop("t_pendiente")
t = st.slider("Segundo de la Simulación", 0, N_CICLOS - 1, key=clave_t, on_change=detener)
st.caption("Mueve el control para ver cualquier segundo de la simulación. "
           "Al cambiar de escenario se coloca en un segundo donde se nota su efecto.")


def pintar_datos(fila, t):
    DATOS = [
        ("Irradiancia (W/m²)", numero(fila["G"], 0), "Energía del sol que llega a los paneles."),
        ("Potencia Solar Disponible (kW)", numero(fila["P_util"]), "Potencia que llega a la bomba después del convertidor."),
        ("Potencia que Pide la Bomba (kW)", numero(fila["P_req"]), "Potencia que necesita la bomba a la presión ordenada."),
        ("Agua Producida (m³/h)", numero(fila["Qp"], 3), "Caudal de agua desalinizada que sale de la membrana."),
        ("Salinidad del Agua Producida (g/L)", numero(fila["Cp"], 3), "Debe quedar en 0,50 g/L o menos."),
    ]
    tarjetas = "".join(dato(n, v, a) for n, v, a in DATOS)
    estado = fila["estado"]
    tarjetas += dato("Estado del Controlador", estado.replace("_", "_<wbr>"),
                     "Modo en que está trabajando el controlador.", COLOR_ESTADO[estado], estado=True)
    st.markdown(ESTILO + f'<div class="datos">{tarjetas}</div>', unsafe_allow_html=True)
    alertas = [a for a in fila["alertas"].split("|") if a]
    if alertas:
        texto = "; ".join(ALERTAS_LEGIBLES[a] for a in alertas)
        st.warning(f"**Alertas activas en el segundo {t}:** {texto}. "
                   f"Acción del controlador: {ACCIONES_LEGIBLES[fila['accion']]}.")
    else:
        st.success(f"Sin alertas activas en el segundo {t}.")


def registro_alertas(df, t):
    """Una fila por cada vez que una alerta se activa, hasta el segundo t elegido."""
    hasta = df.iloc[: t + 1]
    filas = []
    for clave, nombre in ALERTAS_LEGIBLES.items():
        activa = hasta["alertas"].str.contains(clave)
        episodio = (activa != activa.shift()).cumsum()
        for _, grupo in hasta[activa].groupby(episodio[activa]):
            inicio, fin = int(grupo["t_s"].iloc[0]), int(grupo["t_s"].iloc[-1])
            filas.append({"Alerta": nombre, "Desde el Segundo": inicio,
                          "Hasta el Segundo": "Sigue activa" if fin == t else str(fin),
                          "Duración (s)": fin - inicio + 1})
    return pd.DataFrame(filas)

zona_datos = st.empty()

st.subheader("Gráfica de Simulación")
reproduciendo = st.session_state.get("reproduciendo", False)
b1, b2, b3, _ = st.columns([1, 1, 1, 5])
b1.button("Iniciar", on_click=iniciar, icon=":material/play_arrow:")
b2.button("Reiniciar", on_click=reiniciar, args=(clave_t, t_inicial), icon=":material/replay:")
if reproduciendo:
    b3.button("Pausar", on_click=pausar, args=(clave_t,), icon=":material/pause:")
zona_grafica = st.empty()

if reproduciendo:
    inicio = t if t < N_CICLOS - 1 else 0
    for ti in range(inicio, N_CICLOS, SEGUNDOS_POR_CUADRO):
        st.session_state["t_actual"] = ti
        fila_ti = df.iloc[ti]
        with zona_datos.container():
            pintar_datos(fila_ti, ti)
        with zona_grafica.container():
            st.markdown(esquema.dibujar(fila_ti, animar=False), unsafe_allow_html=True)
        time.sleep(PAUSA)
    st.session_state["reproduciendo"] = False
    st.session_state["t_pendiente"] = N_CICLOS - 1
    st.rerun()
else:
    fila = df.iloc[t]
    with zona_datos.container():
        pintar_datos(fila, t)
    with zona_grafica.container():
        pestana_esquema, pestana_curvas = st.tabs(["Esquema de la Planta", "Curvas en el Tiempo"])
        with pestana_esquema:
            st.markdown(esquema.dibujar(fila), unsafe_allow_html=True)
            st.caption("Cada parte se pinta según su estado. Las líneas punteadas son las "
                       "lecturas de los sensores y las órdenes del controlador.")
        with pestana_curvas:
            graficas = curvas.crear(df, t)
            for par in (("presion", "caudales"), ("salinidad", "latencia")):
                for columna, clave in zip(st.columns(2), par):
                    with columna:
                        st.altair_chart(graficas[clave])
                        st.caption(PIES["curva_" + clave])

st.subheader("Registro de Alertas")
registro = registro_alertas(df, t)
if registro.empty:
    st.info("Hasta este segundo no se ha activado ninguna alerta.")
else:
    st.dataframe(registro.sort_values("Desde el Segundo"), hide_index=True)
st.caption("Cada fila es una vez que se activó una alerta, desde el inicio hasta el segundo elegido.")