import os
import shutil
import itertools

from casatasks import fringefit, flagmanager, flagdata
from casatools import ctsys

from casatestutils import testhelper as th

# ASV iteration control (https://asv.readthedocs.io/en/stable/benchmarks.html#benchmark-attributes)
number = 1            # i.e., always run the setup and teardown methods
repeat = (1, 2, 30.0) # between 1 and 2 iterations per round w/ soft cutoff (start no new repeats) past 1m
rounds = 3            # amount of instances a "repeat block" is run to collect samples
min_run_count = 5     # enforce the min_repeat * rounds setting is met
timeout = 3600        # conservative 1hr hard cap for duration of a single test execution

datapath = ctsys.resolve('unittest/fringefit/')

class Sbd():
    prefix = 'n08c1'
    msfile = prefix + '.ms'
    uvfile = 'gaincaltest2copy.ms'

    def setUp(self):
        shutil.copytree(os.path.join(datapath, self.msfile), self.msfile)
        shutil.copytree(os.path.join(datapath, 'gaincaltest2.ms'), self.uvfile)

    def tearDown(self):
        shutil.rmtree(self.msfile)
        shutil.rmtree(self.prefix + '.sbdcal', True)
        shutil.rmtree(self.prefix + '-zerorates.sbdcal', True)
        shutil.rmtree(self.prefix + '.mbdcal', True)
        # shutil.rmtree(self.prefix + '.mbdcal2', True)
        shutil.rmtree(self.uvfile, True)
        shutil.rmtree('uvrange_with.cal', True)

    def time_sbd(self):
        """test_sbd --- test with sbd caltable"""
        sbdcal = self.prefix + '.sbdcal'
        fringefit(vis=self.msfile, caltable=sbdcal, refant='EF')
    time_sbd.version = '14113'

    def time_uvrange(self):
        """test_uvraange --- Check that the uvrnage parameter excludes antennas """
        # create a caltable with uvrange selection
        fringefit(vis=self.uvfile, caltable='uvrange_with.cal', spw='2', refant='0', uvrange='<1160')
    time_uvrange.version = '14113'
    
class Mbd():
    prefix = 'n08c1'
    msfile = prefix + '.ms'
    
    def setUp(self):
        shutil.copytree(os.path.join(datapath, self.msfile), self.msfile)
        
        sbdcal = self.prefix + '-zerorates.sbdcal'
        fringefit(vis=self.msfile, caltable=sbdcal, field='4C39.25',
                  refant='EF', zerorates=True)
        
    def tearDown(self):
        shutil.rmtree(self.msfile)
        shutil.rmtree(self.prefix + '.sbdcal', True)
        shutil.rmtree(self.prefix + '-zerorates.sbdcal', True)
        shutil.rmtree(self.prefix + '.mbdcal', True)

    def time_mbd(self):
        """test_mbd --- test with mbd cal table"""
        sbdcal = self.prefix + '-zerorates.sbdcal'
        mbdcal = self.prefix + '.mbdcal'
        
        fringefit(vis=self.msfile, caltable=mbdcal, field='J0916+3854',
                   combine='spw', gaintable=[sbdcal], refant='EF')
    time_mbd.version = '14113'


class Single():
    prefix = 'n08c1-single'
    msfile = prefix + '.ms'

    def setUp(self):
        shutil.copytree(os.path.join(datapath, self.msfile), self.msfile)

    def tearDown(self):
        shutil.rmtree(self.msfile)
        shutil.rmtree(self.prefix + '.sbdcal', True)
        shutil.rmtree(self.prefix + '-2.sbdcal', True)

    def time_single(self):
        """test_single --- check that the right params are flagged with a single refant"""
        sbdcal = self.prefix + '.sbdcal'
        fringefit(vis=self.msfile, caltable=sbdcal, refant='EF')
    time_single.version = '14113'
        
    def time_param(self):
        """test_param --- test different iterations of paramactive"""
        sbdcal = self.prefix + '-2.sbdcal'
        # We make a triple cartesian product of booleans
        # to test all possible paramactive values
        refant = 0
        refant_s = str(refant)
        for pactive in itertools.product(*3*[[False, True]]):
            fringefit(vis=self.msfile, paramactive=list(pactive), caltable=sbdcal, refant=refant_s)
    time_param.version = '14113'


