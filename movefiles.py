import glob, os, shutil

imdriz = '/Users/baj/acspar/IMDRIZZLE/'
savdir = '/Users/baj/acspar/SAVE/'
datadir = '/Users/baj/Documents/acs_parallels_data/flc/'
listdir = '/Users/baj/Documents/acs_aXe/'

##############
### Move files to SAVE to have a pristine copy and to IMDRIZZLE directory for astrodrizzle
##############

# --------------------------------------------
# This is for the direct image files list

filt = 'F814W'
field = '_GS1'
posang = '_99'

fh = open(listdir + filt + field + posang + '.lis', 'r')

for file in fh.read().splitlines():
    print "Copying direct image", file, "from FLC directory to SAVE and IMDRIZZLE"
    shutil.copy(datadir + file, imdriz + file) # source is first arg and destination is second
    shutil.copy(datadir + file, savdir + file)

shutil.copy(listdir + filt + field + posang + '.lis', imdriz + filt + '.lis')
# this second copy line is required because the combined drizzled image will be made in the IMDRIZZLE folder

# --------------------------------------------
# This is for the grism image files list
# These need to be copied to SAVE but not to IMDRIZZLE. IMDRIZZLE only needs the direct image files

filt = 'G800L_gr' # the _gr is for the list that has only the grism image filenames
field = '_GS1'
posang = '_99'

fh = open(listdir + filt + field + posang + '.lis', 'r')

for file in fh.read().splitlines():
    print "Copying grism image", file, "from FLC directory to SAVE"
    shutil.copy(datadir + file, savdir + file)