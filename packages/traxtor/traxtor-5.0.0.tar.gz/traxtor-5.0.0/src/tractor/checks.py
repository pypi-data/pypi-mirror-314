# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2020-2024.

"""
actions for tractor internals
"""

import socket
import urllib

import socks
from gi.repository import Gio
from stem.util import system

from . import control, db


def running() -> bool:
    """
    checks if Tractor is running or not
    """
    pid = control.get_pid()
    if pid:
        return system.is_running(pid)
    return False


def _getaddrinfo(*args):
    """
    Perform DNS resolution through the socket
    """
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (args[0], args[1]))]


def _fetched() -> bool:
    """
    Checks if the expected resource fetched or not
    """
    port = control.get_listener("socks")[1]
    host = "https://check.torproject.org/"
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", port)
    old_socket = socket.socket
    socket.socket = socks.socksocket
    socket.getaddrinfo = _getaddrinfo
    expectation = "Congratulations."
    err = urllib.error
    try:
        with urllib.request.urlopen(host) as request:
            status = request.status
            response = request.read().decode("utf=8")
    except (err.HTTPError, err.URLError, TimeoutError):
        socket.socket = old_socket
        return False
    socket.socket = old_socket
    if status == 200 and expectation in response:
        return True
    return False


def connected() -> bool:
    """
    checks if Tractor is connected or not
    """
    if running():
        return _fetched()
    return False


def proxy_set() -> bool:
    """
    checks if proxy is set or not
    """
    schema = "org.gnome.system.proxy"
    conf = Gio.Settings.new(schema)
    if conf.get_string("mode") != "manual":
        return False
    try:
        x_ip, x_port = control.get_listener("socks")
    except ValueError:
        x_ip = "0.0.0.0" if db.get_val("accept-connection") else "127.0.0.1"
        x_port = db.get_val("socks-port")
    schema = "org.gnome.system.proxy.socks"
    conf = Gio.Settings.new(schema)
    my_ip = conf.get_string("host")
    my_port = conf.get_int("port")
    if my_ip == x_ip and my_port == x_port:
        return True
    return False


def verbose_print(text: str, verbose):
    """
    Print text only if the verbose is True
    """
    if verbose:
        print(text)


def verbose_return(obj1: type, obj2: type, verbose: bool):
    """
    Return object based on verbosity
    """
    if verbose:
        return obj2
    return obj1
