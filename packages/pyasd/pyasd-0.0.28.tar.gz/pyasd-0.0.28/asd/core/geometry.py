#!/usr/bin/env python

# build lattice for spin dynamics simulations
# last modified: Dec 19 2020
# Shunhong Zhang <szhang2@ustc.edu.cn>

import numpy as np
from scipy.spatial.transform import Rotation as RT

r3h=np.sqrt(3)/2

# in fractional coordinates
# sites should be in shape of (nx,ny,nat,ndim), ndim can be 2 or 3
def get_repeated_sites(sites,repeat_x=1,repeat_y=1):
    nx,ny=sites.shape[:2]
    sites_repeat = np.tile(sites,(repeat_x,repeat_y,1,1))
    for i,j in np.ndindex(repeat_x,repeat_y):
        sites_repeat[i*nx:(i+1)*nx,j*ny:(j+1)*ny,:,0] += i*nx
        sites_repeat[i*nx:(i+1)*nx,j*ny:(j+1)*ny,:,1] += j*ny
    return sites_repeat


# find sites in a shell with circular or elliptic shape
# periodic boundary condition is applied in the 2D lattice
# ellipticity defines the shape of ellipse (1 is circle)
def find_pbc_shell(sites,latt,radius,center_pos=np.zeros(3),ellipticity=1.,orig=None):
    nx,ny,nat = sites.shape[:3]
    if orig is None: orig = np.array([nx,ny])/2.
    rvec_pbc = []
    for ix,iy in np.ndindex(3,3):
        ndim = min(sites.shape[-1], len(orig), len(center_pos), latt.shape[-1])
        r = sites[...,:ndim] - orig[:ndim] - center_pos[:ndim]
        R = np.array([(ix-1)*nx,(iy-1)*ny,0])
        rvec_add = np.dot(r + R[:ndim], latt[:ndim,:ndim])
        rvec_add[...,1] *= ellipticity
        rvec_pbc.append(rvec_add)

    rvec_pbc = np.array(rvec_pbc)
    dist_pbc = np.linalg.norm(rvec_pbc,axis=-1)
    rvec = np.zeros((nx,ny,nat,ndim),float)
    idx = np.argmin(dist_pbc,axis=0)
    for ix,iy,iat in np.ndindex(nx,ny,nat):
        rvec[ix,iy,iat] = rvec_pbc[idx[ix,iy,iat],ix,iy,iat]
    dist = np.min(dist_pbc,axis=0)
    shell_idx=np.array(np.where(dist<=radius)).T
    return shell_idx,rvec


def generate_bond_vectors(latt0, sites, neigh_idx):
    if neigh_idx is None: return None
    bond_vectors=[]
    nat,ndim = sites.shape[-2:]
    ndim = min(ndim, latt0.shape[1])
    for iat in range(nat):
        bond_vectors.append([])
        if neigh_idx[iat] is None: continue
        for inn,neigh in enumerate(neigh_idx[iat]):
            if neigh is None: 
                bond_vectors[iat].append(None)
            else:
                dR = neigh[:-1]
                jat = neigh[-1]
                vec = np.zeros(3)
                r = sites[0,0,jat] - sites[0,0,iat]
                vec[:ndim] = np.einsum('a,ab->b',r[:ndim], latt0[:ndim,:ndim]) + dR[0]*latt0[0,:ndim] + dR[1]*latt0[1,:ndim]
                bond_vectors[iat].append(vec)
    return bond_vectors



def display_bond_vectors(all_bond_vectors):
    for inn, bond_vectors in enumerate(all_bond_vectors):
        print ('\n{}NN bond vectors'.format(inn+1))
        for iat in range(2):
            print ('Site {}'.format(iat))
            for ii, b in enumerate(bond_vectors[iat]): print (('{:6.3f} '*3).format(*tuple(b)))


def build_vacuum(latt, sites_sc, vacuum=10):
    if latt.shape[1]==2:
        latt_3D = np.zeros((3,3))
        latt_3D[:2,:2] = latt
    else:
        latt_3D = latt
    latt_3D[2,2] = vacuum
 
    if sites_sc.shape[-1]==2:
        sites_sc_3D = np.zeros((*tuple(sites_sc.shape[:-1]),3))
        sites_sc_3D[...,:2] = sites_sc
    else:
        sites_sc_3D = sites_sc
    return latt_3D, sites_sc_3D



def build_molecular_model(mol_type, radius=1, orig=np.array([1.5,1.5,0]),
    latt = np.array([[3,0,0],[0,3,0],[0,0,10]]), nat=None ):

    if mol_type=='dimer':
        start_angle=0
        nat=2
    if mol_type=='trimer':
        start_angle=90
        nat=3
    elif mol_type=='tetramer':
        start_angle=45
        nat=4
    elif mol_type=='pentamer':
        start_angle=18
        nat=5
    elif mol_type=='hexamer':
        start_angle=0
        nat=6
    else:
        typeErr = "Wrong mol_type! Should be trimer/ tetramer / pentamer/ hexamer. Or specify nat directly."
        if nat is not None: start_angle=0
        else: raise ValueError(typeErr)

    angle_step = 360.0/nat
    sites_cart = radius * np.array([[[ [np.cos(theta), np.sin(theta), latt[2,2]/2]
    for theta in np.deg2rad(np.arange(start_angle,start_angle+360.0,angle_step)) ]]])
    sites_cart += orig
    neigh_idx = np.zeros((nat,2,3), int)
    for iat in range(nat): neigh_idx[iat,:,2] = np.array([[(iat-1)%nat,(iat+1)%nat]])
    bond_vectors = np.array([
    [sites_cart[jx,jy,jat] - sites_cart[0,0,iat] for (jx,jy,jat) in neigh_idx[iat]]
    for iat in range(sites_cart.shape[-2]) ])

    return latt, sites_cart, neigh_idx, bond_vectors



 
