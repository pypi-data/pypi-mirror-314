#!/usr/bin/env python

#===========================================================================#
#                                                                           #
#  File:       setup.py                                                     #
#  Author:     Shunhong Zhang                                               #
#  Date:       Jun 04, 2023                                                 #
#                                                                           #
#===========================================================================#


from __future__ import print_function
import sys
import os
import glob
import time
import setuptools


def test_modules(module_list,desc,pkg='asd'):
    import importlib
    cwd=os.getcwd()
    os.chdir(os.path.expanduser('~'))
    print ( '\n{0}\nTEST: {1}\n{0}'.format('='*50,desc))
    print ( '{:40s} {:10s}\n{}'.format('MODULE','STATUS','-'*50))
    for mod in module_list:
        try:
            if sys.platform=='linux': mod = mod.replace('/','.')
            elif sys.platform=='win32': mod = mod.replace('\\','.').replace('/','.')
            importlib.import_module(mod)
            print('{0:40s} success'.format(mod))
        except:
            print('{0:40s} failed!'.format(mod))
    print('{0}\n'.format('='*50))
    for item in glob.glob('*pyc'): os.remove(item)
    if os.path.isdir('__pycache__'): shutil.rmtree('__pycache__')
    os.chdir(cwd)
 

def test_mpi():
    try:
        import mpi4py.MPI as MPI
        test_modules(mpi_modules,'mpi modules')
    except:
        print ('Fail to import mpi4py')
        print ('Parallel scripts will be skipped')
        print ('Routine scripts can work')




core_modules = [
'constants',
'random_vectors',
'shell_exchange',
'geometry',
'spin_configurations',
'spin_correlations',
'hamiltonian',
'topological_charge',
'log_general',
'llg_simple',
'llg_advanced',
'monte_carlo',
'gneb',
]

utility_modules = [
'head_figlet',
'plot_tools_3d',
'auxiliary_colormaps',
'asd_arguments',
'Swq',
'ovf_tools',
'spin_visualize_tools',
'spirit_tool',
'mag_thermal',
'four_state_tools',
'curve_fit',
'Kitaev_ham',
]


mpi_modules = [
'mpi_tools',
'topological_charge',
'spin_correlations',
'gneb',
'monte_carlo',
]

platform = sys.platform
database_modules = glob.glob('asd/data_base/exchange_*py')
database_modules = [item.rstrip('.py') for item in database_modules]
init_files = ['asd/__init__']
core_modules  = ['asd/core/{}'.format(item) for item in core_modules]
utility_modules  = ['asd/utility/{}'.format(item) for item in utility_modules]
mpi_modules = ['asd/mpi/{}'.format(item) for item in mpi_modules]


kwargs_setup = dict(
name='pyasd',
version='0.0.28',
author='Shunhong Zhang',
author_email='zhangshunhong.pku@gmail.com',
platform=sys.platform,
url='https://to_be_posted',
download_url='https://on_request',
keywords='spin dynamics simulation',
py_modules = utility_modules + core_modules + database_modules + mpi_modules + init_files,
packages = setuptools.find_packages(),
license='MIT LICENSE',
license_file='LICENSE',
description='A python-based spin dynamics simulator',
long_description='LLG/Monte Carlo/GNEB simulators for classical spin systems',
platforms=[sys.platform],
classifiers=[
'Programming Language :: Python :: 3',],
)

      

def set_build_time_stamp(kwargs_setup):
    import locale
    with open('asd/__init__.py','r') as fw: lines = fw.readlines()
    __doc__ = '{:<20s}  =  "built at {}'.format('__built_time__',time.ctime())
    if locale.getdefaultlocale()[0]=='en_US': __doc__ += '_{}"\n'.format(time.tzname[1])
    else: __doc__ += '"\n'
    lines = [__doc__] + [line for line in lines if '__built_time__' not in line]
    keys = ['__name__','__version__','__author__','__author_email__','__url__','__license__','__platform__']
         
    with open('asd/__init__.py','w') as fw: 
        fw.write(__doc__)
        for key in keys:
            print ('{:<20s}  =  "{}"'.format(key,kwargs_setup[key.strip('__')]),file=fw)
 
 
 
if __name__=='__main__':
    set_build_time_stamp(kwargs_setup)
    print('\n{0}\nINSTALL\n{0}'.format('='*50))
    setuptools.setup(**kwargs_setup)
    test_modules(core_modules,     'core modules')
    test_modules(utility_modules,  'utility_modules')
    test_modules(database_modules, 'materials database')
    test_modules(mpi_modules, 'mpi modules')
    print ('\n{0}\nDone\n{0}\n'.format('='*50))
