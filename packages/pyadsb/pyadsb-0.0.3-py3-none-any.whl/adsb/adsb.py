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

from typing import Optional
import math

from .helpers import ContainerDict
from .crc import crc as adsb_crc

class AdsbData:
    """Base class for all ADSB data classes"""
    def __init__(self, tc: int):
        """:param tc: Type Code"""
        self.tc = tc

    def encode(self) -> bytes:
        raise NotImplementedError()

class AircraftId(AdsbData):
    def __init__(self, tc: int, ec: int, callsign: str):
        super().__init__(tc)
        self.ec = ec
        self.callsign = callsign

    def __str__(self):
        return f'{self.__class__.__name__}(tc={self.tc}, ec={self.ec}, callsign="{self.callsign}")'

    def encode(self):
        return bytes(())

    @staticmethod
    def parse(data: bytes):
        """Parse data as AircraftId data
        :param data: data bytes
        :return: AircraftId object, or None if parsing fails
        """
        tc = data[0] >> 3
        if not tc in range(1, 5):
            return None
        ec = data[0] & 0x7
        cs_int = int.from_bytes(data[1:], 'big', signed=False)
        cs_list = []
        for n in range(0, 8):
            c = cs_int & 0x3f
            cs_int >>= 6
            if c in range(1, 27):
                cs_list.append(65+c)
            elif c in range (48, 58):
                cs_list.append(c)
            elif c == 32:
                cs_list.append(95)
            else:
                cs_list.append(35)
        cs = bytes(cs_list).decode('ascii')
        return AircraftId(tc, ec, cs)

class SurfacePosition(AdsbData):
    def __init__(self, data: bytes):
        super().__init__(data[0] >> 3)
        raise NotImplementedError()

    def __str__(self):
        return f'{self.__class__.__name__}(tc={self.tc})'

    def encode(self):
        raise NotImplementedError()

    @staticmethod
    def parse(data: bytes):
        """Parse data as SurfacePosition data
        :param data: data bytes
        :return: SurfacePosition object, or None if parsing fails
        """
        raise NotImplementedError()

class AirbornePosition(AdsbData):
    def __init__(self, tc, ss, saf, alt, t, f, lat, lon):
        assert tc in range(9, 19) or tc in range(20, 23), f'tc={tc} not in [9..18] or [20..22]'
        super().__init__(tc)
        self.ss = ss
        self.saf = saf
        self.alt = alt
        self.t = t  # Timestamp
        self.f = f  # 1 = odd, 0 = even
        self.lat = lat  # CPR encoded lat
        self.lon = lon  # CPR encoded lon
        self.prev = None  # Previous AirbornePosition message, if any

    NZ = 15

    @classmethod
    def nl(cls, lat):
        from math import pi, acos, cos, floor
        return floor(2*pi/acos(1-(1-cos(pi/(2*cls.NZ)))/cos(pi/180*lat)**2))

    def position(self, last_position=None):
        if not last_position:
            last_position = self.prev
        if not last_position:
            return None, None  # No previous message available
        if self.f + last_position.f != 1:
            return None, None  # Must have one even and one odd position
        if self.f:
            odd = self
            even = last_position
        else:
            odd = last_position
            even = self

        dlat_even = 360./(4*self.NZ)
        dlat_odd = 360./(4*self.NZ-1)
        lat_even = even.lat/2**17
        lon_even = even.lon/2**17
        lat_odd = odd.lat/2**17
        lon_odd = odd.lon/2**17

        from math import floor
        j = floor(59*lat_even - 60*lat_odd + .5)

        lat_even = dlat_even*(j%60 + lat_even)
        if lat_even >= 270:
            lat_even = lat_even - 360
        lat_odd = dlat_odd*(j%60 + lat_odd)
        if lat_odd >= 270:
            lat_odd = lat_odd - 360

        nl = self.nl(lat_even)
        if nl != self.nl(lat_odd):
            return None, None  # Different zones. Not possible to compute lon

        lat = lat_even if even.t >= odd.t else lat_odd
        m = floor(lon_even*(nl - 1) - lon_odd*nl + .5)
        n_even = max(self.nl(lat), 1)
        n_odd = max(self.nl(lat-1), 1)
        dlon_even = 360./n_even
        dlon_odd = 360./n_odd
        lon_even = dlon_even*(m%n_even + lon_even)
        lon_odd = dlon_odd*(m%n_odd + lon_odd)
        lon = lon_even if even.t >= odd.t else lon_odd
        if lon >= 180:
            lon -= 360

        return lat, lon

    def altitude(self) -> Optional[float]:
        """Return altitude in ft"""
        if self.alt == 0:
            return None  # No information available
        alt = self.alt & 0xf | (self.alt >> 1) & 0xff0
        if self.alt & 0x10:
            return alt * 25 - 1000
        else:
            return alt * 100 - 1000

    def __str__(self):
        s = f'{self.__class__.__name__}('
        if self.tc in range(9, 19):
            s += 'Baro alt'
        else:
            s += 'GNSS alt'
        s += f', ss={self.ss}, saf={self.saf}, alt={self.alt}({self.altitude()}ft), t={self.t}, f={self.f}, lat={self.lat}, lon={self.lon})'
        lat, lon = self.position()
        s += f'(lat={lat}, lon={lon})'
        return s+')'

    def encode(self):
        raise NotImplementedError()

    @staticmethod
    def parse(data: bytes):
        """Parse data as AirbornePosition data
        :param data: data bytes
        :return: AirbornePosition object, or None if parsing fails
        """
        tc = data[0] >> 3
        if not (tc in range(9, 19) or tc in range(20, 23)):
            return None
        ss = (data[0] >> 1) & 3
        saf = data[0] & 1
        alt = (data[1] << 4) | (data[2] >> 4)
        t = (data[2] >> 3) & 1
        f = (data[2] >> 2) & 1
        lat = ((data[2] & 3) << 15) | (data[3] << 7) | (data[4] >> 1)
        lon = (data[4] & 1) << 16 | (data[5] << 8) | data[6]
        return AirbornePosition(tc, ss, saf, alt, t, f, lat, lon)