def build_Lieb_lattice(nx,ny,nz=1,latt_const=1,vacuum=None):
    latt = np.eye(2)*latt_const
    nat = 3
    sites_uc = np.array([[0,0],[0.5,0],[0,0.5]])
    sites = np.zeros((nx,ny,nat,2))
    if vacuum is not None: sites = np.zeros((nx,ny,nat,3))
    for ix,iy in np.ndindex(nx,ny):
        sites[ix,iy,:,:2] = sites_uc + np.array([ix,iy])
    neigh1_idx = [ [[0,0,1],[0,0,2],[-1,0,1],[0,-1,2]], [[0,0,0],[1,0,0],None,None], [[0,0,0],[0,1,0],None,None] ]
    neigh2_idx = [ [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0]], [[0,0,2],[1,0,2],[0,-1,2],[1,-1,2]], [[0,0,1],[-1,0,1],[0,1,1],[-1,1,1]] ]
 
    rotvecs = [None, None]
    neigh_idx = [neigh1_idx, neigh2_idx]
    if vacuum is not None: latt, sites = build_vacuum(latt, sites, vacuum)
    return latt, sites, neigh_idx, rotvecs



def rectangular_honeycomb_cell(nx,ny,nz,return_neigh=True,latt_const=1,vacuum=None):
    latt = np.array([[1,0],[0,np.sqrt(3)]])*latt_const
    xx,yy=np.mgrid[0:nx,0:ny]
    nat = 4
    sites=np.zeros((nx,ny,nat,2),float)
    if vacuum is not None: sites=np.zeros((nx,ny,nat,3))
    sites_home = np.array([[1./4,1./3],[3./4,5./6],[3./4,1./6],[1./4,2./3]])
    for iat in range(nat):
        sites[...,iat,0] = xx + sites_home[iat,0]
        sites[...,iat,1] = yy + sites_home[iat,1]

    neigh1_idx = np.array([[[0, 0,3],[-1,0,2],[ 0,0,2]],
                           [[0, 1,2],[ 0,0,3],[ 1,0,3]],
                           [[0,-1,1],[ 1,0,0],[ 0,0,0]],
                           [[0, 0,0],[ 0,0,1],[-1,0,1]]])

    neigh2_idx = np.array([[[1,0,0],[0,0,1],[-1,0,1],[-1,0,0],[-1,-1,1],[0,-1,1]],
                           [[1,0,1],[1,1,0],[ 0,1,0],[-1,0,1],[ 0, 0,0],[1, 0,0]],
                           [[1,0,2],[1,0,3],[ 0,0,3],[-1,0,2],[ 0,-1,3],[1,-1,3]],
                           [[1,0,3],[0,1,2],[-1,1,2],[-1,0,3],[-1, 0,2],[0, 0,2]]])

    neigh3_idx = np.array([[[0,-1,3],[ 1, 0,3],[-1, 0,3]],
                           [[0, 0,2],[ 1, 1,2],[-1, 1,2]],
                           [[0, 0,1],[-1,-1,1],[ 1,-1,1]],
                           [[0, 1,0],[-1, 0,0],[ 1,0,0]]])

    #check_neigh_idx(latt,sites_home,[neigh1_idx,neigh2_idx,neigh3_idx])

    rotvec_neigh1 = np.array([[0.,0.,i*2./3] for i in range(3)])*np.pi
    rotvec_neigh1 = np.tile(rotvec_neigh1,(4,1,1))
    rotvec_neigh2 = np.array([[0,0,0],[r3h,0.5,0],[0,0,2./3],[0,1,0],[0,0,4./3],[r3h,-0.5,0]])*np.pi
    rotvec_neigh2 = np.tile(rotvec_neigh2,(4,1,1))
    rotvec_neigh3 = np.array([np.array([0,0,i*2./3])*np.pi for i in range(3)])
    rotvec_neigh3 = np.tile(rotvec_neigh3,(4,1,1))

    neigh_idx = [neigh1_idx, neigh2_idx, neigh3_idx]
    rotvecs = [rotvec_neigh1, rotvec_neigh2, rotvec_neigh3]
    latt *= latt_const
    if vacuum is not None: latt, sites = build_vacuum(latt, sites, vacuum)
    if return_neigh: return latt, sites, neigh_idx, rotvecs
    else: return latt, sites



