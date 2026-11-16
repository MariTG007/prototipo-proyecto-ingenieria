import pandas as pd
import streamlit as st


def tabla(columnas, filas):
    """Muestra una tabla de texto corto, sin índice y sin barra de desplazamiento."""
    st.table(pd.DataFrame(filas, columns=columnas).style.hide(axis="index"))


st.title("Documentación")

temas = st.tabs(["Conceptos", "Símbolos y Significados", "Fórmulas", "Control y Comunicación",
                 "Cómo Funciona la Simulación", "Escenarios"])

with temas[0]:
    st.write("El prototipo simula en computador una planta que convierte agua de mar en agua potable "
             "con energía solar, y la vigila con sensores conectados por red (IoT).")
    tabla(["Concepto", "Qué Significa"], [
        ("ZNI (Zonas No Interconectadas)", "Lugares de Colombia sin conexión a la red eléctrica nacional; dependen sobre todo de generación diésel."),
        ("Ósmosis Inversa (RO)", "Se empuja el agua de mar con presión a través de una membrana que deja pasar el agua y retiene la sal."),
        ("Sistema PV-RO", "Paneles solares (PV) que dan la energía a la bomba de la ósmosis inversa (RO)."),
        ("IoT", "Los sensores envían sus lecturas por una red a un controlador que decide qué hacer."),
        ("Gemelo Digital", "Cálculo ideal de cómo debería comportarse la planta. Se compara con la planta simulada para medir los desvíos."),
        ("Controlador", "Ajusta la presión de la bomba según la energía disponible y la salinidad, y levanta alertas."),
        ("Prototipo Virtual", "Todo es simulado: los valores son supuestos de diseño, no mediciones, y no certifican la potabilidad del agua."),
    ])

with temas[1]:
    st.write("Cada letra del prototipo es una magnitud con su unidad; los rangos vienen de la Tabla 3 de la Etapa 3.")  # [E3]
    tabla(["Símbolo", "Qué Significa", "Unidad", "Rango o Valor"], [
        ("G", "Irradiancia: potencia del sol que llega a cada m² de panel.", "W/m²", "200 a 1000"),
        ("A", "Área de paneles solares.", "m²", "10"),
        ("ηPV", "Eficiencia del panel: fracción de la luz que se vuelve electricidad.", "sin unidad", "0,20"),
        ("ηconv", "Eficiencia del convertidor eléctrico.", "sin unidad", "0,90"),
        ("Qf", "Caudal de alimentación: agua de mar que entra a la planta.", "m³/h", "0,60 a 1,20"),
        ("Cf", "Salinidad del agua de mar que entra.", "g/L", "30 a 40"),
        ("TMP", "Presión transmembrana: con la que se empuja el agua por la membrana.", "bar", "45 a 60"),
        ("Qp", "Caudal de permeado: agua desalinizada que se produce.", "m³/h", "0 a 0,50"),
        ("Qb", "Caudal de rechazo (salmuera): lo que no atraviesa la membrana.", "m³/h", "Qf − Qp"),
        ("Cp", "Salinidad del permeado (agua producida).", "g/L", "máximo 0,50"),
        ("Cb", "Salinidad del rechazo (salmuera).", "g/L", "se calcula"),
        ("R", "Recuperación: parte del agua de entrada que sale como agua producida.", "sin unidad", "0,25 a 0,40"),
        ("SEC", "Consumo específico: energía gastada por cada m³ de agua producida.", "kWh/m³", "máximo 4,5"),
        ("P_disp", "Potencia disponible: energía solar utilizable en ese momento.", "kW", "se calcula"),
        ("P_req", "Potencia requerida: la que pide la bomba para producir el caudal.", "kW", "se calcula"),
        ("L", "Latencia: tiempo que tarda un dato en llegar al controlador.", "s", "máximo 5"),
        ("D", "Completitud: porcentaje de datos esperados que llegan válidos.", "%", "mínimo 98"),
    ])

with temas[2]:
    st.write("Son siete fórmulas de la memoria de cálculo de la Etapa 3; juntas van de la energía solar "
             "a la presión que ordena el controlador.")  # [E3]
    tabla(["Qué Calcula", "Fórmula", "En Palabras"], [
        ("Potencia solar", "P_PV = ηPV × A × G ÷ 1000", "Energía que generan los paneles, en kW."),
        ("Potencia utilizable", "P_util = P_PV × ηconv", "Lo que llega a la bomba después del convertidor."),
        ("Agua producida", "Qp = R × Qf", "Parte del agua de entrada que sale como agua potable."),
        ("Balance de caudal", "Qb = Qf − Qp", "Lo que no se produce sale como salmuera."),
        ("Balance de sal", "Qf × Cf = Qp × Cp + Qb × Cb", "La sal que entra es la que sale; de aquí se despeja Cb."),
        ("Consumo específico", "SEC = E ÷ Vp", "Energía por m³ producido. La potencia requerida es P_req = SEC × Qp."),
        ("Presión de control", "ΔP_cmd = sat(ΔP_nom × P_disp ÷ P_req, 45, 60)", "Si falta energía, baja la presión sin salir de 45 a 60 bar."),
    ])
    st.write("Ejemplo con G = 800 W/m², Qf = 1,2 m³/h y Cf = 35 g/L: P_util = 1,44 kW, Qp = 0,42 m³/h, "
             "Qb = 0,78 m³/h, Cb = 53,58 g/L y P_req = 1,47 kW, así que faltan 0,03 kW.")

