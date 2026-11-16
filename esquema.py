from nombres import numero

VERDE, NARANJA, VIOLETA, ROJO = "#1B7F3B", "#C2570C", "#6D28D9", "#B91C1C"
AZUL, AMARILLO, GRIS = "#2B6CB0", "#D69E2E", "#6B7280"

ACCION = {
    "REDUCIR_TMP": "Reduce la presión",
    "ALERTAR": "Avisa al operador",
    "DESVIAR_PERMEADO": "Desvía el agua",
    "PRESION_MINIMA": "Presión mínima",
    "": "Sin acción",
}
COLOR_ESTADO = {"NORMAL": VERDE, "ENERGY_LIMIT": NARANJA, "HIGH_SALINITY": VIOLETA, "SAFE_MODE": ROJO}
Y = 270  # altura de la línea principal del agua

DEFS = (
    '<linearGradient id="metalV" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#8A95A1"/>'
    '<stop offset=".35" stop-color="#F4F6F8"/><stop offset=".7" stop-color="#C5CCD4"/>'
    '<stop offset="1" stop-color="#7D8895"/></linearGradient>'
    '<linearGradient id="metalH" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#8A95A1"/>'
    '<stop offset=".35" stop-color="#F4F6F8"/><stop offset=".7" stop-color="#C5CCD4"/>'
    '<stop offset="1" stop-color="#7D8895"/></linearGradient>'
    '<linearGradient id="mar" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#6FB6E8"/>'
    '<stop offset="1" stop-color="#1B6BB5"/></linearGradient>'
    '<linearGradient id="cielo" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/>'
    '<stop offset="1" stop-color="#E6F1FA"/></linearGradient>'
    '<linearGradient id="panel" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#3B82D0"/>'
    '<stop offset="1" stop-color="#123F7A"/></linearGradient>'
    '<linearGradient id="motor" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#1E4D78"/>'
    '<stop offset=".4" stop-color="#4D86B8"/><stop offset="1" stop-color="#1E4D78"/></linearGradient>'
    '<linearGradient id="agua" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#9ACDF3"/>'
    '<stop offset="1" stop-color="#3D8FD6"/></linearGradient>'
    '<filter id="sombra" x="-20%" y="-20%" width="150%" height="150%">'
    '<feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.28"/></filter>'
)


def texto(x, y, s, tam=15, color="#111827", ancla="start", peso=700, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{tam}" font-weight="{peso}" fill="{color}" '
            f'text-anchor="{ancla}"{extra}>{s}</text>')


def titulo(x, y, lineas):
    return "".join(texto(x, y + 18 * i, l, 16, ancla="middle") for i, l in enumerate(lineas))


def tarjeta(x, y, w, lineas, color):
    h = 14 + 21 * len(lineas)
    partes = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="#FFFFFF" '
              f'stroke="{color}" stroke-width="2.5" filter="url(#sombra)"/>']
    for i, linea in enumerate(lineas):
        partes.append(texto(x + 11, y + 23 + 21 * i, linea, 14.5, "#1F2937"))
    return "".join(partes)


def punto(x, y, color):
    return f'<circle cx="{x}" cy="{y}" r="8.5" fill="{color}" stroke="#FFFFFF" stroke-width="3"/>'


