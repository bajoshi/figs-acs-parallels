from __future__ import division

import numpy as np
from astropy.io import fits

import os
import sys
import datetime

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages

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

    # Create grid for making grid plots
    gs = gridspec.GridSpec(15,15)
    gs.update(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.0, hspace=0.2)

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

                    print "plotting", extname, "on chip", chip, "in grism image", gr_basename

                    fig = plt.figure()

                    ax1 = fig.add_subplot(gs[:10,:])
                    ax2 = fig.add_subplot(gs[10:,:])

                    lam = spcfile[extname].data['LAMBDA']
                    flam = spcfile[extname].data['FLUX']
                    ferr = spcfile[extname].data['FERROR']
                    contam = spcfile[extname].data['CONTAM']

                    flam -= contam

                    ax1.plot(lam, flam, '-', color='k')
                    ax1.fill_between(lam, flam + ferr, flam - ferr, color='lightgray')

                    ax1.set_yscale('log')

                    ax2.imshow(stpfile[extname].data, origin='lower', cmap='magma')

                    pdf.savefig(bbox_inches='tight')
                    plt.show()

                    plt.clf()
                    plt.cla()
                    plt.close()

        pdf.close()
        break

    sys.exit(0)