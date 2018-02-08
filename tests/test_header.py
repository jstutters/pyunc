"""UNC header tests."""

import numpy as np
import pytest
from fixtures import pdt2, t13d


@pytest.fixture
def pdt2_header(pdt2):
    return pdt2.header


@pytest.fixture
def t13d_header(t13d):
    return t13d.header


def test_patient_name(pdt2_header):
    assert pdt2_header.patient_name == 'Anonymous'


def test_patient_id(pdt2_header):
    assert pdt2_header.patient_id == 'Anonymous ID'


def test_dob(pdt2_header):
    assert pdt2_header.patient_birth_date.year == 1970
    assert pdt2_header.patient_birth_date.month == 1
    assert pdt2_header.patient_birth_date.day == 1


def test_scan_date(pdt2_header):
    assert pdt2_header.scan_date.year == 2017
    assert pdt2_header.scan_date.month == 7
    assert pdt2_header.scan_date.day == 4
    assert pdt2_header.scan_date.hour == 14
    assert pdt2_header.scan_date.minute == 46


def test_flip_angle(pdt2_header):
    assert pdt2_header.flip_angle == 90.0


def test_slice_thickness_mm(pdt2_header):
    assert pdt2_header.slice_thickness_mm == 3.0


def test_intensity_rescale_units(pdt2_header):
    assert pdt2_header.intensity_rescale_units == 'US'


def test_intensity_rescale_slope(pdt2_header):
    assert pdt2_header.intensity_rescale_slope == 1.0


def test_intensity_rescale_slope(pdt2_header):
    assert pdt2_header.intensity_rescale_intercept == 0.0


def test_colour_mapping(pdt2_header):
    assert pdt2_header.colour_mapping == 'MONOCHROME2'


def test_dicom_SAR(pdt2_header):
    assert pdt2_header.dicom['SAR'] == 0.17767155170440


def test_dicom_transmitting_coil_name(pdt2_header):
    assert pdt2_header.dicom['Transmitting Coil Name'] == 'S'


def test_image_orientation_patient_coordinates(pdt2_header):
    expected = np.array([
        0.99714857,
        0.027466424,
        0.07028771,
        -0.019286815,
        0.99323463,
        -0.11451198,
    ])
    assert np.allclose(
        np.array(pdt2_header.image_orientation_patient_coordinates),
        expected
    )
