#
# Copyright © 2024 Oskar Enoksson <enok@lysator.liu.se> - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license
#
# You should have received a copy of the MIT license with this file.
# See also https://github.com/enok71/adsb/LICENSE
#
"""
Some helper classes unrelated to ADSB
"""

class ContainerDict(dict):
    """Dictionary where keys may be containers
    More specifically the underlying dict can have keys which supports
    the `in` operator on the actual key type.
    E.g.
    d = ContainerDict({1: 'one',
                       2: 'two',
                       range(3,10), 'others'
                       (20, 30, 40), 'few more'
                       }, default='not here')
    Beware that if multiple containers contain a key then the first matching
    container's value will be returned by __getitem__ for that key, and which
    one is "first" is unpredictable.

    There is also an optional "default" attribute returned if no match is found.
    """
    def __init__(self, items, default=None):
        self.default = default
        super().__init__(items)

    def __getitem__(self, key):
        """Return matching value for a key (just like ordinary dict)
        If no match found search all keys for one matching with the `in` operator
        If no match is still found and `default` argument was given on creation, return
        the default value.
        """
        try:
            return dict.__getitem__(self, key)
        except KeyError as e:
            err = e  # Save for later.
        for k, value in self.items():
            try:
                if key in k:
                    return value
            except TypeError:
                pass
        return err

    def __contains__(self, key):
        if key in self.__dict__:
            return True
        for k, value in self.__dict__.items():
            try:
                if key in k:
                    return True
            except TypeError:
                pass
        return False
