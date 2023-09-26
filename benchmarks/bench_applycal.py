import os, shutil
from casatools import ctsys
from casatasks import applycal

# ASV iteration control (https://asv.readthedocs.io/en/stable/benchmarks.html#benchmark-attributes)
number = 1            # i.e., always run the setup and teardown methods
repeat = 10           # fixed at 10 iterations per round, no range or soft cutoff
rounds = 1            # amount of instances a "repeat block" is run to collect samples
min_run_count = 10    # enforce the min_repeat * rounds setting is met
timeout = 3600        # conservative 1hr hard cap should never be met for these test cases

class DataSetUp():

    datapath = ctsys.resolve('unittest/applycal/')

    def setup_basic(self):
        self.vis = 'applycalcopy.ms'
        self.gCal = 'tempgcal.G0'
        self.tCal = 'temptcal.T0'
        self.callibfile = 'refcallib.txt'

        if os.path.exists(self.vis):
            shutil.rmtree(self.vis)

        if os.path.exists(self.vis):
            shutil.rmtree(self.vis)
        if os.path.exists(self.gCal):
            shutil.rmtree(self.gCal)
        if os.path.exists(self.tCal):
            shutil.rmtree(self.tCal)
        if (os.path.exists(self.callibfile)):
            os.remove(self.callibfile)

        shutil.copytree(os.path.join(self.datapath, 'gaincaltest2.ms'), self.vis)
        shutil.copytree(os.path.join(self.datapath, 'gaincaltest2.ms.G0'), self.gCal)
        shutil.copytree(os.path.join(self.datapath, 'gaincaltest2.ms.T0'), self.tCal)
        self.callibfile = os.path.join(self.datapath, self.callibfile)

class Parang(DataSetUp):
    """
    Benchmark runtime when using parang
    """

    def setup(self):
        self.setup_basic()

    def time_applycal_parang(self):
        applycal(vis=self.vis, gaintable=[self.gCal], parang=True)

class ApplyModes(DataSetUp):
    """
    Benchmark runtime for different apply modes
    """

    def setup(self):
        self.setup_basic()

    def time_applycal_cal_only_mode(self):
        applycal(vis=self.vis, gaintable=[self.gCal], applymode='calonly')
