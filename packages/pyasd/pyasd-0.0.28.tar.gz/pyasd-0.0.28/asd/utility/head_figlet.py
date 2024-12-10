#!/usr/bin/env python

#=================================
#
# This script is part of pyasd,
# a python-based package for
# atomistic magnetic simulations.
#
# Copyright @ Shunhong Zhang
# 2022 - 2024
#
# Usage, modification, and 
# re-distribution of this code
# should be consent to the 
# MIT license
# For details pelase refer to
# https://pypi.org/project/pyasd/
#
#==================================



#==========================================
# Use figlet to render the text,
# just for aesthetic purpose.
# If pyfiglet is not installed,
# this will be replaced by plain text, but
# the scientific part won't be influenced
#
# You can install pyfiglet via conda/pip
# or from source 
# https://pipy.org/project/pyfiglet
#
# Shunhong Zhang
# Sep 12, 2021
#
#==========================================


try:
    from pyfiglet import Figlet
    f = Figlet()
    asd_text = f.renderText('PyASD')
    llg_text = f.renderText('LLG')
    mcs_text = f.renderText('Monte  Carlo')
    pmc_text = f.renderText('PTMC')
    neb_text = f.renderText('GNEB')
    err_text = f.renderText('Error')

    asd_text = ' '+asd_text.replace('\n','\n ').rstrip(' ')
    llg_text = ' '+llg_text.replace('\n','\n ').rstrip(' ')
    mcs_text = ' '+mcs_text.replace("\n","\n ").rstrip(' ')
    pmc_text = ' '+pmc_text.replace("\n","\n ").rstrip(' ')
    neb_text = ' '+neb_text.replace("\n","\n ").rstrip(' ')
    err_text = ' '+err_text.replace("\n","\n ").rstrip(' ')
except:
    ads_text = 'ASD TOOLS\n'
    llg_text = 'LLG simulation\n'
    mcs_text = 'Monte Carlo simulation\n'
    pmc_text = 'Parallel Temperature Monte Carlo\n'
    neb_text = 'GNEB'
    err_text = 'Error!\n'


class pkg_info():
    def __init__(self):
        import asd
        self.__dict__.update(asd.__dict__)

    def verbose_info(self,fw=None):
        import time
        start_year=2022
        this_year=time.ctime().split()[-1]
        print ('='*60,file=fw)
        print (asd_text,file=fw)
        print ('{:>33s}'.format('version {}'.format(self.__version__)))
        print ('{:>33s}'.format('Copyright @ Shunhong Zhang'))
        print ('{:>33s}'.format('{} - {}'.format(start_year,this_year)))
        print ('')

        print ('Basic information'.center(35),file=fw)
        for key in ['__name__','__version__','__author__','__author_email__','__built_time__']:
            print ('{:16s}  =  {:<20s}'.format(key.center(15),self.__dict__[key]),file=fw)
        print ('='*60,file=fw)

    def verbose_head(self,fw=None):
        import time
        start_year=2022
        this_year=time.ctime().split()[-1]
        print ('')
        print (asd_text,file=fw)
        print ('{:>33s}'.format('version {}'.format(self.__version__)))
        print ('{:>33s}'.format('Copyright @ Shunhong Zhang'))
        print ('{:>33s}'.format('{} - {}'.format(start_year,this_year)))
        print ('')


if __name__=='__main__':
    code_info = pkg_info()
    code_info.verbose_info()
    code_info.verbose_head()

