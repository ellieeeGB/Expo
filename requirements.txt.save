"""
Script de experimentos: ejecuta la comparación secuencial vs paralela
con 1, 2, 4 y 8 procesos, guarda los resultados en JSON/CSV y genera
las gráficas.

Uso:
    python scripts/run_experiments.py

Salida:
    - resultados/resultados.json
    - resultados/resultados.csv
    - resultados/resultados_completos.csv
    - resultados/resumen.txt
    - resultados/graficas.png
    - resultados/graficas/01_tiempos.png
    - resultados/graficas/02_speedup.png
    - resultados/graficas/03_eficiencia.png
"""

import os
import sys
import time
import json
import random
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Backend sin ventana (para servidores)
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

# Asegurar que encontramos el worker y los módulos de src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.montecarlo_worker import contar_puntos_en_circulo


# ------------------------------------------------------------------
# PARÁMETROS DEL EXPERIMENTO
# ------------------------------------------------------------------
N_PUNTOS = 10_000_000
PROCESOS = [1, 2, 4, 8]
REPETICIONES = 3

# Rutas relativas desde la raíz del proyecto
RUTA_RESULTADOS = "resultados"
RUTA_GRAFICAS = os.path.join(RUTA_RESULTADOS, "graficas")


# ------------------------------------------------------------------
# FUNCIONES DE CÓMPUTO
# ------------------------------------------------------------------
def montecarlo_secuencial(n_puntos):
    """Versión secuencial de Monte Carlo."""
    dentro_circulo = 0
    for _ in range(n_puntos):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            dentro_circulo += 1
    return 4 * dentro_circulo / n_puntos


def montecarlo_paralelo(n_puntos, n_procesos):
    """Versión paralela de Monte Carlo con multiprocessing."""
    chunk_size = n_puntos // n_procesos
    resto = n_puntos % n_procesos
    chunks = [chunk_size] * n_procesos
    for i in range(resto):
        chunks[i] += 1

    with ProcessPoolExecutor(max_workers=n_procesos) as executor:
        resultados = list(executor.map(contar_puntos_en_circulo, chunks))

    return 4 * sum(resultados) / n_puntos


# ------------------------------------------------------------------
# EJECUCIÓN DEL EXPERIMENTO
# ------------------------------------------------------------------
def ejecutar_experimento():
    resultados = []

    # --- Secuencial ---
    print("Ejecutando versión secuencial...")
    for i in range(REPETICIONES):
        inicio = time.perf_counter()
        pi = montecarlo_secuencial(N_PUNTOS)
        fin = time.perf_counter()
        tiempo = fin - inicio
        resultados.append({
            "configuracion": "Secuencial",
            "procesos": 1,
            "repeticion": i + 1,
            "tiempo": tiempo,
            "pi": pi,
        })
        print(f"  Repetición {i+1}: {tiempo:.4f} s, π = {pi:.6f}")

    # --- Paralelo ---
    for p in PROCESOS:
        print(f"Ejecutando versión paralela con {p} proceso(s)...")
        for i in range(REPETICIONES):
            inicio = time.perf_counter()
            pi = montecarlo_paralelo(N_PUNTOS, p)
            fin = time.perf_counter()
            tiempo = fin - inicio
            resultados.append({
                "configuracion": f"Paralelo {p} proc",
                "procesos": p,
                "repeticion": i + 1,
                "tiempo": tiempo,
                "pi": pi,
            })
            print(f"  Repetición {i+1}: {tiempo:.4f} s, π = {pi:.6f}")

    return pd.DataFrame(resultados)


