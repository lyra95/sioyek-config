"""Local TCP messaging used to refresh an existing translator window."""

from __future__ import annotations

import getpass
import hashlib
import json
import socket
import threading
from typing import Callable


def _port(app_name: str) -> int:
    identity = f"{getpass.getuser()}:{app_name}".encode("utf-8")
    digest = hashlib.sha256(identity).digest()
    return 40000 + int.from_bytes(digest[:2], "big") % 20000


def _send(value: str, key: str, port: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.3) as connection:
            connection.sendall((json.dumps({key: value}) + "\n").encode("utf-8"))
        return True
    except OSError:
        return False


def start_message_server(server: socket.socket, key: str, on_message: Callable[[str], None]) -> None:
    def serve() -> None:
        while True:
            try:
                connection, _ = server.accept()
            except OSError:
                return
            with connection:
                try:
                    payload = connection.makefile("r", encoding="utf-8").readline()
                    value = json.loads(payload).get(key, "")
                    if isinstance(value, str) and value.strip():
                        on_message(value)
                except (OSError, json.JSONDecodeError):
                    continue

    threading.Thread(target=serve, daemon=True).start()


def run_single_instance(
    app_name: str,
    message_key: str,
    initial_value: str,
    run_window: Callable[[str, socket.socket], None],
) -> None:
    port = _port(app_name)
    if _send(initial_value, message_key, port):
        return

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(("127.0.0.1", port))
        server.listen()
    except OSError:
        server.close()
        for _ in range(10):
            if _send(initial_value, message_key, port):
                return
            threading.Event().wait(0.1)
        raise RuntimeError(f"Could not start {app_name} server on 127.0.0.1:{port}")
    run_window(initial_value, server)
