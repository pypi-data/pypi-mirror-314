#!/usr/bin/env python


#========================================================
#
# bilinear and biquadratic spin exchange couplings
# in generic matrix form
# grouped by shells 
# (usually pairs with the same bond length)
# four-site biquadratic exchanges in scalar form
#
# Shunhong Zhang <szhang2@ustc.edu.cn>
# Nov 21 2022
#
#=========================================================

#*********************************************************
# for the DM vectors we use the rpz coordinate as input
# the definition of rpz coordinate can be found in 
# Xu et al. npj Comput. Mater. 4, 57 (2018)
# r: along the exchange bond
# p: normal to r, and in the basal plane of the 2D lattice
# z: normal to the basal plane
#*********************************************************

#*********************************************************
#
# multi-site spin interactions are included
# but more tests are still under way
#
#*********************************************************

# Important Note: effective fields calculated in this script are in meV
# the spins are normalized to be unit vectors


import os
import numpy as np
from scipy.spatial.transform import Rotation as RT
import copy
from asd.utility.head_figlet import err_text
try:
    import asd.mpi.mpi_tools as mt
    comm,size,rank,node = mt.get_mpi_handles()
    enable_mpi=True
except:
    enable_mpi=False
 

# If fix_boundary is set to True, index for sites in boundary cells are excluded (for dynamics)
def get_latt_idx(shape,fix_boundary=False,pinned_idx=None,savetxt=False,outdir='.'):
    if len(shape)==4:  # 2D case
        nx,ny,nat = shape[:3]
        nz=1
        mgrid = np.mgrid[:nx,:ny,:nat]
        idx=np.transpose(mgrid,(1,2,3,0))
        if fix_boundary: idx = idx[1:-1,1:-1]
        idx = idx.reshape(-1,3)
    elif len(shape)==5:   # 3D case
        nx,ny,nz,nat = shape[:4]
        mgrid = np.mgrid[:nx,:ny,:nz,:nat]
        idx=np.transpose(mgrid,(1,2,3,4,0))
        if fix_boundary: idx = idx[1:-1,1:-1,1:-1]
        idx = idx.reshape(-1,4)
    else:
        print (err_text)
        exit ('get_latt_idx: sp_lat with invalid shape!')
    if pinned_idx is not None:
        for idx0 in pinned_idx:
            idx = idx[np.linalg.norm(idx-idx0,axis=1)!=0]
    if savetxt:
        qn = 'nx ny nz nat'.split()
        if idx.shape[1]==4: qn.remove('nz')
        fmt = '{:>5s}'+' {:>7s}'*(len(qn)-1)
        if os.path.isdir(outdir)==False: print ('skip saving dyn_idx.dat because {} not found'.format(outdir))
        else: np.savetxt('{}/dyn_idx.dat'.format(outdir),idx,fmt='%7d',header=fmt.format(*tuple(qn)))
    return nx,ny,nz,nat,idx



# get the exchange matrix/vector for all neighbors, from one specific pair
# via symmetric operation (rotation)
def get_exchange_xyz(exch,rotvec_neighbor):
    nat,n_neigh = rotvec_neighbor.shape[:2]
    shape0=[nat,n_neigh]+list(exch.shape[1:])
    exch_xyz = np.zeros(shape0,float)
    for iat,inn in np.ndindex(nat,n_neigh):
        rot = RT.from_rotvec(rotvec_neighbor[iat,inn]).as_matrix()
        if len(exch.shape)==2: exch_xyz[iat,inn] = np.dot(rot,exch[iat])               # vectorial exchange
        if len(exch.shape)==3: exch_xyz[iat,inn] = np.dot(np.dot(rot,exch[iat]),rot.T) # tensorial exchange
    return exch_xyz



# only applicable to periodic boundary condtion case
def calc_neighbors_in_sp_lat(neigh_idx,sp_lat):
    shape = sp_lat.shape
    nx,ny,nz,nat,idx = get_latt_idx(shape)
    n_neigh = neigh_idx.shape[1]
    neigh_idx_all = np.zeros((nx,ny,nz,nat,n_neigh,len(shape)-1),int)
    if len(shape)==4: neigh_idx_all = neigh_idx_all[:,:,0]
    for i,idx0 in enumerate(idx):
        iat = idx0[-1]
        for j,idx_n in enumerate(neigh_idx[iat]):
            idx1 = [(m+n)%s for m,n,s in zip(idx0[:-1],idx_n[:-1],shape[:-2])] + [idx_n[-1]]
            neigh_idx_all[tuple(idx0)][j] = idx1
    return neigh_idx_all