class AirborneVelocities(AdsbData):
    def __init__(self, tc, st, ic, ifr, vrsrc, svr, vr, sdif, dalt, nuc,
                 dew=None, vew=None, dns=None, vns=None,
                 sh=None, hdg=None, t=None, as_=None):
        assert tc == 19, f'tc={tc} != 19'
        super().__init__(tc)
        self.st = st
        self.ic = ic
        self.ifr = ifr
        self.nuc = nuc
        self.vrsrc = vrsrc
        self.svr = svr
        self.vr = vr
        self.sdif = sdif
        self.dalt = dalt
        self.dew = dew
        self.vew = vew
        self.dns = dns
        self.vns = vns
        self.sh = sh
        self.hdg = hdg
        self.t = t
        self.as_ = as_

    def speed(self) -> Optional[float]:
        """Return speed in knots, or None if not available"""
        if self.st in {1, 2}:
            if self.vew == 0 or self.vns == 0:
                return None  # No information available
            vew = self.vew - 1.
            vns = self.vns - 1.
            spd = math.sqrt(vew ** 2 + vns ** 2)
            if self.st == 2:
                spd *= 4
            return spd
        if self.st in {3, 4}:
            if self.as_ == 0:
                return None  # No information available
            if self.st == 3:
                return self.as_ - 1.
            if self.st == 4:
                return 4*(self.as_ - 1.)

    def heading(self):
        """Return direction in deg, or None if not available"""
        if self.st in {1, 2}:
            if self.vew == 0 or self.vns == 0:
                return None  # No information available
            vew = (self.vew -1) * -1**self.dew
            vns = (self.vns -1) * -1**self.dns
            return (math.degrees(math.atan2(vew, vns)) +360) %360.
        if self.st in {3, 4}:
            if self.sh == 0:
                return None  # No information available
            return self.hdg * 360/1024.

    def altitude_rate(self):
        """Return altitude rate in knots, or None if not available"""
        if self.vr == 0:
            return None  # No info available
        return (self.vr - 1)*64*-1**self.svr

    def __str__(self):
        s = f'{self.__class__.__name__}(st={self.st}, ic={self.ic}, ifr={self.ifr}'
        s += f', nuc={self.nuc}, vrsrc={self.vrsrc}, svr={self.svr}, vr={self.vr}, sdif={self.sdif}, dalt={self.dalt}'
        if self.st in {1, 2}:
            s += f', dew={self.dew}, vew={self.vew}, dns={self.dns}, vns={self.vns}'
        if self.st in {3, 4}:
            s += f', sh={self.sh}, hdg={self.hdg}, t={self.t}, as={self.as_}'
        s += f'(speed={self.speed()}kn, heading={self.heading()}deg)'
        return s + ')'

    def encode(self):
        raise NotImplementedError()

    @staticmethod
    def parse(data: bytes):
        """Parse data as AirborneVelocities data
        :param data: data bytes
        :return: AirborneVelocities object, or None if parsing fails
        """
        tc = data[0] >> 3
        if tc != 19:
            return None
        st = data[0] & 0x3
        if st not in range(1, 5):
            return None
        ic = (data[1] >> 7)
        ifr = (data[1] >> 6) & 1
        nuc = (data[1] >> 3) & 0x7

        vrsrc = (data[4] >> 4) & 1
        svr = (data[4] >> 3) & 1
        vr = ((data[4] & 0x7) << 6) | (data[5] >> 2)
        sdif = data[6] >> 7
        dalt = data[6] & 0x7f

        if st in (1, 2):
            dew = (data[1] >> 2) & 1
            vew = ((data[1] & 0x3) << 8) | data[2]
            dns = (data[3] >> 7) & 1
            vns = ((data[3] & 0x7f) << 3) | ((data[4] >> 5) & 0x7)
            return AirborneVelocities(tc, st, ic, ifr, vrsrc, svr, vr, sdif, dalt, nuc,
                                      dew=dew, vew=vew, dns=dns, vns=vns)
        elif st in (3, 4):
            sh = (data[1] >> 2) & 1
            hdg = ((data[1] & 0x3) << 8) | data[2]
            t = (data[3] >> 7) & 1
            as_ = ((data[3] & 0x7f) << 3) | ((data[4] >> 5) & 0x7)
            return AirborneVelocities(tc, st, ic, ifr, vrsrc, svr, vr, sdif, dalt, nuc,
                                      sh=sh, hdg=hdg, t=t, as_=as_)
        return None

