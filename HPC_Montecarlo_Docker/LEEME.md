# Presentación HPC con Monte Carlo en vivo

El laboratorio aparece después de la página 11. Son 15 pasos dentro de la página 12 y el cierre pasa a la página 13. Se conserva el diseño de la presentación y se corrige una afirmación absoluta sobre speedup en el cierre.

## Arranque en tu computadora

Descomprime el ZIP y abre una terminal **en Ubuntu, fuera del contenedor**, en la carpeta `HPC_Montecarlo_Docker`.

```bash
python3 iniciar.py
```

El contenedor predeterminado es `aa4953ef04ba`. Debe estar encendido y tu usuario debe poder ejecutar `docker exec`. El lanzador busca primero Python del entorno `pyhpc`, comprueba las dependencias, copia el paquete a una carpeta nueva en `/tmp` dentro del contenedor, inicia un kernel independiente y abre el navegador. No modifica tus notebooks existentes dentro del contenedor ni necesita puertos publicados en Docker.

**Deja la terminal abierta durante la exposición.** Si el navegador no se abre, copia la dirección completa que aparece en la terminal. Al terminar, Ctrl+C cierra el lanzador y solicita apagar el kernel.

No abras únicamente el HTML con doble clic: puedes ver el contenido, pero la ejecución requiere el lanzador.

## Durante la presentación

1. Avanza hasta el laboratorio, después de «¿Cuándo NO usar HPC?».
2. Presiona **Ejecutar** o **Ctrl + Enter** dentro de la celda.
3. Espera a que el indicador diga **Terminado** y pulsa **Siguiente paso**.
4. En el paso 5 puedes editar `N_PUNTOS` y `REPETICIONES`. El valor inicial es 10,000,000 y se hacen 3 repeticiones.
5. Ejecuta por separado la referencia secuencial y las pruebas con 1, 2, 4 y 8 procesos.
6. **Ampliar resultado** oculta el código para dar espacio a tablas y gráficas. También puedes pulsar la gráfica.
7. El último paso lleva al cierre.

Las variables se conservan durante la sesión. Editar o volver a ejecutar un paso invalida los resultados de ese paso y los posteriores. Debes ejecutarlos de nuevo en orden. La barra superior permite revisar pasos anteriores. En el laboratorio, espacio y flechas dejan de cambiar diapositivas para evitar avances accidentales; los botones inferiores de navegación de la presentación siguen disponibles.

**Reiniciar sesión** borra las variables y las salidas, conservando tus ediciones de código en la página. Recargar la página reinicia la interfaz, pero no el kernel: usa Reiniciar sesión para empezar limpio. Las ediciones en el navegador no se escriben automáticamente al `.ipynb`.

## Usar otro entorno o contenedor

**El HTML puede seguir igual.** Elige el entorno al arrancar el lanzador y conserva la carpeta completa del paquete. Estos ejemplos están orientados a Ubuntu/Linux.

Ejecuta los comandos desde la carpeta `HPC_Montecarlo_Docker`. Sustituye los nombres y las rutas de ejemplo por los de tu equipo.

| Destino del cálculo | Cómo iniciar |
| --- | --- |
| Docker actual (`aa4953ef04ba`) | `python3 iniciar.py` |
| Otro Docker | `python3 iniciar.py --container NOMBRE_O_ID` |
| Python específico dentro de otro Docker | `python3 iniciar.py --container NOMBRE_O_ID --python /ruta/del/entorno/bin/python` |
| Conda en tu computadora | Activa el entorno y usa `python iniciar.py --local` |
| `venv` en tu computadora | Activa el entorno y usa `python iniciar.py --local` |
| Python local por ruta absoluta | `/ruta/del/entorno/bin/python iniciar.py --local` |

### Otro contenedor Docker

Desde una terminal de Ubuntu, **fuera del contenedor**:

```bash
python3 iniciar.py --container NOMBRE_O_ID
```

El contenedor debe estar encendido. El lanzador busca primero el entorno `pyhpc` en varias ubicaciones habituales de Miniforge/Conda. Si no lo encuentra, intenta usar `python3` o `python` del contenedor. La autodetección no busca todos los entornos posibles.

