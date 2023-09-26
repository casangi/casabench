from collections import OrderedDict
import re, os, shutil
from casatools import ctsys
from casatasks import casalog
from casatasks import tclean
from casatestutils.imagerhelpers import TestHelpers
th = TestHelpers()

# ASV iteration control (https://asv.readthedocs.io/en/stable/benchmarks.html#benchmark-attributes)
number = 1            # i.e., always run the setup and teardown methods
repeat = 10           # insist upon 10 runs
rounds = 1            # amount of instances a "repeat block" is run to collect samples
min_run_count = 10    # enforce the min_repeat * rounds setting is met
timeout = 3600        # conservative 1hr hard cap for duration of a single test execution

# Test datasets; root directory is read from config.py
datapath = ctsys.resolve("unittest/tclean/")

class BaseTcleanSetup():
    epsilon = 0.05
    cfcache = 'cfcach'
    msfile = ""
    img = "tst"
    imsize = 100
    # To use subdir in the output image names in some tests (CAS-10937)
    img_subdir = 'refimager_tst_subdir'
    parallel = False
    nnode = 0

    # Copy and cleanup datasets
    def prepData(self, msname=""):
        if msname != "":
            self.msfile = msname
        if (os.path.exists(self.msfile)):
            os.system('rm -rf ' + self.msfile)
        shutil.copytree(os.path.join(datapath, self.msfile), self.msfile)

class MemoryWideFieldAWP(BaseTcleanSetup):
    """Peak memory benchmarking tests of tclean on widefield using awproject"""
    def setup(self):
        self.prepData("refim_mawproject.ms")

    def teardown(self):
        os.system('rm -rf ' + self.img_subdir)
        os.system('rm -rf ' + self.img + '*')
        if (os.path.exists(self.msfile)):
            os.system('rm -rf ' + self.msfile)

    def peakmem_cube_awproject_hogbom(self):
        """tclean: Cube with AW-Projection  and rotation off - test_widefield_aproj_cube"""
        ret = tclean(vis=self.msfile, field='*', imagename=self.img, imsize=512, cell='10.0arcsec',
                     phasecenter="J2000 19:59:28.500 +40.44.01.50",specmode='cube', niter=1, gain=1.0,
                     gridder='awproject', cfcache=self.img + '.cfcache',wbawp=True,conjbeams=False,
                     psterm=False, computepastep=360.0, rotatepastep=360.0, deconvolver='hogbom',
                     parallel=False)