def build_latt(lat_type,nx,ny,nz,latt_choice=2,return_neigh=True,latt_const=1,vacuum=None, Kekule_distortion=0.05):
    lat_type_list = ['chain','square','triangular','kagome','honeycomb','simple cubic','lieb']
    lat_type = lat_type.lower()

    neigh4_idx = None
    rotvec_neigh4 = None

    if lat_type=='simple cubic':
        nat=1
        latt=np.eye(3)
        sites=np.zeros((1,1,1,nat,3),float)+0.5
        neigh1_cell_idx = np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]])
        neigh2_cell_idx = np.array([
        [0,1,1],[0,1,-1],[0,-1,1],[0,-1,-1],
        [1,0,1],[1,0,-1],[-1,0,1],[-1,0,-1],
        [1,1,0],[1,-1,0],[-1,1,0],[-1,-1,0]])
        neigh3_cell_idx = np.mgrid[-1:2:2,-1:2:2,-1:2:2].T.reshape(-1,3)
        neigh1_idx = np.zeros((nat, 6,4),int)
        neigh2_idx = np.zeros((nat,12,4),int)
        neigh3_idx = np.zeros((nat, 8,4),int)
        neigh1_idx[:,:,:3] = neigh1_cell_idx
        neigh2_idx[:,:,:3] = neigh2_cell_idx
        neigh3_idx[:,:,:3] = neigh3_cell_idx

        rotvec_neigh1 = np.array([[[0.,0.,i] for i in range(4)]+[[0.,1.,0.],[0.,-1.,0.]]])*np.pi/2
        rotvec_neigh2 = np.array([[[0.,0.,i] for i in range(4)]+[[0.,1.,0.],[0.,-1.,0.]]])*np.pi/2
        rotvec_neigh3 = np.array([[[0.,0.,i] for i in range(4)]+[[0.,1.,0.],[0.,-1.,0.]]])*np.pi/2

    elif lat_type=='bcc':
        nat=2
        latt=np.eye(3)
        sites=np.zeros((1,1,1,nat,3),float)
        sites[...,1,:] += 0.5

        neigh1_cell_idx = np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]])
        neigh2_cell_idx = np.array([
        [0,1,1],[0,1,-1],[0,-1,1],[0,-1,-1],
        [1,0,1],[1,0,-1],[-1,0,1],[-1,0,-1],
        [1,1,0],[1,-1,0],[-1,1,0],[-1,-1,0]])
        neigh3_cell_idx = np.mgrid[-1:2:2,-1:2:2,-1:2:2].T.reshape(-1,3)

    elif lat_type=='chain':    # 1D chain built in 2D form
        if latt_choice == 1:   # monoatomic chain
            nat=1
            latt=np.eye(2)
            sites=np.array([[[0.5,0.5]]])
            neigh1_cell_idx = np.array([[[-1],[1]]])
            neigh2_cell_idx = neigh1_cell_idx*2
            neigh3_cell_idx = neigh1_cell_idx*3
            neigh1_idx = np.zeros((nat,2,3),int)
            neigh2_idx = np.zeros((nat,2,3),int)
            neigh3_idx = np.zeros((nat,2,3),int)
            neigh1_idx[:,:,:1] = neigh1_cell_idx
            neigh2_idx[:,:,:1] = neigh2_cell_idx
            neigh3_idx[:,:,:1] = neigh3_cell_idx
            rotvec_neigh1 = None
            rotvec_neigh2 = None
            rotvec_neigh3 = None

        elif latt_choice == 2:  # biatomic chain
            nat=2
            latt=np.eye(2)
            sites=np.array([[[0.25,0.5],[0.75,0.5]]])
            neigh1_idx = np.array([ [[0,0,1],[-1,0,1]], [[1,0,0],[0, 0,0]] ])
            neigh2_idx = np.array([ [[1,0,0],[-1,0,0]], [[1,0,1],[-1,0,1]] ])
            neigh3_idx = np.array([ [[1,0,1],[-2,0,1]], [[2,0,0],[-1,0,0]] ])
            rotvec_neigh1 = None
            rotvec_neigh2 = None
            rotvec_neigh3 = None

        else:
            raise ValueError('Invalid latt_choice {} for lat_type = {}'.format(latt_choice, lat_type))

    elif lat_type=='square':
        if latt_choice==2:
            nat=1
            latt=np.eye(2)
            sites=np.zeros((1,1,nat,2),float)+0.5
            neigh1_cell_idx = np.array([[[1,0],[0,1],[-1,0],[0,-1]]])
            neigh2_cell_idx = np.array([[[1,1],[-1,1],[-1,-1],[1,-1]]])
            neigh3_cell_idx = neigh1_cell_idx * 2
            neigh4_cell_idx = np.array([[2,1],[1,2],[-1,2],[-2,1],[-2,-1],[-1,-2],[1,-2],[2,-1]])
            neigh1_idx = np.zeros((nat,4,3),int)
            neigh2_idx = np.zeros((nat,4,3),int)
            neigh3_idx = np.zeros((nat,4,3),int)
            neigh4_idx = np.zeros((nat,8,3),int)
            neigh1_idx[:,:,:2] = neigh1_cell_idx
            neigh2_idx[:,:,:2] = neigh2_cell_idx
            neigh3_idx[:,:,:2] = neigh3_cell_idx
            neigh4_idx[:,:,:2] = neigh4_cell_idx

            rotvec_neigh1 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])
            rotvec_neigh2 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])
            rotvec_neigh3 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])
            #rotvec_neigh4 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])

        elif latt_choice==1:
            """ Checkboard-like square lattice containing two sites per cell"""
            nat = 2
            latt = np.sqrt(2)*np.eye(2)
            sites = np.zeros((1,1,nat,2),float)
            sites[...,1,:] += 0.5
            neigh1_idx = np.array([
            [[0,0,1],[-1,0,1],[-1,-1,1],[0,-1,1]],
            [[1,1,0],[0,1,0],[0,0,0],[1,0,0]]
            ])
            neigh2_idx = np.array([
            [[1,0,0],[0,1,0],[-1,0,0],[0,-1,0]],
            [[1,0,1],[0,1,1],[-1,0,1],[0,-1,1]]
            ])
            neigh3_idx = np.array([
            [[1,1,0],[-1,1,0],[-1,-1,0],[1,-1,0]],
            [[1,1,1],[-1,1,1],[-1,-1,1],[1,-1,1]]
            ])
            neigh4_idx = np.array([
            [[1,0,1],[0,1,1],[-1,1,1],[-2,0,1],[-2,-1,1],[-1,-2,1],[0,-2,1],[1,-1,1]],
            [[2,1,0],[1,2,0],[0,2,0],[-1,1,0],[-1,0,0],[0,-1,0],[1,-1,0],[2,0,0]],
            ])

            rotvec_neigh1 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])
            rotvec_neigh2 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])
            rotvec_neigh3 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])

        elif latt_choice==3:
            nat=4
            latt=np.eye(2)*2
            sites = np.array([[0,0],[0.5,0.5],[0.5,0.0],[0.0,0.5]])
            neigh1_idx = np.array([
            [[0,0,2],[0,0,3],[-1,0,2],[0,-1,3]],
            [[1,0,3],[0,1,2],[0,0,3],[0,0,2]],
            [[1,0,0],[0,0,1],[0,0,0],[0,-1,1]],
            [[0,0,1],[0,1,0],[-1,0,1],[0,0,0]] 
            ])
            neigh2_idx = None
            neigh3_idx = None
            neigh4_idx = None

            rotvec_neigh1 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])
            rotvec_neigh2 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])
            rotvec_neigh3 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])
            #rotvec_neigh4 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])
 

    elif lat_type=='lieb':
        latt,sites,all_neigh_idx,rotvecs = build_Lieb_lattice(nx,ny,nz,latt_const=1,vacuum=vacuum)
        if return_neigh: return latt,sites,all_neigh_idx,rotvecs
        else: return latt,sites

    elif lat_type=='triangular':
        if latt_choice == 2:  # the unit cell
            nat=1
            latt=np.array([[1,0],[-0.5,r3h]])
            sites=np.zeros((1,1,nat,2),float)+0.5
            neigh1_cell_idx = np.array([[[1,0],[1,1],[0,1],[-1,0],[-1,-1],[0,-1]]])
            neigh2_cell_idx = np.array([[[2,1],[1,2],[-1,1],[-2,-1],[-1,-2],[1,-1]]])
            neigh3_cell_idx = neigh1_cell_idx * 2
            neigh1_idx = np.zeros((nat,6,3),int)
            neigh2_idx = np.zeros((nat,6,3),int)
            neigh3_idx = np.zeros((nat,6,3),int)
            neigh1_idx[:,:,:2] = neigh1_cell_idx
            neigh2_idx[:,:,:2] = neigh2_cell_idx
            neigh3_idx[:,:,:2] = neigh3_cell_idx

            #rotvec_neigh1 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(6)]])
            rotvec_neigh1 = np.array([[[0,0,0],[r3h,0.5,0],[0,0,2./3],[0,1,0],[0,0,4./3],[r3h,-0.5,0]]])*np.pi
            rotvec_neigh2 = np.array([[[0,0,0],[0.5,r3h,0],[0,0,2./3],[-0.5,r3h,0],[0,0,4./3],[1,0,0]]])*np.pi
            rotvec_neigh3 = np.array([[[0,0,0],[r3h,0.5,0],[0,0,2./3],[0,1,0],[0,0,4./3],[r3h,-0.5,0]]])*np.pi


        elif latt_choice == 1: 
            nat=3
            latt=np.array([[1,0],[-0.5,r3h]])*np.sqrt(3)
            sites=np.zeros((1,1,nat,2),float)
            for i in range(3): 
                sites[:,:,i,0] += 5./6 - i/3.
                sites[:,:,i,1] += 1./6 + i/3.

            neigh1_idx = np.array([
            [ [1,0,1],[0,0,1], [0,-1,1],[1,0,2],[0,-1,2],[1,-1,2] ],
            [ [0,0,2],[0,-1,2],[1,0,2], [0,0,0],[0,1,0], [-1,0,0] ],
            [ [0,1,0],[-1,1,0],[-1,0,0],[0,0,1],[0,1,1], [-1,0,1] ]  ])

            neigh2_cell_idx = np.array([[[1,0],[1,1],[0,1],[-1,0],[-1,-1],[0,-1]]])
            neigh2_idx = np.zeros((nat,6,3),int)
            neigh2_idx[:,:,:2] = neigh2_cell_idx
            for iat in range(nat): neigh2_idx[iat,:,-1] = iat
      
            #neigh3_idx = np.array([[],[],[]])
            neigh3_idx = None

            rotvec_neigh1 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(6)]])
            rotvec_neigh2 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(6)]])
            rotvec_neigh3 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(6)]])

        else:
            raise ValueError('Invalid latt_choice {} for lat_type = {}'.format(latt_choice, lat_type))



    elif lat_type=='kagome':
        nat=3
        latt=np.array([[1,0],[-0.5,r3h]])
        sites=np.zeros((1,1,nat,2),float)
        for i in range(3):
            sites[:,:,i,0] = (i<2)
            sites[:,:,i,1] = (i>0)
        sites *= 0.5

        neigh1_idx = np.array([
        [  [0,-1,2],[0,-1,1],[1,0,2],[0,0,1]  ],
        [  [0, 0,0],[1, 0,2],[0,1,0],[0,0,2]  ],
        [  [-1,0,1],[-1,0,0],[0,0,1],[0,1,0]  ]  
        ])

        neigh2_idx = np.array([
        [  [1, 0,1],[-1,-1,1],[0,0,2],[ 1,-1,2]  ],
        [  [1, 1,0],[-1, 0,0],[1,1,2],[ 0,-1,2]  ],
        [  [0, 0,0],[-1, 1,0],[0,1,1],[-1,-1,1]  ]
        ])

        neigh3_idx = np.array([
        [  [-1,0, 0],[ 1, 0,0]  ],
        [  [-1,-1,1],[ 1, 1,1]  ],
        [  [ 0,-1,2],[ 0, 1,2]  ]
        ])

        # to be developed
        rotvec_neigh1 = None
        rotvec_neigh2 = None
        rotvec_neigh3 = np.array([[[0,0,0],[0,1,0]], [[0,0,2/3],[0.5,-np.sqrt(3)/2,0]], [[0,0,4/3],[-0.5,-np.sqrt(3)/2,0]]])*np.pi


    elif lat_type=='honeycomb':
        sites=np.zeros((1,1,2,2),float)
        nat=2

        if latt_choice == 1:  # consistent with Spirit code
            latt = np.array([[0.5,-r3h],[0.5,r3h]])
            sites[0,0,0]=np.array([0,0])
            sites[0,0,1]=np.array([1./3,2./3])
            neigh1_cell_idx = np.array([[0,0],[-1,-1],[0,-1]])
            neigh2_cell_idx = np.array([[1,1],[0,1],[-1,0],[-1,-1],[0,-1],[1,0]])
            neigh3_cell_idx = np.array([[-1,0],[-1,-2],[1,0]])
            rotvec_neigh1 = np.array([[0.,0.,i*2./3] for i in range(3)])*np.pi

        elif latt_choice == 2:  # consistent with our DFT calculations
            latt = np.array([[1,0],[-0.5,r3h]])
            sites[0,0,0] = np.array([1./3,2./3])
            sites[0,0,1] = np.array([2./3,1./3])
            neigh1_cell_idx = np.array([[0,1],[-1,0],[0,0]])
            neigh2_cell_idx = np.array([[1,0],[1,1],[0,1],[-1,0],[-1,-1],[0,-1]])
            neigh3_cell_idx = np.array([[-1,-1],[1,1],[-1,1]])
            neigh4_idx = np.array([
            [[1,0,1],[1,2,1],[0,2,1],[-2,0,1],[-2,-1,1],[0,-1,1]],
            [[2,0,0],[2,1,0],[0,1,0],[-1,0,0],[-1,-2,0],[0,-2,0]] ])
            rotvec_neigh1 = np.array([[0.,0.,i*2./3] for i in range(3)])*np.pi

        elif latt_choice==3:  # honeycomb lattice with a rectangular 4-site unit cell
            return rectangular_honeycomb_cell(nx,ny,nz,return_neigh=return_neigh,latt_const=1,vacuum=vacuum)

        elif latt_choice==4:  # sqrt(3)*sqrt(3) supercell
            nat = 6
            latt = np.array([[3,0],[-3/2, 3*np.sqrt(3)/2]])
            sites = np.array([[0,0],[1/3,2/3],[2/3,1/3],[1/3,0],[0,1/3],[2/3,2/3]])
            neigh1_idx = np.array([
            [[0,0,3],[0,0,4],[-1,-1,5]],
            [[0,0,5],[0,1,3],[0,0,4],],
            [[1,0,4],[0,0,5],[0,0,3]],
            [[0,0,0],[0,-1,1],[0,0,2]],
            [[-1,0,2],[0,0,0],[0,0,1]],
            [[0,0,1],[0,0,2],[1,1,0]]
            ])
            neigh2_idx = None
            neigh3_idx = None
            rotvec_neigh1 = None
            rotvec_neigh2 = None
            rotvec_neigh3 = None
            rotvec_neigh4 = None

        elif latt_choice==5:  # sqrt(3)*sqrt(3) supercell with Kekule distortion
            nat = 6
            d = Kekule_distortion
            latt = np.array([[3,0],[-3/2, 3*np.sqrt(3)/2]])
            sites = np.array([[0,0],[1/3-d,2/3-2*d],[2/3-2*d,1/3-d],[1/3-d,0],[0,1/3-d],[2/3-2*d,2/3-2*d]])
            neigh1_idx = np.array([
            [[0,0,3],[0,0,4]],
            [[0,0,5],[0,0,4]],
            [[0,0,5],[0,0,3]],
            [[0,0,0],[0,0,2]],
            [[0,0,0],[0,0,1]],
            [[0,0,1],[0,0,2]]
            ])
            neigh2_idx = np.array([
            [[-1,-1,5]],
            [[0,1,3]],
            [[1,0,4]],
            [[0,-1,1]],
            [[-1,0,2]],
            [[1,1,0]],
            ])
            neigh3_idx = None
            rotvec_neigh1 = None
            rotvec_neigh2 = None
            rotvec_neigh3 = None
            rotvec_neigh4 = None

        else:
            print ('Available latt_choice for honeycomb lattice\n')
            print ('1 or 2: rhombohedral; 3: rectangular; 4: sqrt(3)*sqrt(3); 5: Kekule.')
            print ('Now: latt_choice = {}'.format(latt_choice))
            raise ValueError('Invalid latt_choice {} for lat_type = {}'.format(latt_choice, lat_type))

        if latt_choice == 1 or latt_choice==2:
            neigh1_idx = np.zeros((nat,3,3),int)
            neigh1_idx[0,:,:2] =  neigh1_cell_idx
            neigh1_idx[1,:,:2] = -neigh1_cell_idx
            neigh1_idx[0,:,2] = 1
            neigh1_idx[1,:,2] = 0

            neigh2_idx = np.zeros((nat,6,3),int)
            for iat in range(nat): neigh2_idx[iat,:,:2] = neigh2_cell_idx
            neigh2_idx[1,:,2] = 1

            neigh3_idx = np.zeros((nat,3,3),int)
            neigh3_idx[0,:,:2] =  neigh3_cell_idx
            neigh3_idx[1,:,:2] = -neigh3_cell_idx
            neigh3_idx[0,:,2] = 1
            neigh3_idx[1,:,2] = 0

            rotvec_neigh1 = np.array([rotvec_neigh1,rotvec_neigh1])
            rotvec_neigh2 = np.array([[0,0,0],[r3h,0.5,0],[0,0,2./3],[0,1,0],[0,0,4./3],[r3h,-0.5,0]])*np.pi
            rotvec_neigh2 = np.array([rotvec_neigh2,rotvec_neigh2])
            rotvec_neigh3 = np.array([np.array([0,0,i*2./3])*np.pi for i in range(3)])
            rotvec_neigh3 = np.array([rotvec_neigh3,rotvec_neigh3])

    else:
        print ('Currently valid lat_type:')
        for item in lat_type_list: print (item)
        exit ('Your specified lattice type: {}'.format(lat_type))

    ndim=sites.shape[-1]
    if ndim==2:
        xx,yy=np.mgrid[0:nx,0:ny]
        sites_sc = np.zeros((nx,ny,nat,ndim),float)
        for iat in range(nat):
            sites_sc[...,iat,0] = sites[...,iat,0] + xx
            sites_sc[...,iat,1] = sites[...,iat,1] + yy
    elif ndim==3:
        xx,yy,zz = np.mgrid[0:nx,0:ny,0:nz]
        sites_sc = np.zeros((nx,ny,nz,nat,ndim),float)
        for iat in range(nat):
            sites_sc[...,iat,0] = sites[...,iat,0] + xx
            sites_sc[...,iat,1] = sites[...,iat,1] + yy
            sites_sc[...,iat,2] = sites[...,iat,2] + zz

    neigh_idx = [neigh1_idx, neigh2_idx, neigh3_idx, neigh4_idx]
    rotvecs = [rotvec_neigh1, rotvec_neigh2, rotvec_neigh3, rotvec_neigh4]
    latt *= latt_const
    if vacuum is not None: latt, sites_sc = build_vacuum(latt, sites_sc, vacuum)
    if return_neigh: return latt,sites_sc,neigh_idx,rotvecs
    else: return latt,sites_sc



