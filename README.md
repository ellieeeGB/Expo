
# Proyecto HPC: Comparación Secuencial vs. Paralela — Simulación Monte Carlo para π
**Actividad:** Exposición técnica + proyecto/práctica + demostración  

## Integrantes
- Elliot Gonzalez
- Patricia Botello
- Ignacio Rodriguez
- Diego Alamaraz

## Descripción
Este proyecto compara el rendimiento de una implementación **secuencial** y una **paralela** (usando `multiprocessing` de Python) de una simulación **Monte Carlo** para estimar el valor de π.

El objetivo es demostrar experimentalmente cómo la paralelización reduce el tiempo de ejecución, pero también cómo el **speedup** no es lineal debido al overhead y a la **Ley de Amdahl**.

## Objetivo
- Comprender los conceptos de HPC, speedup, eficiencia y escalabilidad.
- Implementar una solución secuencial y una paralela.
- Medir tiempos de ejecución variando el número de procesos (1, 2, 4, 8).
- Analizar los resultados y explicar por qué más procesos no siempre es mejor.

## Arquitectura / Metodología
- **Problema:** Estimar π generando N puntos aleatorios en un cuadrado de lado 2 (de -1 a 1) y contando cuántos caen dentro del círculo unitario (x² + y² ≤ 1).
- **Versión A (Secuencial):** Un solo proceso recorre los N puntos.
- **Versión B (Paralela):** Se divide N en P chunks, cada proceso worker cuenta su chunk, y el proceso principal suma los resultados.
- **Experimentos:** 1, 2, 4 y 8 procesos, 3 repeticiones cada uno.
- **Métricas:** Tiempo de ejecución, Speedup, Eficiencia.

## Requisitos
- Python 3.8 o superior
- matplotlib
- pandas
- numpy
- Jupyter Notebook (para ejecutar el notebook)

## Instalación
```bash
git clone https://github.com/ellieeeGB/Expo.git
cd Expo
pip install -r requirements.txt
```

## Instrucciones de ejecución

### Opción 1: Notebook (recomendado para entender paso a paso)
```bash
jupyter notebook notebooks/montecarlo_hpc.ipynb
```
Ejecutar todas las celdas en orden. El notebook:
- Explica Monte Carlo desde cero.
- Implementa la versión secuencial y paralela.
- Ejecuta los experimentos obligatorios.
- Guarda automáticamente los resultados en `resultados/`.

### Opción 2: Script de experimentos (rápido, sin notebook)
```bash
python scripts/run_experiments.py
```
Este script ejecuta los experimentos y genera todos los archivos en `resultados/`.

### Opción 3: Ejecuciones individuales
```bash
# Versión secuencial
python src/montecarlo_secuencial.py --n 10000000

# Versión paralela con 4 procesos
python src/montecarlo_paralelo.py --n 10000000 --procesos 4
```

## Procedimiento para reproducir los experimentos
1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar el notebook completo (`notebooks/montecarlo_hpc.ipynb`) **o** el script `scripts/run_experiments.py`.
4. Revisar los archivos generados en `resultados/`:
   - `resultados.json`: datos estructurados.
   - `resultados.csv`: tabla resumen.
   - `graficas.png`: visualización de tiempos, speedup y eficiencia.
   - `analisis.txt`: interpretación de los resultados.
5. Para el análisis detallado, abrir el notebook.


