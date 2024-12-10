#!/usr/bin/env python

#=============================================
#
# structure factors of spin configs
# Shunhong Zhang
# Last modified: Nov 27, 2021
#
#=============================================

import sys
import numpy as np
import time
import pickle
from asd.core.constants import *

meV_to_THz = 1e-3/(Hbar*1e12*2*np.pi)


def gen_uniform_qmesh(nqx=100,nqy=100,nqz=None,boundx=1,boundy=1,boundz=1):
    if nqz is None:
        qpt_cart=np.mgrid[-boundx:boundx:1.j*nqx,-boundy:boundy:1.j*nqy]
        qpt_cart = np.transpose(qpt_cart,(1,2,0)).reshape(-1,2)
    else:
        qpt_cart=np.mgrid[-boundx:boundx:1.j*nqx,-boundy:boundy:1.j*nqy, -boundz:boundz:1.j*nqz]
        qpt_cart = np.transpose(qpt_cart,(1,2,3,0)).reshape(-1,3)
    return qpt_cart



# Static spin structure factor
# \sum_{i} { S_{i,miu} * exp(1.j*q*r_i) }
# For references, see, e. g.
# OKubo et al. PRL 108, 017206 (2012)
# Xu et al. PRL 125, 037203 (2020), Supplemental Material
def calc_static_structure_factor(spins,sites_cart,qpt_cart,dump=True):
    stime = time.time()
    fmt_end = 'Done. Time used : {:8.3f} s'
    print ('Calculate phase factor ...')
    phase_factor = np.einsum('qi,ri->qr',qpt_cart,sites_cart)
    print (fmt_end.format(time.time()-stime))
    print ('Calculate phases ...')
    phase = np.exp(1.j*phase_factor)
    print (fmt_end.format(time.time()-stime))
    stime = time.time()
    nsites = np.prod(spins.shape[:-1])
    print ('Calculate structure factor ...')
    S_vector = abs(np.dot(phase,spins))**2/nsites
    print (fmt_end.format(time.time()-stime))
    if dump:  pickle.dump(S_vector,open('S_vector.pickle','wb'))
    return S_vector



