# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2024.
"""
Unit tests for db
"""

import unittest
from unittest.mock import patch
from stem import SocketError
from tractor import control


class SendSignal(unittest.TestCase):
    """
    test case for send_signal
    """

    @patch("gi.repository.GLib.get_user_config_dir", return_value="~/.config")
    @patch("stem.control.Controller.authenticate")
    @patch("stem.control.Controller.from_socket_file")
    def test_send_signal_success(self, mock_sock_controller, *_):
        """
        send defined signals
        """
        mock_controller = (
            mock_sock_controller.return_value.__enter__.return_value
        )
        control.send_signal("term")
        mock_sock_controller.assert_called_once_with(
            path="~/.config/tractor/control.sock"
        )
        mock_controller.authenticate.assert_called_once()
        mock_controller.signal.assert_called_once_with("TERM")
        control.send_signal("newnym")
        mock_controller.signal.assert_called_with("NEWNYM")

    @patch("gi.repository.GLib.get_user_config_dir", return_value="~/.config")
    @patch("stem.control.Controller.authenticate")
    @patch("stem.control.Controller.from_socket_file")
    def test_send_signal_fail(self, *_):
        """
        undefined signal
        """
        with self.assertRaises(ValueError):
            control.send_signal("kill")


class GetListener(unittest.TestCase):
    """
    test case for get_listener
    """

    @patch("gi.repository.GLib.get_user_config_dir", return_value="~/.config")
    @patch("stem.control.Controller.authenticate")
    @patch("stem.control.Controller.from_socket_file")
    def test_get_listener_success(self, mock_sock_controller, *_):
        """
        get listener of any type
        """
        mock_controller = (
            mock_sock_controller.return_value.__enter__.return_value
        )
        mock_controller.get_listeners.return_value = [9052]
        result = control.get_listener("socks")
        mock_sock_controller.assert_called_once_with(
            path="~/.config/tractor/control.sock"
        )
        mock_controller.get_listeners.assert_called_once_with("socks")
        self.assertEqual(result, 9052)

    @patch("gi.repository.GLib.get_user_config_dir", return_value="~/.config")
    @patch("stem.control.Controller.authenticate")
    @patch("stem.control.Controller.from_socket_file")
    def test_get_listener_fail(self, mock_sock_controller, *_):
        """
        get listener of any type
        """
        mock_controller = (
            mock_sock_controller.return_value.__enter__.return_value
        )
        mock_controller.get_listeners.return_value = None
        with self.assertRaises(ValueError):
            control.get_listener("ftp")
        mock_sock_controller.assert_called_once_with(
            path="~/.config/tractor/control.sock"
        )
        mock_controller.get_listeners.assert_called_once_with("ftp")


class GetPid(unittest.TestCase):
    """
    test case for get_pid
    """

    @patch("gi.repository.GLib.get_user_config_dir", return_value="~/.config")
    @patch("stem.control.Controller.from_socket_file")
    def test_getpid_success(self, mock_sock_controller, *_):
        """
        could get pid
        """
        mock_controller = (
            mock_sock_controller.return_value.__enter__.return_value
        )
        mock_controller.get_pid.return_value = 5678
        result = control.get_pid()
        mock_sock_controller.assert_called_once_with(
            path="~/.config/tractor/control.sock"
        )
        self.assertEqual(result, 5678)

    @patch("gi.repository.GLib.get_user_config_dir", return_value="~/.config")
    @patch("stem.control.Controller.from_socket_file", side_effect=SocketError)
    def test_getpid_fail(self, mock_sock_controller, *_):
        """
        couldn't get pid
        """
        result = control.get_pid()
        mock_sock_controller.assert_called_once_with(
            path="~/.config/tractor/control.sock"
        )
        self.assertEqual(result, 0)
