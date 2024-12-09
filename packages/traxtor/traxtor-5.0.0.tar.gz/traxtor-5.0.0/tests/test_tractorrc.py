# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2024.
"""
unit tests for tractorrc
"""

import unittest
from unittest.mock import patch
from tractor import tractorrc


class GetExitLines(unittest.TestCase):
    """
    test case for _get_exit_lines
    """

    @patch("tractor.db.get_val", return_value="ww")
    def test_auto(self, *_):
        """
        auto exit node
        """
        self.assertEqual(tractorrc._get_exit_lines(), "")

    @patch("tractor.db.get_val", return_value="us")
    def test_us(self, *_):
        """
        specific exit node
        """
        self.assertEqual(
            tractorrc._get_exit_lines(), "ExitNodes {us}\nStrictNodes 1\n"
        )


class FillBridgeLines(unittest.TestCase):
    """
    test case for _fill_bridge_lines
    """

    @patch("tractor.db.get_val", return_value="obfs4proxy")
    def test_obfs(self, *_):
        """
        obfs lines
        """
        self.assertEqual(
            tractorrc._fill_bridge_lines("obfs4", ["line1", "line2"]),
            "UseBridges 1\n"
            + "ClientTransportPlugin obfs4 exec obfs4proxy\n"
            + "Bridge line1\n"
            + "Bridge line2\n",
        )

    @patch("tractor.db.get_val", return_value="snowflake")
    def test_snowflake(self, *_):
        """
        obfs lines
        """
        self.assertEqual(
            tractorrc._fill_bridge_lines("snowflake", ["line1", "line2"]),
            "UseBridges 1\n"
            + "ClientTransportPlugin snowflake exec snowflake "
            + "-url https://snowflake-broker.torproject.net.global.prod."
            + "fastly.net/ -front foursquare.com -ice "
            + "stun:stun.l.google.com:19302,stun:stun.antisip.com:3478,"
            + "stun:stun.bluesip.net:3478,stun:stun.dus.net:3478,"
            + "stun:stun.epygi.com:3478,stun:stun.sonetel.net:3478,"
            + "stun:stun.uls.co.za:3478,stun:stun.voipgate.com:3478,"
            + "stun:stun.voys.nl:3478\n"
            + "Bridge line1\n"
            + "Bridge line2\n",
        )

    def test_bad_type(self, *_):
        """
        bad bridge typr
        """
        with self.assertRaises(ValueError):
            tractorrc._fill_bridge_lines(0, "line")


class GetBridgeLines(unittest.TestCase):
    """
    test case for _get_bridge_lines
    """

    @patch("tractor.db.get_val", return_value=2)
    @patch("tractor.bridges.relevant_lines", return_value=None)
    def test_no_bridge(self, *_):
        """
        No relevant bridges found
        """
        with self.assertRaises(EnvironmentError):
            tractorrc._get_bridge_lines()


class Create(unittest.TestCase):
    """
    test case for create
    """

    @patch("tractor.db.get_val", return_value="none")
    def test_local(self, *_):
        """
        local connection
        """
        tmpdir, path = tractorrc.create()
        self.assertTrue(tmpdir.startswith("/tmp/"))
        self.assertTrue(path.endswith("/tractorrc"))

    @patch("tractor.tractorrc._get_bridge_lines", return_value=None)
    @patch("tractor.bridges.relevant_lines", return_value=None)
    @patch("tractor.db.get_val", return_value=True)
    def test_network(self, *_):
        """
        listen on network
        """
        tmpdir, path = tractorrc.create()
        self.assertTrue(tmpdir.startswith("/tmp/"))
        self.assertTrue(path.endswith("/tractorrc"))