def gen_neigh_idx_for_supercell(all_neigh_idx, nx, ny, nz):
    """
    For given lists of neighbor atom indices
    generate the lists for neighbors within a nx*ny*nz supercell
    
    Inputs:
    -----------
    all_neigh_idx: list of lists
    each list represent a shell of neighbors, grouped by atoms

    nx, ny, nz: positive integer
    size of the supercell

    Returns:
    -----------
    all_neigh_idx_sc: list of lists
    lists of neighbors for atoms in the specified supercell
    """

    nshell = len(all_neigh_idx)
    all_neigh_idx_sc = []
    for ishell in range(nshell):
        neigh_idx = all_neigh_idx[ishell]
        if neigh_idx  is None: continue
        neigh_idx_sc = []
        nat = len(neigh_idx)
        for ix, iy in np.ndindex(nx,ny):
            for iat in range(nat):
                neigh_idx_sc.append([])
                for inn, neigh in enumerate(neigh_idx[iat]):
                    dR = neigh[:-1]
                    jat = neigh[-1]
                    jx = ix + dR[0]
                    jy = iy + dR[1]
                    if len(dR)==2:
                        sc_jx = jx//nx
                        sc_jy = jy//ny
                        sc_jat = (jx%nx)*ny*nat + (jy%ny)*nat + jat
                        neigh_idx_sc[-1].append([sc_jx, sc_jy, sc_jat])
                    elif len(dR)==3:
                        jz = dR[2]
                        sc_jz = jz//nz
                        sc_jat = (jx%nx)*ny*nz*nat + (jy%ny)*nz*nat + (jz%nz)*nat + jat
                        neigh_idx_sc[-1].append([sc_jx, sc_jy, sc_jz, sc_jat])

        all_neigh_idx_sc.append(neigh_idx_sc)
    return all_neigh_idx_sc




