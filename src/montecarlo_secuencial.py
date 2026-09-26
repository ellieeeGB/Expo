"""
Versión secuencial de la simulación Monte Carlo para estimar π.

Uso:
    python src/montecarlo_secuencial.py --n 50000000

Descripción:
    Genera N puntos aleatorios en el cuadrado [-1, 1] x [-1, 1] y cuenta
    cuántos caen dentro del círculo unitario (x² + y² ≤ 1).
    La estimación de π es: π ≈ 4 × (puntos_dentro / N).
"""

import random
import time
import argparse


def montecarlo_secuencial(n_puntos):
    """
    Estima π usando simulación Monte Carlo de forma secuencial.

    Parámetros:
    n_puntos (int): Número total de puntos a generar.

    Retorna:
    float: Estimación de π.
    """
    dentro_circulo = 0
    for _ in range(n_puntos):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            dentro_circulo += 1
    return 4 * dentro_circulo / n_puntos


def main():
    parser = argparse.ArgumentParser(
        description="Monte Carlo secuencial para estimar π"
    )
    parser.add_argument(
        "--n", type=int, default=50_000_000,
        help="Número de puntos a generar (default: 50,000,000)"
    )
    args = parser.parse_args()

    print(f"Ejecutando Monte Carlo secuencial con N={args.n:,} puntos...")
    inicio = time.perf_counter()
    pi = montecarlo_secuencial(args.n)
    fin = time.perf_counter()

    tiempo = fin - inicio
    print(f"π estimado: {pi:.8f}")
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos")
    print(f"Error absoluto: {abs(pi - 3.141592653589793):.8f}")


if __name__ == "__main__":
    main()