Para elegir uno de forma explícita:

```bash
python3 iniciar.py --container NOMBRE_O_ID --python /ruta/del/entorno/bin/python
```

La ruta de `--python` corresponde al **interior del contenedor**. No es la ruta del Python de Ubuntu anfitrión.

Para el contenedor actual, si esta es la ubicación real de `pyhpc`:

```bash
python3 iniciar.py --container aa4953ef04ba --python /root/miniforge3/envs/pyhpc/bin/python
```

La opción `--container` acepta el nombre o ID que reconoce Docker. El lanzador usa el cliente Docker instalado en la máquina donde lo ejecutas.

### Un entorno Conda local

Activa el entorno que quieras usar, por ejemplo `pyhpc`:

```bash
conda activate pyhpc
python -c "import sys; print(sys.executable)"
python iniciar.py --local
```

El segundo comando muestra qué Python has activado. En este modo, tanto el kernel como los cálculos corren directamente en tu computadora y no se utiliza Docker.

### Un entorno virtual venv local

Activa tu entorno existente:

```bash
source /ruta/de/tu/venv/bin/activate
python -c "import sys; print(sys.executable)"
python iniciar.py --local
```

También puedes indicar directamente su intérprete sin activar el entorno:

```bash
/ruta/de/tu/venv/bin/python iniciar.py --local
```

**En modo local, se usa el Python que ejecuta `iniciar.py`.** La opción `--python` selecciona el intérprete de Docker y no tiene efecto con `--local`.

### Un servidor remoto, una VPS o Docker en otra máquina

El paquete no incluye opciones para introducir una dirección SSH, credenciales o la URL de un Jupyter remoto. Tampoco se conecta a la sesión de un notebook que ya esté abierto.

Para ese escenario habría que configurar o adaptar la conexión, por ejemplo mediante SSH. La interfaz HTML podría conservarse, pero la conexión remota necesitaría una prueba específica. No basta con pasar una dirección IP a `--container`: esa opción espera un nombre o ID reconocido por tu cliente Docker.

### Dependencias del entorno elegido

El Python que hace los cálculos necesita:

- `jupyter_client`
- `ipykernel`
- `pandas`
- `matplotlib`

Para comprobar un entorno local ya activado:

```bash
python -c "import jupyter_client, ipykernel, pandas, matplotlib; print('Dependencias disponibles')"
```

Si falta algún paquete, instálalo en ese entorno:

```bash
python -m pip install jupyter_client ipykernel pandas matplotlib
```

Dentro de Docker, utiliza la ruta del Python que vas a seleccionar:

```bash
docker exec NOMBRE_O_ID /ruta/del/entorno/bin/python -m pip install jupyter_client ipykernel pandas matplotlib
```

Para el contenedor actual, si la ruta de Miniforge coincide con tu instalación:

```bash
docker exec aa4953ef04ba /root/miniforge3/envs/pyhpc/bin/python -m pip install jupyter_client ipykernel pandas matplotlib
```

No hace falta instalar nada si los paquetes ya están disponibles. El lanzador no instala dependencias automáticamente. Si usas Docker, en Ubuntu anfitrión basta Python 3 y el cliente Docker con acceso al contenedor.

### Puerto y navegador

El servidor de la presentación usa el puerto local `8765`. Puedes cambiarlo sin modificar el HTML:

```bash
python3 iniciar.py --container NOMBRE_O_ID --port 8767
python iniciar.py --local --port 8767
```

Si prefieres abrir el navegador manualmente:

```bash
python3 iniciar.py --no-browser
```

Copia la dirección completa que imprime la terminal. Las opciones `--port` y `--no-browser` se pueden combinar con el modo Docker o local.

### Qué cambia al elegir otro entorno

El cálculo utiliza los recursos del equipo o contenedor donde corre Python. Cambiar de entorno puede cambiar las versiones de las librerías y los tiempos medidos. En Docker también influyen la cuota de CPU y los límites de memoria.

Para comparar resultados entre equipos, conserva el mismo número de puntos, repeticiones y código, y registra el entorno utilizado. Cada arranque crea una sesión nueva: las variables y las salidas no se trasladan automáticamente de un entorno a otro.

