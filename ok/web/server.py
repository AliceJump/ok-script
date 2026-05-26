import json
import os
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class WebStaticHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = json.dumps({"status": "ok"}).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path in ("", "/"):
            self.path = "/index.html"
            return super().do_GET()

        full_path = Path(self.directory) / self.path.lstrip("/")
        if not full_path.exists():
            self.path = "/index.html"
        return super().do_GET()


def run_web_server(host: str = "0.0.0.0", port: int = 10086, static_dir: str = "web"):
    resolved_static_dir = Path(static_dir).resolve()
    if not resolved_static_dir.exists() or not resolved_static_dir.is_dir():
        raise FileNotFoundError(f"Static directory not found: {resolved_static_dir}")

    handler = partial(WebStaticHandler, directory=os.fspath(resolved_static_dir))
    server = ThreadingHTTPServer((host, port), handler)
    print(f"Serving {resolved_static_dir} on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
