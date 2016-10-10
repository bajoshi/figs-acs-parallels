import glob
import os
import sys
import shutil

home = os.getenv('HOME')  # Does not have a trailing slash at the end
acs_home = home + '/Desktop/FIGS/figs-acs-parallels/'

if __name__ == '__main__':

    # Change these two variables below depending on the field and PA you are working with.
    field = '_gs1'
    posang = '_28'

    imdriz = home + '/acspar/IMDRIZZLE' + field + posang + '/'
    savdir = os.getenv('AXE_SAVEDIR_PATH') + '/'
    datadir = "/Volumes/Bhavins_backup/acs_parallels_data/flc/"
    listdir = acs_home
    
    ##############
    ### Move files to SAVE to have a pristine copy and to IMDRIZZLE directory for astrodrizzle
    ##############
    
    # --------------------------------------------
    # This is for the direct image files list
    
    filt = 'f814w'
    
    fh = open(listdir + filt + field + posang + '.lis', 'r')
    
    for file in fh.read().splitlines():
        print "Copying direct image", file, "from FLC directory to IMDRIZZLE and SAVE"
        shutil.copy(datadir + file, imdriz + file) # source is first arg and destination is second
        shutil.copy(datadir + file, savdir + file)
    
    shutil.copy(listdir + filt + field + posang + '.lis', imdriz + filt + '.lis')
    print "\n"
    # this second copy line is required because the combined drizzled image will be made in the IMDRIZZLE folder
    
    # --------------------------------------------
    # This is for the grism image files list
    # These need to be copied to SAVE but not to IMDRIZZLE. IMDRIZZLE only needs the direct image files
    
    filt = 'g800l'
    
    fh = open(listdir + filt + field + posang + '.lis', 'r')
    
    for file in fh.read().splitlines():
        print "Copying grism image", file, "from FLC directory to SAVE"
        shutil.copy(datadir + file, savdir + file)
    
    sys.exit(0)

