from astropy.io import fits

import glob
import os
import shutil
import sys

datadir = '/Volumes/Bhavins_backup/acs_parallels_data/flc'


if __name__ == '__main__':
    
    #
    # This block of code finds the direct and grism image pairs.
    #
    
    ###
    
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

