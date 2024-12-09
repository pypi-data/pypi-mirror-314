# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2024.
"""
Unit tests for db
"""

import unittest
import socket
from unittest.mock import mock_open, patch, Mock
from tractor import checks


class Running(unittest.TestCase):
    """
    test case for running
    """

    @patch("tractor.control.get_pid", return_value=1234)
    @patch("stem.util.system.is_running", return_value=True)
    def test_success(self, mock_is_running, mock_get_pid):
        """
        it is running
        """
        result = checks.running()
        self.assertTrue(result)
        mock_get_pid.assert_called_once()
        mock_is_running.assert_called_once_with(1234)

    @patch("tractor.control.get_pid", return_value=None)
    def test_running_failure(self, mock_get_pid):
        """
        it's not running
        """
        result = checks.running()
        self.assertFalse(result)
        mock_get_pid.assert_called_once()


class GetAddrInfoTestCase(unittest.TestCase):
    """
    test casr for _getaddrinfo
    """
    def test_getaddrinfo(self):
        """
        test _getaddrinfo
        """
        result = checks._getaddrinfo("example.com", 80)
        # Assert the structure of the result
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], tuple)
        self.assertEqual(len(result[0]), 5)
        # Assert the values in the result
        self.assertEqual(result[0][0], socket.AF_INET)
        self.assertEqual(result[0][1], socket.SOCK_STREAM)
        self.assertEqual(result[0][2], 6)  # socket.IPPROTO_TCP
        self.assertEqual(result[0][3], "")
        self.assertEqual(result[0][4], ("example.com", 80))


class Fetched(unittest.TestCase):
    """
    test case for _fetched
    """

    @patch("tractor.control.get_listener")
    @patch("urllib.request.urlopen", side_effect=TimeoutError)
    def test_timeout(self, *_):
        """
        timeout given
        """
        self.assertFalse(checks._fetched())

    @patch("tractor.control.get_listener", return_value=("127.0.0.1", 9052))
    @patch("urllib.request.urlopen")
    def test_failed(self, mock_urlopen, *_):
        """
        not using tor
        """
        mock_response = mock_open(
            read_data="Sorry. You are not using Tor.".encode()
        ).return_value
        mock_response.status = 200
        mock_urlopen.return_value = mock_response
        result = checks._fetched()
        self.assertFalse(result)
        mock_urlopen.assert_called_once_with("https://check.torproject.org/")

    @patch("tractor.control.get_listener", return_value=("127.0.0.1", 9052))
    @patch("urllib.request.urlopen")
    def test_success(self, mock_urlopen, *_):
        """
        connection successful
        """
        mock_response = mock_open(
            read_data=(
                "Congratulations. This browser is configured to use Tor."
            ).encode()
        ).return_value
        mock_response.status = 200
        mock_urlopen.return_value = mock_response
        result = checks._fetched()
        self.assertTrue(result)
        mock_urlopen.assert_called_once_with("https://check.torproject.org/")


class Connected(unittest.TestCase):
    """
    test case for connected
    """

    @patch("tractor.checks.running", return_value=False)
    def test_fail(self, mock_running):
        """
        not running
        """
        result = checks.connected()
        self.assertFalse(result)
        mock_running.assert_called_once()

    @patch("tractor.checks.running", return_value=True)
    @patch("tractor.checks._fetched", return_value=True)
    def test_success(self, mock_fetched, mock_running):
        """
        running
        """
        result = checks.connected()
        self.assertTrue(result)
        mock_running.assert_called_once()
        mock_fetched.assert_called_once()


class ProxySet(unittest.TestCase):
    """
    test case for proxy_set
    """

    @patch("gi.repository.Gio.Settings.new")
    def test_proxy_none(self, mock_gio_settings_new):
        """
        proxy is not on manual
        """
        mock_gio_settings_instance = Mock()
        mock_gio_settings_instance.get_string.return_value = "none"
        mock_gio_settings_new.return_value = mock_gio_settings_instance

        result = checks.proxy_set()
        self.assertFalse(result)
        mock_gio_settings_new.assert_called_with("org.gnome.system.proxy")
        mock_gio_settings_instance.get_string.assert_called_with("mode")

    @patch("tractor.control.get_listener", return_value=("127.0.0.1", 9052))
    @patch("gi.repository.Gio.Settings.new")
    def test_proxy_fail(self, mock_settings, *_):
        """
        proxy mismatch
        """
        mock_settings_instance = Mock()
        mock_settings_instance.get_string.return_value = "manual"
        mock_settings_instance.get_int.return_value = 9050
        mock_settings.return_value = mock_settings_instance
        result = checks.proxy_set()
        self.assertFalse(result)
        mock_settings.assert_called()
        mock_settings_instance.get_string.assert_called()
        mock_settings_instance.get_int.assert_called_with("port")

    @patch("tractor.control.get_listener", return_value=("127.0.0.1", 9052))
    @patch("gi.repository.Gio.Settings.new")
    def test_proxy_set(self, mock_settings, *_):
        """
        proxy is set
        """
        mock_settings_instance = Mock()
        mock_settings_instance.get_string.side_effect = (
            lambda key: "manual" if key == "mode" else "127.0.0.1"
        )
        mock_settings_instance.get_int.return_value = 9052
        mock_settings.return_value = mock_settings_instance

        result = checks.proxy_set()
        self.assertTrue(result)
        mock_settings.assert_called()
        mock_settings_instance.get_string.assert_called()
        mock_settings_instance.get_int.assert_called_with("port")


class Verbose(unittest.TestCase):
    """
    test case for verbose functions
    """

    def test_verbose_print(self):
        """
        print
        """
        with patch("builtins.print") as mock_print:
            checks.verbose_print("Test Message", verbose=True)
            mock_print.assert_called_once_with("Test Message")

    def test_verbose_return(self):
        """
        return
        """
        result = checks.verbose_return(True, False, verbose=True)
        self.assertFalse(result)

    def test_nonverbose_return(self):
        """
        return
        """
        result = checks.verbose_return(True, False, verbose=False)
        self.assertTrue(result)
