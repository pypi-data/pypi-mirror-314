#
# Copyright © 2024 Oskar Enoksson <enok@lysator.liu.se> - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license
#
# You should have received a copy of the MIT license with this file.
# See also https://github.com/enok71/adsb/LICENSE
#
"""
Contains ADSB message and data classes
"""

import time

from .adsb import AircraftOperationStatus, AirborneVelocities, AirbornePosition, Adsb

class Vehicle:
    def __init__(self, icao):
        self.ver = 0
        self.last_position = None
        self.lat = None
        self.lon = None
        self.speed = None
        self.heading = None
        self.icao = icao
        self.last_seen = time.time()

    def process(self, adsb):
        if adsb.icao != self.icao:
            return False
        self.last_seen = time.time()
        if isinstance(adsb.data, AircraftOperationStatus):
            self.ver = adsb.data.ver
        if isinstance(adsb.data, AirborneVelocities):
            self.speed = adsb.data.speed()
            self.heading = adsb.data.heading()
        if isinstance(adsb.data, AirbornePosition):
            adsb.data.prev = self.last_position
            lat, lon = adsb.data.position()
            self.last_position = adsb.data
            if lat is not None and lon is not None:
                self.lat, self.lon = lat, lon

    def __str__(self):
        lat, lon = self.lat, self.lon
        if lat is not None:
            lat = f'{self.lat:2.6f}'
        if lon is not None:
            lon = f'{self.lon:2.6f}'
        speed, heading = self.speed, self.heading
        if speed is not None:
            speed = f'{speed:.2f}'
        if heading is not None:
            heading = f'{heading:.2f}'
        return f'icao={self.icao}: lat={lat} lon={lon} speed={speed} heading={heading}'

class Tracker:
    def __init__(self):
        self.vehicles = {}

    def process(self, adsb):
        if not adsb.icao in self.vehicles:
            vehicle = Vehicle(adsb.icao)
            self.vehicles[adsb.icao] = vehicle
        else:
            vehicle = self.vehicles[adsb.icao]
        vehicle.process(adsb)

def test():
    msgs = [
        b'\x8D\x48\x40\xD6\x20\x2C\xC3\x71\xC3\x2C\xE0\x57\x60\x98',
        0x8D40621D58C382D690C8AC2863A7,
        0x8D40621D58C386435CC412692AD6,
        0x8D40621D58C382D690C8AC2863A7,
        0x8D485020994409940838175B284F,
        0x8DA05F219B06B6AF189400CBC33F,
    ]
    tracker = Tracker()
    for msg in msgs:
        if isinstance(msg, int):
            msg = msg.to_bytes(14, 'big')
        m = Adsb.parse(msg)
        tracker.process(m)

if __name__ == '__main__':
    test()
