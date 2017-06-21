from __future__ import division

import numpy as np
from astropy.io import fits
from astropy.visualization import (ZScaleInterval, LogStretch, ImageNormalize)

import os
import sys
import datetime

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.axes_grid.inset_locator import inset_axes

home = os.getenv('HOME')  # Does not have a trailing slash at the end
figs_acs_dir = home + '/Desktop/FIGS/figs-acs-parallels/'
acspar = home + '/acspar/'
axeconf = acspar + 'CONF/'
savedir = home + '/acspar/SAVE/'

stacking_analysis_codes = home + '/Desktop/FIGS/stacking-analysis-pears/codes/'

sys.path.append(stacking_analysis_codes)
import fast_chi2_jackknife as fcj

def plot_indiv_spec(obj, chip, gr_im_name):

    gr_basename = gr_im_name.split('.')[0]

    ext = 'BEAM_' + str(obj) + 'A'

    if chip == 1:
        spcfile = fits.open(acspar + 'OUTPUT_gs1_28/' + gr_basename + '_5_opt.SPC.fits')
        stpfile = fits.open(acspar + 'OUTPUT_gs1_28/' + gr_basename + '_5.STP.fits')
    elif chip == 2:
        spcfile = fits.open(acspar + 'OUTPUT_gs1_28/' + gr_basename + '_2_opt.SPC.fits')
        stpfile = fits.open(acspar + 'OUTPUT_gs1_28/' + gr_basename + '_2.STP.fits')

    lam = spcfile[ext].data['LAMBDA']
    flam = spcfile[ext].data['COUNT']
    ferr = spcfile[ext].data['ERROR']
    contam = spcfile[ext].data['CONTAM']

    flam -= contam

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(lam, flam, '-', color='k')
    ax.fill_between(lam, flam + ferr, flam - ferr, color='lightgray')

    ax.set_yscale('log')

    print repr(stpfile[ext].header)

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.imshow(stpfile[ext].data, vmin=50, vmax=150, origin='lower')
    plt.show()

    return None

