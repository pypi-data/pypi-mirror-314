#!/usr/bin/env python


import numpy as np
from asd.core.llg_simple import *
from asd.data_base.exchange_for_CrMnI6_rect import *
from asd.core.geometry import build_latt
from asd.core.spin_configurations import *
from asd.utility.spirit_tool import *
import asd.mpi.mpi_tools as mt
import pickle
import os
import glob

def get_time(runs=4):
    times = []
    for i in range(runs):
        time = np.array([time.split()[-2] for time in os.popen('grep time run{}/spin_confs.ovf'.format(i+1)).readlines()],float)
        if i>0: time = time[1:] + times[i-1][-1]
        times.append(time)
    return np.concatenate((times),axis=0)


def get_pos_from_Sz(all_sites_cart,confs_all):
    confs = np.swapaxes(confs_all,1,2)
    nframe = confs.shape[0]

    up_core_idx_from_Sz = np.array([np.argmax(confs[i,...,2]) for i in range(0,nframe,nn)])
    up_core_pos_from_Sz = np.array([all_sites_cart[idx] for idx in up_core_idx_from_Sz])

    dn_core_idx_from_Sz = np.array([np.argmin(confs[i,...,2]) for i in range(0,nframe,nn)])
    dn_core_pos_from_Sz = np.array([all_sites_cart[idx] for idx in dn_core_idx_from_Sz])

    return up_core_pos_from_Sz, dn_core_pos_from_Sz


def plot_pos_from_Sz(time,up_core_pos_from_Sz,dn_core_pos_from_Sz,legend=True,tag='core'):
    fig,ax=plt.subplots(1,1)
    ax_plot_pos_from_Sz(ax,time,up_core_pos_from_Sz,dn_core_pos_from_Sz,legend=True,tag='core')
    ax.legend()
    ax.set_xlabel('Time (ps)')
    ax.set_ylabel('meron core position')
    plt.show()


def ax_plot_pos_from_Sz(ax,time,up_core_pos_from_Sz,dn_core_pos_from_Sz,tag='core',color='g'):
    ax.scatter(time,up_core_pos_from_Sz[:,0],facecolor=color,edgecolor='none',label='{}: up_x'.format(tag),marker='x')
    ax.scatter(time,up_core_pos_from_Sz[:,1],edgecolor=color,facecolor='none',label='{}: up_y'.format(tag),marker='o')

    ax.scatter(time,dn_core_pos_from_Sz[:,0],facecolor=color,edgecolor='none',label='{}: dn_x'.format(tag),marker='x')
    ax.scatter(time,dn_core_pos_from_Sz[:,1],edgecolor=color,facecolor='none',label='{}: dn_y'.format(tag),marker='o')


def mpi_plot_positions_from_Q(time):
    core_pos_all = []

    sp_lat = np.swapaxes(confs_all[-2],0,1)
    tri_simplices,Q_distri,Q = mpi_calc_topo_chg_one_conf(sp_lat,tri_simplices=LLG._simplices,spatial_resolved=True)

    for i in range(0,nframe,nn):
        sp_lat = np.swapaxes(confs_all[i],0,1)
        tri_simplices,Q_distri,Q = mpi_calc_topo_chg_one_conf(sp_lat,tri_simplices=LLG._simplices,spatial_resolved=True)
        core_idx = np.argmax(Q_distri)
        core_sites = all_sites_cart[LLG._simplices[core_idx]]
        
        spins = sp_lat.reshape(-1,3)
        if np.min([spins[ii,2] for ii in LLG._simplices[core_idx]])>0:
            core_pos = np.average(core_sites,axis=0)
            core_pos_all.append(core_pos)
        else:
            spins = np.delete(spins,core_idx)
            Q_distri = np.delete(Q_distri,core_idx)
            core_idx = np.argmax(Q_distri)
            core_sites = all_sites_cart[LLG._simplices[core_idx]]
            core_pos = np.average(core_sites,axis=0)
            core_pos_all.append(core_pos)

        
        if not rank: print ('{:4d} of {:4d}'.format(i,nframe))

    core_pos_all = np.array(core_pos_all)



    if not rank:
        with open('core_pos.dat','w') as fw:
            for i in range(core_pos_all.shape[0]):
                fw.write('{:10.5f} {:10.5f} {:10.5f}\n'.format(time[i],core_pos_all[i,0],core_pos_all[i,1]))
        data = np.loadtxt('core_pos.dat')
        time = data[:,0]
        core_pos_all = data[:,1:]

        fig,ax=plt.subplots(1,1)
        ax.scatter(time,core_pos_all[:,0],c='r',label='x')
        ax.scatter(time,core_pos_all[:,1],c='b',label='y')
        ax.legend()
        ax.set_xlabel('Time (ps)')
        ax.set_ylabel('meron core position')
        plt.show()



