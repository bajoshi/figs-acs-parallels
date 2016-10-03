from __future__ import division
import numpy as np
from astropy.io import fits
import glob, os, shutil

datadir = '/Users/baj/Documents/acs_parallels_data/flc/'
#
# These are from the floor values of the position angles in the header keyword PA_V3
# There are 20 ACS pointings corresponding to 5 different PAs of 4 fields of the primary WFC3 pointings
# These are not required by the program but are listed below for reference --
# GS1_PAlist = ['28', '37', '99', '106', '167']
# GS2_PAlist = ['28', '88', '124', '155', '299']
# GN1_PAlist = ['111', '150', '186', '216', '258']
# GN2_PAlist = ['23', '106', '156', '162', '231']
#

#
# Find the direct image files that correspond to a single pointing
#
"""
fh = open('F814W_GS1_99.lis', 'wa')

for file in glob.glob(datadir + '*.fits'):
    
    filename = os.path.basename(file)
    
    if filename[4] == '1':
        fitsfile = fits.open(file)
        posang = fitsfile[0].header['PA_V3']
        filt1 = fitsfile[0].header['FILTER1']
        filt2 = fitsfile[0].header['FILTER2']
        if np.floor(posang) == 99:
            if filt2 == 'F814W':
                print filename, filt1, filt2
                fh.write(filename+'\n')

        fitsfile.close()

fh.close()
"""
#
# This next block of code checks if there are equal number of direct and grism images.
# There seem to be more grism exposures than direct images by almost a factor of 2.
#

"""
grism_count = 0
f814w_count = 0

for file in glob.glob(datadir + "*.fits"):
    fitsfile = fits.open(file)
    filename = os.path.basename(file)
    if (filename[4] == '1'):
        filt1 = fitsfile[0].header['FILTER1']
        filt2 = fitsfile[0].header['FILTER2']
        if filt1 == 'G800L':
            grism_count += 1
        else:
            f814w_count += 1
    
    fitsfile.close()

print grism_count, f814w_count
"""

#
# This block of code finds the direct and grism image pairs.
#

grism_filelist = []
f814w_filelist = []
ra_targ = []
dec_targ = []

for file in glob.glob(datadir + "*.fits"):
    fitsfile = fits.open(file)
    filename = os.path.basename(file)
    if (filename[4:6] == '1e') or (filename[4:6] == '1f') or (filename[4:6] == '1g') or (filename[4:6] == '1h'):
        filt1 = fitsfile[0].header['FILTER1']
        filt2 = fitsfile[0].header['FILTER2']
        
        if filt1 == 'G800L':
            grism_filelist.append(filename)
        else:
            f814w_filelist.append(filename)
            ra_targ.append(fitsfile[0].header['RA_TARG'])
            dec_targ.append(fitsfile[0].header['DEC_TARG'])

    fitsfile.close()

matched_grism_list = []

fh = open('G800L_GS1_99.lis', 'wa')

count = 0
for file_dirim in f814w_filelist:
    for file_gr in grism_filelist:
        fitsfile = fits.open(datadir + file_gr)
        
        grism_ra = fitsfile[0].header['RA_TARG']
        grism_dec = fitsfile[0].header['DEC_TARG']
        
        ra_diff = ra_targ[count] - grism_ra
        dec_diff = dec_targ[count] - grism_dec
        
        if abs(ra_diff) < 1e-15:
            if abs(dec_diff) < 1e-15:
                print ra_diff, dec_diff
                print ra_targ[count], grism_ra, dec_targ[count], grism_dec
                print file_dirim, file_gr
                print '\n'
                fh.write(file_gr + ',' + file_dirim.replace('.fits','') + '_1.cat' +  ',' + file_dirim.replace('.fits','') + '_2.cat' +  ',' + file_dirim + '\n')
    count += 1

fh.close()
