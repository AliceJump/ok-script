from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def _resolve_frontend_path(path):
    frontend_path = Path(path).expanduser().resolve()
    if not frontend_path.exists():
        raise ValueError(f"Frontend path does not exist: {frontend_path}")
    if not frontend_path.is_dir():
        raise ValueError(f"Frontend path must be a directory: {frontend_path}")
    return frontend_path


def serve_frontend(path=".", host="127.0.0.1", port=10086):
    frontend_path = _resolve_frontend_path(path)
    handler = partial(SimpleHTTPRequestHandler, directory=str(frontend_path))
    access_host = "127.0.0.1" if host == "0.0.0.0" else host
    try:
        with ThreadingHTTPServer((host, port), handler) as server:
            print(f"Serving frontend: {frontend_path}")
            print(f"URL: http://{access_host}:{port}")
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
    except OSError as e:
        raise RuntimeError(f"Failed to start web server on {host}:{port}: {e}") from e
