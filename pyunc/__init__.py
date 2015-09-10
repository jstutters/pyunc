import os
import re
import struct
import sys
import numpy as np

MAXMIN = 0
HISTO = 1
TITLE = 2
PIXEL_FORMAT = 3
DIMC = 4
DIMV = 5
PIXELS = 6
INFO = 7
VERSION = 8

SIZES = {
    'title': 81,
    'validmaxmin': 4,
    'maxmin': 8,
    'validhistogram': 4,
    'histogram': 4096,
    'pixelformat': 4,
    'dimc': 4,
    'dimv': 40,
}

PIXEL_FMTS = {
    0o0010: 'GREY',
    0o0020: 'COLOR',
    0o0040: 'COLORPACKED',
    0o0200: 'USERPACKED',
    0o0001: 'BYTE',
    0o0002: 'SHORT',
    0o0003: 'LONG',
    0o0004: 'REAL',
    0o0005: 'COMPLEX'
}


class REMatcher(object):
    def __init__(self, match_string):
        self.match_string = match_string

    def match(self, regexp):
        self.rematch = re.match(regexp, self.match_string)
        return bool(self.rematch)

    def group(self, i):
        return self.rematch.group(i)


class UNCHeader(object):
    def __init__(self, info):
        infoarr = info.split('\n')
        for l in infoarr:
            print(l)
            m = REMatcher(l)
            if m.match(r'Patient_Birth_Date=(\w+)\s(\d+),\s(\d+)'):
                self.birth_year = m.group(3)


class UNCFile(object):
    def __init__(self, f):
        self.read_addresses(f)
        self.read_title(f)
        self.read_maxmin(f)
        self.read_histogram(f)
        self.read_pixel_format(f)
        self.read_dimc(f)
        self.read_dimv(f)
        self.calculate_pixel_count()
        self.read_info(f)
        self.read_pixels(f)
        self.header = UNCHeader(self.info)

    @classmethod
    def from_path(cls, path):
        with open(path, 'rb') as f:
            instance = cls(f)
        return instance

    def read_addresses(self, f):
        f.seek(0, os.SEEK_SET)
        self.addresses = struct.unpack('>9i', f.read(36))

    def read_title(self, f):
        f.seek(self.addresses[TITLE], os.SEEK_SET)
        title_field = struct.unpack('>81s', f.read(SIZES['title']))[0].decode('ascii')
        self.title = title_field.split('\0', 1)[0]

    def read_maxmin(self, f):
        f.seek(self.addresses[MAXMIN], os.SEEK_SET)
        self.valid_maxmin = struct.unpack('>i', f.read(SIZES['validmaxmin']))[0] == 1
        maxmin = struct.unpack('>2i', f.read(SIZES['maxmin']))
        self.min, self.max = maxmin

    def read_histogram(self, f):
        f.seek(self.addresses[HISTO], os.SEEK_SET)
        self.valid_histogram = struct.unpack('>i', f.read(SIZES['validhistogram']))[0] == 1
        self.histogram = struct.unpack('>1024i', f.read(SIZES['histogram']))

    def read_pixel_format(self, f):
        f.seek(self.addresses[PIXEL_FORMAT], os.SEEK_SET)
        self.pixel_format = struct.unpack('>i', f.read(SIZES['pixelformat']))[0]

    def read_dimc(self, f):
        f.seek(self.addresses[DIMC], os.SEEK_SET)
        self.dimc = struct.unpack('>i', f.read(SIZES['dimc']))[0]

    def read_dimv(self, f):
        f.seek(self.addresses[DIMV], os.SEEK_SET)
        self.dimv = struct.unpack('>10i', f.read(SIZES['dimv']))

    def calculate_pixel_count(self):
        pixel_count = 1
        for i in range(self.dimc):
            pixel_count *= self.dimv[i]
        self.pixel_count = pixel_count

    def read_info(self, f):
        f.seek(0, os.SEEK_END)
        cnt = f.tell()
        info_len = cnt - self.addresses[INFO]
        f.seek(self.addresses[INFO], os.SEEK_SET)
        info_field = f.read(info_len).decode('ascii')
        self.info = info_field.split('\0', 1)[0]

    def read_pixels(self, f):
        f.seek(self.addresses[PIXELS], os.SEEK_SET)
        lin_pixels = np.fromfile(f, dtype=np.dtype('>i2'), count=self.pixel_count)
        self.pixels = np.reshape(lin_pixels, self.dimv[0:self.dimc])
