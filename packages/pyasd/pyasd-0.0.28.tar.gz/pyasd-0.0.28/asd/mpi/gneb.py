#!/usr/bin/env python

#==============================================================
# Geodesic Nudged Elastic Band (GNEB)
# Estimate barriers of transition between two 
# stable of metastable magnetic states
# Shunhong Zhang
# Mar 05, 2022
#==============================================================

# TODO: try to make the energy and gradient calculation more generic
# probably without involve the spin_hamiltonian object
# to realize this we may need 
# en_calc_func, en_calc_func_args
# en_grad_func, en_grad_func_args
# which can be passed to the run_gneb function 
# as positional arguments


import numpy as np
import time
import copy
import os
import sys
from asd.core.constants import muB
from asd.utility.head_figlet import neb_text,pkg_info
from asd.utility.ovf_tools import gen_params_for_ovf,write_ovf,parse_ovf
from scipy.spatial.transform import Rotation as RT
from asd.core.shell_exchange import get_latt_idx
from asd.core.log_general import log_general
from asd.core.gneb import *
import asd.mpi.mpi_tools as mt
 

log_fmt = 'iter {:5d}  of  {}, time: {:8.3f} s, ci_idx = {}'


log_handle = log_general(
prefix='GNEB',
n_log_conf = 10,
n_log_ener = 10)


def mpi_linear_interpolate_images(conf_init,conf_finl,nimage=10,final_image_from_interpolation=True):
    comm,size,rank,node = mt.get_mpi_handles()
    shape = conf_init.shape
    assert shape==conf_finl.shape,'initial and final configs should be in the same shape!'
    nx,ny,nz,nat,dyn_idx = get_latt_idx(shape)
    confs = np.zeros((nimage+2,*tuple(shape)))
    confs[0]  = conf_init
    confs[-1] = conf_finl
    ntask = len(dyn_idx)
    start,last = mt.assign_task(ntask,size,rank)
    vecs = np.zeros((last-start,3))
    for jj in range(start,last):
        idx = dyn_idx[jj] 
        n1 = conf_init[tuple(idx)]
        n2 = conf_finl[tuple(idx)]
        if np.linalg.norm(n1-n2)<1e-3:
            for ii in range(1,nimage+2): confs[ii][tuple(idx)] = n1
        else:
            vec = np.cross(n1,n2)
            norm = np.linalg.norm(vec)
            if norm < 1e-3:
                n2_new = rot_vec_small_angle(n2)
                vec = np.cross(n1,n2_new)
            vec = vec/np.linalg.norm(vec)
            dot_prod = np.dot(n1,n2)
            angle = np.arccos(dot_prod/np.linalg.norm(n1)/np.linalg.norm(n2))
            angle_step = angle/(nimage+1)
            vecs[jj-start] = vec*angle_step
    for ii in range(1,nimage+2):
        conf_temp = np.zeros((last-start,3))
        for jj in range(last-start):
            idx = dyn_idx[jj+start]
            n1 = conf_init[tuple(idx)]
            mat = RT.from_rotvec(vecs[jj]*ii).as_matrix()
            conf_temp[jj] = np.dot(mat,n1)
        conf_temp = comm.gather(conf_temp)
        if rank==0:
            conf_temp = np.concatenate(conf_temp,axis=0)
            for kk,idx in enumerate(dyn_idx): confs[ii][tuple(idx)] = conf_temp[kk]
        confs[ii] = comm.bcast(confs[ii],root=0)
    if final_image_from_interpolation == False: confs[-1] = conf_finl
    return confs



def mpi_calc_dists(confs,geodesic_method='Vincenty'):
    comm,size,rank,node = mt.get_mpi_handles()
    start,last = mt.assign_task(len(confs),size,rank)
    dists = np.array([get_geodesic_distance(confs[ic-1],confs[ic],geodesic_method) for ic in range(max(1,start),last)])
    dists = comm.allgather(dists)
    dists = np.concatenate(dists,axis=0)
    return dists


