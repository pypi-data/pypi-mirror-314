# Python-based Atomistic Spin Dynamics simulator (pyasd)

## Code description

This is a python package for spin dynamics simulations

Copyright Shunhong Zhang 2023

zhangshunhong.pku@gmail.com


## Code distributions

### In the "asd" directory
* core: core scripts for spin dynamics simulations
* utility: scripts for post-processing, applied to the current code and Spirit
* data_base: some exchange parameters for typical magnetic materials, udner construction
* mpi: some scripts for parallelization implementing mpi4py

### In the root directory
* scripts: some scripts for post-processing of simulation results
* examples: some examples to do fast test on the code
* tests_basic: some testing cases


## Code installation

* Fast installation via pypi

    pip install pyasd


* Install manually from tarball 
1. Download the zip or tarball (tar.gz) of the package
2. unzip the package
3. Run the following command

    python setup.py install --user

* To check whether you have successfully installed the package, go to the python interactive shell
 
    import asd.core

    import asd.utility

    If everything runs smoothly, the installation should be done. 

* Contact the author if you come across any problem.


## Clean installation
./clean

This operation removes "build" and "dists" generated during installation

Results in the examples and tests_basic directories are also removed

including dat and ovf files, and figures in png


## Additional Notes

Note: This is a .md file in Markdown, to have a better view on the contants

we suggest you to install mdview, a free software for viewing .md files

Under Ubuntu, run the following commands to install it

sudo atp update

sudo apt install snapd

sudo snap install mdview

