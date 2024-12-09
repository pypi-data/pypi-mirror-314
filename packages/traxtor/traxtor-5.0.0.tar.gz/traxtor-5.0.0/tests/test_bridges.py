# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2024.
"""
Unit tests for bridges
"""

import unittest
from unittest.mock import patch
from tractor import bridges


class GetSampleBridges(unittest.TestCase):
    """
    Testcase for get_sample_bridges
    """

    def test_get_sample_bridges(self):
        """
        Test get_sample_bridges
        """
        result = bridges.get_sample_bridges()
        self.assertTrue(result.endswith("/SampleBridges"))


class CopySampleBridges(unittest.TestCase):
    """
    Testcase for copy_sample_bridges
    """

    @patch("shutil.copyfile")
    def test_copy_done(self, mock_copyfile):
        """
        Test copy_sample_bridges
        """
        with patch(
            "tractor.bridges.get_sample_bridges",
            return_value="/path/to/module/SampleBridges",
        ):
            bridges.copy_sample_bridges("/path/to/destination")
        mock_copyfile.assert_called_once_with(
            "/path/to/module/SampleBridges",
            "/path/to/destination",
        )

    @patch("shutil.copyfile", side_effect=Exception("Simulated copy error"))
    def test_copy_failed(self, mock_copyfile):
        """
        When copy fails
        """
        with patch(
            "tractor.bridges.get_sample_bridges",
            return_value="/path/to/module/SampleBridges",
        ):
            with self.assertRaises(IOError):
                bridges.copy_sample_bridges("/path/to/destination")
        mock_copyfile.assert_called_once_with(
            "/path/to/module/SampleBridges",
            "/path/to/destination",
        )


class GetFile(unittest.TestCase):
    """
    TestCase for get_file
    """

    @patch("tractor.db.data_directory", return_value="/path/to/data")
    @patch("os.makedirs")
    @patch("os.path.isfile", return_value=False)
    @patch("tractor.bridges.copy_sample_bridges")
    def test_file_doesnt_exists(self, mock_copy, *_):
        """
        bridge file does not exist
        """
        self.assertEqual(bridges.get_file(), "/path/to/data/Bridges")
        mock_copy.assert_called_once_with("/path/to/data/Bridges")


class RelevantLines(unittest.TestCase):
    """
    Main class for testing bridges
    """

    def setUp(self):
        """
        initialize class
        """
        super().setUp()
        self.lines = (
            "obfs4 162.223.88.72:43565 "
            "FADC7451A08A3B9690E38137C440C209E6683409 "
            "cert=DYku/2U6MZXDSoE9fiLmgdldLbaPjhAjdxMWPMU0Of4BL54a1cT6QDQv8V1"
            "H3onvlG80SQ iat-mode=2\n"
            "obfs4 81.169.154.212:8181 "
            "C13FE89EC22ED9DC26BC4EA40740C0DEEDC4B0D9 "
            "cert=GT7NbRmPO+2ieNlAlbhp+VFG2lHnY2ABGXAF+eaSlcw3P/v4Gpc5gjexjcm"
            "x5/sI+XWFXA iat-mode=0\n"
            "188.121.110.127:9056 F3D627AFD9EB5E1B8843733B06EBC2D3B6BAB209\n"
            "209\n"
            "snowflake 82.36.31.1:1 4D6FEC29302160C16E03A3FDBA6FD0983CCF6D60\n"
            "webtunnel [2001:db8:9971:e9c7:2b64:916b:17f8:7775]:443 "
            "2F104EE04E1224CAFF6B8DFC62F83550CA2958DC "
            "url=https://learnstack.xyz/tohG1pieHieJ0eit43k ver=0.0.1\n"
        )

    def test_vanilla(self):
        """
        test vanilla bridge
        """
        expected = [
            "188.121.110.127:9056 F3D627AFD9EB5E1B8843733B06EBC2D3B6BAB209",
        ]
        self.assertEqual(
            bridges.relevant_lines(self.lines, "vanilla"), expected
        )

    def test_obfs(self):
        """
        test obfs4 bridge
        """
        expected = [
            "obfs4 162.223.88.72:43565 "
            "FADC7451A08A3B9690E38137C440C209E6683409 "
            "cert=DYku/2U6MZXDSoE9fiLmgdldLbaPjhAjdxMWPMU0Of4BL54a1cT6QDQv8V1"
            "H3onvlG80SQ iat-mode=2",
            "obfs4 81.169.154.212:8181 "
            "C13FE89EC22ED9DC26BC4EA40740C0DEEDC4B0D9 "
            "cert=GT7NbRmPO+2ieNlAlbhp+VFG2lHnY2ABGXAF+eaSlcw3P/v4Gpc5gjexjcm"
            "x5/sI+XWFXA iat-mode=0",
        ]
        self.assertEqual(bridges.relevant_lines(self.lines, "obfs4"), expected)

    def test_snowflake(self):
        """
        test snowflake bridge
        """
        expected = [
            "snowflake 82.36.31.1:1 4D6FEC29302160C16E03A3FDBA6FD0983CCF6D60"
        ]
        self.assertEqual(
            bridges.relevant_lines(self.lines, "snowflake"), expected
        )

    def test_webtunnel(self):
        """
        test webtunnel bridge
        """
        expected = [
            "webtunnel [2001:db8:9971:e9c7:2b64:916b:17f8:7775]:443 "
            "2F104EE04E1224CAFF6B8DFC62F83550CA2958DC "
            "url=https://learnstack.xyz/tohG1pieHieJ0eit43k ver=0.0.1"
        ]
        self.assertEqual(
            bridges.relevant_lines(self.lines, "webtunnel"), expected
        )


class CreateEmoji(unittest.TestCase):
    """
    TestCase for creating emojis from bridge lines
    """

    def test_create_emoji(self):
        """
        test the function
        """
        line = "82.65.123.107:9001 5105C5FD49A1A8DEF6CD754F7657BDA13BA2A3FE"
        self.assertEqual(bridges.create_emoji(line), ["⏰", "🚚", "🎡", "🦌"])
