"""
Worker para multiprocessing: cuenta cuántos puntos caen dentro del
círculo unitario. Debe estar en un archivo separado para que
ProcessPoolExecutor pueda importarlo correctamente.
"""

import random


def contar_puntos_en_circulo(n_puntos):
    """
    Cuenta cuántos puntos aleatorios caen dentro del círculo unitario.

    Parámetros:
    n_puntos (int): Número de puntos a generar en este chunk.

    Retorna:
    int: Cantidad de puntos dentro del círculo.
    """
    dentro = 0
    for _ in range(n_puntos):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            dentro += 1
    return dentro
