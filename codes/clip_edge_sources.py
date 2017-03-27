from __future__ import division

import numpy as np
from astropy.io import fits

import os
import sys

home = os.getenv('HOME')
acspar = home + '/acspar/'
acs_home = home + '/Desktop/FIGS/figs-acs-parallels/'

if __name__ == '__main__':

    # define the pointing
    filt = 'f814w'
    field = 'gs1'
    posang = '28'

    # read in catalog
    names_header = ['num','mag','x','y','ra','dec','xw','yw','a_im','b_im','theta_im','theta_w','aw','bw']

    catfile = acspar + filt + '_' + field + '_' + posang + '.cat'
    cat = np.genfromtxt(catfile, dtype=None, names=names_header, skip_header=14)

    # figure out which indices you want to keep
    # Important to clip using physical pixels instead 
    # of sky coordinates because the X and Y axes of 
    # the image will probably not align with the ra and dec axes.
    all_x = cat['x']
    all_y = cat['y']

    # I'm harcoding this in but this should be read in from the image
    # header using NAXIS1 and NAXIS2 and divding them by 2
    x_cen = 2111
    y_cen = 2170

    x_lim = 1800  # in pixels
    y_lim = 1800

    valid_idx = np.where((all_x >= x_cen - x_lim) & (all_x <= x_cen + x_lim) &\
     (all_y >= y_cen - y_lim) & (all_y <= y_cen + y_lim))[0]

    # loop over catalog and rewrite the valid entries after writing the header
    sextractor_header = "# 1  NUMBER  Running object number" + "\n" +\
                        "# 2  MAG_F0805  Kron-like elliptical aperture magnitude  [mag]" + "\n" +\
                        "# 3  X_IMAGE  Object position along x  [pixel]" + "\n" +\
                        "# 4  Y_IMAGE  Object position along y  [pixel]" + "\n" +\
                        "# 5  ALPHA_J2000  Right ascension of barycenter (J2000)  [deg]" + "\n" +\
                        "# 6  DELTA_J2000  Declination of barycenter (J2000)  [deg]" + "\n" +\
                        "# 7  X_WORLD  Barycenter position along world x axis  [deg]" + "\n" +\
                        "# 8  Y_WORLD  Barycenter position along world y axis  [deg]" + "\n" +\
                        "# 9  A_IMAGE  Profile RMS along major axis  [pixel]" + "\n" +\
                        "# 10 B_IMAGE  Profile RMS along minor axis  [pixel]" + "\n" +\
                        "# 11 THETA_IMAGE  Position angle (CCW/x)  [deg]" + "\n" +\
                        "# 12 THETA_WORLD  Position angle (CCW/world-x)  [deg]" + "\n" +\
                        "# 13 A_WORLD  Profile RMS along major axis (world units)  [deg]" + "\n" +\
                        "# 14 B_WORLD  Profile RMS along minor axis (world units)  [deg]"

    catname = acspar + os.path.basename(catfile).split('.')[0] + '_clipped.cat'
    fh = open(catname, 'wa')
    
    fh.write(sextractor_header)
    fh.write('\n')

    for i in range(len(cat)):

        if i in valid_idx:
            rewritestr = str(cat[i]).replace(',', ' ').replace('(', '').replace(')', '') + '\n'
            fh.write(rewritestr)

    fh.close()
    
    sys.exit(0)