class AircraftStatus(AdsbData):
    def __init__(self, data: bytes):
        super().__init__(data[0] >> 3)
        raise NotImplementedError()

    def __str__(self):
        return f'{self.__class__.__name__}(tc={self.tc})'

    def encode(self):
        raise NotImplementedError()

    @staticmethod
    def parse(data: bytes):
        """Parse data as AircraftStatus data
        :param data: data bytes
        :return: AircraftStatus object, or None if parsing fails
        """
        raise NotImplementedError()


class TargetStateStatus(AdsbData):
    def __init__(self, data: bytes):
        super().__init__(data[0] >> 3)
        raise NotImplementedError()

    def __str__(self):
        return f'{self.__class__.__name__}(tc={self.tc})'

    def encode(self):
        raise NotImplementedError()

    @staticmethod
    def parse(data: bytes):
        """Parse data as TargetStateStatus data
        :param data: data bytes
        :return: TargetStateStatus object, or None if parsing fails
        """
        raise NotImplementedError()


class AircraftOperationStatus(AdsbData):
    ST = {
        0: 'Airborne',
        1: 'Surface',
    }
    def __init__(self, tc, st, cc, om, ver,
                 nica=None, nics=None, nacp=None,
                 baq=None, gva=None, sil=None,
                 hrd=None, sils=None):
        super().__init__(tc)
        self.st = st
        self.cc = cc
        self.om = om
        self.ver = ver
        self.nica = nica
        self.nics = nics
        self.nacp = nacp
        self.baq = baq
        self.gva = gva
        self.sil = sil
        self.hrd = hrd
        self.sils = sils

    def __str__(self):
        base = f'{self.__class__.__name__}(st={self.st}, cc={self.cc}, om={self.om}, ver={self.ver}'
        if self.ver==0:
            return base+')'
        if self.ver==1:
            s = base + f', nics={self.nics}), nacp={self.nacp}'
            if self.st==0:
                s += f', baq={self.baq}'
            s += f', sil={self.sil}, hrd={self.hrd}'
            return s+')'
        if self.ver==2:
            s = base + f', nica={self.nica}), nacp={self.nacp}'
            if self.st==0:
                s += f', gva={self.gva}'
            s += f', sil={self.sil}, hrd={self.hrd}, sils={self.sils}'
            return s+')'

    def encode(self):
        raise NotImplementedError()

    @staticmethod
    def parse(data: bytes):
        """Parse data as AircraftOperationStatus data
        :param data: data bytes
        :return: AircraftOperationStatus object, or None if parsing fails
        """
        tc = data[0] >> 3
        if not tc != 0x31:
            return None
        st = data[0] & 0x7
        assert st in {0, 1}, f'reserved sub-type code {st}'
        ver = data[5] >> 5
        assert ver in {0, 1, 2}, f'reserved ADS-B version number {ver}'
        cc = data[1]>>4, data[1]&0xf, data[2]>>4, data[2]&0xf
        om = data[3]>>4, data[3]&0xf, data[4]>>4, data[4]&0xf
        if ver == 0:
            return AircraftOperationStatus(tc, st=st, cc=cc, om=om, ver=ver)
        if ver==1:
            nics = (data[5] >> 4) & 1
            nacp = data[5] & 0xf
            baq = data[6] >> 6
            if st!=0 and baq!=0:
                raise AssertionError(f'baq={baq}!=0 reserved for st={st}')
            sil = ( data[6] >> 4) & 0x3
            hrd = ( data[6] >> 2) & 1
            return AircraftOperationStatus(tc, st=st, cc=cc, om=om, ver=ver,
                                           nics=nics, nacp=nacp, baq=baq, sil=sil,
                                           hrd=hrd)
        if ver==2:
            nica = (data[5] >> 4) & 1
            nacp = data[5] & 0xf
            gva = data[6] >> 6
            sil = ( data[6] >> 4) & 0x3
            hrd = ( data[6] >> 2) & 1
            sils = ( data[6] >> 1) & 1
            return AircraftOperationStatus(tc, st=st, cc=cc, om=om, ver=ver,
                                           nica=nica, nacp=nacp, gva=gva, sil=sil,
                                           hrd=hrd, sils=sils)

        return Unknown(data)

