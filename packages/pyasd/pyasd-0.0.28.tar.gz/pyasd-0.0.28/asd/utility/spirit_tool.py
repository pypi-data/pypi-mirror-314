#!/usr/bin/env python

#=============================================
#
# Analyze Spirit results
#
# Shunhong Zhang
# Last modified: Dec 21, 2020
#
#=============================================

import os
import numpy as np
import matplotlib.pyplot as plt
from .spin_visualize_tools import *


def plot_mc(outdir='output',fout='output_mc.txt'):
    data=np.loadtxt(open('{}/{}'.format(outdir, fout)),skiprows=1)
    T,E,M,chi,c_v,cumulant=data.T
    fig,ax=plt.subplots(1,1)
    ax.plot(T,M/np.max(M),label='M')
    #ax.plot(T,E/np.max(abs(E)),label='E')
    ax.plot(T,chi/np.max(chi),label='$\chi$')
    #ax.plot(T,c_v/np.max(c_v),label='$C_v$')
    ax.set_xlabel('T (K)')
    ax.set_ylabel('normalized values')
    ax.legend(loc='upper right')
    ax.axhline(0,c='gray',ls='--',zorder=-1,alpha=0.7)
    return fig


def get_energy_archive(fil_en):
    lines=open(fil_en).readlines()[3:]
    data=np.array([line.split('|') for line in lines])
    return np.array(data[:,np.array([0,2,4,5,6])],float)


def plot_energy_archive(iter_scale=1, save=True, show=False):
    import glob
    fil_en = glob.glob('output/*Image-00_Energy-archive.txt')[0]
    data=get_energy_archive(fil_en)
    iters,E_tot,E_ani,E_ex,E_DM = data.T
    iters //= iter_scale
    fig,ax=plt.subplots(1,1,figsize=(5,5))
    ax.plot(iters,E_tot,label='$E_{tot}$')
    ax.plot(iters,E_ani,label='$E_{ani}$')
    ax.plot(iters,E_ex,label='$E_{ex}$')
    ax.plot(iters,E_DM,label='$E_{DM}$')
    xl = 'Iterations'
    cc = np.log(iter_scale)/np.log(10)
    if cc>0: xl+='/10'
    if cc>1: xl+='$^{0:1.0f}$'.format(cc)
    ax.set_xlabel(xl)
    ax.set_ylabel('E (eV)')
    ax.set_ylim(-1.8,0.5)
    ax.legend(loc='upper center',ncol=2)
    fig.tight_layout()
    if save: fig.savefig('Spirit_energy',dpi=500)
    if show: plt.show()
    return fig


def verbose_quantities(p_state,conf_name,write_spin=False):
    from spirit import quantities, system, io
    mg=quantities.get_magnetization(p_state)
    sp = system.get_spin_directions(p_state)
    tc = quantities.get_topological_charge(p_state)
    en = system.get_energy(p_state,idx_image=0)
    fmt='{:30s}, Q = {:10.5f}, E_tot = {:10.5f} eV, M =['+' {:10.6f}'*3+' ]'
    print (fmt.format(conf_name,tc,en/1e3,*tuple(mg)))
    filename='spin_{0}.ovf'.format(conf_name)
    if write_spin: io.image_write(p_state, filename, fileformat=3)
    return mg,en,tc


def get_spin_sites_from_cfg(fil_cfg='input.cfg'):
    from spirit import state, geometry
    with state.State(fil_cfg,quiet=True) as p_state:
        cell = geometry.get_bravais_vectors(p_state)
        pos = geometry.get_positions(p_state)
        ncell = geometry.get_n_cells(p_state)
        nat = geometry.get_n_cell_atoms(p_state)
        np.savetxt('Positions.dat',pos,fmt='%12.5f')
    pos = np.loadtxt('Positions.dat')
    pos = pos.reshape(ncell[2],ncell[1],ncell[0],nat,3)
    pos = np.transpose(pos,(2,1,0,3,4))
    os.remove('Positions.dat')
    return cell,pos
    

def trace_quantities(fils,fil_cfg='input.cfg'):
    from spirit import io, quantities, state, system, geometry, chain, configuration
    def conf_prop(p_state,conf_name):
        fmt='conf from fil: {:55s}, topo chg = {:8.4f}, en ={:12.6f} eV, M=[{:8.4f},{:8.4f},{:8.4f}]'
        system.update_data(p_state)
        tc=quantities.get_topological_charge(p_state)
        en = system.get_energy(p_state)
        mg = quantities.get_magnetization(p_state)
        print (fmt.format(conf_name,tc,en/1e3,*tuple(mg)))
    indice_int = np.array([fil.split('_')[-1].rstrip('.ovf') for fil in fils],int)
    fils = [fils[np.where(indice_int==i)[0][0]] for i in sorted(indice_int)]
    print ('\nTrace quantities')
    with state.State(fil_cfg,quiet=True) as p_state:
        chain.set_length(p_state,len(fils)+1)
        for i,fil in enumerate(fils):
            chain.jump_to_image(p_state,idx_image=i)
            io.image_read(p_state,fil)
            conf_prop(p_state,fil)
        chain.jump_to_image(p_state,idx_image=len(fils))
        configuration.plus_z(p_state)
        conf_prop(p_state,'ferromagnetic')


if __name__=='__main__':
    print ('post-processing of LLG simulation results produced by Spirit')
