#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *

r3 = np.sqrt(3)


def gen_three_zigzag_phases():
    conf_1 = np.zeros((2,2,2,3))
    conf_1[:,:1,:,2]=1
    conf_2 = np.zeros((2,2,2,3))
    conf_2[:1,:,:,2]=1
    conf_3 = np.zeros((2,2,2,3))
    conf_3[0,0,1,2] = conf_3[1,0,0,2] = conf_3[1,1,1,2] = conf_3[0,1,0,2] = 1
    confs = [conf_1,conf_2,conf_3]
    return confs
 


def plot_uc(sites_cart):
    ss = sites_cart.reshape(-1,2)
    fig,ax=plt.subplots(1,1)
    ax.scatter(*tuple(sites_cart.T),s=300,c='cyan',alpha=0.5)
    for ii in range(8):
        ax.text(ss[ii,0],ss[ii,1],str(ii),va='center',ha='center',fontsize=20)
    ax.set_aspect('equal')
    ax.set_axis_off()
    fig.tight_layout()
    plt.show()



def plot_cell(ax,orig,slatt,color='cyan'):
    path = np.array( [orig,orig+slatt[0],orig+slatt[0]+slatt[1],orig+slatt[1],orig] )
    p = PatchCollection( [Polygon(path)] , fc=color, alpha = 0.3, zorder=-1)
    ax.add_collection(p)


def ax_plot_cells(ax,orig):
    slatt_0 = np.array([[2,0],[-1,r3]])
    plot_cell(ax,orig,slatt,color='cyan')
    slatt_1 = np.array([[1,r3],[-1,r3]])
    plot_cell(ax,orig+slatt[1],slatt_1,color='royalblue')
    slatt_2 = np.array([[-2,0],[-1,-r3]])
    plot_cell(ax,orig+slatt[1],slatt_2,color='violet')



def get_four_sublatt_sites(s0,slatt,nx,ny):
    sites_snapshot = []
    for iat in range(4):
        sites_snapshot.append([])
        kws = dict(s=250,c='C{}'.format(iat))
        for ix,iy in np.ndindex(nx,ny):
            R_vec = np.dot(np.diag([ix,iy]),slatt)
            ss = np.zeros((8,2))
            for ii in range(2): ss[:,ii] += s0[:,ii] + R_vec[0,ii] + R_vec[1,ii]
            if 0<=ss[iat,0]<xbound and 0<=ss[iat,1]<ybound:
                sites_snapshot[iat].append(ss[iat])
            if 0<=ss[7-iat,0]<xbound and 0<=ss[7-iat,1]<ybound:
                sites_snapshot[iat].append(ss[7-iat])
    return sites_snapshot 



def set_bounds(ax,xbound,bound):
    ax.set_aspect('equal')
    ax.set_axis_off()
    xmargin = abs(xbound)/10
    ymargin = abs(ybound)/10
    ax.set_xlim(-xmargin, xbound + xmargin)
    ax.set_ylim(-ymargin, ybound + ymargin)

 
def plot_sublat_supercell(sites_snapshot,xbound,ybound,orig=None,show=True):
    sites_snapshot = get_four_sublatt_sites(s0,slatt,nx,ny)

    fig,ax=plt.subplots(1,1)
    for iat in range(4): ax.scatter(*tuple(np.array(sites_snapshot[iat]).T),s=150,c='C{}'.format(iat))

    if orig is not None: ax_plot_cells(ax,orig)

    labels = {0:'A',1:'B',2:'C',3:'D'}
    text_kws=dict(va='center',ha='center',fontsize=12,c='w',weight='bold')

    ss = s0 + orig
    shift = 0.01
    for iat in range(4): ax.text(ss[iat,0]-shift,ss[iat,1]-shift,labels[iat],**text_kws)
    set_bounds(ax,xbound,ybound)
    fig.tight_layout()
    if show: plt.show()
    return fig


def animate_sublat_supercell(sites_snapshot,xbound,ybound,orig=None,show=True,
    save=False,gif_name='four_sublat_illustration.gif'):
    from matplotlib.animation import FuncAnimation, PillowWriter

    nat = len(sites_snapshot)
 
    def update(ii,scats,sites_snapshot):
        for i in range(1,ii):
            if i>nat: continue
            scats[i-1].set_offsets(sites_snapshot[i-1])
            scats[i-1].set_color('C{}'.format(i-1))

    fig,ax=plt.subplots(1,1)
    if orig is not None: ax_plot_cells(ax,orig)
    scats = [ax.scatter([],[],s=100)  for iat in range(nat)]
    set_bounds(ax,xbound,ybound)
    fig.tight_layout()

    anim = FuncAnimation(fig, update, frames=nat+2, interval=1e3,
    repeat=False,fargs=[scats,sites_snapshot])
    if show: plt.show()
    if save: anim.save(gif_name,dpi=200,writer='imagemagick')
    return anim


latt,sites = build_latt('honeycomb',2,2,1,return_neigh=False)
sites_cart = np.dot(sites,latt)
slatt = np.dot(np.diag([2,2]),latt)
orig = np.sum( np.dot(np.diag([6,1]),latt), axis=0 )
 

nx=15
ny=5
xbound = 12
ybound = 7.6
s0 = sites_cart.reshape(-1,2)

if __name__=='__main__':
    confs = gen_three_zigzag_phases()
    fig,ax=plt.subplots(1,3,sharey=True,figsize=(10,3))
    for ii in range(3):
        
    #plot_uc(sites_cart)
    sites_snapshot = get_four_sublatt_sites(s0,slatt,nx,ny)
    #fig = plot_sublat_supercell(sites_snapshot,xbound,ybound,orig,show=True)
    #anim = animate_sublat_supercell(sites_snapshot,xbound,ybound,save=True)
