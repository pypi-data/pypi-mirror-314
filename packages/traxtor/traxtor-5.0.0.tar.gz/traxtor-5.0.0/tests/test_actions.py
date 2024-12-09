# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2024.
"""
unit tests for actions
"""

import signal
import unittest
from unittest.mock import patch
from tractor import actions


class MsgHandler(unittest.TestCase):
    """
    test case for message handlers
    """

    @patch("builtins.print")
    def test_print_bootstrap_lines_no(self, mock_print):
        """
        should not print
        """
        actions._print_bootstrap_lines("line")
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_print_bootstrap_lines_yes(self, mock_print):
        """
        should print
        """
        actions._print_bootstrap_lines("Bootstrapped line")
        mock_print.assert_called_once_with(
            "\x1b[34mBootstrapped line\x1b[0m", flush=True
        )

    @patch("builtins.print")
    def test_print_all_lines(self, mock_print):
        """
        should print
        """
        actions._print_all_lines("line")
        mock_print.assert_called_once_with("\x1b[34mline\x1b[0m", flush=True)


class FinishNotification(unittest.TestCase):
    """
    test case for _finish_notification
    """

    @patch("tractor.checks.running", return_value=False)
    @patch("sys.stdout")
    @patch("tractor.checks.verbose_print")
    def test_finish_notification_fail(self, mock_verbose_print, *_):
        """
        couldn't connect
        """
        actions._finish_notification(verbose=False)
        mock_verbose_print.assert_not_called()

    @patch("stem.util.term.format", return_value="connected")
    @patch("tractor.checks.running", return_value=True)
    @patch("tractor.db.get_val", return_value=True)
    @patch("tractor.proxy.proxy_set")
    @patch("tractor.checks.verbose_print")
    def test_finish_notification_done(self, mock_verbose_print, *_):
        """
        connected
        """
        actions._finish_notification(verbose=False)
        mock_verbose_print.assert_called_once_with("connected", False)


class Launch(unittest.TestCase):
    """
    test case for _launch
    """

    @patch("os.rmdir")
    @patch("os.remove")
    @patch("sys.stdout")
    @patch("tractor.actions.launch_tor", side_effect=OSError)
    @patch("tractor.actions._finish_notification")
    def test_launch_os_error(self, mock_finish, *_):
        """
        Couldn't launch
        """
        actions._launch("torrc", "tmpdir", False)
        mock_finish.assert_not_called()

    @patch("os.rmdir")
    @patch("os.remove")
    @patch("tractor.actions.launch_tor", side_effect=KeyboardInterrupt)
    @patch("tractor.actions._finish_notification")
    def test_launch_interrupt(self, mock_finish, *_):
        """
        Keyboard interrupt
        """
        actions._launch("torrc", "tmpdir", False)
        mock_finish.assert_not_called()

    @patch("os.rmdir")
    @patch("os.remove")
    @patch("tractor.db.set_val")
    @patch("tractor.actions.launch_tor")
    @patch("tractor.actions._finish_notification")
    def test_launch_ok(self, mock_finish, *_):
        """
        successful
        """
        actions._launch("torrc", "tmpdir", False)
        mock_finish.assert_called_once_with(False)


class StartLaunch(unittest.TestCase):
    """
    test case for _start_launch
    """

    @patch("sys.stdout")
    @patch("os.makedirs")
    @patch("tractor.tractorrc.create", side_effect=ValueError)
    @patch("tractor.actions._launch")
    def test_start_launch_value_error(self, mock_launch, *_):
        """
        configuration error
        """
        actions._start_launch(verbose=False)
        mock_launch.assert_not_called()

    @patch("sys.stdout")
    @patch("os.makedirs")
    @patch("tractor.tractorrc.create", side_effect=EnvironmentError)
    @patch("tractor.actions._launch")
    def test_start_launch_env_error(self, mock_launch, *_):
        """
        no bridge
        """
        actions._start_launch(verbose=False)
        mock_launch.assert_not_called()

    @patch("sys.stdout")
    @patch("os.makedirs")
    @patch("tractor.tractorrc.create", return_value=("a", "b"))
    @patch("tractor.actions._launch")
    def test_start_launch_success(self, mock_launch, *_):
        """
        starting launch
        """
        actions._start_launch(verbose=False)
        mock_launch.assert_called_once_with("b", "a", False)