# suppose a magnetic bond is composed of sites 1 and 2
# idx0 is the index for site 1 of the bond
# idx_n is the neighbor index given in magnetic unit cell
# idx1 is the index for site 2 of the bond 
# if the bond is broken down due to open boundary
# the function returns None
#
# idx0, idx_n and the returned idx1 are in shape of 
# ix,iy    for 2D lattice, and
# ix,iy,iz for 3D lattice
#
# shape is the shape of sp_lat array
# for 2D, it is (nx,ny,nat,3)
# for 3D, it is (nx,ny,nz,nat,3)
def calc_neigh_bond_idx(idx0,idx_n,shape,boundary_condition):
    idx1 = [m+n for m,n in zip(idx0[:-1],idx_n[:-1])]
    for k,item in enumerate(idx1):
        if boundary_condition[k]==0 and (item<0 or item>shape[k]-1): return None
        else: idx1[k] = item%shape[k]
    idx1 += [idx_n[-1]]
    return idx1


fmt_head = '{:>3s} '*4+'{:>10s}'*3
fm1 = '{:3d} '+'{:3.0f} '*3+'{:10.4f}'*3
fm2 = (' '*16+'{:10.4f}'*3+'\n')*2
head_tags = ['iat','Rx','Ry','jat','x','y','z']

def display_exchange(neigh_idx,exchange_xyz,exchange_type,file_handle=None):
    if exchange_xyz is None: return 1
    if np.max([np.abs(exch) for exch in exchange_xyz]):
        print ('\n{0}'.format(exchange_type),file=file_handle)
        print (fmt_head.format(*tuple(head_tags)),file=file_handle)
    for iat in range(len(exchange_xyz)):
        exch = exchange_xyz[iat]
        if exch is None: continue
        for inn in range(len(exch)):
            if np.linalg.norm(exch[inn]):
                print (fm1.format(iat,*tuple(np.append(neigh_idx[iat][inn],exch[inn]))),file=file_handle)
            if inn==len(exch)-1: print ('',file=file_handle)


def display_exchange_matrix(neigh_idx,exchange_xyz,exchange_type,file_handle=None):
    if exchange_xyz is None: return 1
    if np.max([np.abs(exch) for exch in exchange_xyz]):
        print ('\n{0}'.format(exchange_type),file=file_handle)
        print (fmt_head.format(*tuple(head_tags)),file=file_handle)
        for iat in range(len(exchange_xyz)):
            exch = exchange_xyz[iat]
            if exch is None: continue
            for inn in range(len(exch)):
                if np.max(abs(exch[inn])):
                    print (fm1.format(iat,*tuple(np.append(neigh_idx[iat][inn],exch[inn,0]))),file=file_handle)
                    print (fm2.format(*tuple(exch[inn,1:].flatten())),file=file_handle)
    else:
        print ('{} is set but the magnitude is zero'.format(exchange_type),file=file_handle)




def DM_vector_to_matrix(DM_vec):
    DM_as_mat = np.zeros((3,3),float)
    for k in range(3):
        i=(k+1)%3
        j=(k+2)%3
        DM_as_mat[i,j] = DM_vec[k]
        DM_as_mat[j,i] =-DM_vec[k]
    return DM_as_mat




