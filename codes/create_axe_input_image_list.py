from __future__ import division

import numpy as np
from astropy.io import fits

import os
import sys

home = os.getenv('HOME')  # Does not have a trailing slash at the end
acs_home = home + '/Desktop/FIGS/figs-acs-parallels/'

if __name__ == '__main__':
    
    datadir = '/Volumes/Bhavins_backup/acs_parallels_data/flc/'

    # First read in teh original .lis files
    direct_lis = np.loadtxt(acs_home + 'f814w_gs1_28.lis', dtype=np.str)
    grism_lis = np.loadtxt(acs_home + 'g800l_gs1_28.lis', dtype=np.str)

    fh = open(acs_home + 'input_image_lists/' + 'gs1_28.lis', 'wa')

    for file_dir in direct_lis:
        for file_gr in grism_lis:
            h_dir = fits.open(datadir + file_dir)
            h_grism = fits.open(datadir + file_gr)

            crval1_dir = h_dir[1].header['CRVAL1']
            crval2_dir = h_dir[1].header['CRVAL2']

            crval1_gr = h_grism[1].header['CRVAL1']
            crval2_gr = h_grism[1].header['CRVAL2']

            if (crval1_dir == crval1_gr) and (crval2_dir == crval2_gr):
                fh.write(file_gr + ' ' + file_dir.replace('.fits','') + '_1.cat' +  ',' + file_dir.replace('.fits','') + '_2.cat' +  ' ' + file_dir + '\n')
                print crval1_dir, crval1_gr, crval2_dir, crval2_gr, file_gr, file_dir

    fh.close()

    sys.exit(0)