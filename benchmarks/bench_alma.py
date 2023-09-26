import os, shutil
from casatools import ctsys
from casatasks import tclean

# ASV iteration control (https://asv.readthedocs.io/en/stable/benchmarks.html#benchmark-attributes)
number = 1            # i.e., always run the setup and teardown methods

# Test datasets; root directory is read from config.py
datapath = ctsys.resolve("stakeholder/alma/")

class BaseMosaicSetup():
    img = "tst"
    parallel = False

    # Copy and cleanup datasets
    def prepData(self, msname=""):
        if msname != "":
            self.msfile = msname
        if (os.path.exists(self.msfile)):
            os.system('rm -rf ' + self.msfile)
        shutil.copytree(os.path.join(datapath, self.msfile), self.msfile)

class BaseMosaic(BaseMosaicSetup):
    """Runtime benchmarking tests adapted from ALMA stakeholder tests, mosaic use case"""
    def setup(self):
        self.prepData("2018.1.00879.S_tclean.ms")

    def teardown(self):
        os.system('rm -rf ' + self.img + '*')
        if (os.path.exists(self.msfile)):
            os.system('rm -rf ' + self.msfile)

    def time_mosaic_cube_eph_pcwdT_restart(self):
        """Mosaic ephemeris cube imaging with briggsbwtaper - field Venus, spw 45"""
        ret = tclean(vis=self.msfile, imagename=self.img+"0", field='Venus', spw=['1'], antenna=['0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46'], scan=['7,11'], intent='OBSERVE_TARGET#ON_SOURCE', datacolumn='corrected', imsize=[480, 420], cell=['0.14arcsec'], phasecenter='TRACKFIELD', stokes='I', specmode='cubesource', nchan=948, start='261.7643758544GHz', width='0.2441755MHz', perchanweightdensity=True, gridder='mosaic', mosweight=True, usepointing=False, pblimit=0.2, deconvolver='hogbom', restoration=False, restoringbeam='common', pbcor=False, weighting='briggs', robust=0.5, npixels=0, niter=0, threshold='0.0mJy', nsigma=0.0, usemask='auto-multithresh', sidelobethreshold=2.0, noisethreshold=4.25, lownoisethreshold=1.5, negativethreshold=15.0, minbeamfrac=0.3, growiterations=50, dogrowprune=True, minpercentchange=1.0, fastnoise=False, savemodel='none', parallel=self.parallel, verbose=True)
        # restart the tclean call to actually perform deconvolution
        ret = tclean(vis=self.msfile, imagename=self.img+"0", field='Venus', spw=['1'], antenna=['0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46'],scan=['7,11'], intent='OBSERVE_TARGET#ON_SOURCE', datacolumn='corrected', imsize=[480, 420], cell=['0.14arcsec'], phasecenter='TRACKFIELD', stokes='I', specmode='cubesource', nchan=948, start='261.7643758544GHz', width='0.2441755MHz', perchanweightdensity=True, gridder='mosaic', mosweight=True, usepointing=False, pblimit=0.2, deconvolver='hogbom', restoration=True, restoringbeam='common', pbcor=True, weighting='briggs', robust=0.5, npixels=0, niter=700000, threshold='0.0106Jy', nsigma=0.0, usemask='auto-multithresh', sidelobethreshold=2.0, noisethreshold=4.25, lownoisethreshold=1.5, negativethreshold=15.0, minbeamfrac=0.3, growiterations=50, dogrowprune=True, minpercentchange=1.0, fastnoise=False, restart=True, savemodel='none', calcres=False, calcpsf=False, parallel=self.parallel, verbose=True)
    time_mosaic_cube_eph_pcwdT_restart.version = "CAS-14086"
    time_mosaic_cube_eph_pcwdT_restart.repeat = 3 # insist that this long test is run 3x
    time_mosaic_cube_eph_pcwdT_restart.rounds = 1
    time_mosaic_cube_eph_pcwdT_restart.min_run_count = 1
    time_mosaic_cube_eph_pcwdT_restart.timeout = 14400 # raise to 4hr hard cap since this is a long test
