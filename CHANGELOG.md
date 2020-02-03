# CHANGELOG

## [Unreleased]

## [0.6.3] - 2020-02-03

### Fixed

- Handle non-ASCII characters in some headers.
- Handle dates where seconds are missing.

## [0.6.2] - 2019-06-10

### Fixed

- Get Image Orientation (Patient) from first slice if not in the global header.

## [0.6.1] - 2019-05-10

### Added

- DICOM attributes can now be referenced by tag.
- PAT, IMG, PROC, and PLUT DICOM attributes are now read.

### Fixed
- Can now read files where numeric values in DICOM header are empty.

## [0.5.1] - 2018-08-22

### Fixed
- Parse Image_Orientation_Patient_Coordinates and
  Image_Position_Patient_Coordinates if they are in general file info.
