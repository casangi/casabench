
import os
import sys
import shutil

from casatools import ctsys
from casatasks import importasdm, casalog

# ASV iteration control (https://asv.readthedocs.io/en/stable/benchmarks.html#benchmark-attributes)
number = 1            # i.e., always run the setup and teardown methods
repeat = (1, 2, 30.0) # between 1 and 2 iterations per round w/ soft cutoff (start no new repeats) past 1m
rounds = 1            # amount of instances a "repeat block" is run to collect samples
min_run_count = 1     # enforce the min_repeat * rounds setting is met
timeout = 3600        # conservative 1hr hard cap for duration of a single test execution

datapath = ctsys.resolve('unittest/importasdm/')

# benchmarks grouped by ASDM used
# original test name from test_task_importasdm.py indicated in quoted string after function def

class Basic():
    # the test code says this is an M51 ASDM but the source name and direction are for 1924-202, which is a quasar
    asdm_name = 'uid___X5f_X18951_X1'
    ms_name = asdm_name + '.ms'

    def setup(self):
        shutil.copytree(os.path.join(datapath,self.asdm_name), self.asdm_name)

    def teardown(self):
        shutil.rmtree(self.asdm_name)
        shutil.rmtree(self.ms_name)
        shutil.rmtree(self.ms_name+'.flagversions')

    def time_all_defaults(self):
        '''test_import2 --- importasdm with default arguments'''
        importasdm(self.asdm_name)
    time_all_defaults.version = 14114

    def time_lazy_pc_true(self):
        '''test1_lazy1 --- lazy mode, with pointing_correction=True'''
        importasdm(asdm=self.asdm_name, vis=self.ms_name, lazy=True, with_pointing_correction=True)
    time_lazy_pc_true.version = 14114

    def time_pc_true(self):
        '''test1_lazy1 --- standard fill (lazy=False), with pointing_correction=True'''
        importasdm(asdm=self.asdm_name, vis=self.ms_name, lazy=False, with_pointing_correction=True)
    time_pc_true.version = 14114

class Evla():
    # EVLA sdm
    asdm_name = 'X_osro_013.55979.93803716435'
    ms_name = asdm_name + '.ms'
    cmdfile = ms_name.replace('.ms','_cmd.txt')

    def setup(self):
        shutil.copytree(os.path.join(datapath,self.asdm_name), self.asdm_name)

    def teardown(self):
        shutil.rmtree(self.asdm_name)
        shutil.rmtree(self.ms_name)
        if (os.path.exists(self.ms_name+'.flagversions')):
            shutil.rmtree(self.ms_name+'.flagversions')
        if (os.path.exists(self.cmdfile)):
            os.remove(self.cmdfile)        
    
    def time_pc_true(self):
        '''test_evlatest1 - test of importing evla data, with_pointing_correction=True is normal for EVLA data'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='2',ocorr_mode='co',with_pointing_correction=True)
    time_pc_true.version = 14114

    def time_applyflags_true(self):
        '''test_evla_apply2 - test of importing evla data and applying the online flags'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='2',ocorr_mode='co', with_pointing_correction=True,
                   process_flags=True, applyflags=True, savecmds=False, flagbackup=False)
    time_applyflags_true.version = 14114

    def time_scan_selection(self):
        '''test_evla_apply3 - test of importing evla data, two difference scans, do not apply online flags'''
        # appears to also be the same importasdm as test_evla_apply3_flagdata
        
        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='2,13', ocorr_mode='co', with_pointing_correction=True,
                   process_flags=False,flagbackup=False)
    time_scan_selection.version = 14114

    def time_all_scans(self):
        '''test_evla_apply5 - test of importing evla data: all scans, do not process flags'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name, ocorr_mode='co', with_pointing_correction=True,
                   process_flags=False, flagbackup=False)
    time_all_scans.version = 14114

    def time_process_flags_savecmds_true(self):
        '''test_evla_savepars - test importing evla data: save the flag commands and do not apply'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name,scans='11~13', ocorr_mode='co', with_pointing_correction=True,
                   process_flags=True, applyflags=False, savecmds=True, flagbackup=False)
    time_process_flags_savecmds_true.version = 14114

    def time_process_applyflags_savecmds_true(self):
        '''test_evla_apply1_flagdata - test of importing evla data, apply onlineflags'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='2', ocorr_mode='co', with_pointing_correction=True,
                   process_flags=True, applyflags=True, savecmds=True, outfile=self.cmdfile, flagbackup=False)
    time_process_applyflags_savecmds_true.version = 14114
                
    def time_process_flags_true_applyflags_false(self):
        '''test_evla_savepars_flagdata - test importing evla data: save the flag commands and do not apply; using flagdata'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name,scans='11~13', ocorr_mode='co', with_pointing_correction=True,
                   process_flags=True, applyflags=False, savecmds=True, outfile=self.cmdfile, flagbackup=False)
    time_process_flags_true_applyflags_false.version = 14114


        
