# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2020-2024.

"""
module to manages bridges
"""

import os
import re
import shutil

from . import db


def get_sample_bridges() -> str:
    """
    there should be some sample bridges in the package
    """
    return os.path.dirname(os.path.abspath(__file__)) + "/SampleBridges"


def copy_sample_bridges(bridges_file) -> None:
    """
    function to copy sample bridges for tractor
    """
    sample_bridges_file = get_sample_bridges()
    try:
        shutil.copyfile(sample_bridges_file, bridges_file)
    except Exception as exception:
        raise IOError from exception


def get_file() -> str:
    """
    get bridges file address
    """
    data_dir = db.data_directory()
    os.makedirs(data_dir, mode=0o700, exist_ok=True)
    bridges_file = data_dir + "/Bridges"
    if not os.path.isfile(bridges_file):
        copy_sample_bridges(bridges_file)
    return bridges_file


def relevant_lines(my_bridges: str, bridge_type: str) -> list:
    """
    return the relevant bridge lines from bridge list
    """
    obfs_transports = [
        "meek_lite",
        "obfs2",
        "obfs3",
        "obfs4",
        "scramblesuit",
        "webtunnel",
    ]
    transports = obfs_transports if bridge_type == "obfs4" else [bridge_type]
    matches = [
        bridge
        for bridge in my_bridges.split("\n")
        if parse_bridge_line(bridge)["transport"] in transports
    ]
    return matches


def parse_bridge_line(line: str):
    """
    return a dict of transport, addr, id and args for a bridge line
    """
    if not line:
        return {"transport": None}
    pattern = re.compile(
        r"""
        (?:(?P<transport>\S+)\s+)?
        (?P<addr>[0-9a-fA-F\.\[\]\:]+:\d{1,5})
        (?:\s+(?P<id>[0-9a-fA-F]{40}))?
        (?:\s+(?P<args>.+))?
        """,
        re.VERBOSE,
    )
    match = re.match(pattern, line)
    if not match:
        return {"transport": None}
    bridge = match.groupdict()
    if "transport" not in bridge or not bridge["transport"]:
        bridge["transport"] = "vanilla"
    return bridge


def create_emoji(bridge_line: str) -> list:
    """
    Create FNV-1a hash for the given address and map it to the emoji list.
    """
    emoji_list = [
        "👽️",
        "🤖",
        "🧠",
        "👁️",
        "🧙",
        "🧚",
        "🧜",
        "🐵",
        "🦧",
        "🐶",
        "🐺",
        "🦊",
        "🦝",
        "🐱",
        "🦁",
        "🐯",
        "🐴",
        "🦄",
        "🦓",
        "🦌",
        "🐮",
        "🐷",
        "🐗",
        "🐪",
        "🦙",
        "🦒",
        "🐘",
        "🦣",
        "🦏",
        "🐭",
        "🐰",
        "🐿️",
        "🦔",
        "🦇",
        "🐻",
        "🐨",
        "🦥",
        "🦦",
        "🦘",
        "🐥",
        "🐦️",
        "🕊️",
        "🦆",
        "🦉",
        "🦤",
        "🪶",
        "🦩",
        "🦚",
        "🦜",
        "🐊",
        "🐢",
        "🦎",
        "🐍",
        "🐲",
        "🦕",
        "🐳",
        "🐬",
        "🦭",
        "🐟️",
        "🐠",
        "🦈",
        "🐙",
        "🐚",
        "🐌",
        "🦋",
        "🐛",
        "🐝",
        "🐞",
        "💐",
        "🌹",
        "🌺",
        "🌻",
        "🌷",
        "🌲",
        "🌳",
        "🌴",
        "🌵",
        "🌿",
        "🍁",
        "🍇",
        "🍈",
        "🍉",
        "🍊",
        "🍋",
        "🍌",
        "🍍",
        "🥭",
        "🍏",
        "🍐",
        "🍑",
        "🍒",
        "🍓",
        "🫐",
        "🥝",
        "🍅",
        "🫒",
        "🥥",
        "🥑",
        "🍆",
        "🥕",
        "🌽",
        "🌶️",
        "🥬",
        "🥦",
        "🧅",
        "🍄",
        "🥜",
        "🥐",
        "🥖",
        "🥨",
        "🥯",
        "🥞",
        "🧇",
        "🍔",
        "🍕",
        "🌭",
        "🌮",
        "🍿",
        "🦀",
        "🦞",
        "🍨",
        "🍩",
        "🍪",
        "🎂",
        "🧁",
        "🍫",
        "🍬",
        "🍭",
        "🫖",
        "🧃",
        "🧉",
        "🧭",
        "🏔️",
        "🌋",
        "🏕️",
        "🏝️",
        "🏡",
        "⛲️",
        "🎠",
        "🎡",
        "🎢",
        "💈",
        "🚆",
        "🚋",
        "🚍️",
        "🚕",
        "🚗",
        "🚚",
        "🚜",
        "🛵",
        "🛺",
        "🛴",
        "🛹",
        "🛼",
        "⚓️",
        "⛵️",
        "🛶",
        "🚤",
        "🚢",
        "✈️",
        "🚁",
        "🚠",
        "🛰️",
        "🚀",
        "🛸",
        "⏰",
        "🌙",
        "🌡️",
        "☀️",
        "🪐",
        "🌟",
        "🌀",
        "🌈",
        "☂️",
        "❄️",
        "☄️",
        "🔥",
        "💧",
        "🌊",
        "🎃",
        "✨",
        "🎈",
        "🎉",
        "🎏",
        "🎀",
        "🎁",
        "🎟️",
        "🏆️",
        "⚽️",
        "🏀",
        "🏈",
        "🎾",
        "🥏",
        "🏓",
        "🏸",
        "🤿",
        "🥌",
        "🎯",
        "🪀",
        "🪁",
        "🔮",
        "🎲",
        "🧩",
        "🎨",
        "🧵",
        "👕",
        "🧦",
        "👗",
        "🩳",
        "🎒",
        "👟",
        "👑",
        "🧢",
        "💄",
        "💍",
        "💎",
        "📢",
        "🎶",
        "🎙️",
        "📻️",
        "🎷",
        "🪗",
        "🎸",
        "🎺",
        "🎻",
        "🪕",
        "🥁",
        "☎️",
        "🔋",
        "💿️",
        "🧮",
        "🎬️",
        "💡",
        "🔦",
        "🏮",
        "📕",
        "🏷️",
        "💳️",
        "✏️",
        "🖌️",
        "🖍️",
        "📌",
        "📎",
        "🔑",
        "🪃",
        "🏹",
        "⚖️",
        "🧲",
        "🧪",
        "🧬",
        "🔬",
        "🔭",
        "📡",
        "🪑",
        "🧹",
        "🗿",
    ]
    prime = 0x01000193
    offset = 0x811C9DC5
    hash_value = offset
    # Calculate FNV-1a hash of the bridge_line
    for byte in bridge_line.encode("utf-8"):
        hash_value = (hash_value ^ byte) * prime
        hash_value %= 2**32  # Get the last 32-bit of the integer
    # Map every 4 bytes of the hash to emojis
    hash_bytes = hash_value.to_bytes(length=4, byteorder="big")
    return [emoji_list[hash_bytes[i] % len(emoji_list)] for i in range(4)]
