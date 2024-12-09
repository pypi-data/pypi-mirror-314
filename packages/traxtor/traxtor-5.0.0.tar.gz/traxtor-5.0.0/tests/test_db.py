# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2024.
"""
Unit tests for db
"""

import unittest
from unittest.mock import patch, Mock
from tractor import db


class Dconf(unittest.TestCase):
    """
    test case for dconf
    """

    @patch("gi.repository.Gio.SettingsSchemaSource.lookup", return_value=False)
    def test_absent(self, *_):
        """
        if dconf is not installed
        """
        with self.assertRaises(FileNotFoundError):
            db.dconf()

    @patch("gi.repository.Gio.SettingsSchemaSource.lookup", return_value=True)
    @patch("gi.repository.Gio.Settings.new")
    def test_present(self, mock_settings, *_):
        """
        if dconf is installed
        """
        mock_settings_instance = Mock()
        mock_settings.return_value = mock_settings_instance
        result = db.dconf()
        mock_settings.assert_called_once()
        self.assertIs(result, mock_settings_instance)


class GetVal(unittest.TestCase):
    """
    test case for get_val
    """

    @patch("tractor.db.dconf")
    def test_int(self, mock_dconf):
        """
        get an int value
        """
        mock_get_int = Mock()
        mock_dconf.return_value.get_int = mock_get_int
        key = "socks-port"
        db.get_val(key)
        mock_get_int.assert_called_once_with(key)

    @patch("tractor.db.dconf")
    def test_string(self, mock_dconf):
        """
        get a string value
        """
        mock_get_string = Mock()
        mock_dconf.return_value.get_string = mock_get_string
        key = "exit-node"
        db.get_val(key)
        mock_get_string.assert_called_once_with(key)

    @patch("tractor.db.dconf")
    def test_boolean(self, mock_dconf):
        """
        get a boolean value
        """
        mock_get_boolean = Mock()
        mock_dconf.return_value.get_boolean = mock_get_boolean
        key = "accept-connection"
        db.get_val(key)
        mock_get_boolean.assert_called_once_with(key)

    @patch("tractor.db.dconf")
    def test_pluggable_transport(self, mock_dconf):
        """
        get pluggable-transport
        """
        mock_get_value = Mock()
        mock_dconf.return_value.get_value = mock_get_value
        mock_get_value.return_value = [1, 2, 3]
        mock_get_string = Mock()
        mock_dconf.return_value.get_string = mock_get_string
        mock_get_string.return_value = "vanilla"
        key = "pluggable-transport"
        result = db.get_val(key)
        mock_get_value.assert_called_once_with(key)
        mock_get_string.assert_called_once_with("bridge-type")
        self.assertEqual(result, 2)

    def test_invalid(self):
        """
        get invalid key
        """
        with self.assertRaises(TypeError):
            try:
                db.get_val("pi")
            except (FileNotFoundError, TypeError):
                with patch("tractor.db.dconf"):
                    db.get_val("pi")


class SetVal(unittest.TestCase):
    """
    test case for set_val
    """

    @patch("tractor.db.dconf")
    def test_int(self, mock_dconf):
        """
        set an int value
        """
        mock_set_int = Mock()
        mock_dconf.return_value.set_int = mock_set_int
        key = "http-port"
        value = 9080
        db.set_val(key, value)
        mock_set_int.assert_called_once_with(key, value)

    @patch("tractor.db.dconf")
    def test_string(self, mock_dconf):
        """
        set a string value
        """
        mock_set_string = Mock()
        mock_dconf.return_value.set_string = mock_set_string
        key = "exit-node"
        value = "ww"
        db.set_val(key, value)
        mock_set_string.assert_called_once_with(key, value)

    @patch("tractor.db.dconf")
    def test_boolean(self, mock_dconf):
        """
        set a boolean value
        """
        mock_set_boolean = Mock()
        mock_dconf.return_value.set_boolean = mock_set_boolean
        key = "accept-connection"
        value = True
        db.set_val(key, value)
        mock_set_boolean.assert_called_once_with(key, value)

    @patch("tractor.db.get_val", return_value="vanilla")
    @patch("tractor.db.dconf")
    def test_pluggable_transport(self, mock_dconf, *_):
        """
        set pluggable transport
        """
        mock_set_value = Mock()
        mock_dconf.return_value.set_value = mock_set_value
        mock_dconf.return_value.get_value.return_value = (
            "1",
            "2",
            "3",
            "4",
            "5",
        )
        key = "pluggable-transport"
        value = "6"
        db.set_val(key, value)
        mock_set_value.assert_called_once()

    def test_invalid(self):
        """
        set invalid value
        """
        with self.assertRaises(TypeError):
            try:
                db.set_val("pi", 3.14)
            except (FileNotFoundError, TypeError):
                with patch("tractor.db.dconf"):
                    db.set_val("pi", 3.14)


class Reset(unittest.TestCase):
    """
    TestCase for reset
    """

    @patch("tractor.db.dconf")
    def test_reset(self, mock_dconf):
        """
        resetting a key
        """
        mock_reset_method = Mock()
        mock_dconf.return_value.reset = mock_reset_method
        db.reset("socks-port")
        mock_reset_method.assert_called_once_with("socks-port")


class DataDirectory(unittest.TestCase):
    """
    TestCase for get_file
    """

    @patch(
        "gi.repository.GLib.get_user_config_dir", return_value="/path/to/data"
    )
    def test_data_directory(self, *_):
        """
        correct adding of `tractor`
        """
        self.assertEqual(db.data_directory(), "/path/to/data/tractor")
