# [E3] significa etapa 3

A_PV = 10.0      # m2, area de los paneles [E3]
ETA_PV = 0.20    # eficiencia del panel [E3]
ETA_CONV = 0.90  # eficiencia del convertidor [E3]

R_REF = 0.35    # recuperacion de diseño: Qp/Qf [E3]
SEC_REF = 3.5   # kWh/m3, consumo especifico de referencia [E3]
CP_REF = 0.50   # g/L, salinidad del agua producida que usa el balance de sal [E3]

TMP_MIN, TMP_MAX = 45.0, 60.0   # bar, limites de presion [E3]
TMP_NOM = 55.0                  # bar, presion nominal [SUPUESTO] - 55 cumple rango 45 a 60, y reproduce el caso nominal
CF_ALTA = 38.0                  # g/L, desde aqui hay HIGH_SALINITY [SUPUESTO] - 38 cumple las condiciones del rango 30 a 40
CP_MAX = 0.50                   # g/L, limite del agua producida [E3]
TOL_ENERGIA = 0.05              # banda del 5 %: ENERGY_LIMIT solo si falta mas de 5 % [SUPUESTO]
KR = 40.0                       # bar por unidad de R, ajuste fino [SUPUESTO]

UMBRAL_LATENCIA = 5.0   # s, un dato es valido si llega en 5 s o menos [E3]
T_TIMEOUT = 5           # s sin datos validos => SAFE_MODE [SUPUESTO]

K_PI = 0.77                     # bar por (g/L): presion osmotica aproximada
KM = 0.020                      # m3/h por bar: cuanta agua deja pasar la membrana
BAM = 0.0033                    # m3/h: paso de sal por la membrana
K_E = 1.47 / (1.2 * 55.0)       # kW por (m3/h * bar): calibrado para dar 1,47 kW
TAU_TMP = 5.0                   # s, la bomba tarda en llegar a la presion ordenada
DERIVA_ENSUCIAMIENTO = 1e-5     # perdida de permeabilidad por segundo

SIGMA = {"G": 5.0, "Qf": 0.012, "Cf": 0.3, "TMP": 0.3, "Qp": 0.004, "Cp": 0.02}
ENLACE_NORMAL = (0.5, 0.4, 0.005)    # latencia minima s, escala s, probabilidad de perdida
ENLACE_DEGRADADO = (0.5, 3.0, 0.40)
N_CICLOS = 600                       # 1 ciclo = 1 s simulado

def escenario(nombre, descripcion, G, Qf=1.2, Cf=35.0, deg_sal=1.0,
              ventana_com=None, t_evento=0, esperado="NORMAL", tabla10="", tol=TOL_ENERGIA):
    return dict(nombre=nombre, descripcion=descripcion, G=G, Qf=Qf, Cf=Cf,
                deg_sal=deg_sal, ventana_com=ventana_com, t_evento=t_evento,
                esperado=esperado, tabla10=tabla10, tol=tol)

ESCENARIOS = {
    "V01": escenario("V01", "Nominal", [(0, 800)], esperado="NORMAL", tabla10="NORMAL"),
    "V01b": escenario("V01b", "Nominal SIN banda de tolerancia", [(0, 800)],
                      esperado="ENERGY_LIMIT", tabla10="NORMAL", tol=0.0),
    "V02": escenario("V02", "Irradiancia baja", [(0, 400)], esperado="ENERGY_LIMIT", tabla10="ENERGY_LIMIT"),
    "V03": escenario("V03", "Irradiancia alta", [(0, 1000)], esperado="NORMAL", tabla10="NORMAL"),
    "V04": escenario("V04", "Salinidad alta", [(0, 800)], Cf=40.0, esperado="HIGH_SALINITY", tabla10="HIGH_SALINITY"),
    "V05": escenario("V05", "Caudal reducido", [(0, 800)], Qf=0.6, esperado="NORMAL", tabla10="NORMAL"),
    "V06": escenario("V06", "Comunicacion degradada", [(0, 850)], ventana_com=(200, 400),
                     t_evento=200, esperado="SAFE_MODE", tabla10="SAFE_MODE"),
    "V07": escenario("V07", "Salto de irradiancia 1000 a 600", [(0, 1000), (300, 600)],
                     t_evento=300, esperado="ENERGY_LIMIT", tabla10="(Tabla 9: V-06)"),
    "T6": escenario("T6", "Salinidad de permeado alta", [(0, 850)], deg_sal=4.0,
                    esperado="CP_ALTO", tabla10="Alerta + accion"),
    "T7": escenario("T7", "Sobredemanda energetica", [(0, 600)], esperado="ENERGY_LIMIT",
                    tabla10="ENERGY_LIMIT"),
}