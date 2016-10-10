from __future__ import division

import numpy as np
from astropy.io import fits

import os
import sys
import glob
import shutil

home = os.getenv('HOME')  # Does not have a trailing slash at the end
acs_home = home + '/Desktop/FIGS/figs-acs-parallels/'

def get_unique_filters(fits_path):
    filterlist = []

    for file in glob.glob(fits_path + "*.fits"):

        h = fits.open(file)

        filt1 = h[0].header['FILTER1']
        filt2 = h[0].header['FILTER2']

        if ('CLEAR' in filt1) and (filt2 not in filterlist):
            filterlist.append(filt2)
        elif ('CLEAR' in filt2) and (filt1 not in filterlist):
            filterlist.append(filt1)

    return filterlist

def create_lists(field, field_posangs, field_idx, posang_list, visit_id_list, filename_list):

    for i in range(len(field_posangs)):

        current_posang = field_posangs[i]
        temp = np.around(posang_list[field_idx], decimals=1)
        mat_idx = np.where(temp == current_posang)[0] # Careful! Indices of a sub-array

        # Save filename pairs into files
        fh_606direct = open(acs_home + 'f606w_' + field + '_' + str(int(current_posang)) + '.lis', 'wa')
        fh_814direct = open(acs_home + 'f814w_' + field + '_' + str(int(current_posang)) + '.lis', 'wa')
        fh_grism = open(acs_home + 'g800l_' + field + '_' + str(int(current_posang)) + '.lis', 'wa')

        for filename in filename_list[field_idx][mat_idx]:

            h = fits.open(acs_flc_path + filename)

            filt1 = h[0].header['FILTER1']
            filt2 = h[0].header['FILTER2']

            if (filt1 == 'G800L') or (filt2 == 'G800L'):
                fh_grism.write(filename)
                fh_grism.write('\n')

            elif (filt1 == 'F606W') or (filt2 == 'F606W'):
                fh_606direct.write(filename)
                fh_606direct.write('\n')

            elif (filt1 == 'F814W') or (filt2 == 'F814W'):
                fh_814direct.write(filename)
                fh_814direct.write('\n')

            h.close()

        fh_606direct.close()
        fh_814direct.close()
        fh_grism.close()

    return None

if __name__ == '__main__':
    
    acs_flc_path = "/Volumes/Bhavins_backup/acs_parallels_data/flc/"

    # The HST file naming convention can be found here: https://archive.stsci.edu/hlsp/ipppssoot.html
    
    # Run the line below to get the list of unique filters for any given set of observations stored in fits files
    # uniq_filt = get_unique_filters(acs_flc_path)
    # Result for FIGS ACS parallels:
    # ['G800L', 'F606W', 'F814W', 'F435W']

    # Run the for loop through all files once to get lists of unique pointing coordinates and position angles
    # Run it a second time to get matched pairs of coordinates and position angles.
    posang_list = []
    ra_targ_list = []
    dec_targ_list = []
    visit_id_list = []
    field_list = []
    filename_list = []
    filt1_list = []
    filt2_list = []

    for file in glob.glob(acs_flc_path + "*.fits"):

        h = fits.open(file)

        ra = h[0].header['RA_TARG']
        dec = h[0].header['DEC_TARG']
        posang = h[0].header['PA_V3']
        visit_id = h[0].header['FILENAME'][4:6] # its a string split according to the naming convention
        filename = h[0].header['FILENAME']
        filt1 = h[0].header['FILTER1']
        filt2 = h[0].header['FILTER2']

        if visit_id[0] == '1':
            field = 'gs1'
        elif visit_id[0] == '2':
            field = 'gs2'
        elif visit_id[0] == '3':
            field = 'gn1'
        elif visit_id[0] == '4':
            field = 'gn2'

        ra_targ_list.append(ra)
        dec_targ_list.append(dec)
        posang_list.append(posang)
        visit_id_list.append(visit_id)
        field_list.append(field)
        filename_list.append(filename)
        filt1_list.append(filt1)
        filt2_list.append(filt2)

        h.close()
        
    # Convert to numpy arrays so that I can use numpy operations on them
    posang_list = np.asarray(posang_list)
    ra_targ_list = np.asarray(ra_targ_list)
    dec_targ_list = np.asarray(dec_targ_list)
    visit_id_list = np.asarray(visit_id_list)
    field_list = np.asarray(field_list)
    filename_list = np.asarray(filename_list)
    filt1_list = np.asarray(filt1_list)
    filt2_list = np.asarray(filt2_list)

    # Get the position angles for each field
    gs1_idx = np.where(field_list == 'gs1')[0]
    gs2_idx = np.where(field_list == 'gs2')[0]
    gn1_idx = np.where(field_list == 'gn1')[0]
    gn2_idx = np.where(field_list == 'gn2')[0]

    gs1_posangs = np.around(posang_list[gs1_idx], decimals=1)
    gs2_posangs = np.around(posang_list[gs2_idx], decimals=1)
    gn1_posangs = np.around(posang_list[gn1_idx], decimals=1)
    gn2_posangs = np.around(posang_list[gn2_idx], decimals=1)

    gs1_posangs = np.unique(gs1_posangs)
    gs2_posangs = np.unique(gs2_posangs)
    gn1_posangs = np.unique(gn1_posangs)
    gn2_posangs = np.unique(gn2_posangs)

    # Run through the files again and match the files in the same pointing using the position angle
    create_lists('gs1', gs1_posangs, gs1_idx, posang_list, visit_id_list, filename_list)
    create_lists('gs2', gs2_posangs, gs2_idx, posang_list, visit_id_list, filename_list)
    create_lists('gn1', gn1_posangs, gn1_idx, posang_list, visit_id_list, filename_list)
    create_lists('gn2', gn2_posangs, gn2_idx, posang_list, visit_id_list, filename_list)

    sys.exit(0)