def plot_cell(ax,latt,origin=None,color='gray'):
    points = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]])
    if origin is not None: points += origin
    points_cart = np.dot(points,latt[:2,:2])
    frame, = ax.plot(*tuple(points_cart.T),ls='--',c=color,alpha=0.7,zorder=-1)
    return frame


def show_neighbors(latt,sites_sc,neigh_idx,central_atom_index=0,title=None,
    legend_position = [0.95,0.8], show=True):

    import matplotlib.pyplot as plt

    shape = sites_sc.shape
    if len(shape)==4: 
        nx,ny,nat = shape[:-1]
    else:
        nx,ny,nz,nat = shape[:-1] 
        raise Exception('3D lattice? Cannot be displayed!')

    sites_cart = np.dot(sites_sc,latt)
    cnx = nx//2
    cny = ny//2

    print ('Showing neighbors of atom {} (red star)'.format(central_atom_index))

    fig,ax = plt.subplots(1,1)
    plot_cell(ax, latt, origin=np.array([cnx,cny]))
    for iat in range(nat): ax.scatter(*tuple(sites_cart[...,iat,:2].T),s=30)
    ax.scatter(*tuple(sites_cart[cnx,cny,central_atom_index,:2].T),marker='*',c='r',s=80)
    for ish,neigh_shell in enumerate(neigh_idx):
        if neigh_shell is None: continue
        s_shell = []
        for inn,(dx,dy,jat) in enumerate(neigh_shell[central_atom_index]):
            jx = cnx + dx
            jy = cny + dy
            if jx>=nx or jy>=ny:
                print ('\nSkip plotting the {}-th neighbor because it is out of range'.format(inn))
            else:
                s = sites_cart[jx,jy,jat]
                s_shell.append(s)
                ax.text(*tuple(s.T[:2]),'{:1d}'.format(inn),c='w',ha='center',va='center')
        s_shell = np.array(s_shell)
        ax.scatter(*tuple(s_shell.T[:2]),ec='none',fc='C{}'.format(ish+1),s=150,label='{}NN'.format(ish+1))
    ax.legend(bbox_to_anchor=legend_position)
    if title is not None: ax.set_title(title)
    ax.set_aspect('equal')
    ax.set_axis_off()
    fig.subplots_adjust(right=0.9)
    fig.tight_layout()
    if show: plt.show()
    return fig



