import os

import streamlit as st

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AZUL, VERDE, NARANJA = "#1E4D78", "#2F7D3E", "#B5651D"

ESTILO = """
<style>
.rejilla { display: grid; gap: 1.6rem 2.4rem; margin: 0.8rem 0 1.1rem 0; }
.rejilla.c4 { grid-template-columns: repeat(4, 1fr); }
.rejilla.c5 { grid-template-columns: repeat(5, 1fr); }
.rejilla.c2 { grid-template-columns: repeat(2, 1fr); }
.tarjeta { position: relative; background: #FFFFFF; border: 1.5px solid var(--c);
           border-top: 5px solid var(--c); border-radius: 12px; padding: 0.9rem 1rem;
           box-shadow: 0 2px 8px rgba(15, 23, 42, 0.10); }
.tarjeta.punteada { border-style: dashed; border-top-style: solid; }
.tarjeta .titulo { display: flex; align-items: center; gap: 0.55rem; font-weight: 700;
                   font-size: 1.02rem; line-height: 1.25; color: #111827; }
.tarjeta .num { flex: 0 0 auto; display: inline-flex; align-items: center; justify-content: center;
                width: 1.6rem; height: 1.6rem; border-radius: 50%; background: var(--c);
                color: #FFFFFF; font-size: 0.85rem; font-weight: 700; }
.tarjeta .detalle { margin-top: 0.5rem; font-weight: 600; font-size: 0.93rem;
                    line-height: 1.4; color: #374151; }
.tarjeta.conecta::after { content: "→"; position: absolute; right: -1.9rem; top: 50%;
                          transform: translateY(-50%); font-size: 1.5rem; font-weight: 700;
                          color: #6B7280; }
.separa { text-align: center; margin: 1.1rem 0 0.7rem 0; font-weight: 700; color: #6B7280; }
.grupo { background: var(--f); border: 1px solid var(--c); border-radius: 14px;
         padding: 0.8rem 1rem 1.1rem 1rem; }
.grupo .rotulo { margin-bottom: 0.7rem; font-weight: 700; font-size: 0.95rem;
                 letter-spacing: 0.03em; text-transform: uppercase; color: var(--c); }
.grupo .interior { display: grid; grid-template-columns: 1fr 1fr; gap: 2.4rem; }
</style>
"""


def tarjeta(titulo, detalle, color=AZUL, numero=None, conecta=False, punteada=False):
    clases = "tarjeta" + (" conecta" if conecta else "") + (" punteada" if punteada else "")
    num = f'<span class="num">{numero}</span>' if numero else ""
    lineas = "<br>".join(detalle)
    return (
        f'<div class="{clases}" style="--c:{color}">'
        f'<div class="titulo">{num}<span>{titulo}</span></div>'
        f'<div class="detalle">{lineas}</div></div>'
    )


def grupo(rotulo, color, fondo, tarjetas):
    return (
        f'<div class="grupo" style="--c:{color};--f:{fondo}">'
        f'<div class="rotulo">{rotulo}</div><div class="interior">{tarjetas}</div></div>'
    )


st.markdown(ESTILO, unsafe_allow_html=True)

st.title("Bienvenido")
st.write(
    "Simula, con datos generados por computador, una planta que usa paneles solares "
    "para mover una bomba de ósmosis inversa en una zona no interconectada de Colombia. "
    "Nada de lo que se ve aquí es una medición real."
)

ACCESOS = [
    ("Gemelo", "paginas/gemelo_pagina.py", ":material/monitoring:",
     "Ejecuta la simulación y compara la planta con su modelo ideal."),
    ("Reportes", "paginas/reportes.py", ":material/table_chart:",
     "Tablas de verificación, desvíos y gráficos de cada escenario."),
    ("Documentación", "paginas/documentacion.py", ":material/menu_book:",
     "Conceptos, símbolos, fórmulas y cómo funciona la simulación."),
]
for columna, (titulo, ruta, icono, texto) in zip(st.columns(3), ACCESOS):
    with columna.container(border=True):
        st.subheader(titulo)
        st.write(texto)
        st.page_link(ruta, label=f"Ir a {titulo}", icon=icono)

