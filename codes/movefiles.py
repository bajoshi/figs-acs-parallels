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
    flcdir = "/Volumes/Bhavins_backup/acs_parallels_data/flc/"
    listdir = acs_home
    
    ##############
    ### Move files to SAVE to have a pristine copy and to IMDRIZZLE directory for astrodrizzle
    ##############
    
    # --------------------------------------------
    # This is for the direct image files list
    filt = 'f814w'
    
    fh = open(listdir + filt + field + posang + '.lis', 'r')

    print "Will copy the following direct image files to IMDRIZZLE and SAVE"
    print fh.read().splitlines()
    
    for file in fh.read().splitlines():
        
        # Check if file exists and if it doesn't then copy it.
        if os.path.isfile(savdir + file):
            print file, "exists in SAVE. Checking IMDRIZZLE next."
        elif not os.path.isfile(savdir + file):
            print "Copying grism image", file, "from FLC directory to SAVE"
            shutil.copy(flcdir + file, savdir + file)  # source is first arg and destination is second

        if os.path.isfile(imdriz + file):
            print file, "exists in IMDRIZZLE. Moving to next file in the list."
        elif not os.path.isfile(imdriz + file):
            print "Copying direct image", file, "from FLC directory to IMDRIZZLE"
            shutil.copy(flcdir + file, imdriz + file)
    
    shutil.copy(listdir + filt + field + posang + '.lis', imdriz + filt + '.lis')
    print "\n"
    # this second copy line is required because the combined drizzled direct image will be made in the IMDRIZZLE folder
    
    # --------------------------------------------
    # This is for the grism image files list
    
    filt = 'g800l'
    
    fh = open(listdir + filt + '_f814w' + field + posang + '.lis', 'r')
    
    print "Will copy the following grism image files to IMDRIZZLE and SAVE"
    print fh.read().splitlines()

    for file in fh.read().splitlines():

        # Check if file exists and if it doesn't then copy it.
        if os.path.isfile(savdir + file):
            print file, "exists in SAVE. Checking IMDRIZZLE next."
        elif not os.path.isfile(savdir + file):
            print "Copying grism image", file, "from FLC directory to SAVE"
            shutil.copy(flcdir + file, savdir + file)

        if os.path.isfile(imdriz + file):
            print file, "exists in IMDRIZZLE. Moving to next file in the list."
        elif not os.path.isfile(imdriz + file):
            print "Copying grism image", file, "from FLC directory to IMDRIZZLE"
            shutil.copy(flcdir + file, imdriz + file)

    shutil.copy(listdir + filt + field + posang + '.lis', imdriz + filt + '.lis')
    print "\n"
    # this second copy line is required because the combined drizzled grism image will be made in the IMDRIZZLE folder
    
    sys.exit(0)