# ------------------------------------------------------------------
# ANÁLISIS Y GUARDADO
# ------------------------------------------------------------------
def analizar_y_guardar(df_resultados):
    resumen = df_resultados.groupby(["configuracion", "procesos"]).agg(
        tiempo_promedio=("tiempo", "mean"),
        tiempo_std=("tiempo", "std"),
        pi_promedio=("pi", "mean"),
    ).reset_index()

    tiempo_secuencial = resumen[
        resumen["configuracion"] == "Secuencial"
    ]["tiempo_promedio"].values[0]

    resumen["speedup"] = tiempo_secuencial / resumen["tiempo_promedio"]
    resumen["eficiencia"] = resumen["speedup"] / resumen["procesos"]

    print("\nTabla de resultados:")
    print(resumen.to_string(index=False))

    # Crear carpetas
    os.makedirs(RUTA_RESULTADOS, exist_ok=True)
    os.makedirs(RUTA_GRAFICAS, exist_ok=True)

    # 1. CSV completo (todas las repeticiones)
    df_resultados.to_csv(
        os.path.join(RUTA_RESULTADOS, "resultados_completos.csv"), index=False
    )

    # 2. CSV resumen
    resumen.to_csv(
        os.path.join(RUTA_RESULTADOS, "resultados.csv"), index=False
    )

    # 3. JSON estructurado
    datos_json = {
        "n_puntos": N_PUNTOS,
        "repeticiones": REPETICIONES,
        "procesos_probados": PROCESOS,
        "tiempo_secuencial_promedio": float(tiempo_secuencial),
        "resultados": [],
    }
    for _, fila in resumen.iterrows():
        datos_json["resultados"].append({
            "configuracion": fila["configuracion"],
            "procesos": int(fila["procesos"]),
            "tiempo_promedio": float(fila["tiempo_promedio"]),
            "tiempo_std": float(fila["tiempo_std"]),
            "pi_promedio": float(fila["pi_promedio"]),
            "speedup": float(fila["speedup"]),
            "eficiencia": float(fila["eficiencia"]),
        })
    with open(
        os.path.join(RUTA_RESULTADOS, "resultados.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(datos_json, f, indent=2, ensure_ascii=False)

    # 4. Resumen en texto
    with open(
        os.path.join(RUTA_RESULTADOS, "resumen.txt"), "w", encoding="utf-8"
    ) as f:
        f.write("RESUMEN DEL EXPERIMENTO MONTE CARLO — HPC\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"N puntos por experimento: {N_PUNTOS:,}\n")
        f.write(f"Repeticiones por configuración: {REPETICIONES}\n")
        f.write(f"Procesos probados: {PROCESOS}\n\n")
        f.write(
            f"{'Configuración':<20}{'Proc':<6}{'Tiempo(s)':<12}"
            f"{'Speedup':<10}{'Eficiencia':<10}\n"
        )
        f.write("-" * 58 + "\n")
        for _, fila in resumen.iterrows():
            f.write(
                f"{fila['configuracion']:<20}{int(fila['procesos']):<6}"
                f"{fila['tiempo_promedio']:<12.4f}"
                f"{fila['speedup']:<10.4f}"
                f"{fila['eficiencia']:<10.4f}\n"
            )

    return resumen, tiempo_secuencial


def generar_graficas(resumen):
    paralelos = resumen[resumen["configuracion"] != "Secuencial"]

    # --- Gráfica combinada (3 subplots) ---
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    axes[0].bar(
        resumen["configuracion"],
        resumen["tiempo_promedio"],
        yerr=resumen["tiempo_std"],
        capsize=5,
        color="#3498db",
    )
    axes[0].set_title("Tiempo de ejecución", fontsize=14)
    axes[0].set_ylabel("Tiempo (s)")
    axes[0].tick_params(axis="x", rotation=45)
    axes[0].grid(axis="y", alpha=0.3)

    axes[1].plot(
        paralelos["procesos"], paralelos["speedup"], "o-",
        label="Speedup real", color="#2ecc71", linewidth=2, markersize=8,
    )
    axes[1].plot(
        paralelos["procesos"], paralelos["procesos"], "--",
        label="Speedup ideal", color="#95a5a6", linewidth=2,
    )
    axes[1].set_title("Speedup vs. Número de procesos", fontsize=14)
    axes[1].set_xlabel("Procesos")
    axes[1].set_ylabel("Speedup")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    axes[2].bar(
        paralelos["procesos"].astype(str),
        paralelos["eficiencia"],
        color="#9b59b6",
    )
    axes[2].set_title("Eficiencia paralela", fontsize=14)
    axes[2].set_xlabel("Procesos")
    axes[2].set_ylabel("Eficiencia (S/N)")
    axes[2].set_ylim(0, 1.2)
    axes[2].axhline(y=1.0, color="r", linestyle="--", alpha=0.5, label="Ideal")
    axes[2].legend()
    axes[2].grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        os.path.join(RUTA_RESULTADOS, "graficas.png"),
        dpi=150,
        bbox_inches="tight",
    )
    plt.close(fig)

    # --- Gráficas individuales ---
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(
        resumen["configuracion"],
        resumen["tiempo_promedio"],
        yerr=resumen["tiempo_std"],
        capsize=5,
        color="#3498db",
    )
    ax1.set_title("Tiempo de ejecución")
    ax1.set_ylabel("Tiempo (s)")
    ax1.tick_params(axis="x", rotation=45)
    ax1.grid(axis="y", alpha=0.3)
    fig1.tight_layout()
    fig1.savefig(os.path.join(RUTA_GRAFICAS, "01_tiempos.png"), dpi=150)
    plt.close(fig1)

    fig2, ax2 = plt.subplots(figsize=(7, 5))
    ax2.plot(
        paralelos["procesos"], paralelos["speedup"], "o-",
        label="Speedup real", color="#2ecc71", linewidth=2, markersize=8,
    )
    ax2.plot(
        paralelos["procesos"], paralelos["procesos"], "--",
        label="Speedup ideal", color="#95a5a6", linewidth=2,
    )
    ax2.set_title("Speedup vs. Número de procesos")
    ax2.set_xlabel("Procesos")
    ax2.set_ylabel("Speedup")
    ax2.legend()
    ax2.grid(alpha=0.3)
    fig2.tight_layout()
    fig2.savefig(os.path.join(RUTA_GRAFICAS, "02_speedup.png"), dpi=150)
    plt.close(fig2)

    fig3, ax3 = plt.subplots(figsize=(7, 5))
    ax3.bar(
        paralelos["procesos"].astype(str),
        paralelos["eficiencia"],
        color="#9b59b6",
    )
    ax3.set_title("Eficiencia paralela")
    ax3.set_xlabel("Procesos")
    ax3.set_ylabel("Eficiencia (S/N)")
    ax3.set_ylim(0, 1.2)
    ax3.axhline(y=1.0, color="r", linestyle="--", alpha=0.5, label="Ideal")
    ax3.legend()
    ax3.grid(axis="y", alpha=0.3)
    fig3.tight_layout()
    fig3.savefig(os.path.join(RUTA_GRAFICAS, "03_eficiencia.png"), dpi=150)
    plt.close(fig3)


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
def main():
    print("=" * 60)
    print("EXPERIMENTO: MONTE CARLO SECUENCIAL vs PARALELO")
    print("=" * 60)
    print(f"N puntos: {N_PUNTOS:,}")
    print(f"Repeticiones: {REPETICIONES}")
    print(f"Procesos a probar: {PROCESOS}")
    print("=" * 60 + "\n")

    df_resultados = ejecutar_experimento()
    resumen, tiempo_sec = analizar_y_guardar(df_resultados)
    generar_graficas(resumen)

    print("\n" + "=" * 60)
    print("EXPERIMENTOS COMPLETADOS")
    print("=" * 60)
    print(f"Resultados guardados en: {os.path.abspath(RUTA_RESULTADOS)}")
    print("  - resultados.json")
    print("  - resultados.csv")
    print("  - resultados_completos.csv")
    print("  - resumen.txt")
    print("  - graficas.png")
    print("  - graficas/01_tiempos.png")
    print("  - graficas/02_speedup.png")
    print("  - graficas/03_eficiencia.png")


if __name__ == "__main__":
    main()
