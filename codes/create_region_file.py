from __future__ import division
import numpy as np

import os
import sys

home = os.getenv('HOME')
acspar = home + '/acspar/'
acs_home = home + '/Desktop/FIGS/figs-acs-parallels/'

if __name__ == '__main__':

    dir_filt = 'f814w'
    field = 'gs1'
    posang = '28'
    
    catfile = acspar + 'IMDRIZZLE_' + field + '_' + posang + '/' + dir_filt + '_' + field + '_' + posang + '_prep.cat'
    regfile = open(catfile.replace('.cat', '.reg'), 'wa')

    header = ['id', 'ra', 'dec']
    cat = np.genfromtxt(catfile, dtype=None, names=header, usecols=(0,6,7))

    for i in range(len(cat)):
        regfile.write('fk5;circle(' + str(cat[i][1]) + ',' + str(cat[i][2]) +\
                      ',1") # color=green width=1 text = {' + str(cat[i][0]) + '};' + '\n')

    regfile.close()

    sys.exit(0)