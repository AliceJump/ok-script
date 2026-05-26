import json
import os
import threading
from collections import deque
from copy import deepcopy
from datetime import datetime, timezone
from http import HTTPStatus
from pathlib import Path


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class WebConfigStore:
    DEFAULTS = {
        "locale": "zh-CN",
        "theme": "system",
        "auto_start": False,
        "trigger_interval_ms": 1000,
        "debug": False,
    }
    ENV_MAPPING = {
        "WEB_LOCALE": ("locale", str),
        "WEB_THEME": ("theme", str),
        "WEB_AUTO_START": ("auto_start", lambda value: value.lower() in {"1", "true", "yes", "on"}),
        "WEB_TRIGGER_INTERVAL_MS": ("trigger_interval_ms", int),
        "WEB_DEBUG": ("debug", lambda value: value.lower() in {"1", "true", "yes", "on"}),
    }

    def __init__(self, config_path=None):
        self._lock = threading.Lock()
        self.config_path = Path(config_path) if config_path else None
        self._file_values = self._load_file_values()
        self._runtime_overrides = {}

    def _load_file_values(self):
        if self.config_path is None or not self.config_path.exists():
            return {}
        with self.config_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError("Config file must contain a JSON object.")
        return data

    def _env_values(self):
        values = {}
        for env_key, (config_key, parser) in self.ENV_MAPPING.items():
            raw = os.getenv(env_key)
            if raw is None:
                continue
            values[config_key] = parser(raw)
        return values

    def get_all(self):
        with self._lock:
            return self._merged_values_locked()

    def _merged_values_locked(self):
        merged = deepcopy(self.DEFAULTS)
        merged.update(self._file_values)
        merged.update(self._env_values())
        merged.update(self._runtime_overrides)
        return merged

    def update(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("Config payload must be a JSON object.")

        unknown = sorted(set(payload) - set(self.DEFAULTS))
        if unknown:
            raise KeyError(f"Unknown config keys: {', '.join(unknown)}")

        merged = self.get_all()
        for key, value in payload.items():
            expected_type = type(self.DEFAULTS[key])
            if not isinstance(value, expected_type):
                raise TypeError(f"Config key {key!r} must be {expected_type.__name__}.")
            merged[key] = value

        with self._lock:
            self._runtime_overrides.update(payload)
            effective = self._merged_values_locked()
            if self.config_path is not None:
                self.config_path.parent.mkdir(parents=True, exist_ok=True)
                with self.config_path.open("w", encoding="utf-8") as fh:
                    json.dump(effective, fh, ensure_ascii=False, indent=2, sort_keys=True)
                    fh.write("\n")
            return effective


class WebRuntime:
    def __init__(self, config_path=None):
        self._lock = threading.Lock()
        self.state = "idle"
        self.last_error = None
        self.started_at = None
        self.last_state_change_at = utc_now()
        self.config_store = WebConfigStore(config_path=config_path)
        self.tasks = [
            {
                "id": "diagnosis",
                "name": "Diagnosis",
                "mode": "one_time",
                "enabled": True,
                "status": "idle",
                "last_run_at": None,
                "last_result": None,
            },
            {
                "id": "trigger_scan",
                "name": "Trigger Scan",
                "mode": "trigger",
                "enabled": True,
                "status": "idle",
                "last_run_at": None,
                "last_result": None,
            },
            {
                "id": "scheduled_cleanup",
                "name": "Scheduled Cleanup",
                "mode": "scheduled",
                "enabled": True,
                "status": "idle",
                "last_run_at": None,
                "last_result": None,
            },
        ]
        self.events = deque(maxlen=200)
        self.add_event("runtime.ready", "Web runtime initialized.")

    def add_event(self, event, message, level="info", **details):
        record = {
            "time": utc_now(),
            "event": event,
            "level": level,
            "message": message,
            "details": details,
        }
        with self._lock:
            self.events.append(record)
        return record

    def _set_state(self, state, message, **details):
        with self._lock:
            self.state = state
            self.last_state_change_at = utc_now()
            if state == "running":
                self.started_at = self.started_at or self.last_state_change_at
            elif state == "idle":
                self.started_at = None
            if state != "error":
                self.last_error = None
        self.add_event(f"runtime.{state}", message, **details)

    def get_state(self):
        with self._lock:
            return {
                "state": self.state,
                "started_at": self.started_at,
                "last_state_change_at": self.last_state_change_at,
                "last_error": self.last_error,
            }

    def start(self):
        current = self.get_state()["state"]
        if current == "running":
            self.add_event("runtime.start.duplicate", "Runtime start requested while already running.")
            return self.get_state(), HTTPStatus.OK
        self._set_state("starting", "Runtime is starting.")
        self._set_state("running", "Runtime is running.")
        return self.get_state(), HTTPStatus.OK

    def stop(self):
        current = self.get_state()["state"]
        if current == "idle":
            self.add_event("runtime.stop.duplicate", "Runtime stop requested while already idle.")
            return self.get_state(), HTTPStatus.OK
        self._set_state("stopping", "Runtime is stopping.")
        self._set_state("idle", "Runtime is idle.")
        return self.get_state(), HTTPStatus.OK

    def get_tasks(self):
        with self._lock:
            return {"items": deepcopy(self.tasks)}

    def run_task(self, task_id):
        with self._lock:
            task = next((task for task in self.tasks if task["id"] == task_id), None)
            if task is None:
                raise KeyError(task_id)
            if self.state != "running":
                raise RuntimeError("Runtime must be running before tasks can execute.")
            task["status"] = "running"
            task["last_run_at"] = utc_now()
        self.add_event("task.started", f"Task {task_id} started.", task_id=task_id)
        result = {
            "success": True,
            "error_code": None,
            "duration_ms": 0,
            "context": {"task_id": task_id},
        }
        with self._lock:
            task["status"] = "success"
            task["last_result"] = result
            response = deepcopy(task)
        self.add_event("task.finished", f"Task {task_id} finished.", task_id=task_id, success=True)
        return response

    def get_config(self):
        return self.config_store.get_all()

    def update_config(self, payload):
        updated = self.config_store.update(payload)
        self.add_event("config.updated", "Web config updated.", keys=sorted(payload))
        return updated

    def get_logs(self, limit=50):
        with self._lock:
            records = list(self.events)[-limit:]
        return {"items": records, "total": len(records)}
