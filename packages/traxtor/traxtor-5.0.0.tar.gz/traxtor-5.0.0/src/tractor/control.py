# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2024.
"""
Things to do with control socket
"""

from gi.repository import GLib
from stem import Signal, SocketError
from stem.control import Controller


def send_signal(signal: str) -> None:
    """
    Send a signal to the tor process
    """
    control_socket = GLib.get_user_config_dir() + "/tractor/control.sock"
    with Controller.from_socket_file(path=control_socket) as controller:
        controller.authenticate()
        match signal:
            case "term":
                controller.signal(Signal.TERM)
            case "newnym":
                controller.signal(Signal.NEWNYM)
            case _:
                raise ValueError(f"Wrong signal '{signal}'.")


def get_listener(listener_type: str) -> int:
    """
    Get configuration from control socket
    """
    control_socket = GLib.get_user_config_dir() + "/tractor/control.sock"
    try:
        with Controller.from_socket_file(path=control_socket) as controller:
            controller.authenticate()
            value = controller.get_listeners(listener_type)
    except Exception as exc:
        raise ValueError from exc
    if value:
        return value[0]
    raise ValueError("No listener.")


def get_pid() -> int:
    """
    Get pid of the tor process
    """
    control_socket = GLib.get_user_config_dir() + "/tractor/control.sock"
    try:
        with Controller.from_socket_file(path=control_socket) as controller:
            pid = controller.get_pid()
    except (SocketError, ValueError):
        return 0
    return pid if pid else 0


def get_bridges() -> str:
    """
    Get the current using bridges
    """
    control_socket = GLib.get_user_config_dir() + "/tractor/control.sock"
    try:
        with Controller.from_socket_file(path=control_socket) as controller:
            controller.authenticate()
            if controller.get_conf("UseBridges"):
                return controller.get_conf("Bridge")
    except (SocketError, ValueError):
        return ""
    return ""
