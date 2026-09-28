"""Protocolo JSON por stdin/stdout. Python y procesos viven en el contenedor."""
import json
import os
import queue
import sys
import time
from jupyter_client import KernelManager


def emit(data):
    print(json.dumps(data, ensure_ascii=False), flush=True)


def main():
    km = KernelManager(kernel_name='python3', ip='127.0.0.1')
    # Usar exactamente el intérprete elegido, aunque python3 apunte a otro entorno.
    km.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
    km.start_kernel(cwd=os.path.dirname(os.path.abspath(__file__)), stdout=sys.stderr, stderr=sys.stderr)
    client = km.blocking_client()
    client.start_channels()
    client.wait_for_ready(timeout=60)
    emit({'type': 'ready', 'python': sys.executable})
    try:
        for line in sys.stdin:
            try:
                request = json.loads(line)
                action = request.get('action')
                if action == 'shutdown':
                    break
                if action == 'reset':
                    client.stop_channels()
                    km.restart_kernel(now=True)
                    client = km.blocking_client()
                    client.start_channels()
                    client.wait_for_ready(timeout=60)
                    emit({'type': 'done', 'ok': True})
                    continue
                if action != 'execute':
                    raise ValueError('Acción no válida')
                msg_id = client.execute(request['code'], allow_stdin=False, stop_on_error=True)
                deadline = time.monotonic() + 900
                ok = True
                while True:
                    try:
                        msg = client.get_iopub_msg(timeout=1)
                    except queue.Empty:
                        if not km.is_alive():
                            raise RuntimeError('El kernel se cerró. Reinicia la sesión.')
                        if time.monotonic() > deadline:
                            km.interrupt_kernel()
                            raise TimeoutError('La celda superó 15 minutos. Reinicia la sesión.')
                        continue
                    if msg.get('parent_header', {}).get('msg_id') != msg_id:
                        continue
                    kind, data = msg['msg_type'], msg['content']
                    if kind == 'status' and data['execution_state'] == 'idle':
                        break
                    if kind == 'error':
                        ok = False
                    if kind in ('stream', 'display_data', 'execute_result', 'error', 'clear_output'):
                        emit({'type': kind, 'content': data})
                emit({'type': 'done', 'ok': ok})
            except Exception as exc:
                emit({'type': 'error', 'content': {'ename': type(exc).__name__, 'evalue': str(exc)}})
                emit({'type': 'done', 'ok': False})
    finally:
        client.stop_channels()
        km.shutdown_kernel(now=True)


if __name__ == '__main__':
    main()