def mpi_calc_total_force(ham,confs,dists,eners,dyn_idx,spring_const,idx_climb_image,gather=False):
    comm,size,rank,node = mt.get_mpi_handles()
    shape = confs.shape[1:]
    nimage = confs.shape[0]-2

    # first parallel on images, calculate the tangents
    start,last = mt.assign_task(nimage+2,size,rank)
    tangents = np.zeros((last-start,*tuple(shape)))
    F_S_s = np.zeros((last-start,*tuple(shape)))
    for ic in range(start,last):
        tangents[ic-start],F_S_s[ic-start] = calc_spring_force(ic,ham,confs,dists,eners,spring_const)
        if ic==idx_climb_image: F_S_s[ic-start] = 0
    tangents = comm.allgather(tangents)
    F_S_s = comm.allgather(F_S_s)
    tangents = np.concatenate(tangents,axis=0)
    F_S = np.concatenate(F_S_s,axis=0)

    # then parallel on calculation of Energy gradient force, normal to path
    start_idx,last_idx = mt.assign_task(len(dyn_idx),size,rank)
    F_E = np.zeros((nimage+2,last_idx-start_idx,3))
    for ic in range(nimage+2):
        F_E[ic] = calc_energy_gradient_force(ham,confs[ic],tangents[ic],dyn_idx[start_idx:last_idx],(ic==idx_climb_image),dyn_only=True)
    if gather:
        F_E = comm.gather(F_E)
        if rank==0: F_E = np.concatenate(F_E,axis=1)
        F_E = comm.bcast(F_E)
        return F_S + F_E
    else:
        F_tot = np.zeros_like(F_E)
        for ic in range(nimage+2):
            for ii,idx in enumerate(dyn_idx[start_idx:last_idx]):
                F_tot[ic,ii] = F_S[ic][tuple(idx)] + F_E[ic,ii]
        return F_tot

 
def mpi_calc_eners(ham,confs):
    comm,size,rank,node = mt.get_mpi_handles()
    start,last = mt.assign_task(len(confs),size,rank)
    eners = np.array([ham.calc_total_E(conf,average_on_sites=False) for conf in confs[start:last]])
    eners = comm.allgather(eners)
    eners = np.concatenate(eners,axis=0)
    return eners