# exchange pairs grouped by shell (e.g. 1st NN, 2nd NN, ...)
class exchange_shell():

    def __init__(self,neigh_idx,
        J_iso=None,J_sym_xyz=None,DM_xyz=None,
        Kitaev_mag=None,Kitaev_xyz=None,
        Jmat=None,shell_name='shell exch'):

        self._neigh_idx = neigh_idx
        self._J_iso = J_iso
        self._J_sym_xyz = J_sym_xyz
        self._DM_xyz = DM_xyz
        self._Kitaev_mag = Kitaev_mag
        self._Kitaev_xyz = Kitaev_xyz
        self._Jmat = Jmat
        self._shell_name = shell_name
        self._nat = len(self._neigh_idx) 

        if J_sym_xyz is not None and self._Jmat is None: 
            self._Jmat = self.calc_Jmat()

        if self._Jmat is not None and self._J_sym_xyz is None and self._DM_xyz is None:
            self._J_sym_xyz, self._DM_xyz = self.calc_sym_mat_and_DMI()


    def calc_Jmat(self):
        nat,nneigh = self._neigh_idx.shape[:2]
        Jmat = np.zeros((nat,nneigh,3,3),float)
        if self._J_sym_xyz is not None:
            Jmat = copy.copy(self._J_sym_xyz)
        else:
            if self._J_iso is not None:
                for iat,i in np.ndindex(nat,3):
                    Jmat[iat,:,i,i] = self._J_iso[iat]
            if self._Kitaev_mag is not None and self._Kitaev_xyz is not None:
                for iat,inn,i,j in np.ndindex(nat,nneigh,3,3):
                    Jmat[iat,inn,i,j] += self._Kitaev_mag[iat] * self._Kitaev_xyz[iat,inn,i] * self._Kitaev_xyz[iat,inn,j]

        if self._DM_xyz is not None:
            for iat,inn in np.ndindex(nat,nneigh):
                if self._DM_xyz[iat] is None: continue
                DM_as_mat = DM_vector_to_matrix(self._DM_xyz[iat][inn])
                Jmat[iat,inn] += DM_as_mat
        return Jmat



    def calc_sym_mat_and_DMI(self):
        nat = len(self._neigh_idx)
        nneigh = max([len(neigh) for neigh in self._neigh_idx if neigh is not None])
        #nat,nneigh = self._neigh_idx.shape[:2]
        J_sym_xyz = np.zeros((nat,nneigh,3,3),float)
        DM_xyz = np.zeros((nat,nneigh,3),float)
 
        for iat,inn in np.ndindex(nat,nneigh):
            J0 = self._Jmat[iat][inn]
            J_sym_xyz[iat][inn] = (J0 + J0.T)/2
            for k in range(3):
                i=(k+1)%3
                j=(k+2)%3
                DM_xyz[iat][inn,k] = (J0[i,j] - J0[j,i])/2
        return J_sym_xyz, DM_xyz



    def verbose_interactions(self,sym_mat=False,Jmat=False,file_handle=None):
        print ('\n{0}\n{1:20s}\n{0}'.format('*'*50,self._shell_name),file=file_handle)
        if sym_mat:
            display_exchange_matrix(self._neigh_idx,self._J_sym_xyz,'symm exch',file_handle=file_handle)
        elif Jmat:
            display_exchange_matrix(self._neigh_idx,self._Jmat,'Jmat exch',file_handle=file_handle)
        else:
            print ('\nHeisenberg exchange',file=file_handle)
            nat = len(self._J_iso)
            if nat>10:
                fmt='{:10.4f}'*10+'\n'
                fmt_grid = fmt*(nat//10)+'{:10.4f}'*np.mod(nat,10)+'\n'
                print (fmt_grid.format(*tuple(self._J_iso)),file=file_handle)
            else: 
                print (('J_iso = '+'{:10.4f}'*self._nat).format(*tuple(self._J_iso)),file=file_handle)
            if self._Kitaev_mag is not None:
                if np.linalg.norm(self._Kitaev_mag):
                    print (('\nKitaev strength '+'{:10.4f}'*self._nat).format(*tuple(self._Kitaev_mag)),file=file_handle)
                    display_exchange(self._neigh_idx,self._Kitaev_xyz,'Kitaev',file_handle=file_handle)
        display_exchange(self._neigh_idx,self._DM_xyz,'DM',file_handle=file_handle)


    def shell_isotropic_exch_energy(self,sp_lat,boundary_condition=[1,1,1],parallel=False):
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        ntask = len(idx)
        start,last = (0,ntask)
        if parallel and enable_mpi: start,last = mt.assign_task(ntask,size,rank)
        E_iso = 0.
        for ii,idx0 in enumerate(idx[start:last]):
            iat = idx0[-1]
            n_i = sp_lat[tuple(idx0)]
            for j,idx_n in enumerate(self._neigh_idx[iat]):
                idx1 = calc_neigh_bond_idx(idx0,idx_n,shape,boundary_condition)
                if idx1 is not None:
                    n_j = sp_lat[tuple(idx1)]
                    E_iso -= self._J_iso[iat]*np.dot(n_i,n_j)
        if parallel: E_iso = comm.allreduce(E_iso)
        return E_iso/2


    def shell_exch_energy(self,sp_lat,boundary_condition=[1,1,1],parallel=False):
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        ntask = len(idx)
        start,last = (0,ntask)
        if parallel and enable_mpi: start,last = mt.assign_task(ntask,size,rank)
 
        E_iso = 0.
        E_DMI = 0.
        E_Kitaev = 0.
        for idx0 in idx[start:last]:
            iat = idx0[-1]
            n_i = sp_lat[tuple(idx0)]
            for j,idx_n in enumerate(self._neigh_idx[iat]):
                idx1 = calc_neigh_bond_idx(idx0,idx_n,shape,boundary_condition)
                if idx1 is not None:
                    n_j = sp_lat[tuple(idx1)]
                    E_iso -= self._J_iso[iat]*np.dot(n_i,n_j)
                    if self._Kitaev_mag is not None: 
                        E_Kitaev -= self._Kitaev_mag[iat]*np.dot(n_i,self._Kitaev_xyz[iat,j])*np.dot(n_j,self._Kitaev_xyz[iat,j])
                    if self._DM_xyz is not None: 
                        #E_DMI -= np.dot(np.cross(n_i,n_j),self._DM_xyz[iat][j])
                        E_DMI -= np.linalg.det([self._DM_xyz[iat][j],n_i,n_j])
        if parallel: 
            E_iso = comm.allreduce(E_iso)
            E_sym = comm.allreduce(E_sym)
            E_DMI = comm.allreduce(E_DMI)
        return E_iso/2, E_DMI/2, E_Kitaev/2


    def shell_exch_energy_from_sym_mat(self,sp_lat,boundary_condition=[1,1,1],parallel=False):
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        ntask = len(idx)
        start,last = (0,ntask)
        if parallel and enable_mpi: start,last = mt.assign_task(ntask,size,rank)
        E_sym = 0.
        E_DMI = 0.
        for idx0 in idx[start:last]:
            iat = idx0[-1]
            n_i = sp_lat[tuple(idx0)]
            for j,idx_n in enumerate(self._neigh_idx[iat]):
                idx1 = calc_neigh_bond_idx(idx0,idx_n,shape,boundary_condition)
                if idx1 is not None:
                    n_j = sp_lat[tuple(idx1)]
                    if self._J_sym_xyz is not None: E_sym -= np.einsum('a,ab,b', n_i, self._J_sym_xyz[iat][j] ,n_j)
                    if self._DM_xyz is not None: E_DMI -= np.linalg.det([self._DM_xyz[iat][j],n_i,n_j])
        if parallel: 
            E_sym = comm.allreduce(E_sym)
            E_DMI = comm.allreduce(E_DMI)
        return E_sym/2, E_DMI/2


    def shell_exch_energy_from_Jmat(self,sp_lat,boundary_condition=[1,1,1],parallel=False):
        if self._Jmat is None: return 0
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        ntask = len(idx)
        start,last = (0,ntask)
        if parallel and enable_mpi: start,last = mt.assign_task(ntask,size,rank)
        E_exch = 0.
        for idx0 in idx[start:last]:
            iat = idx0[-1]
            n_i = sp_lat[tuple(idx0)]
            for j,idx_n in enumerate(self._neigh_idx[iat]):
                idx1 = calc_neigh_bond_idx(idx0,idx_n,shape,boundary_condition)
                if idx1 is not None:
                    n_j = sp_lat[tuple(idx1)]
                    E_exch -= np.einsum('a,ab,b', n_i, self._Jmat[iat][j],n_j)
        if parallel: E_exch = comm.allreduce(E_exch)
        return E_exch/2


    def shell_exch_energy_from_Jmat_new(self,sp_lat):
        nat = sp_lat.shape[-2]
        E_exch = 0
        for iat in range(nat):
            for j,idx_n in enumerate(self._neigh_idx[iat]):
                dR = idx_n[:-1]
                jat = idx_n[-1]
                sp_lat_tmp = np.roll(sp_lat,tuple(-dR),axis=range(len(dR)))
                E_exch -= np.einsum('...m,mn,...n',sp_lat[...,iat,:],self._Jmat[iat,j],sp_lat_tmp[...,jat,:]).sum()
        return E_exch/2


    def local_exchange_energy(self,sp_lat,site_idx,boundary_condition=[1,1,1]):
        shape=sp_lat.shape
        E_local = 0.
        iat = site_idx[-1]
        n_i = sp_lat[tuple(site_idx)]
        for j,idx_n in enumerate(self._neigh_idx[iat]):
            idx1 = calc_neigh_bond_idx(site_idx,idx_n,shape,boundary_condition)
            if idx1 is None: continue
            n_j = sp_lat[tuple(idx1)]
            if self._Jmat is not None: E_local -= np.dot(np.dot(n_i,self._Jmat[iat,j]),n_j)
            else: E_local -= self._J_iso[iat]*np.dot(n_i,n_j)
        return E_local
 

    def shell_isotropic_exch_field(self,sp_lat,site_idx,boundary_condition=[1,1,1]):
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        B_eff = np.zeros(3,float)
        iat = site_idx[-1]
        n_i = sp_lat[tuple(site_idx)]
        for j,idx_n in enumerate(self._neigh_idx[iat]):
            idx1 = calc_neigh_bond_idx(site_idx,idx_n,shape,boundary_condition)
            if idx1 is not None:
                n_j = sp_lat[tuple(idx1)]
                B_eff += self._J_iso[iat]*n_j
        return B_eff


    def local_exch_field(self,sp_lat,site_idx,boundary_condition=[1,1,1]):
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        B_eff = np.zeros(3,float)
        iat = site_idx[-1]
        n_i = sp_lat[tuple(site_idx)]
        for j,idx_n in enumerate(self._neigh_idx[iat]):
            idx1 = calc_neigh_bond_idx(site_idx,idx_n,shape,boundary_condition)
            if idx1 is not None:
                n_j = sp_lat[tuple(idx1)]
                B_eff += self._J_iso[iat]*n_j
                B_eff += np.cross(n_j,self._DM_xyz[iat][j])
                if self._Kitaev_mag is not None:
                    B_eff += self._Kitaev_mag[iat]*np.dot(n_j,self._Kitaev_xyz[iat,j])*self._Kitaev_xyz[iat,j]
        return B_eff


    def local_exch_field_from_sym_mat(self,sp_lat,site_idx,boundary_condition=[1,1,1]):
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        B_eff = np.zeros(3,float)
        iat = site_idx[-1]
        n_i = sp_lat[tuple(site_idx)]
        for j,idx_n in enumerate(self._neigh_idx[iat]):
            idx1 = calc_neigh_bond_idx(site_idx,idx_n,shape,boundary_condition)
            if idx1 is not None:
                n_j = sp_lat[tuple(idx1)]
                B_eff += np.dot(self._J_sym_xyz[iat][j], n_j)
                B_eff += np.cross(n_j,self._DM_xyz[iat][j])
        return B_eff


    def local_exch_field_from_Jmat(self,sp_lat,site_idx,boundary_condition=[1,1,1]):
        if self._Jmat is None: return np.zeros(3)
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        B_eff = np.zeros(3,float)
        iat = site_idx[-1]
        n_i = sp_lat[tuple(site_idx)]
        for j,idx_n in enumerate(self._neigh_idx[iat]):
            idx1 = calc_neigh_bond_idx(site_idx,idx_n,shape,boundary_condition)
            if idx1 is not None:
                n_j = sp_lat[tuple(idx1)]
                B_eff += np.dot(self._Jmat[iat][j], n_j)
        return B_eff


    def local_exch_field_from_Jmat_new(self,sp_lat,site_idx):
        neigh_idx_all = calc_neighbors_in_sp_lat(self._neigh_idx,sp_lat)
        B_eff = np.zeros(3,float)
        iat = site_idx[-1]
        for j,idx1 in enumerate(neigh_idx_all[tuple(site_idx)]):
            n_j = sp_lat[tuple(idx1)]
            B_eff += np.dot(self._Jmat[iat,j], n_j)
        return B_eff



# we currently only support scalar biquadratic exchange
# the magnitude is given by BQ
class biquadratic_exchange_shell():
    def __init__(self,neigh_idx,BQ,shell_name):
        self._neigh_idx = neigh_idx
        self._BQ = BQ
        self._shell_name = shell_name
        self._nat = len(self._neigh_idx)


    def verbose_interactions(self,file_handle=None):
        print ('\nBiquadratic exchange {}'.format(self._shell_name),file=file_handle)
        try: print (('{:8.5f} '*len(self._BQ)+'\n').format(*tuple(self._BQ)),file=file_handle)
        except: print ('None',file=file_handle)


    def shell_exch_energy(self,sp_lat,boundary_condition=[1,1,1],parallel=False):
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        ntask = len(idx)
        start,last = (0,ntask)
        if parallel and enable_mpi: start,last = mt.assign_task(ntask,size,rank)
        E_bq = 0.
        for idx0 in idx[start:last]:
            iat = idx0[-1]
            n_i = sp_lat[tuple(idx0)]
            for j,idx_n in enumerate(self._neigh_idx[iat]):
                idx1 = calc_neigh_bond_idx(idx0,idx_n,shape,boundary_condition)
                if idx1 is not None:
                    n_j = sp_lat[tuple(idx1)]
                    E_bq -= self._BQ[iat] * (n_i[2]*n_j[2])**2
        return E_bq/2


    def shell_exch_energy_new(self,sp_lat):
        neigh_idx_all = calc_neighbors_in_sp_lat(self._neigh_idx,sp_lat)
        shape = sp_lat.shape
        E_bq = 0.
        for idx0 in np.ndindex(shape[:-1]):
            n_i = sp_lat[tuple(idx0)]
            iat = idx0[-1]
            for j,idx1 in enumerate(neigh_idx_all[tuple(idx0)]):
                n_j = sp_lat[tuple(idx1)]
                E_bq -= self._BQ[iat] * (n_i[2]*n_j[2])**2
        if parallel: E_bq = comm.allreduce(E_bq)
        return E_bq/2


    def local_exch_field(self,sp_lat,site_idx,boundary_condition=[1,1,1]):
        shape = sp_lat.shape
        iat = site_idx[-1]
        n_i = sp_lat[tuple(site_idx)]
        B_eff = np.zeros(3)
        for j,idx_n in enumerate(self._neigh_idx[iat]):
            idx1 = calc_neigh_bond_idx(site_idx,idx_n,shape,boundary_condition)
            if idx1 is not None:
                n_j = sp_lat[tuple(idx1)]
                B_eff += 2*self._BQ[iat]*n_i[2]*n_j[2]**2
        return B_eff


    def local_exch_field_new(self,sp_lat,site_idx):
        neigh_idx_all = calc_neighbors_in_sp_lat(self._neigh_idx,sp_lat)
        shape = sp_lat.shape
        n_i = sp_lat[tuple(site_idx)]
        iat = site_idx[-1]
        B_eff = np.zeros(3)
        for j,idx1 in enumerate(neigh_idx_all[tuple(site_idx)]):
            n_j = sp_lat[tuple(idx1)]
            B_eff += 2*self._BQ[iat]*n_i[2]*n_j[2]**2
        return B_eff


# A generic form of biquadratic exchange
# in the form of (S_i * B_{ij} * S_j)**2
# the parameter BQ should be an numpy.ndarray
# in shape of (nat,n_neigh,3,3)
# One should note that, for the BQ matrix here
# the zz component is indeed the square root 
# of the BQ exchange in biquadratic_exchange_shell
# the previous class
class biquadratic_exchange_shell_general():
    def __init__(self,neigh_idx,BQ,shell_name):
        self._neigh_idx = neigh_idx
        self._BQ = BQ
        self._shell_name = shell_name
        self._nat = len(self._neigh_idx)


    def verbose_interactions(self,file_handle=None):
        print ('\nBiquadratic exchange {}, in generic matrix form'.format(self._shell_name),file=file_handle)
        display_exchange_matrix(self._neigh_idx,self._BQ,'Biquadratic exchange',file_handle=file_handle)


    def shell_exch_energy(self,sp_lat,boundary_condition=[1,1,1],parallel=False):
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        ntask = len(idx)
        start,last = (0,ntask)
        if parallel and enable_mpi: start,last = mt.assign_task(ntask,size,rank)
        E_bq = 0.
        for idx0 in idx[start:last]:
            iat = idx0[-1]
            n_i = sp_lat[tuple(idx0)]
            for j,idx_n in enumerate(self._neigh_idx[iat]):
                idx1 = calc_neigh_bond_idx(idx0,idx_n,shape,boundary_condition)
                if idx1 is not None:
                    n_j = sp_lat[tuple(idx1)]
                    E_bq -= np.einsum('mn,m,n', self._BQ[iat,j], n_i, n_j)**2
        if parallel: E_bq = comm.allreduce(E_bq)
        return E_bq/2


    def shell_exch_energy_new(self,sp_lat):
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        E_bq = 0.
        for iat in range(nat):
            for j,idx_n in enumerate(self._neigh_idx[iat]):
                dR = idx_n[:-1]
                jat = idx_n[-1]
                sp_lat_tmp = np.roll(sp_lat,tuple(-dR),axis=range(len(dR)))
                E_bq -= (np.einsum('...m,mn,...n',sp_lat[...,iat,:],self._BQ[iat,j],sp_lat_tmp[...,jat,:])**2).sum()
        return E_bq/2


    def local_exchange_energy(self,sp_lat,site_idx,boundary_condition=[1,1,1]):
        shape = sp_lat.shape
        E_local = 0.
        iat = site_idx[-1]
        n_i = sp_lat[tuple(site_idx)]
        for j,idx_n in enumerate(self._neigh_idx[iat]):
            idx1 = calc_neigh_bond_idx(site_idx,idx_n,shape,boundary_condition)
            if idx1 is None: continue
            n_j = sp_lat[tuple(idx1)]
            E_local -= np.einsum('mn,m,n', self._BQ[iat,j], n_i, n_j)**2
        return E_local


    def local_exch_field(self,sp_lat,site_idx,boundary_condition=[1,1,1]):
        shape = sp_lat.shape
        iat = site_idx[-1]
        n_i = sp_lat[tuple(site_idx)]
        B_eff = np.zeros(3)
        for j,idx_n in enumerate(self._neigh_idx[iat]):
            idx1 = calc_neigh_bond_idx(site_idx,idx_n,shape,boundary_condition)
            if idx1 is not None:
                n_j = sp_lat[tuple(idx1)]
                B_eff += 2*np.einsum('mn,m,n',self._BQ[iat,j],n_i,n_j) * np.dot(self._BQ[iat,j], n_j)
        return B_eff


    def local_exch_field_new(self,sp_lat,site_idx):
        n_i = sp_lat[tuple(site_idx)]
        iat = site_idx[-1]
        B_eff = np.zeros(3)
        for j,idx_n in enumerate(self._neigh_idx[iat]):
            dR = idx_n[:-1]
            jat = idx_n[-1]
            sp_lat_tmp = np.roll(sp_lat,tuple(-dR),axis=range(len(dR)))
            n_j = sp_lat_tmp[tuple(idx_n)]
            B_eff += 2*np.einsum('mn,m,n',self._BQ[iat,j],n_i,n_j) * np.dot(self._BQ[iat,j],n_j)
        return B_eff


    # exchange field over the whole spin lattice
    def shell_exch_field(self,sp_lat):
        B_eff = np.zeros_like(sp_lat)
        nat = sp_lat.shape[-2]
        for iat in range(nat):
            for j,idx_n in enumerate(self._neigh_idx[iat]):
                dR = idx_n[:-1]
                jat = idx_n[-1]
                sp_lat_tmp = np.roll(sp_lat,tuple(-dR),axis=tuple(range(len(dR))))
                B_eff[...,iat,:] += 2*np.einsum('mn,...m,...n->...',self._BQ[iat,j],sp_lat[...,iat,:],sp_lat_tmp[...,jat,:]) * np.dot(self._BQ[iat,j],sp_lat_tmp[...,jat,:])
        return B_eff





# four-site biquadratic exchange coupling
class four_site_biquadratic_exchange_shell():
    def __init__(self,neigh_idx,BQ,shell_name):
        self._neigh_idx = neigh_idx
        self._BQ = BQ
        self._shell_name = shell_name
        self._nat = len(self._neigh_idx)


    def verbose_interactions(self,file_handle=None):
        print ('\nFour-site Biquadratic exchange {}, in generic matrix form'.format(self._shell_name),file=file_handle)
        display_exchange_matrix(self._neigh_idx,self._BQ,'Biquadratic exchange',file_handle=file_handle)


    def shell_exch_energy(self,sp_lat,boundary_condition=[1,1,1],parallel=False):
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        ntask = len(idx)
        start,last = (0,ntask)
        if parallel and enable_mpi: start,last = mt.assign_task(ntask,size,rank)
        E_bq = 0.
        for idx0 in idx[start:last]:
            iat = idx0[-1]
            n_i = sp_lat[tuple(idx0)]
            for inn,idx_n in enumerate(self._neigh_idx[iat]):
                idx_j = calc_neigh_bond_idx(idx0,idx_n[0],shape,boundary_condition)
                idx_k = calc_neigh_bond_idx(idx0,idx_n[1],shape,boundary_condition)
                idx_l = calc_neigh_bond_idx(idx0,idx_n[2],shape,boundary_condition)
                #if None in [idx_j,idx_k,idx_l]: continue
                if idx_j is None or idx_k is None or idx_l is None: continue
                n_j = sp_lat[tuple(idx_j)]
                n_k = sp_lat[tuple(idx_k)]
                n_l = sp_lat[tuple(idx_l)]
                E_bq -= self._BQ[iat,inn] * np.dot(n_i, n_j) * np.dot(n_k, n_l)
        if parallel:  E_bq = comm.allreduce(E_bq)
        return E_bq


    def shell_exch_energy_new(self,sp_lat):
        shape = sp_lat.shape
        nx,ny,nz,nat,idx = get_latt_idx(shape)
        E_bq = 0.
        for iat in range(nat):
            for j,idx_n in enumerate(self._neigh_idx[iat]):
                dR = idx_n[:-1]
                jat = idx_n[-1]
                sp_lat_tmp = np.roll(sp_lat,tuple(-dR),axis=range(len(dR)))
                E_bq -= (np.einsum('...m,mn,...n',sp_lat[...,iat,:],self._BQ[iat,j],sp_lat_tmp[...,jat,:])**2).sum()
        return E_bq


    def local_exchange_energy(self,sp_lat,site_idx,boundary_condition=[1,1,1]):
        E_local = 0.
        iat = site_idx[-1]
        n_i = sp_lat[tuple(site_idx)]
        for inn,idx_n in enumerate(self._neigh_idx[iat]):
            idx_j = calc_neigh_bond_idx(idx0,idx_n[0],shape,boundary_condition)
            idx_k = calc_neigh_bond_idx(idx0,idx_n[1],shape,boundary_condition)
            idx_l = calc_neigh_bond_idx(idx0,idx_n[2],shape,boundary_condition)
            if idx_j is None or idx_k is None or idx_l is None: continue
            n_j = sp_lat[tuple(idx_j)]
            n_k = sp_lat[tuple(idx_k)]
            n_l = sp_lat[tuple(idx_l)]
            E_local -= self._BQ[iat,inn] * np.dot(n_i, n_j) * np.dot(n_k, n_l)
        return E_local


    def local_exch_field(self,sp_lat,site_idx,boundary_condition=[1,1,1]):
        shape = sp_lat.shape
        iat = site_idx[-1]
        n_i = sp_lat[tuple(site_idx)]
        B_eff = np.zeros(3)
        for inn,idx_n in enumerate(self._neigh_idx[iat]):
            idx_j = calc_neigh_bond_idx(site_idx,idx_n[0],shape,boundary_condition)
            idx_k = calc_neigh_bond_idx(site_idx,idx_n[1],shape,boundary_condition)
            idx_l = calc_neigh_bond_idx(site_idx,idx_n[2],shape,boundary_condition)
            #if None in [idx_j,idx_k,idx_l]: continue
            if idx_j is None or idx_k is None or idx_l is None: continue
            n_j = sp_lat[tuple(idx_j)]
            n_k = sp_lat[tuple(idx_k)]
            n_l = sp_lat[tuple(idx_l)]
            B_eff += self._BQ[iat,inn] * n_j * np.dot(n_k, n_l)
        return B_eff


    def local_exch_field_new(self,sp_lat,site_idx):
        n_i = sp_lat[tuple(site_idx)]
        iat = site_idx[-1]
        B_eff = np.zeros(3)
        for inn,idx_n in enumerate(self._neigh_idx[iat]):
            dR = idx_n[:-1]
            jat = idx_n[-1]
            sp_lat_tmp = np.roll(sp_lat,tuple(-dR),axis=range(len(dR)))
            n_j = sp_lat_tmp[tuple(idx_n)]
            B_eff += 2*np.einsum('mn,m,n',self._BQ[iat,j],n_i,n_j) * np.dot(self._BQ[iat,inn],n_j)
        return B_eff