def plot_all_cores(llg_file='llg',nn=20,nruns=1):
    llg=importlib.import_module(llg_file)

    all_sites = llg.sites.reshape(-1,llg.sites.shape[-1])
    all_sites_cart = np.dot(all_sites,llg.latt)

    colors=['r','g','b','m']

    up_cores = []
    dn_cores = []
    cores = []
    tags = []

    fig,ax=plt.subplots(1,1,figsize=(5,4))

    for i in range(3):
        tag = '{:3.1f}K'.format((i+1)*0.5)
        os.chdir(tag)
        confs_all = pickle.load(open('confs.pickle','rb'))
        time = get_time(runs=nruns)[::nn]

        up_core, dn_core = get_pos_from_Sz(all_sites_cart,confs_all)
        up_cores.append(up_core)
        dn_cores.append(dn_core)
        cores.append((up_core+dn_core)/2)
        tags.append(tag)
        os.chdir('..')

    for i in range(3):
        color = colors[i]
        #ax.plot(time,up_core[:,0],'-' , c=color,label='{}: up_x'.format(tag))
        #ax.plot(time,up_core[:,1],'--', c=color,label='{}: up_y'.format(tag))

        #ax.plot(time,dn_core[:,0],'-' ,c=color,label='{}: dn_x'.format(tag))
        #ax.plot(time,dn_core[:,1],'--',c=color,label='{}: dn_y'.format(tag))

    for i in range(3):  ax.plot(time,cores[i][:,0],'-',  c=colors[i],label='{}: x'.format(tags[i]))
    for i in range(3):  ax.plot(time,cores[i][:,1],'--', c=colors[i],label='{}: y'.format(tags[i]))

    ax.legend(ncol=2)
    ax.set_xlabel('Time (ps)',fontsize=14)
    ax.set_ylabel('normalized bimeron position',fontsize=14)
    fig.tight_layout()
    fig.savefig('core_positions',dpi=500)

    plt.show()

nx=100
ny=36
latt,sites = rectangular_honeycomb_cell(nx,ny,1,return_neigh=False)
nn=20


LLG_kws = dict(
alpha=0.3,
dt=1e-3,
nstep=1000,
S_values=S_values,
temperature=0.5,
conv_ener=1e-8, 
damping_only=False)

LLG = llg_solver(**LLG_kws)


comm,size,rank,node = mt.get_mpi_handles()

if __name__=='__main__':
    nruns = len(glob.glob('run*'))
    time = get_time(runs=nruns)[::nn]

    if not rank: confs_all = pickle.load(open('confs.cpl','rb'))
    else:        confs_all = None
    confs_all=comm.bcast(confs_all,root=0)
    nframe = confs_all.shape[0]

    all_sites = sites.reshape(-1,sites.shape[-1])
    all_sites_cart = np.dot(all_sites,latt)

    if not rank: 
        up_core_pos_from_Sz,dn_core_pos_from_Sz = get_pos_from_Sz(all_sites_cart,confs_all)
        plot_pos_from_Sz(time,up_core_pos_from_Sz,dn_core_pos_from_Sz,legend=True,tag='core')
    #mpi_plot_positions_from_Q(time)
    plot__all_cores()
