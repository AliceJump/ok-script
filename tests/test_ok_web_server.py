import json
import threading
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ok_web import create_web_server


class TestOkWebServer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        root = Path(self.temp_dir.name)
        (root / "index.html").write_text("<!doctype html><title>ok-web-test</title>", encoding="utf-8")
        self.config_path = root / "runtime-config.json"
        self.server = create_web_server(host="127.0.0.1", port=0, static_dir=root, config_path=self.config_path)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp_dir.cleanup()

    def request_json(self, path, method="GET", payload=None):
        data = None
        headers = {}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = Request(f"{self.base_url}{path}", method=method, data=data, headers=headers)
        with urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))

    def test_health_and_static_shell(self):
        status, payload = self.request_json("/health")
        self.assertEqual(200, status)
        self.assertEqual("ok", payload["status"])
        self.assertEqual("idle", payload["runtime"]["state"])

        with urlopen(f"{self.base_url}/missing-route", timeout=5) as response:
            html = response.read().decode("utf-8")
        self.assertIn("ok-web-test", html)

    def test_runtime_task_flow(self):
        _, runtime = self.request_json("/runtime/state")
        self.assertEqual("idle", runtime["state"])

        _, started = self.request_json("/runtime/start", method="POST")
        self.assertEqual("running", started["state"])

        _, task = self.request_json("/tasks/diagnosis/run", method="POST")
        self.assertEqual("success", task["status"])
        self.assertTrue(task["last_result"]["success"])

        _, stopped = self.request_json("/runtime/stop", method="POST")
        self.assertEqual("idle", stopped["state"])

    def test_task_requires_running_runtime(self):
        with self.assertRaises(HTTPError) as cm:
            self.request_json("/tasks/diagnosis/run", method="POST")
        self.assertEqual(409, cm.exception.code)
        payload = json.loads(cm.exception.read().decode("utf-8"))
        self.assertIn("Runtime must be running", payload["error"])

    def test_config_roundtrip_and_validation(self):
        _, config = self.request_json("/config")
        self.assertEqual("zh-CN", config["locale"])
        self.assertEqual(1000, config["trigger_interval_ms"])

        _, updated = self.request_json(
            "/config",
            method="PUT",
            payload={"theme": "dark", "trigger_interval_ms": 1500, "debug": True},
        )
        self.assertEqual("dark", updated["theme"])
        self.assertEqual(1500, updated["trigger_interval_ms"])
        self.assertTrue(updated["debug"])
        self.assertTrue(self.config_path.exists())

        with self.assertRaises(HTTPError) as cm:
            self.request_json("/config", method="PUT", payload={"trigger_interval_ms": "fast"})
        self.assertEqual(400, cm.exception.code)


if __name__ == "__main__":
    unittest.main()
