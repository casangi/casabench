
import os
import sys
import shutil

from casatools import ctsys
from casatasks import importasdm, casalog

# ASV iteration control (https://asv.readthedocs.io/en/stable/benchmarks.html#benchmark-attributes)
number = 1            # i.e., always run the setup and teardown methods
repeat = (1, 2, 30.0) # between 1 and 2 iterations per round w/ soft cutoff (start no new repeats) past 1m
rounds = 3            # amount of instances a "repeat block" is run to collect samples
min_run_count = 5     # enforce the min_repeat * rounds setting is met
timeout = 3600        # conservative 1hr hard cap for duration of a single test execution

datapath = ctsys.resolve('unittest/importasdm/')

# benchmarks grouped by ASDM used

class M51():
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

    def time_lazy_pc(self):
        '''test1_lazy1 --- lazy mode, with pointing_correction=True'''
        importasdm(asdm=self.asdm_name, vis=self.ms_name, lazy=True, with_pointing_correction=True)

    def time_pc(self):
        '''test1_lazy1 --- standard fill (lazy=False), with pointing_correction=True'''
        importasdm(asdm=self.asdm_name, vis=self.ms_name, lazy=False, with_pointing_correction=True)

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
    
    def time_evlatest1(self):
        '''test_evlatest1 - test of importing evla data, with_pointint_correction=True is normal for EVLA data'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='2',ocorr_mode='co',with_pointing_correction=True)

    def time_evla_apply2(self):
        '''test_evla_apply2 - test of importing evla data and applying the online flags'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='2',ocorr_mode='co', with_pointing_correction=True,
                   process_flags=True, applyflags=True, savecmds=False, flagbackup=False)

    def time_evla_apply3(self):
        '''test_evla_apply3 - test of importing evla data, two difference scans, do not apply online flags'''
        
        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='2,13', ocorr_mode='co', with_pointing_correction=True,
                   process_flags=False,flagbackup=False)

    def time_evla_apply5(self):
        '''test_evla_apply5 - test of importing evla data: all scans, do not process flags'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name, ocorr_mode='co', with_pointing_correction=True,
                   process_flags=False, flagbackup=False)

    def time_evla_savepars(self):
        '''test_evla_savepars - test importing evla data: save the flag commands and do not apply'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name,scans='11~13', ocorr_mode='co', with_pointing_correction=True,
                   process_flags=True, applyflags=False, savecmds=True, flagbackup=False)


    def time_evla_apply1_flagdata(self):
        '''test_evla_apply1_flagdata - test of importing evla data, apply onlineflags'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='2', ocorr_mode='co', with_pointing_correction=True,
                   process_flags=True, applyflags=True, savecmds=True, outfile=self.cmdfile, flagbackup=False)
                
    def time_evla_apply3_flagdata(self):
        '''test_evla_apply3_flagdata - test of importing evla data'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='2,13', ocorr_mode='co', with_pointing_correction=True,
                   process_flags=False,flagbackup=False)

    def time_evla_savepars_flagdata(self):
        '''test_evla_savepars_flagdata - test importing evla data: save the flag commands and do not apply; using flagdata'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name,scans='11~13', ocorr_mode='co', with_pointing_correction=True,
                   process_flags=True, applyflags=False, savecmds=True, outfile=self.cmdfile, flagbackup=False)


        
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
    
    def time_evlatest2(self):
        '''test_evlatest2 - test of importing evla data, test2: Good input asdm with polynomial ephemeris'''
        
        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='0:5',ocorr_mode='co',with_pointing_correction=True,polyephem_tabtimestep=0.001,convert_ephem2geo=False)

                
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
            os.remove(outfile)
    
    def time_autocorr(self):
        '''test_autocorr - importasdm: auto-correlations should be written to online flags'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='3', savecmds=True, outfile=outfile)

    def time_flagautocorr1(self):
        '''test_flagautocorr1 - importasdm: test that auto-correlations from online flags are correctly flagged'''        

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='3', applyflags=True)

    def time_flagautocorr3(self):
        '''test_flagautocorr3 - importasdm: do not process flags''' 

        importasdm(asdm=self.asdm_name, vis=self.ms_name, scans='3', process_flags=False, flagbackup=False)

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
               
    def time_aca_lazy(self):
        '''test6_lazy1 - lazy fill: Test good ACA ASDM with mixed pol/channelization input with default filler in lazy mode'''

        importasdm(asdm=self.asdm_name, vis=self.ms_name, lazy=True, scans='0:1~3')

    def time_aca(self):
        '''test6_lazy1 - standard fill : Test good ACA ASDM with mixel pol/channelization input with default filler'''
        importasdm(asdm=self.asdm_name, vis=self.ms_name, lazy=False, scans='0:1~3')

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

    def time_test7_1_lazy(self):
        '''test7_lazy1 - lazy fill: Test good 12 m ASDM with mixed pol/channelization input with default filler in lazy mode'''
        importasdm(self.asdm_name, vis=self.ms_name, lazy=True, scans='0:1~4') 

    def time_test7_1(self):
        '''test7_lazy1 - standard fill: Test good 12 m ASDM with mixed pol/channelization with default filler'''
        importasdm(self.asdm_name, vis=self.ms_name, lazy=False, scans='0:1~4')

    def time_test7_2_lazy2(self):
        '''test7_lazy2 - Test good 12 m ASDM with mixed pol/channelisation input with default filler in lazy mode with reading the BDF flags'''
        importasdm(self.asdm_name, vis=self.ms_name, lazy=True, bdfflags=True) 

    def time_test7_4_lazy4(self):
        '''test7_lazy4 - lazy fill, Test good 12 m ASDM with mixed pol/channelisation input with default filler in lazy mode selecting only AUTO data, writing to FLOAT_DATA'''
        importasdm(self.asdm_name, vis=self.ms_name, ocorr_mode="ao", lazy=True, scans='0:1~4') 

    def time_test7_4(self):
        '''test7_lazy4 - standard fill: Test good 12 m ASDM with mixed pol/channelisation input with default filler in lazy mode selecting only AUTO data, writing to FLOAT_DATA'''
        importasdm(self.asdm_name, vis=self.ms_name, ocorr_mode="ao", lazy=False, scans='0:1~4')

    def time_bdflags(self):
        '''test7_bdflags1 - Test good 12 m ASDM with mixed pol/channelisation input with default filler selecting "co" on output and using the BDF flags'''
        importasdm(asdm=self.asdm_name, vis=self.ms_name, ocorr_mode="co", bdfflags=True) 

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
    
    def time_sd_lazy(self):
        '''test7_lazy5 - lazy fill : Test TP asdm with default filler in lazy mode selecting only AUTO data, writing to FLOAT_DATA'''
        
        importasdm(self.asdm_name, vis=self.ms_name, ocorr_mode="ao", bdfflags=True, applyflags=True, lazy=True)
        
    def time_sd(self):
        '''test7_lazy5 - standard fill : Test TP asdm with default filler selecting only AUTO data, writing to FLOAT_DATA'''
        importasdm(self.asdm_name, vis=self.ms_name, ocorr_mode="ao", lazy=False, bdfflags=True, applyflags=True)

