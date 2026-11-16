from parametros import *

def sat(x, lo, hi):
    return max(lo, min(hi, x))

def gemelo(G, Qf, Cf, tol=TOL_ENERGIA):
    p_pv = ETA_PV * A_PV * G / 1000     # kW que generan los paneles
    p_util = p_pv * ETA_CONV            # kW que llegan a la bomba

    qp = R_REF * Qf                          # agua producida
    qb = Qf - qp                             # salmuera
    cb = (Qf * Cf - qp * CP_REF) / qb        # salinidad de la salmuera
    p_req = SEC_REF * qp                     # kW que pide la bomba

    tmp_cmd = sat(TMP_NOM * p_util / p_req, TMP_MIN, TMP_MAX)
    estado = "ENERGY_LIMIT" if p_util < p_req * (1 - tol) else "NORMAL"
    if Cf >= CF_ALTA:
        estado = "HIGH_SALINITY"
    return dict(p_pv=p_pv, p_util=p_util, qp=qp, qb=qb, cb=cb, p_req=p_req,
                R=R_REF, SEC=SEC_REF, tmp_cmd=tmp_cmd, estado=estado)



# pruebas
if __name__ == "__main__":
    r = gemelo(800, 1.20, 35)
    assert abs(r["p_util"] - 1.44) < 1e-9
    assert abs(r["qp"] - 0.42) < 1e-9
    assert abs(r["qb"] - 0.78) < 1e-9
    assert abs(r["cb"] - 53.58) < 0.01
    print("OK: el gemelo reproduce la memoria de calculo de la Etapa 3")