## Qué ejecuta

`kernel_bridge.py` inicia un kernel IPython mediante `jupyter_client`, usando el intérprete seleccionado. En modo Docker, el HTML envía una celda al servidor de la máquina anfitriona y este se comunica por stdin/stdout con `docker exec -i`. En modo local, el lanzador inicia el puente directamente con el mismo intérprete que ejecuta `iniciar.py`. Los textos, errores, tablas y gráficas se transmiten conforme llegan. El servidor se vincula únicamente a `127.0.0.1` y las operaciones de ejecución requieren un token nuevo por sesión. No se conecta al kernel de un notebook que ya tengas abierto.

El código de Monte Carlo y el worker proceden de tus archivos. La interfaz divide la medición en etapas. No simula tiempos ni reutiliza resultados históricos. El tiempo medido corresponde a la función de cálculo, incluida la creación del pool paralelo; no incluye dibujar la gráfica ni transportar la salida al navegador.

Los resultados dependen de la CPU, su carga y las restricciones del contenedor. `os.cpu_count()` muestra CPU lógicas visibles y no garantiza que todas estén disponibles en la cuota de Docker.

La interfaz del laboratorio no descarga librerías web. Las fuentes de Google y las dos fotos de Unsplash de la presentación original siguen siendo externas; su carga necesita Internet. Sin ellas el navegador utiliza fuentes de respaldo.

## Archivos y resultados

- `presentacion.html`: presentación integrada.
- `Montecarlo.ipynb`: notebook original con conclusiones en Markdown, análisis corregido y salidas antiguas eliminadas.
- `Laboratorio.ipynb`: las 15 celdas de ejecución de la presentación, para abrirlas también en Jupyter.
- `montecarlo_worker.py`: tu worker original, al lado de los notebooks para que se pueda importar.
- `src/` y `scripts/`: tus archivos Python originales, conservando la estructura que espera `run_experiments.py`.
- `iniciar.py`, `kernel_bridge.py`, `laboratorio.py`: lanzador, puente Jupyter y apoyo de medición.

Al ejecutar el paso de la tabla, se guardan `resultados/resultados_completos.csv` y `resultados/resumen.csv` en la carpeta de la sesión dentro del contenedor. El lanzador imprime esa carpeta al iniciar. Para recuperarla, sustituye `RUTA_MOSTRADA` por la ruta exacta impresa:

```bash
docker cp aa4953ef04ba:RUTA_MOSTRADA/resultados ./resultados_montecarlo
```

Si elegiste otro contenedor, sustituye también `aa4953ef04ba` por su nombre o ID. En modo Docker, el directorio está en `/tmp`: copia los resultados que quieras conservar antes de limpiar o eliminar el contenedor.

En modo `--local`, los CSV se guardan en la subcarpeta `resultados/` de `HPC_Montecarlo_Docker`, directamente en tu computadora. Volver a ejecutar la tabla reemplaza esos CSV en la misma sesión o carpeta. Las gráficas de la presentación aparecen en pantalla; el script original `scripts/run_experiments.py` permite generar también sus archivos con su propio experimento completo.

## Si algo falla

- **Sin conexión:** abre la dirección completa que imprime el lanzador y mantén su terminal abierta.
- **Contenedor detenido:** inícialo con `docker start aa4953ef04ba` antes de ejecutar el lanzador.
- **Permisos de Docker:** usa una terminal de tu máquina donde ya funcione `docker exec aa4953ef04ba ...`.
- **Puerto ocupado:** usa `--port 8767` u otro puerto libre.
- **Error de importación:** revisa que se eligió el entorno correcto y que sus dependencias están instaladas.
- **Tarda demasiado:** prueba primero con 1,000,000 de puntos en el paso 5. Mantén el mismo número para todas las configuraciones.
- **Kernel cerrado o ejecución bloqueada:** termina el lanzador y vuelve a iniciarlo. Una celda tiene un límite aproximado de 15 minutos sin finalización.

La conexión final con tu contenedor debe comprobarse en tu computadora. No se ha accedido a tu Docker desde aquí.
