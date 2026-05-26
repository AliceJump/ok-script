import json
import os
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from ok_web.runtime import WebRuntime


class WebStaticHandler(SimpleHTTPRequestHandler):
    server_version = "ok-web/1.0"

    @property
    def runtime(self):
        return self.server.runtime

    def _write_json(self, payload, status=HTTPStatus.OK):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0:
            return {}
        raw = self.rfile.read(content_length)
        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("Request body must be valid JSON.") from exc

    def _handle_api(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if self.command == "GET" and path == "/health":
            self._write_json(
                {
                    "status": "ok",
                    "service": "ok_web",
                    "runtime": self.runtime.get_state(),
                }
            )
            return True
        if self.command == "GET" and path == "/runtime/state":
            self._write_json(self.runtime.get_state())
            return True
        if self.command == "POST" and path == "/runtime/start":
            payload, status = self.runtime.start()
            self._write_json(payload, status=status)
            return True
        if self.command == "POST" and path == "/runtime/stop":
            payload, status = self.runtime.stop()
            self._write_json(payload, status=status)
            return True
        if self.command == "GET" and path == "/tasks":
            self._write_json(self.runtime.get_tasks())
            return True
        if self.command == "POST" and path.startswith("/tasks/") and path.endswith("/run"):
            task_id = path[len("/tasks/"):-len("/run")].strip("/")
            if not task_id:
                self._write_json({"error": "Task id is required."}, status=HTTPStatus.BAD_REQUEST)
                return True
            try:
                self._write_json(self.runtime.run_task(task_id))
            except KeyError:
                self._write_json({"error": f"Task {task_id!r} not found."}, status=HTTPStatus.NOT_FOUND)
            except RuntimeError as exc:
                self._write_json({"error": str(exc)}, status=HTTPStatus.CONFLICT)
            return True
        if self.command == "GET" and path == "/config":
            self._write_json(self.runtime.get_config())
            return True
        if self.command == "PUT" and path == "/config":
            try:
                payload = self._read_json_body()
                self._write_json(self.runtime.update_config(payload))
            except (ValueError, TypeError, KeyError) as exc:
                self._write_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
            return True
        if self.command == "GET" and path == "/logs":
            self._write_json(self.runtime.get_logs())
            return True
        return False

    def send_error(self, code, message=None, explain=None):
        index_path = os.path.join(self.directory, "index.html")
        if (
            code == HTTPStatus.NOT_FOUND
            and self.command == "GET"
            and self.path != "/index.html"
            and os.path.isfile(index_path)
        ):
            self.path = "/index.html"
            return super().do_GET()
        return super().send_error(code, message, explain)

    def do_GET(self):
        if self._handle_api():
            return

        if self.path in ("", "/"):
            self.path = "/index.html"
            return super().do_GET()

        return super().do_GET()

    def do_POST(self):
        if self._handle_api():
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_PUT(self):
        if self._handle_api():
            return
        self.send_error(HTTPStatus.NOT_FOUND)


def create_web_server(host: str = "0.0.0.0", port: int = 10086, static_dir: str = "web", config_path=None):
    resolved_static_dir = Path(static_dir).resolve()
    if not resolved_static_dir.exists() or not resolved_static_dir.is_dir():
        raise FileNotFoundError(f"Static directory not found: {resolved_static_dir}")

    handler = partial(WebStaticHandler, directory=os.fspath(resolved_static_dir))
    server = ThreadingHTTPServer((host, port), handler)
    server.runtime = WebRuntime(config_path=config_path)
    return server


def run_web_server(host: str = "0.0.0.0", port: int = 10086, static_dir: str = "web", config_path=None):
    server = create_web_server(host=host, port=port, static_dir=static_dir, config_path=config_path)
    print(f"Serving {Path(static_dir).resolve()} on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
