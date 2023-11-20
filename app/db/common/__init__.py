"""ROBERT"""
from .engine import Engine
from .config import Config
from .session import dbSession

__all__ = (
    "Engine",
    "Config",
    "dbSession",
)


def check_internet_connection() -> bool:
    try:
        import socket

        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False