st.header("La Planta por Fuera y por Dentro")
IMAGENES = [
    ("imagenes/exterior_etiquetada.png", "Vista exterior de la planta, con cada parte rotulada."),
    ("imagenes/interior_etiquetada.png", "Vista interior de la planta, con cada parte rotulada."),
]
for columna, (archivo, pie) in zip(st.columns(2), IMAGENES):
    with columna:
        ruta = os.path.join(RAIZ, archivo)
        if os.path.exists(ruta):
            st.image(ruta)
            st.caption(pie)
        else:
            st.warning(f"Falta el archivo {archivo}")

st.header("Arquitectura")
st.caption("Cómo viaja la información, desde el sensor hasta el panel de control.")
BLOQUES = [
    ("Proceso Virtual", ["Produce caudales,", "salinidades y presión"]),
    ("Sensado y Adquisición", ["Mide con ruido", "seis variables"]),
    ("Comunicación IoT", ["Envía un paquete", "por segundo"]),
    ("Motor de Control", ["Decide el estado y", "la presión de la bomba"]),
    ("Gemelo Digital", ["Calcula el caso ideal", "para comparar"]),
    ("Analítica e Indicadores", ["Calcula los KPIs", "y los desvíos"]),
    ("Panel de Control", ["Muestra tarjetas,", "curvas y alertas"]),
]
bloques = "".join(
    tarjeta(titulo, detalle, numero=i, conecta=i not in (4, 7))
    for i, (titulo, detalle) in enumerate(BLOQUES, start=1)
)
st.markdown(f'<div class="rejilla c4">{bloques}</div>', unsafe_allow_html=True)
st.caption(
    "Se miden seis variables: irradiancia, caudal de entrada, salinidad de entrada, "
    "presión de la membrana, caudal producido y salinidad del agua producida."
)

st.header("Mapa Conceptual: Cómo se Mueve el Agua")
recorrido_agua = [
    ("Agua de Mar", ["Salinidad (Cf):", "30 a 40 g/L"], False),
    ("Captación", ["Caudal (Qf):", "0,60 a 1,20 m³/h"], False),
    ("Pretratamiento", ["Filtros que retiran", "sólidos"], True),
    ("Bomba de Alta Presión", ["Presión (TMP):", "45 a 60 bar"], False),
    ("Ósmosis Inversa", ["Recuperación (R):", "0,25 a 0,40"], False),
]
recorrido = "".join(
    tarjeta(titulo, detalle, numero=i, conecta=i < 5, punteada=punteada)
    for i, (titulo, detalle, punteada) in enumerate(recorrido_agua, start=1)
)
producida = (
    tarjeta("Agua Producida", ["Salinidad (Cp):", "0,50 g/L o menos"], VERDE, conecta=True)
    + tarjeta("Almacenamiento y Distribución", ["A la comunidad"], VERDE, punteada=True)
)
salmuera = (
    tarjeta("Salmuera (Rechazo)", ["Caudal (Qb = Qf − Qp)", "Salinidad (Cb)"], NARANJA, conecta=True)
    + tarjeta("Manejo Ambiental y Retorno al Mar", ["Difusor de descarga"], NARANJA, punteada=True)
)
st.markdown(
    f'<div class="rejilla c5">{recorrido}</div>'
    '<div class="separa">&#9660; Después de la membrana, el agua sigue dos caminos &#9660;</div>'
    '<div class="rejilla c2">'
    + grupo("Camino del agua producida", VERDE, "#F1F8F2", producida)
    + grupo("Camino de la salmuera", NARANJA, "#FDF4EA", salmuera)
    + "</div>",
    unsafe_allow_html=True,
)
st.caption(
    "Las cajas con borde punteado son contexto del proceso: "
    "el modelo no calcula variables para ellas."
)