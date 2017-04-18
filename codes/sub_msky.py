from __future__ import division

import numpy as np
from astropy.io import fits
import numpy.ma as ma

import os
import sys

home = os.getenv('HOME')
acspar = home + '/acspar/'
acs_home = home + '/Desktop/FIGS/figs-acs-parallels/'
savedir = home + '/acspar/SAVE/'

stacking_analysis_codes = home + '/Desktop/FIGS/stacking-analysis-pears/codes/'

sys.path.append(stacking_analysis_codes)
import fast_chi2_jackknife as fcj

def getmask(chip1_cat, chip2_cat):

    # create empty zeros array which will have 1's where sources are to be masked
    chip1_mask = np.zeros((2048, 4096))
    chip2_mask = np.zeros((2048, 4096))

    # create coordinate array and grid to easily measure radius 
    xarr = np.arange(4096)
    yarr = np.arange(4096)

    X, Y = np.meshgrid(xarr, yarr)

    allcats = [chip1_cat, chip2_cat]
    allmasks = [chip1_mask, chip2_mask]

    # loop over all sources
    for u in range(len(allcats)):

        for i in range(len(allcats[u])):

            xcen = allcats[u]['x'][i]
            ycen = allcats[u]['y'][i]

            eff_rad = allcats[u]['re'][i]

            rad = np.sqrt((X - xcen)**2 + (Y - ycen)**2)
            idx_list = np.where(rad <= eff_rad)

            #print xcen, ycen, eff_rad, len(idx_list[0]), len(idx_list[1])

            allmasks[u][idx_list[0] - 2048*u, idx_list[1]] = 1.0

    return chip1_mask, chip2_mask

def save_chip_masks(chip1_mask, chip2_mask, dir_im_hdu, dir_im):

    hdr1 = dir_im_hdu[4].header
    hc1 = fits.PrimaryHDU(data=chip1_mask, header=hdr1)
    basename = dir_im.split('.')[0]
    hc1.writeto(savedir + basename + '_chip1_mask.fits', clobber=True)

    hdr2 = dir_im_hdu[1].header
    hc2 = fits.PrimaryHDU(data=chip2_mask, header=hdr2)
    basename = dir_im.split('.')[0]
    hc2.writeto(savedir + basename + '_chip2_mask.fits', clobber=True)

    return None

def getmask_from_dir(dir_im_list, gr_im_list):

    # name header for source catalogs
    names_header = ['num','mag','mag_err','re','x','y','ra','dec','xw','yw','a_im','b_im','theta_im','theta_w','aw','bw']

    for j in range(len(dir_im_list)):

        dir_im = dir_im_list[j]
        gr_im = gr_im_list[j]

        print "working with direct and grism image pair:", dir_im, gr_im

        # read in catalogs from iolprep
        dir_im_basename = dir_im.replace('.fits','')

        chip1_catname = acspar + 'IMDRIZZLE_' + field + '_' + posang + '/' + dir_im_basename + '_2.cat'
        chip2_catname = acspar + 'IMDRIZZLE_' + field + '_' + posang + '/' + dir_im_basename + '_1.cat'

        chip1_cat = np.genfromtxt(chip1_catname, dtype=None, names=names_header, skip_header=16)
        chip2_cat = np.genfromtxt(chip2_catname, dtype=None, names=names_header, skip_header=16)

        print "Chip 1 and 2 have total sources:", len(chip1_cat), len(chip2_cat)
        print "Creating mask for sources now..."

        # the next line of code allows you to 
        # create masks based simply on the direct image
        # this isn't entirely correct but you can then do the background 
        # subtraction without having to run axecore to generate PETs
        chip1_mask, chip2_mask = getmask(chip1_cat, chip2_cat)

        # save mask if you want to compare in ds9
        #save_chip_masks(chip1_mask, chip2_mask, dir_im_hdu, dir_im)

    return chip1_mask, chip2_mask

