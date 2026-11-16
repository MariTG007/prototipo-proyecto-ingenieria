import pandas as pd

NOMBRES_KPI = {
    "e_TMP_media_%": "Error Promedio entre la Presión Medida y la Ordenada (%)",
    "ciclos_e_TMP<=5%_%": "Segundos con Error de Presión de 5 % o Menos (%)",
    "TMP_media_bar": "Presión Promedio en la Membrana (bar)",
    "R_media": "Recuperación Promedio: Agua Producida ÷ Agua de Mar",
    "R_en_rango_%": "Tiempo con Recuperación entre 0,25 y 0,40 (%)",
    "SEC_kWh_m3": "Consumo de Energía por Cada m³ de Agua Producida (kWh/m³)",
    "Cp_media_g_L": "Salinidad Promedio del Agua Producida (g/L)",
    "Cp_max_g_L": "Salinidad Máxima del Agua Producida (g/L)",
    "Cb_media_g_L": "Salinidad Promedio de la Salmuera (g/L)",
    "Qp_media_m3_h": "Caudal Promedio de Agua Producida (m³/h)",
    "latencia_media_s": "Tiempo Promedio de Llegada de los Datos (s)",
    "latencia<=5s_%": "Datos que Llegaron en 5 s o Menos (%)",
    "completitud_%": "Datos Válidos Recibidos (%)",
    "disponibilidad_%": "Tiempo con Orden de Presión Disponible (%)",
    "reaccion_alerta_s": "Tiempo de Reacción ante la Alerta (s)",
    "err_balance_masa_max_%": "Error Máximo del Balance de Agua (%)",
    "err_balance_sal_max_%": "Error Máximo del Balance de Sal (%)",
    "deficit_energia_medio_kW": "Déficit Promedio de Energía Solar (kW)",
    "ciclos_SAFE_MODE_%": "Tiempo en Modo Seguro, SAFE_MODE (%)",
    "estado_dominante": "Estado del Controlador más Frecuente",
}

NOMBRES_COLUMNAS = {
    "escenario": "Escenario",
    "semilla": "Semilla",
    "t_s": "Segundo de la Simulación",
    "G": "Irradiancia (W/m²)",
    "Qf": "Caudal de Agua de Mar (m³/h)",
    "Cf": "Salinidad del Agua de Mar (g/L)",
    "TMP_cmd": "Presión Ordenada (bar)",
    "TMP_med": "Presión Medida (bar)",
    "TMP_real": "Presión Real (bar)",
    "Qp": "Agua Producida (m³/h)",
    "Qb": "Salmuera (m³/h)",
    "Cp": "Salinidad del Agua Producida (g/L)",
    "Cb": "Salinidad de la Salmuera (g/L)",
    "R": "Recuperación",
    "P_util": "Potencia Solar Disponible (kW)",
    "P_req": "Potencia que Pide la Bomba (kW)",
    "deficit_kW": "Déficit de Energía (kW)",
    "SEC": "Consumo de Energía por m³ (kWh/m³)",
    "estado": "Estado del Controlador",
    "alertas": "Alertas Activas",
    "accion": "Acción del Controlador",
    "latencia_s": "Tiempo de Llegada del Dato (s)",
    "dato_valido": "Dato Válido (1 = Sí, 0 = No)",
}

PIES = {
    "curva_presion": "Presión que ordena el controlador y presión que mide el sensor. Baja cuando falta energía solar o se pierde la comunicación.",
    "curva_caudales": "Agua producida y salmuera en cada segundo. Las dos juntas suman el agua de mar que entra a la planta.",
    "curva_salinidad": "Sal del agua producida y de la salmuera. El agua producida debe quedar por debajo de 0,50 g/L.",
    "curva_latencia": "Tiempo que tarda cada paquete en llegar al controlador. Los puntos sobre 5 s no se usan; los paquetes perdidos no se dibujan.",
    "reporte_1": "Cada punto compara la presión ordenada con la medida. Entre las líneas punteadas el error es de 5 % o menos.",
    "reporte_2": "Compara el agua producida por el modelo ideal con la de la planta simulada. Los puntos sobre la diagonal coinciden; la distancia a ella es el desvío.",
    "reporte_3": "Muestra cuánta energía cuesta cada m³ producido según la irradiancia. La línea roja marca el límite de 4,5 kWh/m³.",
    "reporte_4": "Muestra cómo sube la sal del agua producida cuando sube la del agua de mar. La línea roja marca el límite de 0,50 g/L.",
    "reporte_5": "Compara cuánto tardan en llegar los datos con la red normal (V01) y con la degradada (V06). Sobre los 5 s el dato no se usa.",
    "reporte_6": "Muestra qué parte del agua de mar se convierte en agua producida según la irradiancia. La banda verde es el rango de diseño, de 0,25 a 0,40.",
}


ALERTAS_LEGIBLES = {
    "ENERGY_LIMIT": "Energía solar insuficiente (ENERGY_LIMIT)",
    "HIGH_SALINITY": "Salinidad alta en el agua de mar (HIGH_SALINITY)",
    "CP_ALTO": "Salinidad alta en el agua producida (CP_ALTO)",
    "COMMUNICATION_LOSS": "Pérdida de comunicación (COMMUNICATION_LOSS)",
    "SAFE_MODE": "Modo seguro (SAFE_MODE)",
}

ACCIONES_LEGIBLES = {
    "REDUCIR_TMP": "reducir la presión de la bomba",
    "ALERTAR": "avisar al operador",
    "DESVIAR_PERMEADO": "desviar el agua producida",
    "PRESION_MINIMA": "bajar a la presión mínima",
}


def numero(v, decimales=2):
    return f"{v:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatear(v):
    if isinstance(v, str):
        return v
    if v != v:
        return "No aplica"
    return f"{v:.2f}".replace(".", ",")


def tabla_indicadores(kpis):
    filas = [(NOMBRES_KPI.get(k, k), formatear(v)) for k, v in kpis.items()]
    return pd.DataFrame(filas, columns=["Indicador", "Valor"])


# pruebas

if __name__ == "__main__":
    from simulador import simular
    from kpis import calcular
    from parametros import ESCENARIOS
    esc = ESCENARIOS["V01"]
    print(tabla_indicadores(calcular(simular(esc, semilla=1), esc)).to_string(index=False))