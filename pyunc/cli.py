import argparse
import sys
import nibabel as nib
from . import UNCFile
from . import conversion


def unc_to_nifti():
    parser = argparse.ArgumentParser(description='Convert UNC to NIFTI')
    parser.add_argument('--volumes', '-v', type=int, nargs='?', default=1, help='Number of volumes')
    parser.add_argument('unc_filename', help='UNC file')
    args = parser.parse_args()
    if args.unc_filename.endswith('.unc'):
        name = args.unc_filename[0:-4]
    unc = UNCFile.from_path(args.unc_filename)
    if unc.num_echoes > 1:
        echoes = unc.split_echoes()
        for echo_num, echo in enumerate(echoes):
            if args.volumes > 1:
                vols = echo.split_volumes(args.volumes)
                for vol_num, vol in enumerate(vols):
                    nii = conversion.unc_to_nifti(vol)
                    nii_name = '{0}_v{1}_e{2}.nii.gz'.format(name, vol_num, echo_num)
                    nib.save(nii, nii_name)
            else:
                nii = conversion.unc_to_nifti(echo)
                nii_name = '{0}_e{1}.nii.gz'.format(name, echo_num)
                nib.save(nii, nii_name)
    else:
        if args.volumes > 1:
            vols = unc.split_volumes(args.volumes)
            for vol_num, vol in enumerate(vols):
                nii = conversion.unc_to_nifti(echo)
                nii_name = '{0}_v{1}.nii.gz'.format(name, vol_num)
                nib.save(nii, nii_name)
        else:
            nii = conversion.unc_to_nifti(unc)
            nii_name = '{0}.nii.gz'.format(name)
            nib.save(nii, nii_name)
