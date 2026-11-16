from parametros import *


def calcular(df, esc):
    d = df.copy()
    e_tmp = (d["TMP_med"] - d["TMP_cmd"]).abs() / d["TMP_cmd"] * 100
    energia = (d["P_req"] / 3600).sum()
    volumen = (d["Qp"] / 3600).sum()
    lat = d["latencia_s"].dropna()

    t0 = esc["t_evento"]
    despues = d[(d["t_s"] >= t0) & (d["alertas"].str.contains(esc["esperado"]) |
                                    (d["estado"] == esc["esperado"]))]
    reaccion = float("nan")
    if esc["esperado"] != "NORMAL" and len(despues):
        reaccion = float(despues["t_s"].iloc[0] - t0)

    err_masa = ((d["Qf"] - d["Qp"] - d["Qb"]).abs() / d["Qf"]).max() * 100
    err_sal = ((d["Qf"] * d["Cf"] - d["Qp"] * d["Cp"] - d["Qb"] * d["Cb"]).abs()
               / (d["Qf"] * d["Cf"])).max() * 100

    return {
        "e_TMP_media_%": e_tmp.mean(),
        "ciclos_e_TMP<=5%_%": (e_tmp <= 5).mean() * 100,
        "TMP_media_bar": d["TMP_med"].mean(),
        "R_media": d["R"].mean(),
        "R_en_rango_%": d["R"].between(0.25, 0.40).mean() * 100,
        "SEC_kWh_m3": energia / volumen,
        "Cp_media_g_L": d["Cp"].mean(),
        "Cp_max_g_L": d["Cp"].max(),
        "Cb_media_g_L": d["Cb"].mean(),
        "Qp_media_m3_h": d["Qp"].mean(),
        "latencia_media_s": lat.mean(),
        "latencia<=5s_%": (lat <= UMBRAL_LATENCIA).sum() / len(d) * 100,
        "completitud_%": d["dato_valido"].mean() * 100,
        "disponibilidad_%": d["TMP_cmd"].notna().mean() * 100,
        "reaccion_alerta_s": reaccion,
        "err_balance_masa_max_%": err_masa,
        "err_balance_sal_max_%": err_sal,
        "deficit_energia_medio_kW": d["deficit_kW"].mean(),
        "ciclos_SAFE_MODE_%": (d["estado"] == "SAFE_MODE").mean() * 100,
        "estado_dominante": d["estado"].mode().iloc[0],
    }


# pruebas
if __name__ == "__main__":
    from simulador import simular
    for nombre in ("V01", "V06"):
        esc = ESCENARIOS[nombre]
        k = calcular(simular(esc, semilla=1), esc)
        print(nombre)
        for clave, valor in k.items():
            print(" ", clave, valor if isinstance(valor, str) else round(valor, 3))