with temas[3]:
    st.write("El controlador recibe los datos por el enlace IoT, elige un estado y ordena la presión de la bomba. "
             "Si varios estados aplican, gana el de mayor prioridad.")
    tabla(["Prioridad", "Estado", "Cuándo se Activa", "Qué Hace"], [
        ("1", "SAFE_MODE", "Más de 5 s sin datos válidos (el tiempo es un supuesto del grupo).", "Baja la presión al mínimo (45 bar) y avisa pérdida de comunicación."),
        ("2", "HIGH_SALINITY", "Salinidad de entrada de 38 g/L o más (umbral supuesto).", "Emite una alerta de salinidad alta."),
        ("3", "ENERGY_LIMIT", "La potencia disponible queda más de 5 % por debajo de la requerida (banda supuesta).", "Reduce la presión en proporción a la energía disponible."),
        ("4", "NORMAL", "Ninguna de las anteriores.", "Mantiene la presión nominal (55 bar) con un ajuste fino de la recuperación."),
        ("Alerta aparte", "CP_ALTO", "Salinidad del permeado mayor que 0,50 g/L.", "Desvía el permeado en lugar de entregarlo."),
    ])
    tabla(["Regla del Enlace IoT", "Detalle"], [
        ("Un paquete por segundo", "Cada segundo se envían las lecturas de los sensores, con ruido."),
        ("Dato válido", "El paquete llega y su latencia es de 5 s o menos; el controlador solo usa datos válidos."),
        ("Latencia y pérdidas", "Normal: cerca de 1,3 s y 0,5 % de paquetes perdidos. Degradado: cerca de 6,5 s y 40 % perdidos (valores supuestos)."),
        ("Último dato válido", "Si no llega nada, el controlador conserva el último dato válido; pasados 5 s entra en SAFE_MODE."),
    ])

with temas[4]:
    st.write("Cada corrida repite 600 ciclos de un segundo; en cada ciclo la planta produce, los sensores miden, "
             "el enlace envía, el controlador decide y la bomba ajusta la presión.")
    tabla(["Concepto", "Qué Significa"], [
        ("Ciclo y duración", "1 ciclo = 1 segundo simulado. Cada corrida tiene 600 ciclos, del segundo 0 al 599 (duración supuesta)."),
        ("Gemelo y planta simulada", "El gemelo calcula el caso ideal con las fórmulas. La planta simulada agrega ensuciamiento de la membrana, retardo de la bomba y paso de sal."),
        ("Desvío", "Diferencia entre lo simulado y el modelo ideal, en valor y en porcentaje."),
        ("Ruido de sensores", "Cada lectura se altera con una variación aleatoria pequeña, como en un sensor real."),
        ("Semilla", "Número que fija lo aleatorio (ruido, pérdidas del enlace y estado inicial de la membrana). Misma semilla, mismos resultados."),
        ("Segundo de la simulación", "Instante que eliges con el control deslizante. Las tarjetas muestran ese segundo; los indicadores resumen toda la corrida."),
    ])

with temas[5]:
    st.write("Son diez pruebas: seis de la Tabla 10 de la Etapa 3, dos del Anexo D (T6 y T7) y dos propias "
             "(V01b y V07). Cada una se corre con tres semillas.")
    tabla(["Escenario", "Qué se Cambia", "Qué se Espera", "Origen"], [
        ("V01 Nominal", "G = 800 W/m², Qf = 1,2 m³/h, Cf = 35 g/L", "Estado NORMAL y balances consistentes (con la banda de 5 %).", "Etapa 3"),
        ("V01b Nominal sin banda", "Igual que V01, con tolerancia de energía 0", "ENERGY_LIMIT: muestra que la fórmula pura da 0,03 kW de déficit.", "Propio"),
        ("V02 Irradiancia baja", "G = 400 W/m²", "ENERGY_LIMIT y la carga se reduce.", "Etapa 3"),
        ("V03 Irradiancia alta", "G = 1000 W/m²", "NORMAL, con el control dentro de límites.", "Etapa 3"),
        ("V04 Salinidad alta", "Cf = 40 g/L", "HIGH_SALINITY y alerta.", "Etapa 3"),
        ("V05 Caudal reducido", "Qf = 0,6 m³/h", "NORMAL, con balance y estabilidad.", "Etapa 3"),
        ("V06 Comunicación degradada", "Latencia alta y pérdidas entre los segundos 200 y 400", "SAFE_MODE por pérdida de comunicación.", "Etapa 3"),
        ("V07 Salto de irradiancia", "G baja de 1000 a 600 W/m² en el segundo 300", "ENERGY_LIMIT en 10 s o menos (caso V-06 de la Tabla 9).", "Propio"),
        ("T6 Salinidad de permeado alta", "Paso de sal multiplicado por 4", "Alerta CP_ALTO y desvío del permeado.", "Anexo D"),
        ("T7 Sobredemanda energética", "G = 600 W/m²", "ENERGY_LIMIT.", "Anexo D"),
    ])