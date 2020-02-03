"""UNC conversion tests."""

import numpy as np
from pyunc.conversion import unc_to_nifti
from fixtures import flair, spine, t13d, pdt2


def test_2d_conversion(spine):
    # expected value from dcm2niix v1.0.20170623
    expected_qform = np.array([
        [-6.69590948e-01, -5.75567974e-04, 4.09939091e-02, 7.17391205e+01],
        [3.24284079e-08, 6.68045511e-01, 2.27797188e-01, -7.21104355e+01],
        [8.33846604e-03, -4.62215433e-02, 3.29186962e+00, -7.47424622e+01],
        [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]
    ])
    nii = unc_to_nifti(spine)
    assert np.allclose(nii.get_qform(), expected_qform)


def test_3d_conversion(t13d):
    # expected value from dcm2niix v1.0.20170623
    expected_qform = np.array([
        [9.97147244e-01, -1.92868142e-02, 7.29574222e-02, -9.45174637e+01],
        [2.74663883e-02, 9.93234627e-01, -1.12829829e-01, -1.00241058e+02],
        [-7.02876179e-02, 1.14511980e-01, 9.90932210e-01, -1.22561035e+02],
        [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]
    ])
    nii = unc_to_nifti(t13d)
    assert np.allclose(nii.get_qform(), expected_qform)


def test_split_conversion(pdt2):
    # expected value from dcm2niix v1.0.20170623
    expected_affine = np.array([
        [-9.97148573e-01, -1.92868151e-02, 2.18872011e-01, 1.18133919e+02],
        [-2.74664238e-02, 9.93234634e-01, -3.38489085e-01, -9.25773315e+01],
        [7.02877119e-02, 1.14511982e-01, 2.97279334e+00, -8.33553391e+01],
        [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]
    ])
    e1, e2 = pdt2.split_echoes()
    nii_e1 = unc_to_nifti(e1)
    nii_e2 = unc_to_nifti(e2)
    assert np.allclose(nii_e1.header.get_best_affine(), expected_affine, atol=1e-6)
    assert np.allclose(nii_e2.header.get_best_affine(), expected_affine, atol=1e-6)


def test_ascii_conversion(flair):
    _ = unc_to_nifti(spine)

