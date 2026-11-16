from parametros import *
from gemelo import sat


class Controlador:
    def __init__(self, tol=TOL_ENERGIA):
        self.tol = tol
        self.ultimo = None
        self.t_ultimo = 0

    def decidir(self, t, paquete):
        if paquete is not None:
            self.ultimo, self.t_ultimo = paquete, t
        sin_datos = (t - self.t_ultimo) > T_TIMEOUT

        if sin_datos:
            return dict(tmp_cmd=TMP_MIN, estado="SAFE_MODE",
                        alertas="COMMUNICATION_LOSS|SAFE_MODE", accion="PRESION_MINIMA")
        if self.ultimo is None:
            return dict(tmp_cmd=TMP_NOM, estado="NORMAL", alertas="", accion="")

        d = self.ultimo
        p_disp = ETA_PV * A_PV * d["G"] * ETA_CONV / 1000
        p_req = SEC_REF * R_REF * d["Qf"]
        r_med = d["Qp"] / d["Qf"]
        tmp_base = TMP_NOM + KR * (R_REF - r_med)

        alertas, accion = [], ""
        if p_disp < p_req * (1 - self.tol):
            tmp_cmd = sat(tmp_base * p_disp / p_req, TMP_MIN, TMP_MAX)
            alertas.append("ENERGY_LIMIT")
            accion = "REDUCIR_TMP"
        else:
            tmp_cmd = sat(tmp_base, TMP_MIN, TMP_MAX)
        if d["Cf"] >= CF_ALTA:
            alertas.append("HIGH_SALINITY")
            accion = accion or "ALERTAR"
        if d["Cp"] > CP_MAX:
            alertas.append("CP_ALTO")
            accion = "DESVIAR_PERMEADO"

        estado = "NORMAL"
        for e in ("ENERGY_LIMIT", "HIGH_SALINITY"):
            if e in alertas:
                estado = e
        return dict(tmp_cmd=tmp_cmd, estado=estado, alertas="|".join(alertas), accion=accion)

if __name__ == "__main__":
    c = Controlador()
    base = dict(G=800, Qf=1.2, Cf=35.0, Qp=0.42, Cp=0.3)
    print(c.decidir(0, base))
    print(c.decidir(1, dict(base, G=400)))
    print(c.decidir(2, dict(base, Cf=40.0)))
    print(c.decidir(3, dict(base, Cp=0.6)))
    print(c.decidir(4, None))
    print(c.decidir(10, None))
    print(Controlador(0.0).decidir(0, base))