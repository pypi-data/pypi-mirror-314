#
# Copyright © 2024 Oskar Enoksson <enok@lysator.liu.se> - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license
#
# You should have received a copy of the MIT license with this file.
# See also https://github.com/enok71/adsb/LICENSE
#
"""
ADSB checksum function
"""

from typing import Union

CRC_GENERATOR = 0x1FFF409

def crc(m: Union[int, bytes]) -> int:
    """ Compute ADSB message checksum (88 data bits + 24 checksum bits)
    :param m: Message as bytes or int
    :return: 24-bit checksum of message, should be 0 for an uncorrupted 112 bit message
    """
    if isinstance(m, bytes):
        m = int.from_bytes(m, 'big', signed=False)
    for i in range(0, 88): # 112 bits - 88 data bits and 24 parity bits
        if m & 1:
            m ^= CRC_GENERATOR
        m >>= 1
    return m # last 24 bits of result
