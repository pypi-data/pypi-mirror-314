#!/usr/bin/env python

# ===================================================
# Utility to generate Kitaev-type spin Hamiltonian
# Can be implemented to perform
# Classic spin dyanmics simulations (pyasd) or
# Quantum spin simulation (HPhi or quspin)
#
# Shunhong Zhang <szhang2@ustc.edu.cn>
# Last modified: May 14 2024
#
#====================================================
#
#
# suppose we have a honeycomb lattice, and consider Kitaev interactions between neighboring sites
# for one site in A sublattice, we have three neighboring sites in B sublattice
# the exchange interation is called bond
# for each bond, there is an easy magnetization axis call Kitaev axis
# From symmetry consideration, we can asssume that each Kitaev axis has its in-plane component along the bond
# now we want to calculate the out-of-plane cosine of the Kitaev axis, so that
# the three Kitaev axes subject to three bonds from the same site are perpendicular to each other

import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation as RT

r2h = np.sqrt(2)/2
r3h = np.sqrt(3)/2


# Here, K1, K2, and K3 are mutually orthogonal
# they defines the Kitaev axis foe each bond in the honeycomb lattice
# see Fig. 1 of Phys. Rev. Lett. 124, 087205 (2020) for illustration
# of the local coordinate system obtained from Lowdin orthogonalization
# of the tensorial exchange couplings between nearest neighbors
#
# Note: here the honeycom lattice is defined following HPhi
# cell: [[1,0,0],[0.5,r3h,0],[0,0,c]]
# atom: [[1/3,1/3,1/2],[2/3,2/3,1/2]]
# bond: three bonds denoted as X, Y, and Z respectively
# The IN-PLANE components of each bond and its Kitaev axis are orthogonal
#
def get_axes_vec():
    K1 = np.array([-0.5, r3h,r2h])
    K2 = np.array([-0.5,-r3h,r2h])
    K3 = np.array([1,0,r2h])
    return [K/np.linalg.norm(K) for K in [K1, K2, K3]]


def DMI_vector_to_matrix(DM_vec):
    DM_mat = np.zeros((3,3))
    for i in range(3):
        DM_mat[i,(i+1)%3] = DM_vec[(i+2)%3]
        DM_mat[(i+1)%3,i] =-DM_vec[(i+2)%3]
    return DM_mat



def Lowdin_to_global(J_Heis, Kitaev, Gamma1, Gamma2, verbosity=1):
    # the three Kitaev axes
    # they form a matrix which is the transform matrix between two coordinate systems
    K1,K2,K3 = get_axes_vec()
    if verbosity:
        print ('\nKitaev axes')
        for K in (K1,K2,K3):  print (('{:10.6f} '*3).format(*tuple(K)))
    Kvecs = np.array([K1, K2, K3])

    # the three bond-dependent exchange matrices (3*3)
    J_Lowdin = np.zeros((3,3,3))
    if verbosity: print ('\nExchange matrices in the local alpha-beta-gamma (XYZ) coordinate')

    J_Lowdin[0] = np.array([
    [J_Heis + Kitaev, Gamma2, Gamma2],
    [Gamma2,          J_Heis, Gamma1],
    [Gamma2,          Gamma1, J_Heis]])

    J_Lowdin[1] = np.array([
    [J_Heis, Gamma2,          Gamma1],
    [Gamma2, J_Heis + Kitaev, Gamma2],
    [Gamma1, Gamma2,          J_Heis]])

    J_Lowdin[2] = np.array([
    [J_Heis , Gamma1, Gamma2         ],
    [Gamma1,  J_Heis, Gamma2         ],
    [Gamma2,  Gamma2, J_Heis + Kitaev]])

    for ibond in range(3):
        assert np.allclose(J_Lowdin[ibond], J_Lowdin[ibond].T), 'J matrix of bond {} not symmetryic!'.format(ibond)
        assert np.allclose(np.linalg.norm(Kvecs[ibond]),1,atol=1e-6), 'Kitaev vectors should be normalized'
        if verbosity: print ((('{:10.6f} '*3+'\n')*3).format(*tuple(J_Lowdin[ibond].flatten())))

    if verbosity: print ('\nExchange matrices in the global xyz coordinate')
    J_trans = []
    for ibond in range(3):
        J_mat = J_Lowdin[ibond]
        J_tran = np.dot(np.dot(Kvecs.T,J_mat),Kvecs)
        assert np.allclose(J_tran,J_tran.T), 'J matrix should be symmetric here!'
        J_trans.append( J_tran )
        if verbosity: print ((('{:10.6f} '*3+'\n')*3).format(*tuple(J_trans[ibond].flatten())))

    return J_Lowdin, J_trans


