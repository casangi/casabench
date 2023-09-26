import os, shutil, glob
from casatools import ctsys
from casatasks import tsdimaging as sdimaging

# ASV iteration control (https://asv.readthedocs.io/en/stable/benchmarks.html#benchmark-attributes)
number = 1            # i.e., always run the setup and teardown methods
repeat = 10           # insist on 10 iterations
rounds = 1            # amount of instances a "repeat block" is run to collect samples
min_run_count = 10    # enforce the min_repeat * rounds setting is met
timeout = 3600        # conservative 1hr hard cap should never be met for these test cases

class DataSetUp():

    datapath = ctsys.resolve("unittest/tsdimaging/")

    def setup_basic(self):
        self.vis = "sdimaging_copy.ms"
        self.out = "sdimagingTest.im"

        if os.path.exists(self.vis):
            shutil.rmtree(self.vis, ignore_errors=True)

        existing_images = [ff for ff in glob.glob(self.out+"*")]
        for fname in existing_images:
            os.system(f"rm -rf {fname}")

        # working with a copy of the input MS in all cases to avoid column writes
        shutil.copytree(os.path.join(self.datapath, 'sdimaging.ms'), self.vis)

    def setup_ephemeris(self):
        self.vis = 'ephemtest.spw18_copy.ms'
        self.ephtab = self.vis + '/FIELD/EPHEM0_Sol_58327.6.tab'
        self.out = 'sdimagingTest_eph.im'

        if os.path.exists(self.vis):
            shutil.rmtree(self.vis, ignore_errors=True)

        existing_images = [ff for ff in glob.glob(self.out+"*")]
        for fname in existing_images:
            os.system(f"rm -rf {fname}")

        # working with a copy of the input MS in all cases to avoid column writes
        shutil.copytree(os.path.join(self.datapath, 'ephemtest.spw18.ms'), self.vis)

class Ephemeris(DataSetUp):
    """Benchmark runtime of tsdimaging on tracking moving objects (ephemeris data)
    Adapted from test_task_tsdimaging.py; test_ephemeris_notset, test_ephemeris_sun,
    test_ephemeris_trackf, test_ephemeris_table
    """
    def setup(self):
        self.setup_ephemeris()

    def time_ephemeris_trackf(self):
        sdimaging(infiles=[self.vis], outfile=self.out, overwrite=False, field='Sol',
                  spw='18', mode='channel', nchan=1, start=0, width=1,
                  veltype='radio', specmode='cube', outframe='', gridfunction='BOX', convsupport=-1, truncate=-1,
                  gwidth=-1, jwidth=-1, imsize=[1000], cell='4arcsec', phasecenter='TRACKFIELD', projection='SIN',
                  pointingcolumn='direction', restfreq='', stokes='I', minweight=0.1, brightnessunit='',
                  clipminmax=False)
