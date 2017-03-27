from __future__ import division

import numpy as np
from astropy.io import fits

import os
import sys
import datetime

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

home = os.getenv('HOME')  # Does not have a trailing slash at the end
figs_acs_dir = home + '/Desktop/FIGS/figs-acs-parallels/'
acspar = home + '/acspar/'
axeconf = acspar + 'CONF/'

if __name__ == '__main__':
    
    spc1 = fits.open(acspar + 'OUTPUT_NEW_gs1_28/jcoi1mjyq_flc_2.SPC.fits')
    stp1 = fits.open(acspar + 'OUTPUT_NEW_gs1_28/jcoi1mjyq_flc_2.STP.fits')

    spc2 = fits.open(acspar + 'OUTPUT_NEW_gs1_28/jcoi1mjyq_flc_5.SPC.fits')
    stp2 = fits.open(acspar + 'OUTPUT_NEW_gs1_28/jcoi1mjyq_flc_5.STP.fits')

    ext = 'BEAM_' + str(128) + 'A'

    lam = spc2[ext].data['LAMBDA']
    flam = spc2[ext].data['COUNT']
    ferr = spc2[ext].data['ERROR']
    contam = spc2[ext].data['CONTAM']

    sens_curve = np.genfromtxt(axeconf + 'ACS.WFC.1st.sens.7.dat', dtype=None, names=True, skip_header=4)
    # sensitivity is for the 1st order spectrum
    # sensitivity given in (e s-1)/(erg s-1 cm-2 A-1)
    senslam = sens_curve['Lambda']
    sens = sens_curve['sensitivity']
    senserr = sens_curve['error']

    print flam[100:120]
    print ferr[100:120]

    for i in range(len(lam)):

        idx = np.argmin(abs(senslam - lam[i]))
        flam[i] /= sens[idx]
        ferr[i] /= sens[idx]
        contam[i] /= sens[idx]

    print flam[100:120]
    print ferr[100:120]

    #flam -= contam

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(lam, flam, '-', color='k')
    ax.fill_between(lam, flam + ferr, flam - ferr, color='lightgray')

    ax.set_yscale('log')

    plt.show()

    sys.exit(0)