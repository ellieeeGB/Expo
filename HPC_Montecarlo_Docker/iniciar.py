#!/usr/bin/env python3
"""Abrir en la máquina anfitriona. No necesita puertos publicados en Docker."""
import argparse
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import threading
import time
from urllib.parse import urlsplit, parse_qs
import webbrowser

ROOT = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--container', default='aa4953ef04ba')
    ap.add_argument('--python', dest='interpreter', help='Ruta de Python dentro del contenedor')
    ap.add_argument('--port', type=int, default=8765)
    ap.add_argument('--no-browser', action='store_true')
    ap.add_argument('--local', action='store_true', help='Ejecutar con Python local en vez de Docker')
    args = ap.parse_args()
    if args.local:
        command = [sys.executable, '-u', str(ROOT / 'kernel_bridge.py')]
    else:
        subprocess.run(['docker', 'inspect', args.container], check=True, stdout=subprocess.DEVNULL)
        if args.interpreter:
            interpreter = args.interpreter
        else:
            detect = '''for p in /root/miniforge3/envs/pyhpc/bin/python /opt/conda/envs/pyhpc/bin/python /home/*/miniforge3/envs/pyhpc/bin/python /home/*/miniconda3/envs/pyhpc/bin/python; do if [ -x "$p" ]; then printf '%s\\n' "$p"; exit 0; fi; done; command -v python3 || command -v python'''
            interpreter = subprocess.check_output(['docker', 'exec', args.container, 'sh', '-c', detect], text=True).strip()
        check = subprocess.run(['docker', 'exec', args.container, interpreter, '-c',
            'import jupyter_client, ipykernel, pandas, matplotlib; import sys; print(sys.executable)'])
        if check.returncode:
            raise SystemExit('Faltan dependencias en ese Python. Consulta LEEME.md o usa --python con la ruta de pyhpc.')
        destination = '/tmp/hpc_montecarlo_' + secrets.token_hex(5)
        subprocess.run(['docker', 'exec', args.container, 'mkdir', '-p', destination], check=True)
        subprocess.run(['docker', 'cp', str(ROOT) + '/.', args.container + ':' + destination], check=True)
        command = ['docker', 'exec', '-i', '-w', destination, args.container, interpreter, '-u', 'kernel_bridge.py']
        print('Carpeta de esta sesión en Docker:', destination, flush=True)
    token = secrets.token_urlsafe(32)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    lock = threading.Lock()
    ready = process.stdout.readline()
    if not ready or json.loads(ready).get('type') != 'ready':
        raise SystemExit('No se pudo iniciar el kernel. Revisa el mensaje anterior.')
    print('Kernel listo:', json.loads(ready)['python'], flush=True)

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(ROOT), **kw)

        def log_message(self, *a):
            pass

        def do_GET(self):
            path = urlsplit(self.path)
            if path.path == '/api/status':
                valid = secrets.compare_digest(parse_qs(path.query).get('token', [''])[0], token)
                if not valid:
                    self.send_error(403); return
                data = json.dumps({'connected': process.poll() is None}).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers(); self.wfile.write(data); return
            # Sirve exclusivamente los archivos necesarios, sin listado de directorios.
            allowed = {'/', '/presentacion.html', '/Montecarlo.ipynb', '/Laboratorio.ipynb'}
            if path.path not in allowed:
                self.send_error(404); return
            if path.path == '/': self.path = '/presentacion.html'
            super().do_GET()

        def do_POST(self):
            if urlsplit(self.path).path != '/api/action':
                self.send_error(404); return
            if not secrets.compare_digest(self.headers.get('X-Lab-Token', ''), token):
                self.send_error(403); return
            origin = self.headers.get('Origin')
            if origin and origin != f'http://127.0.0.1:{self.server.server_port}':
                self.send_error(403); return
            try:
                length = int(self.headers.get('Content-Length', 0))
                if not 0 < length <= 200000: raise ValueError('Solicitud demasiado grande')
                request = json.loads(self.rfile.read(length))
                if request.get('action') not in ('execute', 'reset'): raise ValueError('Acción no válida')
                if request['action'] == 'execute' and not isinstance(request.get('code'), str): raise ValueError('Código no válido')
            except Exception:
                self.send_error(400); return
            if not lock.acquire(blocking=False):
                self.send_error(409, 'Hay una celda en ejecución'); return
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'application/x-ndjson; charset=utf-8')
                self.send_header('Cache-Control', 'no-store')
                self.send_header('Connection', 'close')
                self.end_headers()
                self.close_connection = True
                process.stdin.write(json.dumps(request) + '\n'); process.stdin.flush()
                connected = True
                while True:
                    line = process.stdout.readline()
                    if not line:
                        raise RuntimeError('Se perdió la conexión con Python. Cierra y vuelve a iniciar el lanzador.')
                    if connected:
                        try:
                            self.wfile.write(line.encode()); self.wfile.flush()
                        except (BrokenPipeError, ConnectionResetError):
                            connected = False
                    if json.loads(line).get('type') == 'done': break
            except Exception as exc:
                try:
                    for event in [{'type':'error','content':{'evalue':str(exc)}},{'type':'done','ok':False}]:
                        self.wfile.write((json.dumps(event)+'\n').encode())
                except OSError:
                    pass
            finally:
                lock.release()

    server = None
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
        url = f'http://127.0.0.1:{server.server_port}/presentacion.html#token={token}'
        print('\nAbre esta dirección en tu navegador:\n' + url, flush=True)
        print('\nDeja esta terminal abierta. Ctrl+C termina la sesión.', flush=True)
        if not args.no_browser: webbrowser.open(url)
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nCerrando la sesión…')
    finally:
        if server: server.server_close()
        try:
            process.stdin.write(json.dumps({'action':'shutdown'})+'\n'); process.stdin.flush()
            process.stdin.close()
            process.wait(timeout=20)
        except (OSError, subprocess.TimeoutExpired):
            process.terminate()


if __name__ == '__main__':
    main()
