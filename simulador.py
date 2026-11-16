import numpy as np
import pandas as pd

import planta
import sensores
from control import Controlador
from iot import Enlace
from parametros import *


def valor_en(perfil, t):
    v = perfil[0][1]
    for t0, val in perfil:
        if t >= t0:
            v = val
    return v


def simular(esc, semilla=1, n_ciclos=N_CICLOS):
    rng = np.random.default_rng(semilla)
    f0 = rng.uniform(0.95, 1.0)
    enlace, ctl = Enlace(rng), Controlador(esc.get("tol", TOL_ENERGIA))
    tmp_real, tmp_cmd = TMP_NOM, TMP_NOM
    filas = []
    for t in range(n_ciclos):
        G = valor_en(esc["G"], t)
        f = f0 - DERIVA_ENSUCIAMIENTO * t
        tmp_real += (tmp_cmd - tmp_real) / TAU_TMP
        p = planta.paso(tmp_real, esc["Qf"], esc["Cf"], f, esc["deg_sal"])
        med = sensores.medir(G, esc["Qf"], esc["Cf"], tmp_real, p, rng)
        v = esc["ventana_com"]
        degradado = bool(v and v[0] <= t < v[1])
        lat, valido = enlace.enviar(t, med, degradado)
        dec = ctl.decidir(t, enlace.recibir(t))
        tmp_cmd = dec["tmp_cmd"]
        p_util = ETA_PV * A_PV * G * ETA_CONV / 1000
        filas.append(dict(
            escenario=esc["nombre"], semilla=semilla, t_s=t, G=G, Qf=esc["Qf"], Cf=esc["Cf"],
            TMP_cmd=tmp_cmd, TMP_med=med["TMP"], TMP_real=tmp_real,
            Qp=p["qp"], Qb=p["qb"], Cp=p["cp"], Cb=p["cb"], R=p["R"],
            P_util=p_util, P_req=p["p_req"], deficit_kW=max(0.0, p["p_req"] - p_util),
            SEC=p["SEC"], estado=dec["estado"], alertas=dec["alertas"], accion=dec["accion"],
            latencia_s=lat, dato_valido=int(valido)))
    return pd.DataFrame(filas)


# prueba

if __name__ == "__main__":
    df = simular(ESCENARIOS["V01"], semilla=1)
    print(df.shape)
    print(df[["t_s", "G", "TMP_cmd", "Qp", "Cp", "estado", "latencia_s"]].iloc[[0, 1, 2, 300, 599]].round(3))
    print(df["estado"].value_counts())
    d6 = simular(ESCENARIOS["V06"], semilla=1)
    print(d6["estado"].value_counts())