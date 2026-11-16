from parametros import SIGMA


def medir(G, Qf, Cf, tmp, planta, rng):
    verdad = dict(G=G, Qf=Qf, Cf=Cf, TMP=tmp, Qp=planta["qp"], Cp=planta["cp"])
    return {k: v + rng.normal(0, SIGMA[k]) for k, v in verdad.items()}


# pruebas
if __name__ == "__main__":
    import numpy as np
    rng = np.random.default_rng(1)
    print(medir(800, 1.2, 35.0, 55.0, {"qp": 0.42, "cp": 0.5}, rng))