from __future__ import division

import numpy as np
from astropy.io import fits

import os
import sys

home = os.getenv('HOME')
acspar = home + '/acspar/'
acs_home = home + '/Desktop/FIGS/figs-acs-parallels/'

if __name__ == '__main__':

    # define the pointing
    dir_filt = 'f814w'
    gr_filt = 'g800l'
    field = 'gs1'
    posang = '28'

    # read in master sky images
    msky_chip1_hdu = fits.open(acspar + 'CONF/ACS.WFC.CHIP1.msky.1.fits')
    msky_chip2_hdu = fits.open(acspar + 'CONF/ACS.WFC.CHIP2.msky.1.fits')

    msky_chip1 = msky_chip1_hdu[0].data
    msky_chip2 = msky_chip2_hdu[0].data

    # loop over all grism images for a given pointing and subtract the master sky from each chip
    grism_im_list = open(acspar + gr_filt + '_' + dir_filt + '_' + field + '_' + posang + '.lis', 'r')

    for grism_im in grism_im_list.read().splitlines():

        print "working with image:", grism_im

        # open grism image
        fitsname = acspar + 'IMDRIZZLE_' + field + '_' + posang + '/' + grism_im
    	grism_im_hdu = fits.open(fitsname)

        # find scale factor that optimizes chi2 and subtract
        num_a1 += np.sum(grism_im_hdu[4].data * msky_chip1 / grism_im_hdu[5].data**2)
        den_a1 += np.sum(msky_chip1**2 / grism_im_hdu[5].data**2)

        num_a2 += np.sum(grism_im_hdu[1].data * msky_chip2 / grism_im_hdu[2].data**2)
        den_a2 += np.sum(msky_chip2**2 / grism_im_hdu[2].data**2)

    	a1 = num_a1 / den_a1
    	a2 = num_a2 / den_a2

    	grism_im_hdu[1].data = grism_im_hdu[1].data - a2 * msky_chip2
    	grism_im_hdu[4].data = grism_im_hdu[4].data - a1 * msky_chip1

        # rewrite grism image
    	grism_im_hdu.writeto(fitsname, clobber=True)
    	grism_im_hdu.close()

    sys.exit(0)