# write inputs for standard mode of HPhi
def write_HPhi_exchange(J_XYZ,DMI_vecs=None,file=None,verbosity=1,coord='Global'):
    dirs = {0:'x',1:'y',2:'z'}
    nbond = len(J_XYZ)
    J_tots = []
    for ibond in range(nbond):
        J_tot = J_XYZ[ibond] 
        if DMI_vecs is not None: 
            if coord=='Global':
                J_tot += DMI_vector_to_matrix(DMI_vecs[ibond]) 
            elif coord=='Lowdin':
                print ('\nNote from write_HPhi_exchange:')
                print ('DMI_vecs provided, but ')
                print ('the symmetric exchange is given in Lowdin coord')
                print ('To avoid silly mistakes, DMI will NOT be added')
        J_tots.append(J_tot)
        print ('',file=file)
        for ii,jj in np.ndindex(3,3):
            if ii==jj: component = dirs[ii]
            else: component = '{}{}'.format(dirs[ii],dirs[jj])
            print (('J{}{:<2s} = {:16.12f}').format(ibond,component,J_tot[ii,jj]),file=file)
        print ('',file=file)
        if file is not None and verbosity: print ((('{:16.12f} '*3+'\n')*3).format(*tuple(J_tot.flatten())))

    if verbosity: print ('Sanity check: the three-fold rotational symmetry')
    if coord=='Global': vec = np.array([0,0,2*np.pi/3])
    if coord=='Lowdin': vec = np.array([1,1,1])*2*np.pi/3/np.sqrt(3)
    rot = RT.from_rotvec(vec).as_matrix()
    for ibond in range(3):
        rotated_J = np.dot(np.dot(rot,J_tots[ibond]),rot.T)
        np.testing.assert_allclose(rotated_J,J_tots[(ibond+1)%3],atol=1e-8,rtol=1e-8)
    if verbosity: print ('passed')
    return J_tots


# Bloch-type, along bonds
def gen_Bloch_DMI_vecs(DMI):
    DM1 = np.array([r3h,0.5,0])*DMI
    DM2 = np.array([-r3h,0.5,0])*DMI
    DM3 = np.array([0,-1,0])*DMI
    DMI_vecs = [DM1, DM2, DM3]
    return DMI_vecs


# Neel-type normal to bonds, in the plane
def gen_Neel_DMI_vecs(DMI):
    DM1 = np.array([-0.5, r3h,0])*DMI
    DM2 = np.array([-0.5,-r3h,0])*DMI
    DM3 = np.array([1,0,0])*DMI
    DMI_vecs = [DM1, DM2, DM3]
    return DMI_vecs


def params_compressed_CrSiTe3():
    # parameters for CrSiTe3 under -2.34 % compressive strain, 
    # which was demonstrated as a QSL candidate
    # See PRL 124, 087205 (2020), Supplementary Table S1
    # Note that the Kitaev term is antiferromagnetic here
    J_Heis = -0.1019
    Kitaev =  0.2747
    Gamma1 =  0.0204
    Gamma2 = -0.0838
    return J_Heis, Kitaev, Gamma1, Gamma2



stan_in_head='''model = "SpinGCCMA"
W = 3
L = 3
method = "Lanczos"
lattice = "Honeycomb"
2S=1
EigenvecIO = "out"
'''

job_script='''#!/bin/bash
#SBATCH -p amd_512
#SBATCH -N 2
#SBATCH -n 256
source /public3/soft/modules/module.sh
module load mpi/openmpi/4.1.1-gcc9.3.0
module load intel/2022.1
HPhi -s stan.in
'''

def test_transformation_by_ED(ntest=3,stan_in_head=stan_in_head,job_script=job_script):

    def test_one_Jmat(Jmat,cdir,coord='Global'):
        os.mkdir(cdir)
        os.chdir(cdir)
        with open('stan.in','w') as fw:
            fw.write(stan_in_head)
            write_HPhi_exchange(Jmat,DMI_vecs=None,file=fw,verbosity=0,coord=coord)
        open('sub.sh','w').write(job_script)
        os.system('sbatch sub.sh')
        os.chdir('..')

    cwd = os.getcwd()
    outdir='test_ED'
    if os.path.isdir(outdir): os.system('rm -rf {}'.format(outdir))
    os.mkdir(outdir)
    os.chdir(outdir)
    for itest in range(ntest):
        cdir = 'ED_{}'.format(itest)
        print ('Create testing case at {}'.format(cdir))
        os.mkdir(cdir)
        os.chdir(cdir)
        J_Heis, Kitaev, Gamma1, Gamma2 = np.random.random(4)
        J_Lowdin, J_XYZ = Lowdin_to_global(J_Heis, Kitaev, Gamma1, Gamma2, verbosity=0)
        test_one_Jmat(J_Lowdin,'Lowdin','Lowdin')
        test_one_Jmat(J_XYZ,'Global','Global')
        os.chdir('..')
    os.chdir(cwd)



J_Heis = 0
Kitaev = -1
Gamma1 = 0
Gamma2 = 0

DMI = 0.
DMI_vecs = gen_Bloch_DMI_vecs(DMI)
DMI_vecs = gen_Neel_DMI_vecs(DMI)

if __name__=='__main__':
    J_lowdin, J_XYZ = Lowdin_to_global(J_Heis, Kitaev, Gamma1, Gamma2)
    write_HPhi_exchange(J_XYZ,DMI_vecs,file=open('stan.in','w'))
    test_transformation_by_ED(ntest=5,stan_in_head=stan_in_head,job_script=job_script)

