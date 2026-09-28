"""
Versión paralela de la simulación Monte Carlo para estimar π.

Uso:
    python src/montecarlo_paralelo.py --n 50000000 --procesos 4

Descripción:
    Divide el total de N puntos en P chunks, cada proceso worker cuenta
    cuántos puntos caen dentro del círculo unitario, y el proceso principal
    suma los resultados parciales.
"""

import time
import argparse
from concurrent.futures import ProcessPoolExecutor

# Importamos el worker desde el mismo directorio src/
# (para que funcione, asegúrate de ejecutar desde la raíz del proyecto)
try:
    from src.montecarlo_worker import contar_puntos_en_circulo
except ImportError:
    from montecarlo_worker import contar_puntos_en_circulo


def montecarlo_paralelo(n_puntos, n_procesos):
    """
    Estima π usando simulación Monte Carlo con múltiples procesos.

    Parámetros:
    n_puntos (int): Número total de puntos.
    n_procesos (int): Número de procesos a utilizar.

    Retorna:
    float: Estimación de π.
    """
    # Dividir el trabajo en chunks
    chunk_size = n_puntos // n_procesos
    resto = n_puntos % n_procesos
    chunks = [chunk_size] * n_procesos
    for i in range(resto):
        chunks[i] += 1

    # Ejecutar en paralelo
    with ProcessPoolExecutor(max_workers=n_procesos) as executor:
        resultados = list(executor.map(contar_puntos_en_circulo, chunks))

    total_dentro = sum(resultados)
    return 4 * total_dentro / n_puntos


def main():
    parser = argparse.ArgumentParser(
        description="Monte Carlo paralelo para estimar π"
    )
    parser.add_argument(
        "--n", type=int, default=50_000_000,
        help="Número total de puntos (default: 50,000,000)"
    )
    parser.add_argument(
        "--procesos", type=int, default=4,
        help="Número de procesos paralelos (default: 4)"
    )
    args = parser.parse_args()

    print(f"Ejecutando Monte Carlo paralelo con N={args.n:,} "
          f"y {args.procesos} procesos...")
    inicio = time.perf_counter()
    pi = montecarlo_paralelo(args.n, args.procesos)
    fin = time.perf_counter()

    tiempo = fin - inicio
    print(f"π estimado: {pi:.8f}")
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos")
    print(f"Error absoluto: {abs(pi - 3.141592653589793):.8f}")


if __name__ == "__main__":
    main()