if __name__ == '__main__':
    
    # define the pointing
    dir_filt = 'f814w'
    gr_filt = 'g800l'
    field = 'gs1'
    posang = '28'

    # read in catalog to apply magnitude cuts
    names_header = ['num','mag','mag_err','re','x','y','ra','dec','xw','yw','a_im','b_im','theta_im','theta_w','aw','bw']

    catfile = acspar + 'IMDRIZZLE_' + field + '_' + posang + '/' + dir_filt + '_' + field + '_' + posang + '.cat'
    cat = np.genfromtxt(catfile, dtype=None, names=names_header, skip_header=16)

    # read in science image    
    sci_im_name = acspar + 'IMDRIZZLE_' + field + '_' + posang + '/' + dir_filt + '_' + field + '_' + posang + '_sci.fits'
    sci_im = fits.open(sci_im_name)

    # Create grid for making grid plots
    gs = gridspec.GridSpec(3,1, height_ratios=[1,0.05,0.3], width_ratios=[1])
    gs.update(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.02, hspace=0.02)

    # open lists
    gr_im_file = open(acspar + gr_filt + '_' + dir_filt + '_' + field + '_' + posang + '.lis', 'r')
    dir_im_file = open(acspar + dir_filt + '_' + field + '_' + posang + '.lis', 'r')

    dir_im_list = []
    gr_im_list = []

    # first create two lists of matched dir and grism pairs 
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

            h_dir.close()
            h_gr.close()

    # loop over each source in each grism image and plot 
    for j in range(len(gr_im_list)):

        gr_basename = gr_im_list[j].split('.')[0]

        pdfname = acspar + 'visualization/' + gr_basename + '.pdf'
        pdf = PdfPages(pdfname)

        spc1 = fits.open(acspar + 'OUTPUT_gs1_28/' + gr_basename + '_2_opt.SPC.fits')
        stp1 = fits.open(acspar + 'OUTPUT_gs1_28/' + gr_basename + '_2.STP.fits')

        spc2 = fits.open(acspar + 'OUTPUT_gs1_28/' + gr_basename + '_5_opt.SPC.fits')
        stp2 = fits.open(acspar + 'OUTPUT_gs1_28/' + gr_basename + '_5.STP.fits')

        chip1_spc_totalext = fcj.get_total_extensions(spc2)
        chip1_stp_totalext = fcj.get_total_extensions(stp2)

        chip2_spc_totalext = fcj.get_total_extensions(spc1)
        chip2_stp_totalext = fcj.get_total_extensions(stp1)

        for chip in range(1,3):

            if chip == 1:
                total_ext = chip1_spc_totalext
                spcfile = spc2
                stpfile = stp2
            elif chip == 2:
                total_ext = chip2_spc_totalext
                spcfile = spc1
                stpfile = stp1

            for k in range(1,total_ext+1):

                extname = spcfile[k].header['EXTNAME']

                if 'A' == extname[-1]:

                    obj_id = int(extname.split('BEAM_')[-1].split('A')[0])
                    obj_idx = np.where(cat['num'] == obj_id)[0]

                    f814w_mag = float(cat['mag'][obj_idx])

                    if f814w_mag <= 19:

                        print "plotting", extname, "on chip", chip, "in grism image", gr_basename,\
                         "with F814W mag", f814w_mag

                        # get stamp image
                        pix_x = cat['x'][obj_idx]
                        pix_y = cat['y'][obj_idx]
                        arr_x = pix_y - 1
                        arr_y = pix_x - 1
                        width = spcfile[extname].header['WIDTH']
                        width += 1.25*width

                        stamp = sci_im[0].data[arr_x-width:arr_x+width+1, arr_y-width:arr_y+width+1]

                        # plot figure
                        fig = plt.figure()

                        ax1 = fig.add_subplot(gs[0,0])
                        ax2 = fig.add_subplot(gs[2,0])

                        lam = spcfile[extname].data['LAMBDA']
                        flam = spcfile[extname].data['FLUX']
                        ferr = spcfile[extname].data['FERROR']
                        contam = spcfile[extname].data['CONTAM']

                        flam -= contam

                        # plot 1d spectrum
                        ax1.plot(lam, flam, '-', color='k')
                        ax1.fill_between(lam, flam + ferr, flam - ferr, color='lightgray')

                        lam_low = 5500
                        lam_high = 10000

                        lam_low_idx = np.argmin(abs(lam-lam_low))
                        lam_high_idx = np.argmin(abs(lam-lam_high))

                        ax1.set_xlim(lam_low, lam_high)
                        ax1.set_ylim(np.nanmin(flam[lam_low_idx:lam_high_idx+1]), np.nanmax(flam[lam_low_idx:lam_high_idx+1]))

                        ax1.minorticks_on()
                        ax1.tick_params('both', width=1, length=3, which='minor')
                        ax1.tick_params('both', width=1, length=4.7, which='major')

                        # plot inset stamp image
                        ax_inset = inset_axes(ax1,
                                            width="30%", # width = 30% of parent_bbox
                                            height=0.5, # height : 1 inch 
                                            loc=1)

                        norm = ImageNormalize(stamp, interval=ZScaleInterval(), stretch=LogStretch())

                        ax_inset.imshow(stamp, origin='lower', cmap='Greys', norm=norm)
                        ax_inset.get_xaxis().set_ticklabels([])
                        ax_inset.get_yaxis().set_ticklabels([])

                        # plot 2d spectrum
                        twod_spec = stpfile[extname].data
                        norm = ImageNormalize(twod_spec, interval=ZScaleInterval(), stretch=LogStretch())
                        ax2.imshow(twod_spec, origin='lower', cmap='Greys', aspect='auto', norm=norm)

                        pdf.savefig(bbox_inches='tight')
                        #plt.show()

                        plt.clf()
                        plt.cla()
                        plt.close()

        pdf.close()
        break

    sys.exit(0)