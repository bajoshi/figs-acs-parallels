from __future__ import division

import numpy as np
import os
import sys
import shutil
import glob

home = os.getenv('HOME')
acspar = home + '/acspar/' 
acs_home = home + '/Desktop/FIGS/figs-acs-parallels/'

if __name__ == '__main__':
    
    names_header = ['num','mag','x','y','ra','dec','xw','yw','a_im','b_im','theta_im','theta_w','aw','bw']
    mag_limit = 24.0
    
    field = '_gs1'
    posang = '_28'

    datadir = acspar + 'DATA' + field + posang + '/'
    store_cat_dir = acspar + 'OrigCats' + field + posang + '/'

    # make sure that the directory to save original catalogs exists 
    if not os.path.isdir(store_cat_dir):
        try:
            os.makedirs(store_cat_dir) 
        except OSError as ose:
            print ose
            print "Oops! Unexpected error encountered while moving original catalogs..."
    else:
        for file in glob.glob(datadir + '*.cat'):
            if os.path.isfile(store_cat_dir + os.path.basename(file)):
                print store_cat_dir + os.path.basename(file), "exists. Will now move the next catalog on the list."
            else:
                shutil.move(file, store_cat_dir + os.path.basename(file))

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

    for file in glob.glob(store_cat_dir + '*.cat'):
        c = np.genfromtxt(file, dtype=None, names=names_header, skip_header=14)
        
        fh = open(datadir + os.path.basename(file), 'wa')
        
        idx_keep = np.where(c['mag'] < mag_limit)[0]
        
        fh.write(sextractor_header)
        fh.write('\n')

        for i in range(len(c)):
            if i in idx_keep:
                fh.write(str(c[i]).replace(',', ' ').replace('(', '').replace(')', '') + '\n')
            else:
                continue
        
        fh.close()