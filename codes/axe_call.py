from __future__ import division

from pyraf import iraf
import os
import sys

grism = sys.argv[1]

iraf.stsdas()
iraf.slitless()
iraf.axe()

def axeprepit(Glist,config,sky):
    iraf.stsdas()
    iraf.slitless()
    iraf.axe()
    
    iraf.axeprep.inlist = Glist
    iraf.axeprep.configs = config
    iraf.axeprep.backgr = "no"
    iraf.axeprep.backims = sky
    iraf.axeprep.norm = "no"
    iraf.axeprep.mfwhm = 3.0
    
    iraf.axeprep.run(mode='h')

os.environ['AXE_IMAGE_PATH'] = './DATA_%s/' % (grism)
print "--> variable AXE_IMAGE_PATH   set to ",os.environ['AXE_IMAGE_PATH']

os.environ['AXE_CONFIG_PATH'] = './CONF/'
print "--> variable AXE_CONFIG_PATH  set to ",os.environ['AXE_CONFIG_PATH'] 

os.environ['AXE_OUTPUT_PATH'] = './OUTPUT_NEW_%s/' % (grism)
print "--> variable AXE_OUTPUT_PATH  set to ",os.environ['AXE_OUTPUT_PATH']

os.environ['AXE_DRIZZLE_PATH'] = './DRIZZLE_NEW_%s/'  % (grism)
print "--> variable AXE_DRIZZLE_PATH set to ",os.environ['AXE_DRIZZLE_PATH']
sys.exit(0)

inlist = "%s.lis" % (grism)
config = "%s.test41.conf" % (grism)
#config = "%s.test.conf" % (grism)
#config = "WFC3.IR.%s.V2.0.conf" % (grism)
fwhm = 12./0.12

sky = "WFC3.IR.%s.sky.V1.0.fits"% (grism)
axeprepit(inlist,config,sky)

iraf.axecore(inlist=inlist, configs=config, back="no", extrfwhm=4*fwhm, backfwhm=.0, drzfwhm=3*fwhm, orient="yes",exclude="no", lambda_mark=650.0,cont_model="gauss", model_scale=fwhm, inter_type="linear",lambda_psf=650.0, spectr="yes", weights="yes",sampling="drizzle",slitless_geom="no")
#iraf.drzprep(inlist=inlist, configs=config,opt_extr="YES", back="NO")
#iraf.axedrizzle(inlist=inlist, configs=config, infwhm=fwhm,outfwhm=fwhm*0.95, back="NO", makespc="YES", opt_extr="YES")