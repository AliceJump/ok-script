import argparse
import os

from ok_web.server import run_web_server


def build_parser():
    parser = argparse.ArgumentParser(prog="python -m ok_web")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host (default: 0.0.0.0)")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", os.getenv("WEB_PORT", "10086"))),
        help="Bind port (default: PORT/WEB_PORT/10086)",
    )
    parser.add_argument(
        "--static-dir",
        default=os.getenv("WEB_STATIC_DIR", "web"),
        help="Static file directory (default: WEB_STATIC_DIR/web)",
    )
    return parser


def main():
    args = build_parser().parse_args()
    run_web_server(host=args.host, port=args.port, static_dir=args.static_dir)


if __name__ == "__main__":
    main()