def tuberia(trazo, color, animar, flecha=True):
    casco = (f'<path d="{trazo}" fill="none" stroke="#CBD3DC" stroke-width="15" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    clase = ' class="flujo"' if animar else ' stroke-dasharray="10 7"'
    marca = f' marker-end="url(#p{color[1:]})"' if flecha else ""
    flujo = (f'<path d="{trazo}" fill="none" stroke="{color}" stroke-width="5"{clase} '
             f'stroke-linejoin="round"{marca}/>')
    return casco + flujo


def senal(trazo):
    return (f'<path d="{trazo}" fill="none" stroke="{GRIS}" stroke-width="2.6" stroke-dasharray="6 5" '
            f'stroke-linejoin="round" marker-end="url(#p{GRIS[1:]})"/>')


def cilindro_v(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w * 0.38:.0f}" fill="url(#metalV)" '
            f'stroke="#6B7280" stroke-width="2" filter="url(#sombra)"/>'
            f'<line x1="{x}" y1="{y + h * 0.2:.0f}" x2="{x + w}" y2="{y + h * 0.2:.0f}" stroke="#6B7280" stroke-width="1.6"/>'
            f'<line x1="{x}" y1="{y + h * 0.8:.0f}" x2="{x + w}" y2="{y + h * 0.8:.0f}" stroke="#6B7280" stroke-width="1.6"/>')


def recipiente_h(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2:.0f}" fill="url(#metalH)" '
            f'stroke="#6B7280" stroke-width="2" filter="url(#sombra)"/>'
            f'<line x1="{x + 24}" y1="{y}" x2="{x + 24}" y2="{y + h}" stroke="#6B7280" stroke-width="1.6"/>'
            f'<line x1="{x + w - 24}" y1="{y}" x2="{x + w - 24}" y2="{y + h}" stroke="#6B7280" stroke-width="1.6"/>')


def bomba_captacion(cx, cy):
    radios = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{cx + 12 * dx:.1f}" y2="{cy + 12 * dy:.1f}" stroke="#6B7280" stroke-width="2.4"/>'
        for dx, dy in ((0, -1), (0.87, 0.5), (-0.87, 0.5)))
    return (f'<circle cx="{cx}" cy="{cy}" r="27" fill="url(#metalV)" stroke="#6B7280" stroke-width="2.2" filter="url(#sombra)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="15" fill="#E8ECF0" stroke="#6B7280" stroke-width="1.8"/>{radios}')


def bomba_alta(x, yc):
    cx = x + 40
    return (
        f'<rect x="{x + 18}" y="{yc - 72}" width="44" height="52" rx="6" fill="url(#motor)" stroke="#12324F" '
        f'stroke-width="2" filter="url(#sombra)"/>'
        + "".join(f'<line x1="{x + 26 + 9 * i}" y1="{yc - 66}" x2="{x + 26 + 9 * i}" y2="{yc - 26}" '
                  f'stroke="#12324F" stroke-width="1.6" opacity=".55"/>' for i in range(4))
        + f'<rect x="{x + 26}" y="{yc - 22}" width="28" height="8" fill="#6B7280"/>'
        f'<rect x="{x}" y="{yc - 16}" width="80" height="38" rx="10" fill="url(#metalH)" stroke="#6B7280" '
        f'stroke-width="2" filter="url(#sombra)"/>'
        f'<circle cx="{cx}" cy="{yc + 3}" r="13" fill="#FFFFFF" stroke="#4B5563" stroke-width="2"/>'
        f'<line x1="{cx}" y1="{yc + 3}" x2="{cx + 8}" y2="{yc - 4}" stroke="#B91C1C" stroke-width="2.4" stroke-linecap="round"/>'
        f'<rect x="{x - 6}" y="{yc + 22}" width="92" height="8" rx="3" fill="#6B7280"/>'
    )


def panel_solar():
    rejilla = "".join(
        f'<line x1="{70 + 33 * i / 4 + 0:.0f}" y1="118" x2="{100 + 140 * i / 4:.0f}" y2="50" '
        f'stroke="#BBD7F2" stroke-width="1.4"/>' for i in range(1, 4))
    sol = "".join(
        f'<line x1="{38 + 17 * dx:.1f}" y1="{58 + 17 * dy:.1f}" x2="{38 + 24 * dx:.1f}" y2="{58 + 24 * dy:.1f}" '
        f'stroke="#F6C945" stroke-width="3" stroke-linecap="round"/>'
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)))
    return (
        '<circle cx="38" cy="58" r="12" fill="#F6C945" stroke="#E0A800" stroke-width="2"/>' + sol
        + '<polygon points="70,118 100,50 240,50 210,118" fill="url(#panel)" stroke="#0F3B73" '
        'stroke-width="2.4" filter="url(#sombra)"/>' + rejilla
        + '<line x1="85" y1="84" x2="225" y2="84" stroke="#BBD7F2" stroke-width="1.4"/>'
    )


