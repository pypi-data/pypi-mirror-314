import argparse
import socket
from pathlib import Path

from .server import app

base_path = Path(__file__).resolve().parent


def run_server(port=5001):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    app.run(host=ip, port=port)


def main():
    parser = argparse.ArgumentParser(description="file server tool")
    parser.add_argument(
        "-p",
        "--port",
        required=False,
        help="port number",
    )
    args = parser.parse_args()
    run_server(port=args.port) if args.port else run_server()
