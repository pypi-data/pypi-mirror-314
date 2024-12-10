#!/usr/bin/env python

import numpy as np
from asd.core.geometry import build_latt
from asd.core.spin_configurations import *
from asd.core.topological_charge import calc_topo_chg
from asd.utility.spin_visualize_tools import *
from asd.utility.Swq import *
import itertools

from asd.core.geometry import calc_space_disp

lat_type = 'triangular'
lat_type = 'honeycomb'
latt_choice=3

latt_uc,sites_uc = build_latt(lat_type,2,2,1,return_neigh=False, latt_choice=2, vacuum=10)
sites_cart_uc = np.dot(sites_uc,latt_uc)


nx=60
ny=30
nx=20
ny=10
latt,sites = build_latt(lat_type,nx,ny,1,return_neigh=False, vacuum=10,latt_choice=latt_choice)
nat = sites.shape[2]
sites_cart = np.dot(sites,latt)

#print (latt_uc)
#print (latt)

quiver_kws = dict(
scale=2,
units='x',pivot='mid')
 
spin_plot_kws=dict(
scatter_size=5,
quiver_kws=quiver_kws,
colorful_quiver=False,
superlatt=np.dot(np.diag([nx,ny,1]),latt),
#superlatt=np.dot(np.diag([2,2,1]),latt),
#facecolor='k',
)

cbar_kws=dict(
colorbar_axes_position=[0.75,0.5,0.02,0.25],
colorbar_orientation='vertical',
#colorbar_shrink=0.5,
)


BZ_1st = np.array([[1/3,1/3,0],[-1/3,2/3,0],[-2/3,1/3,0],[-1/3,-1/3,0],[1/3,-2/3,0],[2/3,-1/3,0],[1/3,1/3,0]])
BZ_2nd = np.array([[1,0,0],[0,1,0],[-1,1,0],[-1,0,0],[0,-1,0],[1,-1,0],[1,0,0]])

rcell = 2*np.pi*np.linalg.inv(latt_uc).T
BZ_1st_cart = np.dot(BZ_1st,rcell)
BZ_2nd_cart = np.dot(BZ_2nd,rcell)


all_confs = [
#'FM',
#'Neel',
'Zigzag',
#'Stripy',
#'super-Neel',
#'Tetrahedra',
#'Cubic',
]


nqx=121
nqy=121
nqx=81
nqy=61
boundx=20
boundy=18
qpt_cart = gen_uniform_qmesh(nqx,nqy,boundx=boundx,boundy=boundy)
qpt_cart = gen_uniform_qmesh(nqx,nqy,nqz=1,boundx=boundx,boundy=boundy)
 
 

sf_kws = dict(
scatter_size=10,
nqx=nqx,
nqy=nqy,
nn=1,
colormap='hot',
)

 
if __name__=='__main__':
    for conf_name in all_confs:
        sp_lat_uc, latt_muc, sites_muc = regular_order(lat_type,conf_name)
        #sites_cart = np.dot(sites_muc, latt)

        #sp_lat_uc = np.roll(sp_lat_uc,axis=0,shift=1)

        sp_lat = np.zeros((nx,ny,nat,3))

        rx=range(0,nx,2)
        ry=range(0,ny,2)
        if latt_choice==2:
            for i,j in itertools.product(rx,ry):
                sp_lat[i:i+2,j:j+2] = sp_lat_uc

        # rectangular unit cell
        if latt_choice==3:
            sp_lat[:,:,0::2,2] = 1
            sp_lat[:,:,1::2,2] = -1

        Q=calc_topo_chg(sp_lat,sites_cart)
        title = '{} order'.format(conf_name)
        #title += ', Q = {:10.5f}'.format(Q)
        spin_plot_kws.update(title=title)
        if conf_name in ['Tetrahedra','Cubic']:  
            spin_plot_kws.update(colorful_quiver=True)


        shape = sites.shape
        nx,ny=shape[:2]
        nz=1
        ndim=sites.shape[-1]
        cutoff_x = max(nx//2-1,1)
        cutoff_y = max(ny//2-1,1)
        cutoff_z = 0

        spins = sp_lat.reshape(-1,3)
        sites_cart = sites_cart.reshape(-1, sites_cart.shape[-1])
        #S_vector = calc_static_structure_factor(spins,sites_cart, qpt_cart)
        S_vector = calc_equal_time_spin_structure_factor(sp_lat,latt,sites,qpt_cart, 
        #cutoff_x=25, cutoff_y=15, confine_cutoff=False, 

        dR_filter=2/np.sqrt(3),
        #dR_filter=1,
        #dR_filter = 1/np.sqrt(3),
        #dR_filter=5,

        #filter_method='smaller',
        filter_method='equal',
        )

        #S_vector = pickle.load(open('S_vector.pickle','rb'))

        fig,ax = plt.subplot_mosaic([['a','a'],['b','c']])
        scat, qv, tl = ax_plot_spin_2d(ax['a'],sites_cart,sp_lat,**spin_plot_kws)
        #scat,qv,tl = ax_plot_spin_2d(ax['a'],sites_cart_uc,sp_lat_uc,**spin_plot_kws)
        axi = ax['a'].inset_axes([1.1,0.1,0.05,0.5])
        cb1 = fig.colorbar(scat,cax=axi)
        axi.set_title('$n_z$')

        #S_vector = np.log(np.abs(S_vector)+1)
        print (np.min(S_vector), np.max(S_vector))
        scat1 = subplot_struct_factor(ax['b'],qpt_cart,S_vector,comp='parall',**sf_kws)
        scat2 = subplot_struct_factor(ax['c'],qpt_cart,S_vector,comp='normal',**sf_kws)

        cb_ax = fig.add_axes([0.47,0.1,0.02,0.3])
        cb2 = fig.colorbar(scat1, cax=cb_ax)
        cb2.ax.set_title(r'S($\mathbf{q}$)', fontsize=12)

        """ Plot the BZs """
        for key in ['b','c']:
            ax[key].plot(BZ_1st_cart[:,0],BZ_1st_cart[:,1],'w--',zorder=1,alpha=0.4)
            ax[key].plot(BZ_2nd_cart[:,0],BZ_2nd_cart[:,1],'w--',zorder=1,alpha=0.4)

        #fig.tight_layout()
        #fig.savefig('Regular_order_Struct_factor',dpi=300)
        plt.show()