def inversor():
    return (
        '<rect x="405" y="45" width="100" height="75" rx="11" fill="url(#metalH)" stroke="#6B7280" '
        'stroke-width="2" filter="url(#sombra)"/>'
        '<polygon points="457,55 441,86 452,86 448,111 471,76 459,76" fill="#D69E2E" stroke="#9C6F10" stroke-width="1.5"/>'
    )


def controlador(estado, color):
    return (
        '<rect x="545" y="45" width="110" height="75" rx="11" fill="#1F2937" stroke="#0F172A" '
        'stroke-width="2" filter="url(#sombra)"/>'
        '<rect x="555" y="54" width="90" height="48" rx="5" fill="#0B1220"/>'
        f'<text x="600" y="84" font-size="12.5" font-weight="700" fill="{color}" text-anchor="middle">{estado}</text>'
        '<path d="M620 66 q10 -9 20 0 M624 70 q6 -5 12 0" fill="none" stroke="#6EE7B7" stroke-width="2" stroke-linecap="round"/>'
        '<rect x="588" y="120" width="24" height="6" fill="#6B7280"/>'
    )


def casa():
    return (
        '<rect x="1156" y="262" width="52" height="76" fill="url(#metalV)" stroke="#6B7280" stroke-width="2" filter="url(#sombra)"/>'
        '<polygon points="1148,264 1182,232 1216,264" fill="#7D8895" stroke="#4B5563" stroke-width="2"/>'
        '<rect x="1174" y="302" width="16" height="36" fill="#EEF1F4" stroke="#6B7280" stroke-width="1.6"/>'
        '<rect x="1164" y="272" width="13" height="13" fill="#DDE5EC" stroke="#6B7280" stroke-width="1.4"/>'
        '<rect x="1187" y="272" width="13" height="13" fill="#DDE5EC" stroke="#6B7280" stroke-width="1.4"/>'
    )


def mar():
    ondas = "M0 478"
    for i in range(0, 1230, 60):
        ondas += f" Q{i + 15} 466 {i + 30} 478 T{i + 60} 478"
    fondo = f'<path d="{ondas} L1230 600 L0 600 Z" fill="url(#mar)"/>'
    brillo = "".join(
        f'<path d="M{x} {y} q15 -6 30 0 t30 0" fill="none" stroke="#FFFFFF" stroke-width="2.2" opacity=".4"/>'
        for x, y in ((40, 500), (300, 520), (540, 505), (940, 525), (1090, 585), (420, 575)))
    return fondo + brillo


def difusor(x):
    burbujas = "".join(
        f'<circle cx="{x + dx}" cy="{y}" r="{r}" fill="none" stroke="#FFFFFF" stroke-width="1.8" opacity=".8"/>'
        for dx, y, r in ((-14, 548, 4), (10, 556, 5), (-4, 566, 3.5), (18, 570, 4)))
    return (f'<rect x="{x - 18}" y="520" width="36" height="12" rx="4" fill="#B7791F" stroke="#7A4F0E" stroke-width="2"/>'
            f'<polygon points="{x - 18},532 {x + 18},532 {x + 8},545 {x - 8},545" fill="#D69E2E" stroke="#7A4F0E" stroke-width="2"/>'
            + burbujas)


