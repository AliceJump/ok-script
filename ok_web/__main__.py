import argparse
import os

from ok_web.server import run_web_server


def _resolve_port(default: int = 10086) -> int:
    value = os.getenv("PORT")
    if value is None:
        value = os.getenv("WEB_PORT")
    if value is None:
        value = str(default)
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid port value: {value!r}. Use an integer.") from exc


def build_parser():
    parser = argparse.ArgumentParser(prog="python -m ok_web")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host (default: 0.0.0.0)")
    parser.add_argument(
        "--port",
        type=int,
        default=_resolve_port(),
        help="Bind port (default: PORT/WEB_PORT/10086)",
    )
    parser.add_argument(
        "--static-dir",
        default=os.getenv("WEB_STATIC_DIR", "web"),
        help="Static file directory (default: WEB_STATIC_DIR/web)",
    )
    parser.add_argument(
        "--config-path",
        default=os.getenv("WEB_CONFIG_PATH"),
        help="Optional JSON config path (default: WEB_CONFIG_PATH)",
    )
    return parser


def main():
    args = build_parser().parse_args()
    run_web_server(host=args.host, port=args.port, static_dir=args.static_dir, config_path=args.config_path)


if __name__ == "__main__":
    main()
