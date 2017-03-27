from __future__ import division
import numpy as np

import os
import sys

home = os.getenv('HOME')
acspar = home + '/acspar/'
acs_home = home + '/Desktop/FIGS/figs-acs-parallels/'

if __name__ == '__main__':

    filt = 'f814w'
    field = 'gs1'
    posang = '28'
    
    catfile = acspar + filt + '_' + field + '_' + posang + '_clipped.cat'
    #catfile = home + '/acspar/IMDRIZZLE_' + field + '_' + posang + '/' + filt + '_' + field + '_' + posang + '.cat'
    regfile = open(catfile.replace('.cat', '.reg'), 'wa')

    header = ['id', 'ra', 'dec']
    cat = np.genfromtxt(catfile, dtype=None, names=header, usecols=(0,4,5))

    for i in range(len(cat)):
        regfile.write('fk5;circle(' + str(cat[i][1]) + ',' + str(cat[i][2]) +\
                      ',1") # color=green width=1' + '\n')

    regfile.close()

    sys.exit(0)