def dibujar(fila, animar=True):
    estado = fila["estado"]
    alertas = fila["alertas"].split("|")
    sin_enlace = fila["dato_valido"] == 0

    c_energia = NARANJA if estado == "ENERGY_LIMIT" else VERDE
    c_bomba = ROJO if estado == "SAFE_MODE" else c_energia
    c_mar = VIOLETA if estado == "HIGH_SALINITY" else VERDE
    c_membrana = NARANJA if "CP_ALTO" in alertas else VERDE
    c_producida = ROJO if "CP_ALTO" in alertas else VERDE
    c_enlace = ROJO if sin_enlace else VERDE
    c_control = COLOR_ESTADO[estado]

    lat = fila["latencia_s"]
    texto_enlace = "Paquete perdido" if lat != lat else f"Enlace IoT: {numero(lat, 1)} s"

    marcadores = "".join(
        f'<marker id="p{c[1:]}" markerWidth="16" markerHeight="16" refX="14" refY="8" orient="auto" '
        f'markerUnits="userSpaceOnUse"><path d="M0 1 L15 8 L0 15 z" fill="{c}"/></marker>'
        for c in (AZUL, AMARILLO, VERDE, NARANJA, GRIS)
    )
    estilo = (
        "<style>.flujo{stroke-dasharray:10 7;animation:mover 0.9s linear infinite}"
        "@keyframes mover{to{stroke-dashoffset:-17}}</style>" if animar else ""
    )
    p = [
        '<svg viewBox="0 0 1230 600" width="100%" xmlns="http://www.w3.org/2000/svg" '
        'style="border:1px solid #E5E7EB;border-radius:14px;font-family:Source Sans Pro,Arial,sans-serif">',
        f"<defs>{DEFS}{marcadores}</defs>{estilo}",
        '<rect width="1230" height="600" fill="url(#cielo)"/>',
        mar(),
        # --- tuberías de agua (debajo de los equipos)
        tuberia(f"M70 515 V{Y} H110", AZUL, animar, flecha=False),
        tuberia(f"M162 {Y} H252", AZUL, animar),
        tuberia(f"M362 {Y} H415", AZUL, animar),
        tuberia(f"M495 {Y} H612", AZUL, animar),
        tuberia(f"M612 {Y - 55} V{Y + 55}", AZUL, animar, flecha=False),
        tuberia(f"M612 {Y - 55} H640", AZUL, animar), tuberia(f"M612 {Y} H640", AZUL, animar),
        tuberia(f"M612 {Y + 55} H640", AZUL, animar),
        tuberia(f"M810 {Y - 55} H862 V{Y} H890", VERDE, animar),
        tuberia(f"M810 {Y + 55} H850 V510", NARANJA, animar),
        tuberia(f"M940 {Y} H1030", VERDE, animar),
        tuberia(f"M1110 {Y + 30} H1150", VERDE, animar),
        # --- energía y señales
        tuberia("M240 84 H403", AMARILLO, animar),
        tuberia("M455 120 V198", AMARILLO, animar),
        senal("M545 82 H520 V228 H488"),
        senal("M740 198 V82 H658"),
        # --- equipos
        panel_solar(), inversor(), controlador(estado, c_control),
        bomba_captacion(136, Y),
        cilindro_v(262, Y - 65, 42, 130), cilindro_v(318, Y - 65, 42, 130),
        bomba_alta(415, Y),
        recipiente_h(640, Y - 72, 170, 34), recipiente_h(640, Y - 17, 170, 34), recipiente_h(640, Y + 38, 170, 34),
        '<rect x="890" y="235" width="50" height="72" rx="8" fill="url(#metalV)" stroke="#6B7280" stroke-width="2" filter="url(#sombra)"/>'
        '<rect x="899" y="219" width="11" height="16" fill="#C5CCD4" stroke="#6B7280" stroke-width="1.6"/>'
        '<rect x="921" y="219" width="11" height="16" fill="#C5CCD4" stroke="#6B7280" stroke-width="1.6"/>',
        cilindro_v(1030, 215, 80, 130),
        '<rect x="1039" y="262" width="62" height="70" rx="5" fill="url(#agua)" stroke="#2F6FAF" stroke-width="1.6"/>',
        casa(), difusor(850),
        # --- indicadores de estado
        punto(240, 50, c_energia), punto(505, 45, c_energia), punto(655, 45, c_control),
        punto(161, Y - 33, c_mar), punto(495, Y - 72, c_bomba), punto(810, Y - 72, c_membrana),
        punto(1110, 215, c_producida), punto(868, 522, VERDE),
        # --- títulos
        titulo(150, 30, ["Paneles solares"]), titulo(455, 30, ["Convertidor"]), titulo(600, 30, ["Controlador"]),
        titulo(135, 362, ["Toma de agua", "de mar y bomba"]),
        titulo(311, 362, ["Filtros", "multimedia"]),
        texto(311, 416, "Solo contexto", 13, GRIS, "middle", 600, ' font-style="italic"'),
        titulo(455, 362, ["Bomba de", "alta presión"]),
        titulo(725, 362, ["Membranas de", "ósmosis inversa"]),
        titulo(915, 362, ["Postratamiento"]),
        texto(915, 380, "Solo contexto", 13, GRIS, "middle", 600, ' font-style="italic"'),
        titulo(1070, 362, ["Tanque de", "agua potable"]), titulo(1182, 362, ["Comunidad"]),
        texto(850, 590, "Difusor de descarga", 15, "#FFFFFF", "middle"),
        # --- tarjetas de datos
        tarjeta(88, 430, 170, [f"Caudal: {numero(fila['Qf'])} m³/h", f"Salinidad: {numero(fila['Cf'], 1)} g/L"], c_mar),
        tarjeta(70, 134, 165, [f"Irradiancia: {numero(fila['G'], 0)} W/m²"], c_energia),
        tarjeta(278, 134, 165, [f"Potencia útil: {numero(fila['P_util'])} kW"], c_energia),
        tarjeta(532, 134, 150, [ACCION[fila["accion"]]], c_control),
        tarjeta(372, 400, 170, [f"Ordenada: {numero(fila['TMP_cmd'], 1)} bar", f"Real: {numero(fila['TMP_real'], 1)} bar",
                                f"Pide: {numero(fila['P_req'])} kW"], c_bomba),
        tarjeta(640, 400, 170, [f"Recuperación: {numero(fila['R'])}", f"Energía: {numero(fila['SEC'])} kWh/m³"], c_membrana),
        tarjeta(980, 400, 175, [f"Caudal: {numero(fila['Qp'], 3)} m³/h", f"Salinidad: {numero(fila['Cp'], 3)} g/L"], c_producida),
        tarjeta(900, 496, 190, ["Salmuera (rechazo)", f"Caudal: {numero(fila['Qb'], 3)} m³/h",
                                f"Salinidad: {numero(fila['Cb'], 1)} g/L"], VERDE),
        # --- etiqueta del enlace y leyenda
        f'<rect x="752" y="130" width="168" height="30" rx="15" fill="#FFFFFF" stroke="{c_enlace}" stroke-width="2.5" filter="url(#sombra)"/>',
        texto(836, 151, texto_enlace, 14, c_enlace, "middle"),
        '<rect x="975" y="22" width="240" height="96" rx="12" fill="#FFFFFF" stroke="#D1D5DB" stroke-width="1.5"/>',
        texto(992, 46, "Colores", 15),
        f'<circle cx="1000" cy="68" r="7" fill="{VERDE}"/>' + texto(1013, 73, "Normal", 13.5, "#374151"),
        f'<circle cx="1105" cy="68" r="7" fill="{NARANJA}"/>' + texto(1118, 73, "Energía", 13.5, "#374151"),
        f'<circle cx="1000" cy="94" r="7" fill="{VIOLETA}"/>' + texto(1013, 99, "Sal alta", 13.5, "#374151"),
        f'<circle cx="1105" cy="94" r="7" fill="{ROJO}"/>' + texto(1118, 99, "Crítico", 13.5, "#374151"),
        "</svg>",
    ]
    return "".join(p)