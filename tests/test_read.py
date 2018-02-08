"""Basic UNC read tests."""

import numpy as np
import pytest
from fixtures import pdt2, pdt2_byte, pdt2_signed_int, t13d


def test_title(pdt2):
    assert pdt2.title == 'Name: Anonymous; ID: Anonymous ID; Series: 301; Sequence: <unknown>'


def test_maxmin(pdt2):
    assert pdt2.valid_maxmin is True
    assert pdt2.min == 0
    assert pdt2.max == 1


def test_histogram(pdt2):
    assert pdt2.valid_histogram is False
    assert pdt2.histogram == (0,) * 1024


def test_pixel_format(pdt2, pdt2_byte, pdt2_signed_int):
    assert pdt2_byte.pixel_format == 0o0001
    assert pdt2.pixel_format == 0o0010
    assert pdt2_signed_int.pixel_format == 0o0003


def test_dimc(pdt2):
    assert pdt2.dimc == 3


def test_dimv(pdt2):
    assert pdt2.dimv == (100, 240, 240, 0, 0, 0, 0, 0, 0, 0)


def test_pixel_count(pdt2, pdt2_byte, pdt2_signed_int, t13d):
    assert pdt2.pixel_count == 100 * 240 * 240
    assert pdt2_byte.pixel_count == 100 * 240 * 240
    assert pdt2_signed_int.pixel_count == 100 * 240 * 240
    assert t13d.pixel_count == 180 * 256 * 256


def test_num_echoes(t13d, pdt2):
    assert t13d.num_echoes == 1
    assert pdt2.num_echoes == 2


def test_pixels(pdt2, pdt2_byte, pdt2_signed_int, t13d):
    assert pdt2.pixels.shape == (100, 240, 240)
    assert np.sum(pdt2.pixels > 0) == 941001
    assert pdt2_byte.pixels.shape == (100, 240, 240)
    assert np.sum(pdt2.pixels > 0) == 941001
    assert pdt2_signed_int.pixels.shape == (100, 240, 240)
    assert np.sum(pdt2.pixels > 0) == 941001
    assert t13d.pixels.shape == (180, 256, 256)
    assert np.sum(t13d.pixels > 0) == 283593
