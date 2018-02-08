"""Classes representing header information."""

from __future__ import print_function
from datetime import datetime
from functools import partial
import re
import sys


class Header(object):
    """Base class for file and slice headers."""

    def __init__(self):
        self.audit_info = []
        self.slices = []
        self.dicom = {}

    def _parse_equals(self, attr, converter, l):
        value = converter(l.split('=', 1)[1].strip())
        setattr(self, attr, value)

    def _parse_dob(self, l):
        date_str = l.split('=', 1)[1]
        setattr(self, 'patient_birth_date', datetime.strptime(date_str, '%B %d, %Y').date())

    def _parse_scan_date(self, l):
        date_str = l.split('=', 1)[1]
        setattr(self, 'scan_date', datetime.strptime(date_str, '%B %d, %Y %I:%M %p'))

    def _parse_split(self, attr, sep, converter, l):
        setattr(self, attr, [converter(x) for x in l.split('=', 1)[1].split(sep)])

    def _parse_dicom_field(self, l):
        exp = (
            r'(?P<tag><0x[0-9a-f]{4},\s0x[0-9a-f]{4}>)\s'
            r'(?P<data_type>[\w\s\(\)]+),\s'
            r'(?:ID|REL|ACQ)?\s(?P<id>[\w\s\(\)]+)'
            r'=(?P<value>.*)'
        )
        m = re.match(exp, l)
        if m:
            if m.group('data_type') == 'Date':
                value = datetime.strptime(m.group('value'), '%Y%m%d').date()
            elif m.group('data_type') == 'Time':
                value = datetime.strptime(m.group('value').split('.')[0], '%H%M%S').time()
            elif m.group('data_type') == 'Decimal String':
                if '\\' in m.group('value'):
                    value = [float(v) for v in m.group('value').split('\\')]
                else:
                    value = float(m.group('value'))
            elif m.group('data_type') == 'Integer String':
                if '\\' in m.group('value'):
                    value = [int(v) for v in m.group('value').split('\\')]
                else:
                    value = int(m.group('value'))
            else:
                value = m.group('value')
            self.dicom[m.group('id')] = value

    def _parse_other(self, l):
        if l.startswith('Audit info'):
            self.audit_info.append(l)
            return
        try:
            key, value = l.strip().rsplit('=', 1)
        except ValueError:
            print('Unable to parse line ({0!r})'.format(l), file=sys.stderr)
        else:
            setattr(self, key.lower(), value)

    def _do_parse(self, info, actions):
        infoarr = info.split('\n')
        for l in infoarr:
            if not l:
                continue
            for a in actions:
                if l.startswith(a):
                    actions[a](l)
                    break
            else:
                self._parse_other(l)
        self.text = infoarr


class SliceHeader(Header):
    """Header information for a single slice."""

    def __init__(self, info):
        super(SliceHeader, self).__init__()
        actions = {
            'Echo_Time=': partial(
                self._parse_equals,
                'echo_time', float
            ),
            'Image_Orientation_Patient_Coordinates=': partial(
                self._parse_split,
                'image_orientation_patient_coordinates', '\\', float
            ),
            'Image_Position_Patient_Coordinates=': partial(
                self._parse_split,
                'image_position_patient_coordinates', '\\', float
            ),
            '<0x': self._parse_dicom_field
        }
        self._do_parse(info, actions)
        try:
            self.slice_location = self._get_slice_location(self.dicom)
        except Exception as e:
            self.slice_location = None
        try:
            self.image_position_patient = self._get_image_position_patient(self.dicom)
        except Exception as e:
            self.image_position_patient = None
        self.text = info

    @staticmethod
    def _get_slice_location(header):
        return header['Slice Location']

    @staticmethod
    def _get_image_position_patient(header):
        return header['Image Position (Patient)']


class UNCHeader(Header):
    """Header information."""

    def __init__(self, info, slice_info):
        super(UNCHeader, self).__init__()
        self.dicom = {}
        actions = {
            'Patient_Name=': partial(
                self._parse_equals,
                'patient_name', str
            ),
            'Patient_ID=': partial(
                self._parse_equals,
                'patient_id', str
            ),
            'Patient_Birth_Date=': self._parse_dob,
            'Scan_Date=': self._parse_scan_date,
            'Modality=': partial(
                self._parse_equals,
                'modality', str
            ),
            'Patient_Position=': partial(
                self._parse_equals,
                'patient_position', str
            ),
            'Scanning_Sequence=': partial(
                self._parse_equals,
                'scanning_sequence', str
            ),
            'Sequence_Variant=': partial(
                self._parse_equals,
                'sequence_variant', str
            ),
            'Flip_Angle=': partial(
                self._parse_equals,
                'flip_angle', float
            ),
            'Slice_Thickness_mm=': partial(
                self._parse_equals,
                'slice_thickness_mm', float
            ),
            'Pixel_Size=': partial(
                self._parse_split,
                'pixel_size', '\\', float
            ),
            'Intensity_Rescale_Units=': partial(
                self._parse_equals,
                'intensity_rescale_units', str
            ),
            'Intensity_Rescale_Slope=': partial(
                self._parse_equals,
                'intensity_rescale_slope', float
            ),
            'Intensity_Rescale_Intercept=': partial(
                self._parse_equals,
                'intensity_rescale_intercept', float
            ),
            'Colour_Mapping=': partial(
                self._parse_equals,
                'colour_mapping', str
            ),
            '<0x': self._parse_dicom_field
        }
        self._do_parse(info, actions)
        self.text = info
        self.slices = []
        for sl in slice_info:
            self.slices.append(SliceHeader(sl))
        self.slices.sort(key=lambda s: s.slice_location)

    @property
    def image_orientation_patient_coordinates(self):
        return self.slices[0].image_orientation_patient_coordinates
