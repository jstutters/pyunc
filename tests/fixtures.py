import gzip
import os
import pytest
from pyunc import UNCFile


def _read_gzipped_unc(path, tmpdir):
    ufgz = gzip.open(path, 'rb')
    tmpuf = tmpdir.join('tmp.unc')
    tmpuf.write_binary(ufgz.read())
    uf = UNCFile.from_path(str(tmpuf))
    return uf


@pytest.fixture
def flair(tmpdir):
    tgt = str(os.path.join(os.path.dirname(__file__), 'data', 'flair.unc.gz'))
    uf = _read_gzipped_unc(tgt, tmpdir)
    return uf


@pytest.fixture
def pdt2(tmpdir):
    tgt = str(os.path.join(os.path.dirname(__file__), 'data', 'pdt2.unc.gz'))
    uf = _read_gzipped_unc(tgt, tmpdir)
    return uf


@pytest.fixture
def pdt2_header(pdt2):
    return pdt2.header


@pytest.fixture
def pdt2_byte(tmpdir):
    tgt = str(os.path.join(os.path.dirname(__file__), 'data', 'pdt2_byte.unc.gz'))
    uf = _read_gzipped_unc(tgt, tmpdir)
    return uf


@pytest.fixture
def pdt2_signed_int(tmpdir):
    tgt = str(os.path.join(os.path.dirname(__file__), 'data', 'pdt2_signed_int.unc.gz'))
    uf = _read_gzipped_unc(tgt, tmpdir)
    return uf


@pytest.fixture
def multi_volume(tmpdir):
    tgt = str(os.path.join(os.path.dirname(__file__), 'data', 'multi_volume.unc.gz'))
    uf = _read_gzipped_unc(tgt, tmpdir)
    return uf


@pytest.fixture
def spine(tmpdir):
    tgt = str(os.path.join(os.path.dirname(__file__), 'data', 'spine.unc.gz'))
    uf = _read_gzipped_unc(tgt, tmpdir)
    return uf


@pytest.fixture
def t13d(tmpdir):
    tgt = str(os.path.join(os.path.dirname(__file__), 'data', 't13dvol.unc.gz'))
    uf = _read_gzipped_unc(tgt, tmpdir)
    return uf
