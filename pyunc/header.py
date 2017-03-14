from __future__ import print_function
from datetime import datetime
from functools import partial
import re


class UNCHeader(object):
    def __init__(self, info):
        self.dicom_header = {}
        actions = {
            'Patient_Name=': partial(self._parse_equals, 'patient_name', str),
            'Patient_ID=': partial(self._parse_equals, 'patient_id', str),
            'Patient_Birth_Date=': self._parse_dob,
            'Scan_Date=': self._parse_scan_date,
            'Modality=': partial(self._parse_equals, 'modality', str),
            'Scanning_Sequence=': partial(self._parse_equals, 'scanning_sequence', str),
            'Sequence_Variant=': partial(self._parse_equals, 'sequence_variant', str),
            'Flip_Angle=': partial(self._parse_equals, 'flip_angle', float),
            'Slice_Thickness_mm=': partial(self._parse_equals, 'slice_thickness_mm', float),
            'Image_Orientation_Patient_Coordinates=': partial(self._parse_split, 'image_orientation_patient_coordinates', '\\', float),
            'Image_Position_Patient_Coordinates=': partial(self._parse_split, 'image_position_patient_coordinates', '\\', float),
            'Intensity_Rescale_Units=': partial(self._parse_equals, 'intensity_rescale_units', str),
            'Intensity_Rescale_Slope=': partial(self._parse_equals, 'intensity_rescale_slope', float),
            'Intensity_Rescale_Intercept=': partial(self._parse_equals, 'intensity_rescale_intercept', float),
            'Colour_Mapping=': partial(self._parse_equals, 'colour_mapping', str),
            '<0x': self._parse_dicom_field
        }
        infoarr = info.split('\n')
        for l in infoarr:
            for a in actions:
                if l.startswith(a):
                    actions[a](l)
        self.text = infoarr
        self.slices = self._read_slices(infoarr)

class Header(object):
    def _parse_dims(self, l):
        dims_value = l.split(':')[1].strip()
        dims = dims_value.split(' ')
        for d in dims:
            if d.startswith('cols'):
                self.cols = int(d.split('=')[1])
            elif d.startswith('rows'):
                self.rows = int(d.split('=')[1])
            elif d.startswith('slices'):
                self.slices = int(d.split('=')[1])

    def _parse_pixel_size(self, l):
        dims_value = l.split(':')[1].strip()
        dims = dims_value.split('x')
        self.pixel_size = [float(d) for d in dims]

    def _parse_min_max_pixel_values(self, l):
        exp = r'Min pixel value is (?P<min>-?[0-9]+\.?[0-9]); max is (?P<max>-?[0-9]+\.?[0-9])'
        m = re.match(exp, l)
        self.min_pixel_value = float(m.group('min'))
        self.max_pixel_value = float(m.group('max'))

    def _parse_strslice(self, attr, key, l):
        value = l[len(key):].strip()
        setattr(self, attr, value)

    def _parse_equals(self, attr, converter, l):
        value = converter(l.split('=', 1)[1].strip())
        setattr(self, attr, value)

    def _parse_dob(self, l):
        date_str = l.split('=', 1)[1]
        self.patient_date_of_birth = datetime.strptime(date_str, '%B %d, %Y').date()

    def _parse_scan_date(self, l):
        date_str = l.split('=', 1)[1]
        self.scan_date = datetime.strptime(date_str, '%B %d, %Y %H:%M %p')

    def _parse_split(self, attr, sep, converter, l):
        setattr(self, attr, [converter(x) for x in l.split('=', 1)[1].split(sep)])

    def _parse_dicom_field(self, l):
        exp = r'(?P<tag><0x[0-9a-f]{4},\s0x[0-9a-f]{4}>)\s(?P<data_type>[\w\s\(\)]+),(\sID)?\s(?P<id>[\w\s]+)=(?P<value>.*)'
        m = re.match(exp, l)
        if m:
            if m.group('data_type') == 'Date':
                value = datetime.strptime(m.group('value'), '%Y%m%d').date()
            elif m.group('data_type') == 'Time':
                value = datetime.strptime(m.group('value').split('.')[0], '%H%M%S').time()
            else:
                value = m.group('value')
            self.dicom_header[m.group('id')] = value

    def _read_slices(self, infoarr):
        slices = []
        found_slice = False
        for l in infoarr:
            print(l)
            if l.startswith('Echo_Time='):
                slices.append([])
                found_slice = True
            if not found_slice:
                continue
            slices[-1].append(l)
        return slices

    def _do_parse(self, info, actions):
        infoarr = info.split('\n')
        for l in infoarr:
            print(l)
            for a in actions:
                if l.startswith(a):
                    actions[a](l)
        self.text = infoarr


class SliceHeader(Header):
    def __init__(self, info):
        print(info)
        actions = {
            'Echo_Time=': partial(self._parse_equals, 'echo_time', str)
        }
        self._do_parse(info, actions)


class UNCHeader(Header):
    def __init__(self, info):
        self.dicom_header = {}
        actions = {
            'Patient_Name=': partial(self._parse_equals, 'patient_name', str),
            'Patient_ID=': partial(self._parse_equals, 'patient_id', str),
            'Patient_Birth_Date=': self._parse_dob,
            'Scan_Date=': self._parse_scan_date,
            'Modality=': partial(self._parse_equals, 'modality', str),
            'Scanning_Sequence=': partial(self._parse_equals, 'scanning_sequence', str),
            'Sequence_Variant=': partial(self._parse_equals, 'sequence_variant', str),
            'Flip_Angle=': partial(self._parse_equals, 'flip_angle', float),
            'Slice_Thickness_mm=': partial(self._parse_equals, 'slice_thickness_mm', float),
            'Image_Orientation_Patient_Coordinates=': partial(self._parse_split, 'image_orientation_patient_coordinates', '\\', float),
            'Image_Position_Patient_Coordinates=': partial(self._parse_split, 'image_position_patient_coordinates', '\\', float),
            'Intensity_Rescale_Units=': partial(self._parse_equals, 'intensity_rescale_units', str),
            'Intensity_Rescale_Slope=': partial(self._parse_equals, 'intensity_rescale_slope', float),
            'Intensity_Rescale_Intercept=': partial(self._parse_equals, 'intensity_rescale_intercept', float),
            'Colour_Mapping=': partial(self._parse_equals, 'colour_mapping', str),
            '<0x': self._parse_dicom_field
        }
        self._do_parse(info, actions)
