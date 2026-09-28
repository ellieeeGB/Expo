"""Medición compartida, sin incluir la representación gráfica en los tiempos."""
import time


def medir(funcion, n, procesos, repeticiones):
    registros = []
    for i in range(repeticiones):
        inicio = time.perf_counter()
        pi = funcion(n) if procesos is None else funcion(n, procesos)
        tiempo = time.perf_counter() - inicio
        registros.append(dict(configuracion='Secuencial' if procesos is None else f'Paralelo {procesos} proc',
            procesos=procesos or 1, repeticion=i+1, tiempo=tiempo, pi=pi))
        print(f'Repetición {i+1}/{repeticiones}: {tiempo:.4f} s   π = {pi:.6f}', flush=True)
    return registros
