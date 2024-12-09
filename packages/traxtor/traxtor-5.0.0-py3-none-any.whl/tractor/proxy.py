# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2024

"""
module for setting and removing proxy
"""

from gi.repository import Gio

from . import checks, control, db


def proxy_set(verbose: bool = False) -> None:
    """
    setup proxy
    """
    if not checks.running():
        print("Tractor is not running!")
    elif checks.proxy_set():
        checks.verbose_print("Proxy is already set", verbose)
    else:
        proxy = Gio.Settings.new("org.gnome.system.proxy")
        mode, host, port = get_proxy()
        if mode in ["socks", "https", "http"]:
            db.set_val("upstream-proxy", (mode, host, port))
        socks = Gio.Settings.new("org.gnome.system.proxy.socks")
        my_ip, socks_port = control.get_listener("socks")
        ignored = [
            "localhost",
            "127.0.0.0/8",
            "::1",
            "192.168.0.0/16",
            "10.0.0.0/8",
            "172.16.0.0/12",
        ]
        socks.set_string("host", my_ip)
        socks.set_int("port", socks_port)
        proxy.set_string("mode", "manual")
        proxy.set_strv("ignore-hosts", ignored)
        checks.verbose_print("Proxy set", verbose)


def proxy_unset(verbose: bool = False) -> None:
    """
    unset proxy
    """
    if checks.proxy_set():
        mode, host, port = tuple(db.get_val("upstream-proxy"))
        proxy = Gio.Settings.new("org.gnome.system.proxy")
        match mode:
            case "none":
                proxy.set_string("mode", "none")
            case "socks":
                proxy.set_string("mode", "manual")
                socks = Gio.Settings.new("org.gnome.system.proxy.socks")
                socks.set_string("host", host)
                socks.set_int("port", port)
            case "https":
                proxy.set_string("mode", "manual")
                https = Gio.Settings.new("org.gnome.system.proxy.https")
                https.set_string("host", host)
                https.set_int("port", port)
            case "http":
                proxy.set_string("mode", "manual")
                http = Gio.Settings.new("org.gnome.system.proxy.http")
                http.set_string("host", host)
                http.set_int("port", port)
        checks.verbose_print("Proxy unset", verbose)
    else:
        checks.verbose_print("Proxy is not set", verbose)


def get_proxy() -> tuple[str, str, int]:
    """
    get current proxy of system
    """
    try:
        if checks.proxy_set():
            return "none", "", 0
    except ValueError:
        return "none", "", 0
    proxy = Gio.Settings.new("org.gnome.system.proxy")
    if proxy.get_string("mode") == "manual":
        socks = Gio.Settings.new("org.gnome.system.proxy.socks")
        host = socks.get_string("host")
        port = socks.get_int("port")
        if host and port:
            return "socks", host, port
        https = Gio.Settings.new("org.gnome.system.proxy.https")
        host = https.get_string("host")
        port = https.get_int("port")
        if host and port:
            return "https", host, port
        http = Gio.Settings.new("org.gnome.system.proxy.http")
        host = http.get_string("host")
        port = http.get_int("port")
        if host and port:
            return "http", host, port
    return "none", "", 0