def display_lattice_sites(latt,sites,show=False):
    import matplotlib.pyplot as plt
    nx,ny,nat=sites.shape[:3]
    points = np.dot([[0,0],[1,0],[1,1],[0,1],[0,0]],latt[:2,:2])
    spoints = np.dot([[0,0],[nx,0],[nx,ny],[0,ny],[0,0]],latt[:2,:2])
    all_sites = np.dot(sites[...,:2],latt[:2,:2]).reshape(-1,2)
    fig,ax=plt.subplots(1,1)
    ax.plot(points[:,0],points[:,1],'g--')
    ax.plot(spoints[:,0],spoints[:,1])
    for iat in range(nat): ax.scatter(*tuple(all_sites[iat::nat].T),label=str(iat))

    for ix, iy in np.ndindex(nx,ny):
        R = np.dot(np.array([ix,iy]), latt)
        p = points + R
        ax.plot(p[:,0], p[:,1], 'm--')
    ax.legend(bbox_to_anchor=[1.01,0.5])
    ax.set_aspect('equal')
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig('cell_sites',dpi=500)
    if show: plt.show()
    return fig



def calc_space_disp(latt,sites,cutoff_x,cutoff_y,cutoff_z=0,ndim=2,verbosity=0):
    from asd.core.shell_exchange import get_latt_idx
    shape = sites.shape
    nx,ny,nz,nat,idx = get_latt_idx(shape)
    nnx = 2*cutoff_x+1
    nny = 2*cutoff_y+1
    nnz = 2*cutoff_z+1
    sites_cart = np.dot(sites,latt)
    ndim = sites_cart.shape[-1]
    if verbosity: print ('Calculate displacements between lattice sites.')
 
    if len(shape)==4:
        space_disp = np.zeros((nnx,nny,nat,nat,ndim),float)
        if verbosity: print (space_disp.shape)
        for iat,jat in np.ndindex(nat,nat):
            r_ij = sites_cart[0,0,jat] - sites_cart[0,0,iat]
            for ii,dx in enumerate(range(-cutoff_x,cutoff_x+1)):
                for jj,dy in enumerate(range(-cutoff_y,cutoff_y+1)):
                    dR = dx*latt[0] + dy*latt[1]
                    space_disp[ii,jj,iat,jat] = r_ij + dR

    if len(shape)==5:
        space_disp = np.zeros((nnx,nny,nnz,nat,nat,ndim),float)
        if verbosity: print (space_disp.shape)
        for iat,jat in np.ndindex(nat,nat):
            r_ij = sites_cart[0,0,jat] - sites_cart[0,0,iat]
            for ii,dx in enumerate(range(-cutoff_x,cutoff_x+1)):
                for jj,dy in enumerate(range(-cutoff_y,cutoff_y+1)):
                    for kk,dz in enumerate(range(-cutoff_z,cutoff_z+1)):
                        dR = np.dot([dx,dy,dz],latt)  
                        space_disp[ii,jj,kk,iat,jat] = r_ij + dR
 
    return space_disp



