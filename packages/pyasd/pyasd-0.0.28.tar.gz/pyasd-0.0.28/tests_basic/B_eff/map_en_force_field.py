#!/usr/bin/env python

from asd.core.hamiltonian import *
import matplotlib.pyplot as plt
from asd.utility.auxiliary_colormaps import parula
from asd.utility.spirit_tool import *
from asd.data_base.exchange_for_CrMnI6 import *
from asd.core.geometry import build_latt
from asd.core.log_general import log_general
from asd.core.topological_charge import get_tri_simplices
from asd.core.spin_configurations import init_random
from asd.core.llg_simple import *


def compare_two_energy_methods(sp_lat):
    e0 = ham.calc_total_E(sp_lat)
    
    e1  = ham.calc_self_exchange_energy(sp_lat)
    e1 += ham.calc_zeeman_energy(sp_lat)
    for bl_exch in ham._BL_exch: e1 += bl_exch.shell_exch_energy_from_Jmat_new(sp_lat)
    for bq_exch in ham._BQ_exch: e1 += bq_exch.shell_exch_energy_new(sp_lat)
    print (e0, e1, np.allclose(e0,e1))


def compare_two_field_methods(sp_lat):
    ham._thermal_factor = 0.
    fmt = '{:10.5f} '*3 + '  |  ' + '{:10.5f} '*3 + '{}'
    for ix,iy,iat in np.ndindex(nx,ny,nat):
        b0 = ham.calc_local_B_eff(sp_lat,(ix,iy,iat))

        n_i = sp_lat[ix,iy,iat]
        b1 = np.array([0,0,2*ham._BL_SIA[0][iat]*n_i[2]])  # SIA contributed effective field
        for bl_exch in ham._BL_exch: b1 += bl_exch.local_exch_field_from_Jmat_new(sp_lat,(ix,iy,iat))
        for bq_exch in ham._BQ_exch: b1 += bq_exch.local_exch_field_new(sp_lat,(ix,iy,iat))
        b1 = b1/(2*ham._S_values[iat]*muB) + ham._Bfield
        print (fmt.format(*tuple(b0), *tuple(b1), np.allclose(b0,b1)) )


def map_force(sites_cart,damping_site):
    fig,ax= plt.subplots(1,1)
    cax = ax.scatter(sites_cart[...,0],sites_cart[...,1],c=damping_site,cmap=parula,s=2)
    cbar = fig.colorbar(cax,shrink=0.6)
    cbar.ax.set_title('|$A_i$| (T)')
    ax.set_title('$\\bf{A}$$_i$$ = \\bf{n}$$_i \\times $$\\bf{B}$$_i$')
    ax.set_axis_off()
    ax.set_aspect('equal')
    plt.show()


def map_energy(sites_cart,en_site):
    fig,ax= plt.subplots(1,1)
    cax = ax.scatter(sites_cart[...,0],sites_cart[...,1],c=en_site,cmap=parula,s=2)
    cbar = fig.colorbar(cax,shrink=0.6)
    cbar.ax.set_title('E (meV)')
    ax.set_axis_off()
    ax.set_aspect('equal')
    plt.show()



nx = 10
ny = 10
latt,sites  = build_latt('honeycomb',nx,ny,1,return_neigh=False)

log_handles = log_general(
n_log_conf=1000,
n_log_magn=200,
log_topo_chg=True,
tri_simplices=get_tri_simplices(np.dot(sites,latt)),
)


llg_kws = dict(
alpha=0.1,
dt=1e-3,
nstep=10000,
conv_ener=1e-8, 
damping_only=True,
temperature=1,
lat_type=lat_type,
log_handle = log_handle,
)


ham_thermal_factor = 0.

LLG = llg_solver(**llg_kws)
sites_cart = np.dot(sites,latt)

ham = ham4

if __name__=='__main__':
    sp_lat = np.zeros((nx,ny,nat,3))
    sp_lat = init_random(sp_lat,verbosity=False)
    #spins = parse_ovf('final_spin_confs.ovf')[1]
    #sp_lat = np.swapaxes(spins.reshape(ny,nx,nat,3),0,1)

    compare_two_energy_methods(sp_lat)
    compare_two_field_methods(sp_lat)
    #map_force(sites_cart,damping_site)
    #map_energy(sites_cart,en_site)
