import streamlit as st

st.set_page_config(
    page_title="Prototipo Virtual de Desalinización Solar",
    page_icon=":material/water_drop:",
    layout="wide",
)

paginas = [
    st.Page("paginas/principal.py", title="Principal", icon=":material/home:", default=True),
    st.Page("paginas/gemelo_pagina.py", title="Gemelo", icon=":material/monitoring:"),
    st.Page("paginas/reportes.py", title="Reportes", icon=":material/table_chart:"),
    st.Page("paginas/documentacion.py", title="Documentación", icon=":material/menu_book:"),
]
pagina = st.navigation(paginas)

ESTILO = """
<style>
[data-testid="stStatusWidget"] {
    display: none !important;
}
header[data-testid="stHeader"] {
    background: #FFFFFF;
    border-bottom: 1px solid #E5E7EB;
    height: 3.75rem;
}
header[data-testid="stHeader"]::before {
    content: "Prototipo Virtual de Desalinización Solar";
    position: absolute;
    left: 1.5rem;
    top: 50%;
    transform: translateY(-50%);
    padding-left: 2.4rem;
    font-size: 1.3rem;
    font-weight: 600;
    color: #1F2937;
    background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='none' stroke='%232B5C8A' stroke-width='1.7' stroke-linejoin='round' d='M12 2.8c-4.6 4-7 7.5-7 10.6 0 4.1 3.1 6.8 7 6.8s7-2.7 7-6.8c0-3.1-2.4-6.6-7-10.6z'/><path fill='none' stroke='%232B5C8A' stroke-width='1.7' stroke-linecap='round' d='M8.6 14.2c.3 1.6 1.5 2.7 3.2 2.9'/></svg>") no-repeat left center / 1.8rem;
}
header[data-testid="stHeader"]::after {
    content: "";
    position: absolute;
    right: 12rem;
    top: 50%;
    transform: translateY(-50%);
    width: 2.2rem;
    height: 2.2rem;
    background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='%236B7280' d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z'/></svg>") no-repeat center / contain;
}
</style>
"""
st.markdown(ESTILO, unsafe_allow_html=True)



st.info(
    "Prototipo virtual: datos simulados con supuestos de diseño; "
    "no son mediciones ni certifican la calidad del agua.",
    icon=":material/info:",
)

pagina.run()