def run_parallel_gneb(ham,
    conf_init,conf_finl,
    nimage=10,
    spring_const=0.2,
    rot_step = 0.01,
    niter=10,  
    log_fmt = log_fmt,
    pre_ci_niter=5,
    relax_init_final_images=False,
    geodesic_method = 'Vincenty',
    fix_boundary=False,
    pinned_idx=None,
    parallel_mode = 'sites',
    average_energy_on_sites = False,
    check_conf_norm = False,
    read_images_from_file = None,
    final_image_from_interpolation=True,
    log_handle = log_handle):

    from asd.core.topological_charge import mpi_calc_topo_chg_one_conf

    comm,size,rank,node = mt.get_mpi_handles()
    mt.inter_node_check(comm,node,rank)
    if log_handle._log_force: log_fmt += ',  max(F) = {:12.7e} meV/rad'

    shape = conf_init.shape
    nsites = np.prod(shape[:-1])
    assert shape==conf_finl.shape,'arrays for initial and final configurations should be in the same shape!'
    if rank==0:  log_handle.prepare_logging_dir()
    nx,ny,nz,nat,dyn_idx = get_latt_idx(shape,fix_boundary,pinned_idx,savetxt=(rank==0),outdir=log_handle._outdir)

    if read_images_from_file is not None:
        confs = load_images_from_file(read_images_from_file,shape,nimage)
        if confs.shape[0]==nimage: confs = np.concatenate(([conf_init],confs,[conf_finl]),axis=0)
    else:
        confs = mpi_linear_interpolate_images(conf_init,conf_finl,nimage,final_image_from_interpolation)

    head = 'GNEB'
    if pre_ci_niter>=0: 
        head = 'climb-image GNEB'
        log_handle._log_ener_file = log_handle._log_ener_file.replace('.dat','_ci.dat')
        log_handle._log_dist_file = log_handle._log_dist_file.replace('.dat','_ci.dat')
        log_handle._log_conf_file = log_handle._log_conf_file.replace('.ovf','_ci.ovf')
        log_handle._log_Q_file = log_handle._log_Q_file.replace('.dat','_ci.dat')
    stime = time.time()
    if log_handle._log_topo_chg: Qs = np.array([mpi_calc_topo_chg_one_conf(image,tri_simplices=log_handle._tri_simplices) for image in confs])
    if rank==0:
        verbose_GNEB_setup(head,nimage,niter,pre_ci_niter,relax_init_final_images,fix_boundary,
        rot_step,spring_const,geodesic_method,size,parallel_mode,read_images_from_file)

        stime = time.time()
        fw = open(log_handle._log_ener_file,'w')
        fd = open(log_handle._log_dist_file,'w')
        fq = open(log_handle._log_Q_file,'w')

        if not relax_init_final_images: 
            params = gen_params_for_ovf(nx,ny,nz,nsegment=1)
            write_single_image(params,conf_init,log_handle._init_conf_file)
            write_single_image(params,conf_finl,log_handle._final_conf_file)
            params = gen_params_for_ovf(nx,ny,nz,nsegment=nimage)
        else: 
            params = gen_params_for_ovf(nx,ny,nz,nsegment=nimage+2)
        write_images(params,confs,log_handle._log_conf_file,0)

        if log_handle._log_topo_chg: 
            fq.write(('{:4d} '+'{:10.5f}'*(nimage+2)+'\n').format(0,*tuple(Qs)))
            fq.flush()
          
    start,last = mt.assign_task(nimage+2,size,rank)
    start_idx,last_idx = mt.assign_task(len(dyn_idx),size,rank)

    idx0 = nimage+2 # never reached for a (nimage+2) chain
    if check_conf_norm: from asd.core.spin_configurations import check_sp_lat_norm
    for ite in range(niter):
        if check_conf_norm and rank==0:
            for ic in range(nimage+2):
                check_sp_lat_norm(confs[ic],verbosity=True,fil='ill_site_index_{}_{}.dat'.format(ite,ic))
        eners = mpi_calc_eners(ham,confs)
        dists = mpi_calc_dists(confs,geodesic_method)
 
        if average_energy_on_sites: eners /= nsites
        if rank==0 and ite%log_handle._n_log_energy==0: write_dists_eners(dists,eners,fw,fd,ite)
        if ite==pre_ci_niter: idx0 = np.where(eners==np.max(eners))[0][0]  # idx0 only changes its value once during a GNEB run
        idx_climb_image = idx0

        max_force = 0
        # parallel on images
        if parallel_mode == 'images':
            F_tot = np.zeros((last-start,*tuple(shape)))
            for ic in range(start,last):
                if not relax_init_final_images and ic in [0,nimage+1]: continue
                F_tot[ic-start] = calc_total_force(ic,ham,confs,dists,eners,dyn_idx,spring_const,idx_climb_image)
            comm.barrier()

            for ic in range(start,last):
                if not relax_init_final_images and ic in [0,nimage+1]: continue
                for idx in dyn_idx:
                    n_i = confs[ic][tuple(idx)]
                    F_i = F_tot[ic-start][tuple(idx)]
                    vec = np.cross(n_i,F_i)
                    norm = np.linalg.norm(vec)
                    if 0<ic<nimage+1: max_force = max(max_force,norm)
                    if norm<1e-5: continue
                    mat = RT.from_rotvec(vec*rot_step).as_matrix()
                    confs[ic][tuple(idx)] = np.dot(mat,n_i)
            new_confs = comm.gather(confs[start:last])
            if rank==0:
                for irank in range(1,size):
                    start0,last0 = mt.assign_task(nimage+2,size,irank)
                    confs[start0:last0] = new_confs[irank]

        # parallel on sites
        elif parallel_mode == 'sites':
            F_tot = mpi_calc_total_force(ham,confs,dists,eners,dyn_idx,spring_const,idx_climb_image,gather=False)
            comm.barrier()
            for ic in range(nimage+2):
                if not relax_init_final_images and ic in [0,nimage+1]: continue
                confs_tmp = np.zeros((last_idx-start_idx,3))
                for ii,idx in enumerate(dyn_idx[start_idx:last_idx]):
                    n_i = confs[ic][tuple(idx)]
                    F_i = F_tot[ic,ii]
                    vec = np.cross(n_i,F_i)
                    norm = np.linalg.norm(vec)
                    if 0<ic<nimage+1: max_force = max(max_force,norm)
                    if norm<1e-5: 
                        confs_tmp[ii] = n_i
                    else:
                        mat = RT.from_rotvec(vec*rot_step).as_matrix()
                        confs_tmp[ii] = np.dot(mat,n_i)
                confs_tmp = comm.gather(confs_tmp,root=0)
                if rank==0:
                    confs_tmp = np.concatenate(confs_tmp,axis=0)
                    for ii,idx in enumerate(dyn_idx):
                        confs[ic][tuple(idx)] = confs_tmp[ii]
        else:
            if rank==0:
                print ('you set parallel_mode = {}'.format(parallel_mode))
                print ('currently we only support parallel_mode = sites (default) / sites')
            exit(1)

        comm.barrier()
        confs = comm.bcast(confs,root=0)

        max_force = comm.allgather(max_force)
        max_force = np.max(max_force)
        if ite==0 and rank==0: print (log_fmt.format(0,niter,time.time()-stime,idx0,max_force))
        if ((ite+1)%log_handle._n_log_configuration==0 or ite==niter-1):
            if log_handle._log_topo_chg: Qs = np.array([mpi_calc_topo_chg_one_conf(image,tri_simplices=log_handle._tri_simplices) for image in confs])
            if rank==0:
                print (log_fmt.format(ite+1,niter,time.time()-stime,idx_climb_image,max_force))
                if log_handle._log_topo_chg: 
                    fq.write(('{:4d} '+'{:10.5f}'*(nimage+2)+'\n').format(ite+1,*tuple(Qs)))
                    fq.flush()
                write_images(params,confs,log_handle._log_conf_file,ite+1)
        sys.stdout.flush()
    eners = mpi_calc_eners(ham,confs)
    dists = mpi_calc_dists(confs,geodesic_method)
    if average_energy_on_sites: eners /= nsites
    if rank==0:
        write_dists_eners(dists,eners,fw,fd,ite+1,finalize=True)
        if log_handle._log_topo_chg: fq.close()
        if pre_ci_niter>=0: print ('\nImage {} is the climbing image (index starts from 0)'.format(idx_climb_image))
        print ('\nFinished at {}\nTime used: {:8.3f} s\n'.format(time.ctime(),time.time()-stime))
    return confs,dists,eners



