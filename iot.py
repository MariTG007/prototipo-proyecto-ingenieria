from parametros import *


class Enlace:
    def __init__(self, rng):
        self.rng = rng
        self.en_vuelo = []

    def enviar(self, t, paquete, degradado):
        minimo, escala, p_perdida = ENLACE_DEGRADADO if degradado else ENLACE_NORMAL
        perdido = self.rng.random() < p_perdida
        latencia = minimo + self.rng.gamma(2.0, escala)
        valido = (not perdido) and latencia <= UMBRAL_LATENCIA
        if valido:
            self.en_vuelo.append((t + latencia, t, paquete))
        return (float("nan") if perdido else latencia), valido

    def recibir(self, t):
        llegados = [x for x in self.en_vuelo if x[0] <= t]
        self.en_vuelo = [x for x in self.en_vuelo if x[0] > t]
        if not llegados:
            return None
        return max(llegados, key=lambda x: x[1])[2]


# pruebas

if __name__ == "__main__":
    import numpy as np
    for degradado in (False, True):
        print("degradado" if degradado else "normal")
        enlace = Enlace(np.random.default_rng(1))
        for t in range(8):
            lat, valido = enlace.enviar(t, {"t": t}, degradado)
            print(t, round(lat, 2), valido, enlace.recibir(t))
