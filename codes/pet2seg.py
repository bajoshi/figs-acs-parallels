from __future__ import division

import numpy as np
from astropy.io import fits

import os
import sys

import matplotlib.pyplot as plt

home = os.getenv('HOME')
acspar = home + '/acspar/'
acs_home = home + '/Desktop/FIGS/figs-acs-parallels/'

if __name__ == '__main__':

    # define the pointing
    dir_filt = 'f814w'
    gr_filt = 'g800l'
    field = 'gs1'
    posang = '28'

    # read in PET files
    chip = 2
    sciext = 1
    basename = 'jcoi1mjyq'
    if chip == 1:
        pet = fits.open(acspar + 'OUTPUT_gs1_28/' + basename + '_flc_2.PET.fits')
    elif chip == 2:
        pet = fits.open(acspar + 'OUTPUT_gs1_28/' + basename + '_flc_5.PET.fits')

    grism_image_hdu = fits.open(acspar + 'SAVE/' + basename + '_flc.fits')

    beam_id = '243A'
    segfitsname = acspar + beam_id + '_PETSEG_fwhm0p5.fits'

    bbox_xmin = pet[beam_id].header['BB0X']
    bbox_xmax = pet[beam_id].header['BB1X']
    bbox_ymin = pet[beam_id].header['BB0Y']
    bbox_ymax = pet[beam_id].header['BB1Y']

    print bbox_xmin, bbox_xmax, bbox_ymin, bbox_ymax

    arr = np.ones((2048, 4096)) * 0.5
    # i put in 0.5 just so that its not 0 and 1 in ds9 and I can see the total extent of the array

    for i in range(bbox_xmin, bbox_xmax, 1):
        for j in range(bbox_ymin, bbox_ymax, 1):

            arr[j-1, i-1] = 1  
            # assuming the fits header gave me ds9 referenced pixels .... 
            # so converting them to numpy array indices

    # write to fits
    hdr = pet[beam_id].header

    # put in WCS keywords so that you can see the PET region in ds9
    hdr['WCSAXES']  = grism_image_hdu['SCI', sciext].header['WCSAXES']
    hdr['CRPIX1']   = grism_image_hdu['SCI', sciext].header['CRPIX1']
    hdr['CRPIX2']   = grism_image_hdu['SCI', sciext].header['CRPIX2']
    hdr['CRVAL1']   = grism_image_hdu['SCI', sciext].header['CRVAL1']
    hdr['CRVAL2']   = grism_image_hdu['SCI', sciext].header['CRVAL2']
    hdr['CTYPE1']   = grism_image_hdu['SCI', sciext].header['CTYPE1']
    hdr['CTYPE2']   = grism_image_hdu['SCI', sciext].header['CTYPE2']
    hdr['CD1_1']    = grism_image_hdu['SCI', sciext].header['CD1_1']
    hdr['CD1_2']    = grism_image_hdu['SCI', sciext].header['CD1_2']
    hdr['CD2_1']    = grism_image_hdu['SCI', sciext].header['CD2_1']
    hdr['CD2_2']    = grism_image_hdu['SCI', sciext].header['CD2_2']
    hdr['LTV1']     = grism_image_hdu['SCI', sciext].header['LTV1']
    hdr['LTV2']     = grism_image_hdu['SCI', sciext].header['LTV2']
    hdr['RAW_LTV1'] = grism_image_hdu['SCI', sciext].header['RAW_LTV1']
    hdr['RAW_LTV2'] = grism_image_hdu['SCI', sciext].header['RAW_LTV2']
    hdr['LTM1_1']   = grism_image_hdu['SCI', sciext].header['LTM1_1']
    hdr['LTM2_2']   = grism_image_hdu['SCI', sciext].header['LTM2_2']
    hdr['ORIENTAT'] = grism_image_hdu['SCI', sciext].header['ORIENTAT']
    hdr['RA_APER']  = grism_image_hdu['SCI', sciext].header['RA_APER']
    hdr['DEC_APER'] = grism_image_hdu['SCI', sciext].header['DEC_APER']
    hdr['PA_APER']  = grism_image_hdu['SCI', sciext].header['PA_APER']
    hdr['VAFACTOR'] = grism_image_hdu['SCI', sciext].header['VAFACTOR']
    
    hdu = fits.PrimaryHDU(data=arr, header=hdr)
    hdu.writeto(segfitsname, clobber=True)

    sys.exit(0)