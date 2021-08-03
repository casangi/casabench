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
        self.number = 2

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
        summary_dict = flagdata(vis=self.datapath, mode='list', inpfile=["mode='summary' name='before'"], 
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

class calibration_suite:
    """
    An example benchmark that adapts PLWG benchmark tests of 7m ALMA project 2019.1.01056.S (MOUS uid://A001/X1465/X1b3c) to asv
    """
    dataroot = ctsys.resolve('/.lustre/naasc/sciops/comm/scastro/pipeline/root_6.2/technical_tests/2019.1.01056.S_2021_07_20T07_45_18.149/SOUS_uid___A001_X1465_X1b3a/GOUS_uid___A001_X1465_X1b3b/MOUS_uid___A001_X1465_X1b3c/parallel_8/working/')
    input_ms = 'uid___A002_Xe1f219_X6d0b.ms'
    cal_library = 'uid___A002_Xe1f219_X6d0b.ms.s12.4.callibrary'
    cal_table = 'uid___A002_Xe1f219_X6d0b.ms.hifa_bandpassflag.s12_4.spw16_18_20_22.solintint.gpcal.tbl'

    timeout = 10000

    def setup_cache(self):
        # only run once for repeated tests
        pass

    def setup(self):
        # run for each repeated test
        
        # iterations per sample
        self.number = 2

        # Delete the MS if already exists locally
        if os.path.exists(self.input_ms):
            shutil.rmtree(self.input_ms)

        # Copy the callibrary into temporary test directory
        if not os.path.exists(self.cal_library):
            shutil.copyfile(os.path.join(self.dataroot, self.cal_library), self.cal_library)

        # Copy the gain table into temporary test directory
        if not os.path.exists(self.cal_table):
            shutil.copyfile(os.path.join(self.dataroot, self.cal_table), self.cal_table)

        # assign our test dataset
        self.datapath = os.path.join(self.dataroot, self.input_ms)

    def time_applycal_callib(self):
        """hifa_bandpassflag

        Note that this is from on-the-fly application of preliminary phase-up, bandpass, and amplitude caltables, not the later stage hifa_applycal
        Expected to take ~48s, could be sped up by splitting out SPWs (especially the square law detector windows) or applying to only one of them.
        """
        applycal( vis=self.input_ms, field='J1924-2914', spw='16,18,20,22', intent='CALIBRATE_BANDPASS#ON_SOURCE', selectdata=True, timerange='', uvrange='', antenna='*&*', scan='', observation='', msselect='', docallib=True, callib=self.cal_library, gaintable=[], gainfield=[], interp=[], spwmap=[], calwt=[True], parang=False, applymode='calflagstrict', flagbackup=False )

    def time_gaincal(self):
        """hifa_bandpassflag

        Expected to take ~7s
        """
gaincal( vis=self.input_ms, caltable=self.cal_table, field='J1924-2914', spw='16,18,20,22', intent='CALIBRATE_BANDPASS#ON_SOURCE', selectdata=True, timerange='', uvrange='', antenna='0~9', scan='', observation='', msselect='', solint='int',combine='', preavg=-1.0, refant='CM03,CM10,CM02,CM12,CM06,CM05,CM11,CM04,CM07,CM01', refantmode='flex', minblperant=4, minsnr=3.0, solnorm=False, normtype='mean', gaintype='G', smodel=[],calmode='p', solmode='', rmsthresh=[], corrdepflags=False, append=False, splinetime=3600.0, npointaver=3, phasewrap=180.0, docallib=False, callib='', gaintable=[self.cal_table], gainfield=['J1924-2914'], interp=['linear,linear'], spwmap=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16, 18, 20, 22, 16, 16, 18, 18, 20, 20, 22], parang=False )

    def time_gaincal(self):
        """Not yet implemeted, could be taken from the same pipeline run"""
        pass

    def teardown(self):
        # remove the data products generated by the setup methods and the task
        os.remove(self.cal_library)
        os.remove(self.cal_table)
        shutil.rmtree(self.input_ms, ignore_errors=True)