class Dispersive():
    prefix = 'n14p1'
    msfile = prefix+'.ms'
    
    def setUp(self):
        shutil.copytree(os.path.join(datapath, self.msfile), self.msfile)
        flagdata(self.prefix + '.ms', mode='manual', spw='*:0~2;29~31')
        
        fringefit(vis="n14p1.ms", caltable="n14p1.mpc",
          scan="1", solint="300", refant="WB",
          minsnr=50, zerorates=True,
          globalsolve=True, niter=100, gaintable=[],
          parang=True)

    def tearDown(self):
        shutil.rmtree(self.msfile)
        shutil.rmtree(self.prefix + '.ms' + '.flagversions')
        shutil.rmtree(self.prefix + '.mpc', True)
        shutil.rmtree(self.prefix + '.disp', True)

    def time_manual_phase_cal(self):
        """test_manual_phase_cal --- test on manually flagged data"""
        fringefit(vis=self.prefix + '.ms',
                  caltable='n14p1.disp', refant="WB",
                  scan='1', solint='60', spw='0,1,2',
                  paramactive=[True, True, True],
                  minsnr=50,
                  niter=100,
                  gaintable=['n14p1.mpc'],
                  parang=True)
    time_manual_phase_cal.version = '14113'


class RefantBookkeeping():
    prefix = 'n08c1-single'
    msfile = prefix + '.ms'
    sbdcal = prefix + '-book.sbdcal'

    def setUp(self):
        shutil.copytree(os.path.join(datapath, self.msfile), self.msfile)
        flagdata(self.prefix + '.ms', mode='manual', spw='*:0~2;29~31')
        flagdata(self.prefix + '.ms', mode='manual', antenna='EF')

    def tearDown(self):
        shutil.rmtree(self.msfile)
        shutil.rmtree(self.msfile + '.flagversions')
        shutil.rmtree(self.sbdcal, True)

    def time_bookkeeping(self):
        """test_bookkeeping --- check effects of using refant WB"""
        fringefit(vis=self.msfile, caltable=self.sbdcal, refant='WB')
    time_bookkeeping.version = '14113'

class FreqMetaTests():
    prefix = 'n08c1'
    msfile = 'n08c1.ms'

    def setUp(self):
        if os.path.exists(self.msfile):
            shutil.rmtree(self.msfile)
        shutil.copytree(os.path.join(datapath, self.msfile), self.msfile)
        
        sbdcal = self.prefix + '-zerorates.sbdcal'
        fringefit(vis=self.msfile, caltable=sbdcal, field='4C39.25',
                  refant='EF', zerorates=True)

    def tearDown(self):
        if os.path.exists(self.msfile):
            shutil.rmtree(self.msfile)
        if os.path.exists(self.prefix + '.mbdcal'):
            shutil.rmtree(self.prefix + '.mbdcal', True)

    def time_metadata(self):
        """test_metadata --- check output table metadata"""
        sbdcal = self.prefix + '-zerorates.sbdcal'
        mbdcal = self.prefix + '.mbdcal'
        
        fringefit(vis=self.msfile, caltable=mbdcal, spw="0,1,2,3", field='J0916+3854', timerange="17:10:00~17:11:00",
                   combine='spw', gaintable=[sbdcal], refant='EF')
    time_metadata.version = '14113'


class Corrcomb():
    polcombtestms = 'gaincalcopy.ms'
    testout = 'polcombout.cal'

    def setUp(self):
        if os.path.exists(self.polcombtestms):
            shutil.rmtree(self.polcombtestms)
        shutil.copytree(os.path.join(datapath, 'gaincaltest2.ms'), self.polcombtestms)

    def tearDown(self):
        shutil.rmtree(self.polcombtestms)
        if os.path.exists(self.testout):
            shutil.rmtree(self.testout)
        
    def time_comb_all(self):
        """test_comb --- last part of the corrcomb test, check that results are coombined"""
        fringefit(vis=self.polcombtestms, caltable=self.testout, refant='0', spw='2~3', corrcomb='all')
    time_comb_all.version = '14113'
    
