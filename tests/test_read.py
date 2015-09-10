"""

"""

import shutil
import pytest
import pyunc
import os.path


@pytest.fixture
def uncfile(tmpdir):
    tgt = str(os.path.join(os.path.dirname(__file__), 'test.unc'))
    uf = pyunc.UNCFile.from_path(tgt)
    return uf


def test_dimc(uncfile):
    assert uncfile.dimc == 3


def test_dimv(uncfile):
    assert uncfile.dimv == (46, 256, 256, 0, 0, 0, 0, 0, 0, 0)


def test_title(uncfile):
    assert uncfile.title == 'Name: Anonymous ; ID: Anonymous ID; DoB: 01-Jan-1970'


def test_maxmin(uncfile):
    assert uncfile.valid_maxmin is True
    assert uncfile.min == 0
    assert uncfile.max == 693


def test_histogram(uncfile):
    assert uncfile.valid_histogram is False
    assert uncfile.histogram == (0,) * 1024


def test_header(uncfile):
    assert uncfile.header.birth_year == '1970'