class Unknown(AdsbData):
    def __init__(self, data: bytes):
        super().__init__(data[0] >> 3)
        self.data = data

    def __str__(self):
        return f'{self.__class__.__name__}(tc={self.tc}, data={self.data.hex()})'

    def encode(self):
        return self.data

    @staticmethod
    def parse(data: bytes):
        """Parse data as Unknown. For unparseable data.
        :param data: data bytes
        :return: Unknown object
        """
        return Unknown(data)

class Adsb:
    """Adsb message class"""
    CA = {  # Capability
        0: 'Level 1 transponder',
        1: 'Reserved (1)',
        2: 'Reserved (2)',
        3: 'Reserved (3)',
        4: 'Level 2+ transponder with ability to set CA to 7, on - ground',
        5: 'Level 2+ transponder with ability to set CA to 7, airborne',
        6: 'Level 2+ transponder with ability to set CA to 7',
        7: 'Signifies the Downlink Request value is 0, or the Flight Status is 2, 3, 4, or 5'
    }

    TC = ContainerDict({  # Type codes.
        range(1, 5): AircraftId,
        range(5, 9): SurfacePosition,
        range(9, 19): AirbornePosition,
        19: AirborneVelocities,
        range(20, 23): AirbornePosition,
        28: AircraftStatus,
        29: TargetStateStatus,
        31: AircraftOperationStatus,
    }, default=Unknown)

    DF = 17  # Downlink Format. 17 is the DF value for all ADS-B messages.

    def __init__(self, ca: int, icao: int, data: AdsbData):
        """Create object from attributes
        :param ca: Transporter Capability
        :param icao: ICAO Aircraft Address
        :param data: Message, extended squitter, decoded into AdsbData subclass
        """
        self.ca = ca
        self.icao = icao
        self.data = data

    def __str__(self):
        if isinstance(self.data, bytes):
            datastr = self.data.hex()
        else:
            datastr = str(self.data)
        return f'ads-b(ca="{Adsb.CA[self.ca]}", icao={self.icao:06x}, data={datastr})'

    def encode(self) -> bytes:
        """Assemble a message
        :return: message as 112-bit bytes
        """
        data = self.data.encode()
        msg = bytes(((self.DF<<3) | self.ca,)) + self.icao.to_bytes(3, 'big') + data
        crc = adsb_crc(msg)
        return msg + crc.to_bytes(3, 'big')

    @staticmethod
    def parse(msg) -> Optional['Adsb']:
        """Parse ADSB message from 112-bit bytes.
        :param msg: message bytes (112 bits)
        :return: Adsb object, or None if parsing fails
        """
        if adsb_crc(msg):
            return None  # Bad CRC
        df = msg[0] >> 3
        if df != Adsb.DF:
            return None  # Not an ADS-B message
        ca = msg[0] & 0x7
        icao = int.from_bytes(msg[1:4], byteorder='big', signed=False)
        data = msg[4:]
        tc = data[0] >> 3
        data_cls = Adsb.TC[tc]
        try:
            data_obj = data_cls.parse(data)
            if data_obj is None:
                data_obj = Unknown.parse(data)
        except NotImplementedError:
            data_obj = Unknown.parse(data)
        return Adsb(ca, icao, data_obj)
