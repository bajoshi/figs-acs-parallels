from __future__ import division

from drizzlepac import skytopix
from astropy.io import fits
from astropy.nddata.utils import Cutout2D
import numpy as np
import astropy.wcs as wcs

import matplotlib.pyplot as plt

import os
import sys
import glob
import shutil

home = os.getenv('HOME')  # Does not have a trailing slash at the end
acs_home = home + '/Desktop/FIGS/figs-acs-parallels/'

if __name__ == '__main__':

    acs_flc_path = "/Volumes/Bhavins_backup/acs_parallels_data/flc/"

    candels_gs = fits.open('/Volumes/Bhavins_backup/hlsp_candels_hst_acs_gs-tot_f814w_v1.0_drz.fits')
    gs1_28_g800l = np.loadtxt(acs_home + 'g800l_gs1_28.lis', dtype=np.str)
    gs1_28_f814w = np.loadtxt(acs_home + 'f814w_gs1_28.lis', dtype=np.str)

    x_pix = []
    y_pix = []
    ra_arr = []
    dec_arr = []

    for file in gs1_28_g800l:

        h = fits.open(acs_flc_path + file)
        ra = h[0].header['RA_TARG']
        dec = h[0].header['DEC_TARG']
        
        x, y = skytopix.rd2xy('/Volumes/Bhavins_backup/hlsp_candels_hst_acs_gs-tot_f814w_v1.0_drz.fits', str(ra), str(dec))

        ra_arr.append(ra)
        dec_arr.append(dec)
        x_pix.append(x)
        y_pix.append(y)

        h.close()

    # ACS FOV is 202 x 202 sq. arcseconds. I'll assume a larger FOV to be safe and crop the CANDELS image accordingly
    # Assuming 210 x 210 sq. arcseconds
    ra_min = min(ra_arr)
    dec_min = min(dec_arr)
    ra_max = max(ra_arr)
    dec_max = max(dec_arr)

    cutout_ra_min = ra_min - np.sqrt(2) * 110 / 3600
    cutout_ra_max = ra_max + np.sqrt(2) * 110 / 3600
    cutout_dec_min = dec_min - np.sqrt(2) * 110 / 3600
    cutout_dec_max = dec_max + np.sqrt(2) * 110 / 3600

    cutout_x_min, cutout_y_min = skytopix.rd2xy('/Volumes/Bhavins_backup/hlsp_candels_hst_acs_gs-tot_f814w_v1.0_drz.fits', str(cutout_ra_min), str(cutout_dec_min))
    cutout_x_max, cutout_y_max = skytopix.rd2xy('/Volumes/Bhavins_backup/hlsp_candels_hst_acs_gs-tot_f814w_v1.0_drz.fits', str(cutout_ra_max), str(cutout_dec_max))

    #print cutout_x_min, cutout_y_min
    #print cutout_x_max, cutout_y_max
    
    cutout_row_cen = int(81000 - (cutout_y_min + cutout_y_max) / 2)
    cutout_col_cen = int((cutout_x_min + cutout_x_max) / 2)

    # Cutout using astropy tool and save
    hdu = fits.PrimaryHDU()
    hdulist = fits.HDUList(hdu)
    w = wcs.WCS(candels_gs[0].header, candels_gs)
    cutout_data = Cutout2D(data=candels_gs[0].data, position=(cutout_row_cen, cutout_col_cen), size=(10000,10000), wcs=w)
    hdulist.append(fits.ImageHDU(data=cutout_data.data, header=cutout_data.wcs.to_header()))

    hdulist.writeto('/Volumes/Bhavins_backup/axe_notes_routines/candels_gs_cropped_gs1_28.fits', clobber=True)