from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading

LOCALHOST = "127.0.0.1"
ALL_INTERFACES = "0.0.0.0"


def _resolve_frontend_path(path):
    frontend_path = Path(path).expanduser().resolve()
    if not frontend_path.exists():
        raise ValueError(f"Frontend path does not exist: {frontend_path}")
    if not frontend_path.is_dir():
        raise ValueError(f"Frontend path must be a directory: {frontend_path}")
    return frontend_path


def get_frontend_url(host, port):
    url_host = LOCALHOST if host == ALL_INTERFACES else host
    return f"http://{url_host}:{port}"


def create_frontend_server(path=".", host=LOCALHOST, port=10086):
    frontend_path = _resolve_frontend_path(path)
    handler = partial(SimpleHTTPRequestHandler, directory=str(frontend_path))
    try:
        server = ThreadingHTTPServer((host, port), handler)
    except OSError as e:
        raise RuntimeError(f"Failed to start web server on {host}:{port}. The port may already be in use: {e}") from e
    return server, frontend_path


def start_frontend_server(path=".", host=LOCALHOST, port=10086):
    server, frontend_path = create_frontend_server(path=path, host=host, port=port)
    thread = threading.Thread(target=server.serve_forever, name="FrontendWebServer", daemon=True)
    thread.start()
    return server, thread, frontend_path, get_frontend_url(host, port)


def serve_frontend(path=".", host=LOCALHOST, port=10086):
    server, frontend_path = create_frontend_server(path=path, host=host, port=port)
    print(f"Serving frontend: {frontend_path}")
    print(f"URL: {get_frontend_url(host, port)}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