# still under test
# \sum_{i,j} { (S_i \dot S_j) * exp(1.j*q*(r_i-r_j) }
def calc_equal_time_spin_structure_factor(sp_lat,latt,sites,qpts_cart,
    cutoff_x=None, cutoff_y=None, cutoff_z=None, confine_cutoff=True, 
    dump=True, dR_filter=None, filter_method='equal'):

    from asd.core.geometry import calc_space_disp

    shape=sp_lat.shape
    nqs = qpts_cart.shape[0]
    ndim=sites.shape[-1]
    S_vector = np.zeros((nqs,3),complex)

    if len(shape)==4: 
        nx,ny=shape[:2]
        nz=1
        if cutoff_x is None: cutoff_x = max(nx//2-1,1)
        if cutoff_y is None: cutoff_y = max(ny//2-1,1)
        if cutoff_z is None: cutoff_z = 0
        space_disp = calc_space_disp(latt,sites,cutoff_x,cutoff_y,cutoff_z)

        phase_factor = np.einsum('qi,...i-> q...',qpts_cart, space_disp, optimize='optimal')
        space_phases = np.exp( 1.j*phase_factor )

        conf = np.array([sp_lat])
        corr = calc_correlation_function(conf, conf, cutoff_x, cutoff_y, subtract_background=False, confine_cutoff=confine_cutoff) 

        if dR_filter is None:
            #S_vector = np.einsum('xyabd, qxyab->qd',corr,space_phases, optimize='optimal')
            S_vector = np.einsum('...d, q...->qd',corr,space_phases, optimize='optimal')

        else:
            shape_d = space_disp.shape
            nnx, nny = shape_d[:2]
            nat = shape_d[-2]
            norms = np.linalg.norm(space_disp, axis=-1)
            if filter_method=='equal':      idx_filter = np.where(np.abs(norms-dR_filter)<1e-4)
            elif filter_method=='smaller':  idx_filter = np.where(norms <= dR_filter)
            elif filter_method=='larger':   idx_filter = np.where(norms >= dR_filter)
            else: raise ValueError ('Invalid filter_meethod = {} (Should be equal, larger or smaller)'.format(filter_method))
 
            phases_filter = np.transpose(space_phases,(1,2,3,4,0))[idx_filter]
            corr_filter = corr[idx_filter]
            print (phases_filter.shape, space_phases.shape)
            S_vector = np.einsum('md,mq->qd', corr_filter, phases_filter)
            """
            for ix in range(nnx):
                for iy in range(nny):
                    for iat,jat in np.ndindex(nat,nat):
                        norm = np.linalg.norm(space_disp[ix,iy,iat,jat])
                        if np.abs(norm-dR_filter)<1e-4:
                            print (ix, iy, iat, jat, space_disp[ix,iy,iat,jat], norm)
                            S_vector += np.einsum('d,q->qd', corr[ix,iy,iat,jat] , space_phases[:,ix,iy,iat,jat])
            """

        S_vector = np.abs(S_vector)

    # not yet developed
    elif len(shape)==5:
        nx,ny,nz = shape[:3]
        ndim=3
        S_vector=None 

    if dump:  pickle.dump(S_vector,open('S_vector.pickle','wb'))
    return S_vector




# According to 
# Phys. Rev. B 87, 144401 (2013)
# Nat. Commun. 5, 4815 (2014)
# the space- and time-displaced correlation function 
# is necessary to calculate the
# dynamic structure factor and the magnon spectra
# Here
# confs_0 contain configurations at moment 0
# confs_t contain configurations at moment t
# from different ensembles
# 
# periodic boundary condition is assumed
#
# Note: in some references, e.g. Phys. Rev. Mater. 4, 024409 (2020)
# Eq. (5): the term <m(R_i,t)> * <m(R_j,0> is not subtracted
# here we follow this convention Jan 02, 2022

alert_cutoff='''
Warning from calc_correlation_function:
The cutoff you set along some direction exceeds
half the size of supercell:
cutoff = {}, supercell size = {}
This might lead to some unphysical "correlation"
originated from the periodic boundary condition
If you want to investigate long-range correlation,
use open boundary condition or larger supercell.
'''
def calc_correlation_function_1(confs_t,confs_0,cutoff_x=3,cutoff_y=3,verbosity=0, confine_cutoff=True):
    ave_confs_0 = np.average(confs_0,axis=0)  # ensemble average of confs_0
    ave_confs_t = np.average(confs_t,axis=0)
    nsample,nx,ny,nat = confs_t.shape[:4]
    nnx = 2*cutoff_x+1
    nny = 2*cutoff_y+1
    if confine_cutoff:
        assert nnx<nx, alert_cutoff.format(cutoff_x,nx)
        assert nny<ny, alert_cutoff.format(cutoff_y,ny)
    Corr = np.zeros((nnx,nny,nat,nat,3),float)
    stime = time.time()
    if verbosity: print ('Calculate spin-spin correlation functions.')
    for ix,iy in np.ndindex(nx,ny):
        if (ix+1)%(nx//5)==0 and (iy+1)%(ny//5)==0 and verbosity:
            print ('ix = {:4d}, iy = {:4d}'.format(ix+1,iy+1))

        for ii,dx in enumerate(range(-cutoff_x,cutoff_x+1)):
            jx = (ix+dx)%nx
            for jj,dy in enumerate(range(-cutoff_y,cutoff_y+1)):
                jy = (iy+dy)%ny
                for iat,jat in np.ndindex(nat,nat):
                    cc = confs_t[:,ix,iy,iat] * confs_0[:,jx,jy,jat]
                    Corr[ii,jj,iat,jat] += np.average(cc, axis=0)
                    if nsample>1: Corr[ii,jj,iat,jat] -= ave_confs_t[ix,iy,iat] * ave_confs_0[jx,jy,jat]
    if verbosity: print ('Finished. Time used: {:8.3f} s'.format(time.time()-stime))
    return Corr/(nx*ny)


def calculate_correlation_function_dR(confs_t,confs_0,dx,dy,ave_on_confs=True):
    confs_tmp = np.roll(confs_0,(-dy,-dx),axis=(2,1))
    cc = np.einsum('...ad,...bd->...abd',confs_t,confs_tmp, optimize='optimal')
    if ave_on_confs: return np.average(cc,axis=(0,1,2))
    else: return np.average(cc,axis=(1,2))


# This new function runs much faster than calc_correlation_function_1 (an early verion)
# thanks to the numpy.roll function of Numpy lib
# Currently it is only tested for static (equal-time) spin correlations
# For dynamic (involve time, omega-dependent) cases, further tests are required
#
# conts_t and confs_0 are collection of spin configurations at the moments t=0 and t=t
# they are numpy.ndarrays in shape of (nsample, nx, ny, nat, 3)
# nsample is the number of samples for ensemble average
def calc_correlation_function(confs_t,confs_0,cutoff_x=3,cutoff_y=3,verbosity=0,subtract_background=True,confine_cutoff=False):
    ave_confs_0 = np.average(confs_0,axis=0)  # ensemble average of confs_0
    ave_confs_t = np.average(confs_t,axis=0)
    nsample,nx,ny,nat = confs_t.shape[:4]
    nnx = 2*cutoff_x+1
    nny = 2*cutoff_y+1
    if confine_cutoff:
        assert nnx<nx, alert_cutoff.format(cutoff_x,nx)
        assert nny<ny, alert_cutoff.format(cutoff_y,ny)
    Corr = np.zeros((nnx,nny,nat,nat,3),float)
    stime = time.time()
    gg = (cutoff_x*2+1)*(cutoff_y*2+1)
    prog = '{:4d} of {} ({:5.1f} %) finished, time used: {:8.3f} s'
    if verbosity: print ('Calculate spin-spin correlation functions.')
    dR_grids = np.mgrid[-cutoff_x:cutoff_x+1,-cutoff_y:cutoff_y+1]
    for ii,jj in np.ndindex(nnx,nny):
        dx,dy = dR_grids[:,ii,jj]
        ig = jj + ii*(cutoff_y*2+1)
        if verbosity and ig%(gg//20)==0: print (prog.format(ig,gg,100.*ig/gg,time.time()-stime))

        # either one should be OK
        #confs_tmp = np.roll(confs_0,(-dy,-dx),axis=(2,1))
        confs_tmp = np.roll(confs_0,(-dx,-dy),axis=(1,2))

        for iat,jat in np.ndindex(nat,nat):
            cc = confs_t[:,:,:,iat] * confs_tmp[:,:,:,jat]
            Corr[ii,jj,iat,jat] = np.average(cc, axis=(0,1,2))
            if nsample>1 and subtract_background:
                ave_confs_tmp = np.average(confs_tmp[:,:,:,jat],axis=0)
                Corr[ii,jj,iat,jat] -= np.average(ave_confs_t[:,:,iat] * ave_confs_tmp, axis=(0,1))
    if verbosity: print ('Finished. Time used: {:8.3f} s'.format(time.time()-stime))
    return Corr


def verbose_Swq_setup(nsample,nconf,nsite,idx0,time_spacing,nq,nomega,max_omega,cutoff_x,cutoff_y,ncore):
    print ('\nCalculating correlation functions of snapshots\n')
    print ('Parallel on {} cores'.format(ncore))
    print ('No. of samples for ensemble average: {}'.format(nsample))
    if nsample==1: print ('Ensemble average not applied')
    print ('No. of spin sites: {}'.format(nsite))
    print ('No. of data points on the time axis: {}'.format(nconf))
    print ('Index for the t=0 snapshot: {}'.format(idx0))
    print ('Time spacing for Fourier transformation: {} ps'.format(time_spacing))
    print ('No. of q-points: {}'.format(nq))
    print ('No. of frequency points: {}'.format(nomega))
    print ('Max frequency = {:.3f} THz'.format(max_omega))
    print ('Max magnon energy = {:.3f} meV'.format(max_omega/meV_to_THz))
    print ('Real space cutoff for correlation function:')
    print ('Rcut_x = {}, Rcut_y = {}\n'.format(cutoff_x,cutoff_y))
    print ('\nStarted at {}\n'.format(time.ctime()))


# shape of confs: nsample, nconf, nx, ny, nat, ndir
# nsample is the number of samples for ensemble averaging
# nconf is the number of components for time-frequency Fourier transformation
def calc_dyn_structure_factor(confs,latt,sites,qpt_cart,time_spacing,omegas,
    cutoff_x=3,cutoff_y=3,cutoff_z=0,
    dump=True,pickle_name='Swq.pickle',verbosity=1):

    from asd.core.geometry import calc_space_disp

    nx,ny = sites.shape[:2]
    nat,ndim = sites.shape[-2:]
    nsite = np.prod(sites.shape[:-1])
    nq = len(qpt_cart)
    nomega = len(omegas)
    shape = confs.shape
    nsample,nconf = shape[:2]

    times = (np.arange(nconf)-nconf//2)*time_spacing
    time_phases = np.exp(2.j*np.pi * np.einsum('w,t->wt',omegas,times) )

    space_disp = calc_space_disp(latt,sites,cutoff_x,cutoff_y,cutoff_z)
    space_phases = np.exp(2.j*np.pi * np.einsum('qi,xyabi-> qxyab',qpt_cart, space_disp) )

    stime = time.time()
    Swq = np.zeros((nq,nomega,3),complex)

    confs_t = np.zeros((nsample,nconf,*tuple(shape[2:])))
    idx0 = np.where(times==0)[0][0]
    confs_0 = confs[:,idx0]
    if verbosity: verbose_Swq_setup(nsample,nconf,nsite,idx0,time_spacing,nq,nomega,np.max(omegas),cutoff_x,cutoff_y,1)
    confs_t = confs
    
    mm = max(1,nconf//10)
    prog = 'Progress {:2d} / {}: Conf {:4d} of {}, time = {:10.3f} s'
    for iconf in range(nconf):
        if iconf%mm==0 and verbosity>1: 
            print (prog.format(iconf//mm,min(max(10,nconf//mm),nconf),iconf,nconf,time.time()-stime))
            sys.stdout.flush()
        Corr = calc_correlation_function(confs_t[:,iconf],confs_0,cutoff_x=cutoff_x,cutoff_y=cutoff_y)
        Swq0 = np.einsum('w,qxyab,xyabi->qwi',time_phases[:,iconf],space_phases,Corr)/np.prod(Corr.shape[:2])
        Swq += Swq0

    Swq *= time_spacing/(2*np.pi)
    if dump:  
        pickle.dump(Swq,open(pickle_name,'wb'))
        print ('\nFinished at {}\nTime used: {:8.2f} s'.format(time.ctime(),time.time()-stime))
    return Swq


if __name__=='__main__':
    print ('Running {}'.format(__file__.split('/')[-1]))