#===============================================
# some functions related to reciprocal lattice
#===============================================

def get_BZ_path_labels(lat_type, latt_choice=2, ribbon=False, ribbon_dir=0, short=False):
    # In fractional coordinate
    if lat_type in ['kagome','triangular', 'triangular_r3'] or (lat_type=='honeycomb' and latt_choice in [1,2,4,5]):
        xlabels='\Gamma M K \Gamma K^\prime M^\prime \Gamma M M^\prime'
        path=[[0,0,0],[0.5,0,0],[1/3,1/3,0],[0,0,0],[-1/3,2/3,0],[0,0.5,0],[0,0,0],[0.5,0,0],[0,0.5,0]]
        if short:
            xlabels = 'M K \Gamma K^\prime M^\prime'
            path = [[1/2,0,0],[1/3,1/3,0],[0,0,0],[-1/3,2/3,0],[0,1/2,0]]
        BZ = np.array([[1,1,0],[-1,2,0],[-2,1,0],[-1,-1,0],[1,-2,0],[2,-1,0],[1,1,0]])/3
    elif lat_type=='square' or (lat_type=='honeycomb' and latt_choice==3) or lat_type=='Lieb':
        xlabels = '\Gamma X M \Gamma M Y \Gamma'
        path = [[0,0,0],[0.5,0,0],[0.5,0.5,0],[0,0,0],[0.5,0.5,0],[0,0.5,0],[0,0,0]]
        BZ = np.array([[-1,-1,0],[-1,1,0],[1,1,0],[1,-1,0],[-1,-1,0]])/2
    elif lat_type=='chain':
        xlabels = 'X \Gamma \\bar{X}'
        path = [[0.5,0,0],[0,0,0],[-0.5,0,0]]
        BZ = np.array([[-0.5,0,0],[0.5,0,0]])
    else:
        exit('get_BZ_path_labels: invalid lat_type {}'.format(lat_type))

    if ribbon:
        if ribbon_dir==0:
            xlabels = 'X \Gamma \\bar{X}'
            path = [[0.5,0,0],[0,0,0],[-0.5,0,0]]
        if ribbon_dir==1:
            xlabels = 'Y \Gamma \\bar{Y}'
            path = [[0,0.5,0],[0,0,0],[0,-0.5,0]]

    return path, xlabels, BZ



