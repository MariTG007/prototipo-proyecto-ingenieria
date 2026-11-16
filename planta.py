from parametros import *


def paso(tmp, Qf, Cf, f, deg_sal):
    qp, cp = 0.3 * Qf, CP_REF
    for _ in range(60):
        cb = (Qf * Cf - qp * cp) / (Qf - qp)
        c_prom = (Cf + cb) / 2
        qp_nuevo = min(max(0.0, KM * f * (tmp - K_PI * c_prom)), 0.95 * Qf)
        qp = 0.5 * qp + 0.5 * qp_nuevo
        cp = BAM * deg_sal * c_prom / (qp + BAM * deg_sal)
    qb = Qf - qp
    cb = (Qf * Cf - qp * cp) / qb
    p_req = K_E * Qf * tmp
    return dict(qp=qp, qb=qb, cp=cp, cb=cb, p_req=p_req, R=qp / Qf,
                SEC=p_req / qp if qp > 1e-6 else float("nan"))


#pruebas
if __name__ == "__main__":
    print({k: round(v, 3) for k, v in paso(55, 1.2, 35.0, 1.0, 1.0).items()})   # normal
    print({k: round(v, 3) for k, v in paso(55, 1.2, 35.0, 0.9, 1.0).items()})   # ensuciada
    print({k: round(v, 3) for k, v in paso(55, 1.2, 35.0, 1.0, 4.0).items()})   # mas sal