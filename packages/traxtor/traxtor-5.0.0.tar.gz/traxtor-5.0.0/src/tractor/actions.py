# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2020-2024.

"""
real actions of tractor
"""

import os
import signal

from stem.process import launch_tor
from stem.util import term

from . import checks, control, db, proxy, tractorrc

no_color = os.environ["NO_COLOR"] if "NO_COLOR" in os.environ else 0


def _print_bootstrap_lines(line) -> None:
    """
    prints bootstrap line in standard output
    """
    if "Bootstrapped " in line:
        print(
            term.format(line, "" if no_color else term.Color.BLUE),
            flush=True,
        )


def _print_all_lines(line) -> None:
    """
    prints bootstrap line in standard output
    """
    print(
        term.format(line, "" if no_color else term.Color.BLUE),
        flush=True,
    )


def _finish_notification(verbose: bool) -> None:
    """
    Notify user after start finished
    """
    if not checks.running():
        print(
            term.format(
                "Tractor could not connect.\n"
                "Please check your connection and try again.",
                "" if no_color else term.Attr.BOLD,
                "" if no_color else term.Color.RED,
            )
        )
    else:
        if db.get_val("auto-set"):
            proxy.proxy_set(verbose)
        checks.verbose_print(
            term.format(
                "Connected",
                "" if no_color else term.Attr.BOLD,
                "" if no_color else term.Color.GREEN,
            ),
            verbose,
        )


def _launch(torrc: str, tmpdir: str, verbose: bool) -> None:
    """
    Actually launch tor
    """
    msg_handler = checks.verbose_return(
        _print_bootstrap_lines, _print_all_lines, verbose
    )
    try:
        tractor_process = launch_tor(
            torrc_path=torrc,
            init_msg_handler=msg_handler,
        )
        db.set_val("pid", tractor_process.pid)
    except OSError as error:
        print(term.format(f"{error}\n", "" if no_color else term.Color.RED))
    except KeyboardInterrupt:
        pass
    else:
        _finish_notification(verbose)
    finally:
        os.remove(torrc)
        os.rmdir(tmpdir)


def _start_launch(verbose: bool) -> None:
    """
    Start launching tor
    """
    data_dir = db.data_directory()
    os.makedirs(data_dir, mode=0o700, exist_ok=True)
    try:
        tmpdir, torrc = tractorrc.create()
    except ValueError as error:
        print(
            term.format(
                f"Error Creating torrc. Check your configurations\n{error}",
                "" if no_color else term.Attr.BOLD,
                "" if no_color else term.Color.RED,
            )
        )
    except EnvironmentError as error:
        print(
            term.format(
                str(error),
                "" if no_color else term.Attr.BOLD,
                "" if no_color else term.Color.RED,
            )
        )
    else:
        checks.verbose_print(
            term.format(
                "Starting connection…",
                "" if no_color else term.Attr.BOLD,
                "" if no_color else term.Color.YELLOW,
            ),
            verbose,
        )
        _launch(torrc, tmpdir, verbose)


def start(verbose: bool = False) -> None:
    """
    starts onion routing
    """
    if not checks.running():
        _start_launch(verbose)
    else:
        print(
            term.format(
                "Tractor is already started",
                "" if no_color else term.Attr.BOLD,
                "" if no_color else term.Color.GREEN,
            )
        )


def stop(verbose: bool = False) -> None:
    """
    stops onion routing
    """
    if checks.running():
        control.send_signal("term")
        db.reset("pid")
        proxy.proxy_unset()
        db.reset("upstream-proxy")
        checks.verbose_print(
            term.format(
                "Tractor stopped",
                "" if no_color else term.Attr.BOLD,
                "" if no_color else term.Color.YELLOW,
            ),
            verbose,
        )
    else:
        checks.verbose_print(
            term.format(
                "Tractor seems to be stopped.",
                "" if no_color else term.Attr.BOLD,
                "" if no_color else term.Color.YELLOW,
            ),
            verbose,
        )


def restart(verbose: bool = False) -> None:
    """
    stop, then start
    """
    stop(verbose)
    start(verbose)


def new_id(verbose: bool = False) -> None:
    """
    gives user a new identity
    """
    if not checks.running():
        print(
            term.format(
                "Tractor is stopped.",
                "" if no_color else term.Attr.BOLD,
                "" if no_color else term.Color.YELLOW,
            )
        )
    else:
        control.send_signal("newnym")
        checks.verbose_print(
            term.format(
                "You now have a new ID.",
                "" if no_color else term.Attr.BOLD,
                "" if no_color else term.Color.GREEN,
            ),
            verbose,
        )


def kill_tor(verbose: bool = False) -> None:
    """
    kill tor process
    """
    pid = control.get_pid()
    if pid:
        os.killpg(os.getpgid(control.get_pid()), signal.SIGTERM)
        db.reset("pid")
        checks.verbose_print(
            term.format(
                "Tor process has been successfully killed!",
                "" if no_color else term.Attr.BOLD,
                "" if no_color else term.Color.GREEN,
            ),
            verbose,
        )
    else:
        checks.verbose_print(
            term.format(
                "Couldn't find any process to kill!",
                "" if no_color else term.Attr.BOLD,
                "" if no_color else term.Color.RED,
            ),
            verbose,
        )