def generate_q_vec(path,nq,rcell):
    nseg = len(path)-1
    ndim = len(path[0])
    q_vec = np.zeros((nseg*nq,3))
    for iseg in range(nseg):
        for ii in range(ndim):
            q_vec[iseg*nq:(iseg+1)*nq,ii] = np.linspace(path[iseg][ii],path[iseg+1][ii],nq,endpoint=False)
    q_vec = np.concatenate((q_vec,[path[-1]]),axis=0)
    q_cart = np.dot(q_vec,rcell)
    dq_cart = q_cart[1:] - q_cart[:-1]
    dq = np.linalg.norm(dq_cart, axis=1)
    q_dist = np.append(0, np.cumsum(dq))
    q_node = q_dist[0::nq]
    return q_vec, q_dist, q_node, q_cart



def display_q_points(q_cart,BZ_cart,path_cart=None,show=False):
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(1,1)
    ax.scatter(q_cart[:,0],q_cart[:,1],s=5)
    ax.plot(BZ_cart[:,0],BZ_cart[:,1],ls='--',c='C2')
    if path_cart is not None:
        for ii in range(len(path_cart)-1):
            dx = path_cart[ii+1][0]-path_cart[ii][0]
            dy = path_cart[ii+1][1]-path_cart[ii][1]
            ax.arrow(path_cart[ii][0],path_cart[ii][1],dx,dy)
    ax.set_aspect('equal')
    ax.set_axis_off()
    fig.tight_layout()
    if show: plt.show()
    return fig




if __name__=='__main__':
    nx = ny = 6
    nz = 1
    
    lat_type='chain'
    for choice in range(1,3):
        print ('lat_type = chain, latt_choice = {}'.format(choice))
        latt,sites,all_neigh_idx,rotvecs = build_latt('chain',nx,ny,nz,latt_choice=choice)
        title = '{} lattice, neighbors of atom {}'.format(lat_type, 0)
        #show_neighbors(latt,sites,all_neigh_idx,central_atom_index=0,title=title,show=False)
        #display_lattice_sites(latt,sites)

    nx = ny = 5
    lat_type='honeycomb'
    for choice in range(1,6):
        print ('lat_type = honeycomb, latt_choice = {}'.format(choice))
        if choice==4: nx=ny=3; lat_type='Kekule'
        latt,sites,all_neigh_idx,rotvecs = build_latt('honeycomb',nx,ny,nz,latt_choice=choice)
        nat = sites.shape[-2]
        for iat in range(nat): 
            title = '{} lattice, neighbors of atom {}'.format(lat_type, iat)
            show_neighbors(latt,sites,all_neigh_idx,central_atom_index=iat,show=(iat==nat-1),title=title)

    nx = ny = 5
    lat_type='square'
    for choice in range(1,3):
        print ('lat_type = square, latt_choice = {}'.format(choice))
        latt,sites,all_neigh_idx,rotvecs = build_latt('square',nx,ny,nz,latt_choice=choice)
        show_neighbors(latt,sites,all_neigh_idx,central_atom_index=-1,title='{} lattice'.format(lat_type), show=False)
        display_lattice_sites(latt,sites,show=True)

    lat_type='triangular'
    for choice in range(1,3):
        print ('lat_type = triangular, latt_choice = {}'.format(choice))
        latt,sites,all_neigh_idx,rotvecs = build_latt('triangular',nx,ny,nz,latt_choice=choice)
        for iat in range(sites.shape[-2]): 
            title = '{} lattice, neighbors of atom {}'.format(lat_type, iat)
            show_neighbors(latt,sites,all_neigh_idx,central_atom_index=iat,title=title,show=False)
        display_lattice_sites(latt,sites,show=True)

    for lat_type in ['square','Lieb','kagome']:
        print ('lat_type={}'.format(lat_type))
        latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,nz)
        title = '{} lattice'.format(lat_type)
        show_neighbors(latt,sites,neigh_idx,central_atom_index=0,title=title,show=False)
        display_lattice_sites(latt,sites,show=True)