class GNEB_controller():
    def __init__(self,
        nimage=10,
        spring_const=0.2,
        rot_step = 0.01,
        niter=10,  
        log_fmt = log_fmt,
        pre_ci_niter=5,
        relax_init_final_images=False,
        geodesic_method = 'Vincenty',
        fix_boundary=False,
        pinned_idx=None,
        parallel_mode = 'sites',
        average_energy_on_sites = False,
        check_conf_norm = False,
        read_images_from_file = None,
        final_image_from_interpolation=True,
        log_handle = log_handle,
        verbosity=1):

        self._nimage = nimage
        self._spring_const = spring_const
        self._rot_step = rot_step
        self._niter = niter
        self._log_fmt = log_fmt
        self._pre_ci_niter = pre_ci_niter
        self._relax_init_final_images = relax_init_final_images
        self._geodesic_method = geodesic_method
        self._fix_boundary = fix_boundary
        self._pinned_idx = pinned_idx
        self._parallel_mode = parallel_mode
        self._average_energy_on_sites = average_energy_on_sites
        self._check_conf_norm = check_conf_norm
        self._read_images_from_file = read_images_from_file
        self._final_image_from_interpolation = final_image_from_interpolation
        self._log_handle = log_handle
        self.set_verbosity(verbosity)


    def set_verbosity(self,verbosity):
        err = 'GNEB_controller: You try to set verbosity = {}, it should be an non-negative integer!'.format(verbosity)
        assert type(verbosity)==int and verbosity>=0, err
        self._verbosity = verbosity


    def verbose_GNEB_setup(self):
        verbose_GENB_setup(head,self._nimage,self._niter,self._pre_ci_niter,self._relax_init_final_images,self._fix_boundary,
        self._rot_step,self._spring_const,self._geodesic_method,-1,self._parallel_mode)
 


    def run_parallel_gneb(self, ham, conf_init, conf_finl):
        return run_parallel_gneb(ham,conf_init,conf_finl,
        self._nimage,
        self._spring_const,
        self._rot_step,
        self._niter,  
        self._log_fmt,
        self._pre_ci_niter,
        self._relax_init_final_images,
        self._geodesic_method,
        self._fix_boundary,
        self._pinned_idx,
        self._parallel_mode,
        self._average_energy_on_sites,
        self._check_conf_norm,
        self._read_images_from_file,
        self._final_image_from_interpolation,
        self._log_handle)



if __name__=='__main__':
    print (neb_text)
    print ('GNEB for estimating barrier between magnetic states')
