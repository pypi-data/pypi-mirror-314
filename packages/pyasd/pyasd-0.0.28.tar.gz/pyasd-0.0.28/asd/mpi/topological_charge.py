#!/usr/bin/env python

#=============================================
#
# calculation of topological charge
# of classic spin systems
# Shunhong Zhang
# Last modified: Mar 11 2022
#
#=============================================

import numpy as np
import pickle
from asd.core.spin_configurations import check_sp_lat_norm
from asd.core.topological_charge import get_tri_simplices,calc_solid_angle_1,calc_solid_angle_2
import asd.mpi.mpi_tools as mt
 


def mpi_calc_topo_chg_one_conf(spins,sites=None,tri_simplices=None,pbc=[0,0,0],spatial_resolved=False,solid_angle_method=2):
    from scipy.spatial import Delaunay
    comm,size,rank,node = mt.get_mpi_handles()

    check_sp_lat_norm(spins)
    all_spins=spins.reshape(-1,3)
 
    if tri_simplices is None and sites is not None:
        assert np.prod(spins.shape[:-1])==np.prod(sites.shape[:-1]),'No. of spins and sites inconsistent!'
        if not rank: tri_simplices = get_tri_simplices(sites)
        tri_simplices = comm.bcast(tri_simplices,root=0)

    start,last = mt.assign_task(len(tri_simplices),size,rank)
    assert solid_angle_method in [1,2], 'valid value for solid_angle_method: 1 or 2'
    tri_local = tri_simplices[start:last]
    if solid_angle_method==1:  Q_distri = np.array([calc_solid_angle_1(*tuple(all_spins[idx])) for idx in tri_local])
    if solid_angle_method==2:  Q_distri = np.array([calc_solid_angle_2(*tuple(all_spins[idx])) for idx in tri_local])
    comm.barrier()
    Q_distri = comm.gather(Q_distri,root=0)
    Q = 0.
    if not rank:
        Q_distri = np.concatenate(Q_distri,axis=0)
        Q = np.sum(Q_distri)/4/np.pi
    Q_distri = comm.bcast(Q_distri)
    Q = comm.bcast(Q)
    if spatial_resolved: return tri_simplices,Q_distri,Q
    else: return Q


if __name__=='__main__':
    print ('Calculate the topological charge, parallel mode')
