# adsb
ADSB and Mode-S decoder/encoder

The `Adsb` class provides `parse` and `encode` functions for creating `Adsb` objects from a bytes object, and encoding an object to bytes respectively.

The `Tracker` class implements a simple aircraft tracker that detects vehicles and collects and updates information about them. The `Tracker` class is meant primarily as an example application.

<b>Example</b>: decoding messages given either as `bytes` or `int`:
```
from adsb import Adsb

print(Adsb.parse(0x8D40621D58C382D690C8AC2863A7))
print(Adsb.parse(b'\x8D\x48\x40\xD6\x20\x2C\xC3\x71\xC3\x2C\xE0\x57\x60\x98')
```

<b>Example</b>: tracking aircrafts:
```
from adsb import Tracker

tracker = Tracker()
for msg in readline():
    m = Adsb.parse(msg.strip().encode())
    tracker.process(m)
```