class Start(unittest.TestCase):
    """
    test case for start
    """

    @patch("tractor.checks.running", return_value=False)
    @patch("tractor.actions._start_launch")
    def test_start_do(self, mock_launch, *_):
        """
        tractor is not running
        """
        actions.start()
        mock_launch.assert_called_once()

    @patch("sys.stdout")
    @patch("tractor.checks.running", return_value=True)
    @patch("tractor.actions._start_launch")
    def test_start_dont(self, mock_launch, *_):
        """
        tractor is already running
        """
        actions.start()
        mock_launch.assert_not_called()


class Stop(unittest.TestCase):
    """
    test case for stop
    """

    @patch("stem.util.term.format", return_value="Tractor stopped")
    @patch("tractor.checks.running", return_value=True)
    @patch("tractor.db.reset")
    @patch("tractor.control.send_signal")
    @patch("tractor.checks.verbose_print")
    def test_stop_do(self, mock_verbose_print, *_):
        """
        tractor is already running
        """
        actions.stop()
        mock_verbose_print.assert_called_once_with("Tractor stopped", False)

    @patch("stem.util.term.format", return_value="Tractor is stopped")
    @patch("tractor.checks.running", return_value=False)
    @patch("tractor.checks.verbose_print")
    def test_stop_dont(self, mock_verbose_print, *_):
        """
        tractor is not running
        """
        actions.stop()
        mock_verbose_print.assert_called_once_with("Tractor is stopped", False)


class Restart(unittest.TestCase):
    """
    test case for restart
    """

    @patch("tractor.actions.stop")
    @patch("tractor.actions.start")
    def test_restart(self, mock_start, mock_stop):
        """
        test restart
        """
        actions.restart()
        mock_stop.assert_called_once()
        mock_start.assert_called_once()


class NewId(unittest.TestCase):
    """
    test case for new_id
    """

    @patch("sys.stdout")
    @patch("tractor.checks.running", return_value=False)
    @patch("tractor.control.send_signal")
    def test_new_id_not_running(self, mock_send_signal, mock_running, *_):
        """
        tractor is not running
        """
        actions.new_id()
        mock_running.assert_called_once()
        mock_send_signal.assert_not_called()

    @patch("stem.util.term.format", return_value="You have a new ID")
    @patch("tractor.checks.running", return_value=True)
    @patch("tractor.control.send_signal")
    @patch("tractor.checks.verbose_print")
    def test_new_id_running(self, mock_verbose_print, mock_send_signal, *_):
        """
        tractor is running
        """
        actions.new_id()
        mock_send_signal.assert_called_once_with("newnym")
        mock_verbose_print.assert_called_once_with("You have a new ID", False)


class KillTor(unittest.TestCase):
    """
    test case for kill_tor
    """

    @patch("stem.util.term.format", return_value="No process to kill")
    @patch("tractor.control.get_pid", return_value=None)
    @patch("os.killpg")
    @patch("tractor.checks.verbose_print")
    def test_kill_tor_not_running(self, mock_verbose_print, mock_killpg, *_):
        """
        tractor is not running
        """
        actions.kill_tor()
        mock_killpg.assert_not_called()
        mock_verbose_print.assert_called_once_with("No process to kill", False)

    @patch("stem.util.term.format", return_value="Process killed")
    @patch("tractor.control.get_pid", return_value=5734)
    @patch("os.getpgid", return_value=1234)
    @patch("tractor.db.reset")
    @patch("os.killpg")
    @patch("tractor.checks.verbose_print")
    def test_kill_tor_running(self, mock_verbose_print, mock_killpg, *_):
        """
        tractor is running
        """
        actions.kill_tor()
        mock_killpg.assert_called_once_with(1234, signal.SIGTERM)
        mock_verbose_print.assert_called_once_with("Process killed", False)