class Evla_ephemeris():
    # EVLA sdm with ephemeris
    asdm_name = 'polyuranus'
    ms_name = asdm_name + '.ms'

    def setup(self):
        shutil.copytree(os.path.join(datapath,self.asdm_name), self.asdm_name)

    def teardown(self):
        shutil.rmtree(self.asdm_name)
        shutil.rmtree(self.ms_name)
        shutil.rmtree(self.ms_name+'.flagversions')
    
    def time_polynomial_ephem(self):
        '''test_evlatest2 - test of importing evla data, test2: Good input asdm with polynomial ephemeris'''
        
        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='0:5',ocorr_mode='co',with_pointing_correction=True,polyephem_tabtimestep=0.001,convert_ephem2geo=False)
    time_polynomial_ephem.version = 14114

                
class AutocorrASDM():
    # ALMA ASDM with auto-correlation data
    asdm_name = 'AutocorrASDM'
    ms_name = asdm_name + '.ms'
    outfile = 'scanflags.txt'

    def setup(self):
        shutil.copytree(os.path.join(datapath,self.asdm_name), self.asdm_name)

    def teardown(self):
        shutil.rmtree(self.asdm_name)
        shutil.rmtree(self.ms_name)
        if (os.path.exists(self.ms_name+'.flagversions')):
            shutil.rmtree(self.ms_name+'.flagversions')
        if os.path.exists(self.outfile):
            os.remove(self.outfile)
    
    def time_savecmds_true(self):
        '''test_autocorr - importasdm: auto-correlations should be written to online flags'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='3', savecmds=True, outfile=self.outfile)
    time_savecmds_true.version = 14114

    def time_applyflags_true(self):
        '''test_flagautocorr1 - importasdm: test that auto-correlations from online flags are correctly flagged'''        

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='3', applyflags=True)
    time_applyflags_true.version = 14114

    def time_process_flags_false(self):
        '''test_flagautocorr3 - importasdm: do not process flags''' 

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='3', process_flags=False, flagbackup=False)
    time_process_flags_false.version = 14114

class Aca():
    # ACA with mixed pol/channelization
    asdm_name = 'uid___A002_X72bc38_X000'
    ms_name = asdm_name + '.ms'

    def setup(self):
        shutil.copytree(os.path.join(datapath,self.asdm_name), self.asdm_name)

    def teardown(self):
        shutil.rmtree(self.asdm_name)
        shutil.rmtree(self.ms_name)
        shutil.rmtree(self.ms_name+'.flagversions')
               
    def time_default_lazy(self):
        '''test6_lazy1 - lazy fill: Test good ACA ASDM with mixed pol/channelization input with default filler in lazy mode'''
        importasdm(asdm=self.asdm_name, vis=self.ms_name, lazy=True, scans='0:1~3')
    time_default_lazy.version = 14114

    def time_default(self):
        '''test6_lazy1 - standard fill : Test good ACA ASDM with mixel pol/channelization input with default filler'''
        importasdm(asdm=self.asdm_name, vis=self.ms_name, lazy=False, scans='0:1~3')
    time_default.version = 14114

class Alma_12m():
    # 12m example with mixed pol/channelization
    asdm_name = 'uid___A002_X71e4ae_X317_short'
    ms_name = asdm_name + '.ms'

    def setup(self):
        shutil.copytree(os.path.join(datapath,self.asdm_name), self.asdm_name)

    def teardown(self):
        shutil.rmtree(self.asdm_name)
        shutil.rmtree(self.ms_name)
        shutil.rmtree(self.ms_name+'.flagversions')

    def time_default_lazy(self):
        '''test7_lazy1 - lazy fill: Test good 12 m ASDM with mixed pol/channelization input with default filler in lazy mode'''
        importasdm(self.asdm_name, vis=self.ms_name, lazy=True, scans='0:1~4')
    time_default_lazy.version = 14114

    def time_default(self):
        '''test7_lazy1 - standard fill: Test good 12 m ASDM with mixed pol/channelization with default filler'''
        importasdm(self.asdm_name, vis=self.ms_name, lazy=False, scans='0:1~4')
    time_default.version = 14114

    def time_bdfflags_true_lazy(self):
        '''test7_lazy2 - Test good 12 m ASDM with mixed pol/channelisation input with default filler in lazy mode with reading the BDF flags'''
        importasdm(self.asdm_name, vis=self.ms_name, lazy=True, bdfflags=True) 
    time_bdfflags_true_lazy.version = 14114
    
    def time_auto_only_lazy(self):
        '''test7_lazy4 - lazy fill, Test good 12 m ASDM with mixed pol/channelisation input with default filler in lazy mode selecting only AUTO data, writing to FLOAT_DATA'''
        importasdm(self.asdm_name, vis=self.ms_name, ocorr_mode="ao", lazy=True, scans='0:1~4') 
    time_auto_only_lazy.version = 14114
    
    def time_auto_only(self):
        '''test7_lazy4 - standard fill: Test good 12 m ASDM with mixed pol/channelisation input with default filler in lazy mode selecting only AUTO data, writing to FLOAT_DATA'''
        importasdm(self.asdm_name, vis=self.ms_name, ocorr_mode="ao", lazy=False, scans='0:1~4')
    time_auto_only.version = 14114
    
    def time_bdfflags_true(self):
        '''test7_bdflags1 - Test good 12 m ASDM with mixed pol/channelisation input with default filler selecting "co" on output and using the BDF flags'''
        importasdm(asdm=self.asdm_name, vis=self.ms_name, ocorr_mode="co", bdfflags=True) 
    time_bdfflags_true.version = 14114
    
class Singledish():
    # single dish
    asdm_name = 'uid___A002_X6218fb_X264'
    ms_name = asdm_name + '.ms'

    def setup(self):
        shutil.copytree(os.path.join(datapath,self.asdm_name), self.asdm_name)

    def teardown(self):
        shutil.rmtree(self.asdm_name)
        shutil.rmtree(self.ms_name)
        shutil.rmtree(self.ms_name+'.flagversions')
    
    def time_auto_only_lazy(self):
        '''test7_lazy5 - lazy fill : Test TP asdm with default filler in lazy mode selecting only AUTO data, writing to FLOAT_DATA'''        
        importasdm(self.asdm_name, vis=self.ms_name, ocorr_mode="ao", bdfflags=True, applyflags=True, lazy=True)
    time_auto_only_lazy.version = 14114

        
    def time_auto_only(self):
        '''test7_lazy5 - standard fill : Test TP asdm with default filler selecting only AUTO data, writing to FLOAT_DATA'''
        importasdm(self.asdm_name, vis=self.ms_name, ocorr_mode="ao", lazy=False, bdfflags=True, applyflags=True)
    time_auto_only.version = 14114

