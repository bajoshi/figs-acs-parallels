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

if __name__ == '__main__':
	
	spc = fits.open(acspar + 'OUTPUT_gs1_28/jcoi1mjyq_flc_2.SPC.fits')
	stp = fits.open(acspar + 'OUTPUT_gs1_28/jcoi1mjyq_flc_2.STP.fits')

    fig = plt.figure()