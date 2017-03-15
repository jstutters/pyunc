from __future__ import absolute_import
import os
import struct
import numpy as np
from .header import UNCHeader, SliceHeader
from .__version__ import __version__

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


class UNCFile(object):
    def __init__(self, f):
        self._read_addresses(f)
        self._read_title(f)
        self._read_maxmin(f)
        self._read_histogram(f)
        self._read_pixel_format(f)
        self._read_dimc(f)
        self._read_dimv(f)
        self._calculate_pixel_count()
        self._read_info(f)
        self._read_pixels(f)

    @classmethod
    def from_path(cls, path):
        with open(path, 'rb') as f:
            instance = cls(f)
        return instance

    def _read_addresses(self, f):
        f.seek(0, os.SEEK_SET)
        self.addresses = struct.unpack('>9i', f.read(36))

    def _read_title(self, f):
        f.seek(self.addresses[TITLE], os.SEEK_SET)
        title_field = struct.unpack('>81s', f.read(SIZES['title']))[0].decode('ascii')
        self.title = title_field.split('\0', 1)[0]

    def _read_maxmin(self, f):
        f.seek(self.addresses[MAXMIN], os.SEEK_SET)
        self.valid_maxmin = struct.unpack('>i', f.read(SIZES['validmaxmin']))[0] == 1
        maxmin = struct.unpack('>2i', f.read(SIZES['maxmin']))
        self.min, self.max = maxmin

    def _read_histogram(self, f):
        f.seek(self.addresses[HISTO], os.SEEK_SET)
        self.valid_histogram = struct.unpack('>i', f.read(SIZES['validhistogram']))[0] == 1
        self.histogram = struct.unpack('>1024i', f.read(SIZES['histogram']))

    def _read_pixel_format(self, f):
        f.seek(self.addresses[PIXEL_FORMAT], os.SEEK_SET)
        self.pixel_format = struct.unpack('>i', f.read(SIZES['pixelformat']))[0]

    def _read_dimc(self, f):
        f.seek(self.addresses[DIMC], os.SEEK_SET)
        self.dimc = struct.unpack('>i', f.read(SIZES['dimc']))[0]

    def _read_dimv(self, f):
        f.seek(self.addresses[DIMV], os.SEEK_SET)
        self.dimv = struct.unpack('>10i', f.read(SIZES['dimv']))

    def _calculate_pixel_count(self):
        pixel_count = 1
        for i in range(self.dimc):
            pixel_count *= self.dimv[i]
        self.pixel_count = pixel_count

    def _read_info(self, f):
        f.seek(0, os.SEEK_END)
        cnt = f.tell()
        info_len = cnt - self.addresses[INFO]
        f.seek(self.addresses[INFO], os.SEEK_SET)
        info_field = f.read(info_len).decode('ascii')
        self.info = info_field.split('\0')
        self.header = UNCHeader(self.info[0])
        self.slice_info = []
        for i in range(1, self.dimv[0]):
            self.slice_info.append(SliceHeader(self.info[i]))

    def _read_pixels(self, f):
        f.seek(self.addresses[PIXELS], os.SEEK_SET)
        lin_pixels = np.fromfile(f, dtype=np.dtype('>i2'), count=self.pixel_count)
        self.pixels = np.reshape(lin_pixels, self.dimv[0:self.dimc])
