import os, shutil
from casatools import ctsys
from casatasks import flagdata

class flagdata_suite:
    """
    An example benchmark that adapts CAS-13490 to asv
    """
    dataroot = ctsys.resolve('/.lustre/naasc/sciops/comm/scastro/casa/Tests/CAS-13490/performance/flagdata_runtime/')
    input_ms = 'uid___A002_Xe1f219_X6d0b_data_autocorr_WRAY_scan7.ms/'
    flags_cmd = 'uid___A002_Xe1f219_X6d0b.flagcmds.txt'

    timeout = 10000

    def setup_cache(self):
        # only run once for repeated tests
        pass

    def setup(self):
        # run for each repeated test
        
        # iterations per sample
        self.number = 10

        # Delete the MS if already exists
        if os.path.exists(self.input_ms):
            shutil.rmtree(self.input_ms)

        # Copy the flagcmd text file into temporary test directory
        if not os.path.exists(self.flags_cmd):
            shutil.copyfile(os.path.join(self.dataroot, self.flags_cmd), self.flags_cmd)

        # assign our test dataset
        self.datapath = os.path.join(self.dataroot, self.input_ms)

    def time_flagdata_summary(self):
        """hifa_importdata"""
        summary_dict = flagdata(vis=self.datapath, flagbackup=False, mode='summary')

    def time_flagdata_list(self):
        """hifa_flagdata"""
        flagdata(vis=self.datapath, mode='list', inpfile=self.flags_cmd, tbuff=[0.048, 0.0], 
                 action='apply', flagbackup=False, savepars=False)

    def time_flagdata_list_summary(self):
        """hifa_rawflagchans"""
        summary_dict = flagdata(vis=input_ms, mode='list', inpfile=["mode='summary' name='before'"], 
                                reason='any', action='apply', flagbackup=False, savepars=False)

    def time_flagdata_bandpassflag(self):
        """hifa_bandpassflag"""
        flagdata(vis=self.datapath, mode='list',
                 inpfile=["intent='CALIBRATE_BANDPASS#ON_SOURCE' spw='16' antenna='CM05' \
                 timerange='20:09:50~20:09:52' field='J1924-2914' reason='bad antenna timestamp'", 
                          "intent='CALIBRATE_BANDPASS#ON_SOURCE' spw='20' antenna='CM05' \
                          timerange='20:09:20~20:09:22' field='J1924-2914' reason='bad antenna timestamp'", 
                          "intent='CALIBRATE_BANDPASS#ON_SOURCE' spw='20' antenna='CM05' \
                          timerange='20:10:21~20:10:22' field='J1924-2914' reason='bad antenna timestamp'", 
                          "intent='CALIBRATE_BANDPASS#ON_SOURCE' spw='22' antenna='CM05' \
                          timerange='20:09:30~20:09:32' field='J1924-2914' reason='bad antenna timestamp'"], 
                 reason='any', action='apply', flagbackup=False, savepars=False)

    def teardown(self):
        # remove the data products generated by the task
        os.remove(self.flags_cmd)
        shutil.rmtree(self.input_ms, ignore_errors=True)