if __name__ == '__main__':

    # write code to change image in both SAVE and IMDRIZZLE
    # put in code to change HISTORY keyword in header to 
    # say that the background was subtracted

    # define the pointing
    dir_filt = 'f814w'
    gr_filt = 'g800l'
    field = 'gs1'
    posang = '28'

    # first create two lists of matched dir and grism pairs 
    gr_im_file = open(acspar + gr_filt + '_' + dir_filt + '_' + field + '_' + posang + '.lis', 'r')
    dir_im_file = open(acspar + dir_filt + '_' + field + '_' + posang + '.lis', 'r')

    dir_im_list = []
    gr_im_list = []

    for dir_im in dir_im_file.read().splitlines():
        
        gr_im_file.seek(0)

        for gr_im in gr_im_file.read().splitlines():

            h_dir = fits.open(savedir + dir_im)
            h_gr = fits.open(savedir + gr_im)

            crval1_dir = h_dir[1].header['CRVAL1']
            crval2_dir = h_dir[1].header['CRVAL2']

            crval1_gr = h_gr[1].header['CRVAL1']
            crval2_gr = h_gr[1].header['CRVAL2']

            if (crval1_dir == crval1_gr) and (crval2_dir == crval2_gr):
                dir_im_list.append(dir_im)
                gr_im_list.append(gr_im)
                #print crval1_dir, crval1_gr, crval2_dir, crval2_gr
                #print dir_im, gr_im

            h_dir.close()
            h_gr.close()

    # read in master sky images
    msky_chip1_hdu = fits.open(acspar + 'CONF/ACS.WFC.CHIP1.msky.1.fits')
    msky_chip2_hdu = fits.open(acspar + 'CONF/ACS.WFC.CHIP2.msky.1.fits')

    msky_chip1 = msky_chip1_hdu[0].data
    msky_chip2 = msky_chip2_hdu[0].data

    # loop over all grism images for a given pointing and subtract the master sky from each chip
    for gr_im in gr_im_list:

        print "working with grism image", gr_im

        # create empty zeros array which will have 1's where sources are to be masked
        chip1_mask = np.zeros((2048, 4096))
        chip2_mask = np.zeros((2048, 4096))

        allmasks = [chip1_mask, chip2_mask]

        gr_basename = gr_im.split('.')[0]

        spc1 = fits.open(acspar + 'OUTPUT_gs1_28/' + gr_basename + '_2_opt.SPC.fits')
        spc2 = fits.open(acspar + 'OUTPUT_gs1_28/' + gr_basename + '_5_opt.SPC.fits')

        chip1_spc_totalext = fcj.get_total_extensions(spc2)
        chip2_spc_totalext = fcj.get_total_extensions(spc1)

        for chip in range(1,3):

            if chip == 1:
                total_ext = chip1_spc_totalext
                spcfile = spc2
            elif chip == 2:
                total_ext = chip2_spc_totalext
                spcfile = spc1

            for k in range(1,total_ext+1):

                extname = spcfile[k].header['EXTNAME']

                xmin = spcfile[extname].header['BB0X']
                xmax = spcfile[extname].header['BB1X']
                ymin = spcfile[extname].header['BB0Y']
                ymax = spcfile[extname].header['BB1Y']

                allmasks[chip-1][ymin-1:ymax-1+1, xmin-1:xmax-1+1] = 1.0
                # the -1 is to convert ds9 x and y to array col and row respectively
                # the +1 is to include the final row and col which the python array notation
                # would otherwise skip.

        print "Masking done. Subtracting background now..."

        # I need to read in the direct image and figure out the background from there
        # and then apply the background subtraction to the grism image
        # open grism image
        gr_filename = acspar + 'DATA_' + field + '_' + posang + '/' + gr_im
        gr_im_hdu = fits.open(gr_filename)

        chip1_sci = gr_im_hdu[4].data
        chip1_err = gr_im_hdu[5].data

        chip2_sci = gr_im_hdu[1].data
        chip2_err = gr_im_hdu[2].data

        chip1_sci = ma.array(chip1_sci, mask=chip1_mask)
        chip1_err = ma.array(chip1_err, mask=chip1_mask)

        chip2_sci = ma.array(chip2_sci, mask=chip2_mask)
        chip2_err = ma.array(chip2_err, mask=chip2_mask)

        # find scale factor that optimizes chi2 and subtract
        num_a1, den_a1, num_a2, den_a2 = 0, 0, 0, 0

        num_a1 = np.sum(chip1_sci * msky_chip1 / chip1_err**2)
        den_a1 = np.sum(msky_chip1**2 / chip1_err**2)

        num_a2 = np.sum(chip2_sci * msky_chip2 / chip2_err**2)
        den_a2 = np.sum(msky_chip2**2 / chip2_err**2)

        a1 = num_a1 / den_a1
        a2 = num_a2 / den_a2

        gr_im_hdu[1].data = gr_im_hdu[1].data - a2 * msky_chip2
        gr_im_hdu[4].data = gr_im_hdu[4].data - a1 * msky_chip1

        # divide by exptime
        exptime = gr_im_hdu[0].header['EXPTIME']

        gr_im_hdu[1].data /= exptime
        gr_im_hdu[4].data /= exptime      

        gr_im_hdu[2].data /= exptime
        gr_im_hdu[5].data /= exptime 

        # rewrite grism image
        gr_im_hdu.writeto(gr_filename, clobber=True)
        gr_im_hdu.close()
        print "Done."

    sys.exit(0)