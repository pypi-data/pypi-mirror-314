#=================================
#
# This script is part of pyasd,
# a python-based package for
# atomistic magnetic simulations.
#
# Copyright @ Shunhong Zhang
# 2022 - 2024
#
# Usage, modification, and 
# re-distribution of this code
# should be consent to the 
# MIT license
# For details pelase refer to
# https://pypi.org/project/pyasd/
#
#==================================


#=============================================
#
# visualize spin configurations
# of classic spin systems
# typically a vector field
# currently focus on 2D lattices
#
# For spin configurations loading
# interfaced to ovf files
# in OOMMF format (.ovf)
# commonly used in Spirit, OOMMF etc.
# Also the current package, pyasd
#
# Shunhong Zhang
# Last modified: Dec 21, 2020
#
#=============================================

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import gridspec
from asd.utility.ovf_tools import *
from asd.utility.auxiliary_colormaps import parula
import pickle
import os


def map_Gilbert_damping(sites_cart,alpha,latt=None,scatter_size=15, save=False, show=True):
    import matplotlib.pyplot as plt
    xlen = np.max(sites_cart[:,0]) - np.min(sites_cart[:,0])
    ylen = np.max(sites_cart[:,1]) - np.max(sites_cart[:,1])
    if xlen>ylen: colorbar_orientation='horizontal'
    else: colorbar_orientation='vertical'
    fig,ax=plt.subplots(1,1)
    scat=ax.scatter(sites_cart[...,0],sites_cart[...,1],s=scatter_size,c=alpha,cmap='viridis')
    cbar=fig.colorbar(scat,shrink=0.5,orientation=colorbar_orientation)
    cbar.ax.set_title('$\\alpha$')
    ax.set_aspect('equal')
    ax.set_axis_off()
    ax.set_title('Map of damping parameter $\\alpha$')
    fig.tight_layout()
    if save: fig.savefig('Alpha_map',dpi=300)
    if show: plt.show()
    return fig


# in fractional coordinates
# sites should be in shape of (nx,ny,nat,ndim), ndim can be 2 or 3
def get_repeated_sites(sites,repeat_x=1,repeat_y=1):
    nx,ny=sites.shape[:2]
    sites_repeat = np.tile(sites,(repeat_x,repeat_y,1,1))
    for i,j in np.ndindex(repeat_x,repeat_y):
        sites_repeat[i*nx:(i+1)*nx,j*ny:(j+1)*ny,:,0] += i*nx
        sites_repeat[i*nx:(i+1)*nx,j*ny:(j+1)*ny,:,1] += j*ny
    return sites_repeat


# conf should be in shape of (nx,ny,nat,3) or (nx,ny,nz,nat,3)
def get_repeated_conf(conf,repeat_x=1,repeat_y=1,repeat_z=0):
    shape = conf.shape
    if len(shape)==4: conf_repeat = np.tile(conf,(repeat_x,repeat_y,1,1))
    elif len(shape)==5: conf_repeat = np.tile(conf,(repeat_x,repeat_y,repeat_z,1,1))
    else: exit('Cannot generate conf_repeat: shape mismatched!')
    return conf_repeat


def get_repeated_data(conf, sites, latt, repeat_x, repeat_y):
    conf_r = get_repeated_conf(conf, repeat_x, repeat_y)
    sites_r = get_repeated_sites(sites, repeat_x, repeat_y)
    sites_cart_r = np .dot(sites_r, latt)
    nx,ny=sites.shape[:2]
    superlatt = np.dot(np.diag([nx,ny,1]), latt) 
    superlatt_r = np.dot(np.diag([repeat_x,repeat_y,0]), superlatt)
    return conf_r, sites_cart_r, superlatt_r



# shift the configuration along specific axes
def get_shifted_conf(conf,dx=1,dy=1,dz=0):
    shape = conf.shape
    if len(shape)==4: conf_shift = np.roll(confs_0,(-dy,-dx),axis=(1,0))
    if len(shape)==5: conf_shift = np.roll(confs_0,(-dz,-dy,-dx),axis=(2,1,0))
    return conf_shift



def get_spin_polar_angle_mapping(spins,color_mapping='phi'):
    phis = np.rad2deg(np.angle(spins[...,0] + 1.j*spins[...,1]))
    phis[phis<0] += 360
    if 'full' in color_mapping: norm = mpl.colors.Normalize(0,360)
    else: norm = mpl.colors.Normalize(np.min(phis),np.max(phis))
    return norm,phis



def ax_map_spin(ax,sites,spins,tri=None,Q_distri=None,color_mapping='Sz_full',
    scatter_size=30,colormap='rainbow',Q_colormap='bwr',Qmin=-0.2,Qmax=0.2):

    all_sites = sites.reshape(-1,sites.shape[-1])
    ndim = spins.shape[-1]
    all_spins = spins.reshape(-1,ndim)
 
    if colormap=='parula': colormap=parula
    if 'S' in color_mapping: 
        idx = {'Sx':0,'Sy':1,'Sz':2}[color_mapping.split('_')[0]]
        cc = all_spins[:,idx]
    if 'phi' in color_mapping: 
        norm,phis = get_spin_polar_angle_mapping(spins,color_mapping)

    Qmap_kwargs = dict(facecolors=Q_distri, edgecolors='none',cmap=Q_colormap,vmin=Qmin,vmax=Qmax,zorder=-2)
    if 'S' in color_mapping:
        Smap_kwargs = dict(c=cc,edgecolor='none',cmap=colormap,zorder=-1,vmin=-1,vmax=1,s=scatter_size)
        if color_mapping in ['Sx','Sy','Sz']:  Smap_kwargs.update(vmin=np.min(cc),vmax=np.max(cc))
        scat = ax.scatter(*tuple(all_sites[:,:2].T),**Smap_kwargs)
    elif 'phi' in color_mapping:
        print ('For mapping polar angles we recommand to set colormap="hsv"')
        Pmap_kwargs = dict(c=phis,cmap='hsv',zorder=-1,norm=norm,s=scatter_size)
        scat = ax.scatter(*tuple(all_sites[:,:2].T),**Pmap_kwargs)
    elif 'Q' in color_mapping:
        Q_mag = np.max(np.abs(Q_distri))
        if color_mapping=='Q' : Qmap_kwargs.update(vmin=-Q_mag,vmax=Q_mag)
        scat = ax.tripcolor(*tuple(all_sites[:,:2].T), tri, **Qmap_kwargs)
    else:
        print ('Currently valid color_mapping:')
        print ('Sx, Sy, Sz, phi (angle of in-plane S relative to x), Q (topological charge)')
        print ('Sx_full, Sy_full, Sz_full, phi_full, Q_full (colormap range [-1,1])')
        scat = None

    return scat


quiver_kws = dict(
units='x',
scale=1.2,
width=0.1,
headlength=5,
headwidth=3,
headaxislength=3,
pivot='mid',
cmap='rainbow',
clim=(-1,1))

def ax_plot_quiver(ax,sites,spins,mapping_prop=None,quiver_kws=quiver_kws,colorful_quiver=False):
    if colorful_quiver: 
        if mapping_prop is None:
            qv = ax.quiver(sites[:,0],sites[:,1],*tuple(spins.T),**quiver_kws)
        else:
            qv = ax.quiver(sites[:,0],sites[:,1],spins[:,0],spins[:,1],mapping_prop,**quiver_kws)
    else:               
        qv = ax.quiver(sites[:,0],sites[:,1],spins[:,0],spins[:,1],**quiver_kws)
    return qv


def ax_plot_framework(ax,sites,latt=None,superlatt=None,framework=False,facecolor=None):
    if facecolor is not None: 
        ax.set_xticks([])
        ax.set_yticks([])
        try: ax.set_facecolor(facecolor)
        except: raise ValueError('Invalid facecolor for plot: {}'.format(facecolor))
    elif framework==False: 
        ax.set_axis_off()

    vertex = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]])
    if superlatt is not None:
        ndim = superlatt.shape[1]
        v = np.zeros((5,ndim))
        v[:,:2] = vertex
        spoints = np.dot(v[:,:ndim],superlatt[:ndim,:ndim])
        ax.plot(*tuple(spoints[:,:2].T),'k--',alpha=0.5,zorder=-1)
    elif latt is not None:
        nx,ny,nat = sites.shape[:3]
        ndim = latt.shape[1]
        v = np.zeros((5,ndim))
        v[:,:2] = vertex
        spoints = np.dot(v[:,:ndim],latt[:ndim,:ndim])
        ax.plot(*tuple(spoints[:,:2].T),'k--',alpha=0.5,zorder=-1)
    else:
        sites_f = sites.reshape(-1,sites.shape[-1])
        up_bound=np.max(sites_f,axis=0)
        dn_bound=np.min(sites_f,axis=0)
        margin = (up_bound-dn_bound)*0.05
        #margin[np.where(margin==0)]=1
        ax.set_xlim(dn_bound[0]-margin[0],up_bound[0]+margin[0])
        ax.set_ylim(dn_bound[1]-margin[1],up_bound[1]+margin[1])


def subplot_spin_2d(ax,sites,spins,xs=1,ys=1,x0=0,y0=0,
    site_plot_idx=-1,scatter_size=1,verbosity=1,
    title='spins',color_mapping='Sz_full',mapping_all_sites=True,
    tri=None,Q_distri=None,Qmin=-0.1,Qmax=0.1,
    framework=False,latt=None,superlatt=None,facecolor=None,
    colormap='rainbow',Q_colormap='bwr',
    quiver_kws=quiver_kws,colorful_quiver=False):

    if colormap=='parula': colormap=parula
    quiver_kws['cmap']=colormap

    shape0=list(sites.shape)
    shape0[-1]=spins.shape[-1]
    spins = spins.reshape(shape0)
    if site_plot_idx == -1: 
        sites_to_plot = sites[x0::xs,y0::ys].reshape(-1,sites.shape[-1])
        spins_to_plot = spins[x0::xs,y0::ys].reshape(-1,shape0[-1])
    else:
        sites_to_plot = sites[x0::xs,y0::ys,np.array(site_plot_idx,int)].reshape(-1,sites.shape[-1])
        spins_to_plot = spins[x0::xs,y0::ys,np.array(site_plot_idx,int)].reshape(-1,shape0[-1])

    mapping_prop=None
    if 'phi' in color_mapping: 
        norm,phis = get_spin_polar_angle_mapping(spins_to_plot,color_mapping)
        mapping_prop = phis

    qv_kws=dict(
    mapping_prop=mapping_prop,
    quiver_kws=quiver_kws,
    colorful_quiver=colorful_quiver)
    qv = ax_plot_quiver(ax,sites_to_plot,spins_to_plot,**qv_kws)

    if not colorful_quiver:
        if mapping_all_sites: scat = ax_map_spin(ax,sites,spins,tri,Q_distri,color_mapping,scatter_size,colormap,Q_colormap,Qmin=Qmin,Qmax=Qmax)
        else: scat = ax_map_spin(ax,sites_to_plot,spins_to_plot,tri,Q_distri,color_mapping,scatter_size,colormap,Q_colormap,Qmin=Qmin,Qmax=Qmax)
    else: scat = None

    tl = ax.set_title(title)
    ax_plot_framework(ax,sites,latt,superlatt,framework,facecolor)
    ax.set_aspect('equal')
    return qv,scat,tl


def select_sites_in_box(sites_cart,region=[0,1,0,1]):
    left,right,bot,top = region
    hor = np.logical_and(sites_cart[...,0]>=left,sites_cart[...,0]<right)
    ver = np.logical_and(sites_cart[...,1]>=bot, sites_cart[...,1]<top)
    idx = np.array(np.where(np.logical_and(hor,ver))).T
    box = np.array([[left,bot],[right,bot],[right,top],[left,top],[left,bot]])
    return idx, box


inset_indicator_kws=dict(
edgecolor='k',
ls='-',
)

def add_zoomin_inset(ax,sites_cart,conf,zoomin_region,inset_pos,spin_plot_kws={},inset_indicator_kws={}):
    idx,box = select_sites_in_box(sites_cart,zoomin_region)
    assert len(idx)>0, 'No sites in the specified region! {}'.format(zoomin_region)
    sites_select = np.array([sites_cart[tuple(ii)] for ii in idx])
    spins_select = np.array([conf[tuple(ii)] for ii in idx])
    if 'color_mapping' in spin_plot_kws.keys():
        if 'Q' in spin_plot_kws['color_mapping']:
            from asd.core.topological_charge import calc_topo_chg
            tri_simplices,Q_distri,Q = calc_topo_chg(spins_select,sites_select,spatial_resolved=True)
            spin_plot_kws.update(tri=tri_simplices,Q_distri=Q_distri)
 
    axins = ax.inset_axes(inset_pos)
    subplot_spin_2d(axins, sites_select, spins_select,**spin_plot_kws)
    axins.set_axis_on()
    axins.set_xticklabels([])
    axins.set_yticklabels([])
    axins.set_xticks([])
    axins.set_yticks([])
    if 'edgecolor' in inset_indicator_kws:
        for pos in ['top','bottom','left','right']: axins.spines[pos].set_color(inset_indicator_kws['edgecolor'])
    ax.indicate_inset_zoom(axins, **inset_indicator_kws)
    return axins



def set_colorbar(fig,cb_ax,mapping_obj,cb_kws={},color_mapping='Sz_full',Qmin=-0.1,Qmax=0.1):
    if color_mapping=='phi_full':
        xval = np.arange(-np.pi, np.pi, 0.01)
        norm = mpl.colors.Normalize(-np.pi, np.pi)
        for r in np.arange(0.5,1,0.05):
            yval = np.ones_like(xval)*r
            cb_ax.scatter(xval, yval, c=xval, s=10, cmap='hsv', norm=norm, linewidths=0)
        cb_ax.text(0,0,'$\phi$',va='center',ha='center')
        cb_ax.set_yticks([])
        cb_ax.set_ylim(0,1)
        cbar = None
    else:
        Q_map = mapping_obj.get_clim()
        Q_mag = np.max(np.abs(Q_map))
        Qmin = np.min(Q_map)
        Qmax = np.max(Q_map)
        #print ('Range of dQ: {:8.3f} {:8.3f}'.format(Qmin,Qmax))
 
        cbar = fig.colorbar(mapping_obj, ax=cb_ax,  **cb_kws)
        if color_mapping == 'Sz_full':
            if cb_ax is None: cbar.set_ticks([-1,0,1])
            else: cb_ax.set_yticks([-1,0,1])
        if color_mapping=='Q_full': 
            if cb_ax is None: 
                cbar.set_ticks([Qmin,Qmax])
            else: 
                cb_ax.set_yticks([Qmin,Qmax])
                cb_ax.set_ylim(Qmin,Qmax)
        if color_mapping=='Q':    
            if cb_ax is None:
                cbar.set_ticks([-Q_mag,0,Q_mag])
                cbar.ax.set_lim(-Qmag,Qmag)
            else:
                cb_ax.set_yticks([-Q_mag,0,Q_mag])
                cb_ax.set_ylim(-Q_mag, Q_mag)
 
        if 'Q' in color_mapping:    cbar.ax.set_title('$dQ\ (\mathbf{r})$')
        if 'S' in color_mapping:    cbar.ax.set_title('$n_{}$'.format(color_mapping[1]))
    return cbar
 


def plot_spin_2d(sites,spins,xs=1,ys=1,x0=0,y0=0,
    site_plot_idx=-1,scatter_size=1,verbosity=1,
    color_mapping='Sz_full',mapping_all_sites=True,
    tri=None,Q_distri=None,Qmin=-0.1,Qmax=0.1,framework=False,latt=None,superlatt=None,facecolor=None,
    colormap='rainbow',Q_colormap='bwr',quiver_kws=quiver_kws,colorful_quiver=False,
    colorbar=True,colorbar_shrink=0.6,colorbar_orientation='auto',colorbar_axes_position=None,
    width_ratios=(8,1),height_ratios=(8,1),figsize=None,
    title='spins',show=False,save=False,figname='spin_conf',fig_dpi=500,
    ):

    if colorbar_orientation=='auto':
        xlen = np.max(sites[...,0]) - np.min(sites[...,0])
        ylen = np.max(sites[...,1]) - np.max(sites[...,1])
        if xlen>ylen: colorbar_orientation='horizontal'
        else: colorbar_orientation='vertical'

    fig = plt.figure(figsize=figsize)

    if colorbar_orientation=='horizontal': gs = gridspec.GridSpec(2,1,height_ratios=height_ratios)
    elif colorbar_orientation=='vertical': gs = gridspec.GridSpec(1,2,width_ratios=width_ratios)
    else: raise ValueError ('Invalied colorbar_orientation!\nSet to "horizontal/vertical/auto"')
    if colorbar:  ax = fig.add_subplot(gs[0])
    else:         ax = fig.add_subplot(1,1,1)

    #if colorful_quiver: print ('Use colorful quivers to represent spins')
    #else: print ('Use colorful scatters to represent out-of-plane magnetization')

    qv,scat,tl = subplot_spin_2d(ax,sites,spins,xs,ys,x0,y0,site_plot_idx,
    scatter_size,verbosity,title,color_mapping,mapping_all_sites,
    tri,Q_distri,Qmin,Qmax,framework,latt,superlatt,facecolor,
    colormap,Q_colormap,
    quiver_kws,colorful_quiver)

    if colorbar: 
        cb_kws = dict(shrink=colorbar_shrink,orientation=colorbar_orientation)
        cb_ax = None
        if color_mapping=='phi_full':
            cb_ax = fig.add_subplot(gs[1],polar=True)
        else:
            if colorbar_axes_position is not None:
                cb_ax = fig.add_axes(colorbar_axes_position)
                cb_kws.update(cax=cb_ax)

        if scat is not None:  mapping_obj = scat
        elif colorful_quiver: mapping_obj = qv
        cbar = set_colorbar(fig,cb_ax,mapping_obj,cb_kws,color_mapping,Qmin,Qmax) 
    
    if colorbar_axes_position is None: fig.tight_layout()
    if save: fig.savefig(figname,dpi=fig_dpi)
    if show: plt.show()
    return fig,ax,scat,qv,tl


def plot_spin_2d_from_ovf(sites,fil_ovf,xs=1,ys=1,x0=0,y0=0,site_plot_idx=-1,quiver_kws={},
    scatter_size=1,verbosity=1,title=None):
    if verbosity: print ('plot spins from file {0}'.format(fil_ovf))
    params,spins = parse_ovf_1(fil_ovf)
    if title is None: tt=fil_ovf.split('_')[-1].rstrip('.ovf')
    else: tt=title
    fig,ax,scat,qv,tl = plot_spin_2d(sites,spins,xs,ys,x0,y0,site_plot_idx,scatter_size,verbosity,tt,quiver_kws=quiver_kws)
    return fig,ax,scat,qv,tl


def display_snapshot_with_topo_chg(sites, conf, title='Spins', superlatt=None, quiver_kws=quiver_kws,
    colorbar1_position=[0.49,0.6,0.01,0.2],
    colorbar2_position=[0.51,0.2,0.01,0.2],
    save=True, show=True ):

    from asd.core.topological_charge import calc_topo_chg
    tri,Q_distri,Q = calc_topo_chg(conf,sites,spatial_resolved=True)
    kws = dict(superlatt=superlatt, quiver_kws=quiver_kws, scatter_size=10,
    tri=tri,Q_distri=Q_distri,color_mapping='Q',title='Q = {:6.3f}'.format(Q))

    fig,ax = plt.subplots(1,2,sharex=True,figsize=(9,4))
    qv,scat,tl = subplot_spin_2d(ax[0],sites,conf,**kws)
    cb_ax1 = fig.add_axes(colorbar1_position)
    cb_ax2 = fig.add_axes(colorbar2_position)
    cb1 = fig.colorbar(scat,shrink=0.3,cax=cb_ax1)
    cb1.ax.set_title('dQ')

    kws.update(color_mapping='Sz_full',scatter_size=20,title=title)
    qv,scat,tl = subplot_spin_2d(ax[1],sites,conf,**kws)
    cb2 = fig.colorbar(scat,shrink=0.3,cax=cb_ax2)
    cb2.ax.set_title('$n_z$')
    cb2.set_ticks([-1,0,1])
    cb_ax2.set_ylim(-1,1)
    #fig.tight_layout()
    if save: fig.savefig('Snapshot_with_topo_chg',dpi=300)
    if show: plt.show()
    return fig



def plot_spin_3d(sites,spins,xs=1,ys=1,x0=0,y0=0,site_plot_idx=-1,scatter_size=1,verbosity=1,
    title='spins',show=False,save=False,figname='spin_conf',color_mapping='Sz_full',mapping_all_sites=True,
    tri=None,Q_distri=None,Qmin=-0.1,Qmax=0.1,framework=False,latt=None,superlatt=None,colormap='rainbow',Q_colormap='bwr',quiver_kws={},colorful_quiver=False,
    colorbar=True,colorbar_shrink=0.6,colorbar_orientation='vertical',width_ratios=(8,1),height_ratios=(8,1)):

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.cm as cm
    from asd.utility.arrow_3d import arrow3d
    if colormap=='parula': colormap=parula

    shape0=list(sites.shape)
    shape0[-1]=3
    spins = spins.reshape(shape0)
    if site_plot_idx == -1:
        sites_to_plot = sites[x0::xs,y0::ys].reshape(-1,sites.shape[-1])
        spins_to_plot = spins[x0::xs,y0::ys].reshape(-1,shape0[-1])
    else:
        sites_to_plot = sites[x0::xs,y0::ys,np.array(site_plot_idx,int)].reshape(-1,sites.shape[-1])
        spins_to_plot = spins[x0::xs,y0::ys,np.array(site_plot_idx,int)].reshape(-1,shape0[-1])


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for idx in range(spins_to_plot.shape[0]):
        x,y=sites_to_plot[idx]
        theta_x = np.rad2deg(np.arccos(spins_to_plot[idx,2]))
        theta_z = np.rad2deg(np.angle(spins_to_plot[idx,1] + 1.j*spins_to_plot[idx,0]))
        arrow3d(ax, offset=[x,y,0],
        theta_x=theta_x, theta_z=theta_z, color=cm.rainbow(theta_x/180.), **quiver_kws)

    #ax.set_xlim(0,10)
    #ax.set_ylim(-1,1)
    #ax.set_zlim(-1,1)
    ax.set_axis_off()
    plt.show()


def make_ani(sites,all_spins,xs=1,ys=1,x0=0,y0=0,
    site_plot_idx=-1,scatter_size=1,verbosity=1,
    color_mapping='Sz_full',mapping_all_sites=True,
    tri=None,Q_distri=None,Qmin=-0.1,Qmax=0.1,framework=False,latt=None,superlatt=None,
    colormap='rainbow',Q_colormap='bwr',quiver_kws=quiver_kws,colorful_quiver=False,
    colorbar=True,colorbar_shrink=0.6,colorbar_orientation='auto',colorbar_axes_position=None,
    width_ratios=(8,1),height_ratios=(8,1),figsize=None,
    titles=None,show=False,
    jump=1,interval=1e3,savegif=False,gif_name='LLG.ani',gif_dpi=300,
    ):

    from matplotlib.animation import FuncAnimation, PillowWriter

    def update(i, qv, scat, all_spins_to_plot, titles, tl, all_spins_to_map):
        spins = all_spins_to_plot[i].reshape(-1,3)
        spins_map = all_spins_to_map[i].reshape(-1,3)
        if colorful_quiver: qv.set_UVC(spins[:,0],spins[:,1],spins[:,2])
        else: qv.set_UVC(spins[:,0],spins[:,1])
        if scat is not None: 
            if 'Sz' in color_mapping: 
                scat.set_array(spins_map[:,2])
            elif 'phi' in color_mapping:
                phi = np.rad2deg(np.angle(spins_map[...,0] + 1.j*spins_map[...,1]))
                scat.set_array(phi)
        if titles is not None: tl.set_text(titles[i])

    if jump!=1:
        idx = np.arange(0,len(all_spins),jump)
        if len(all_spins)-1 not in idx: idx = np.append(idx,[-1])
        all_spins = all_spins[idx]
        if titles is not None: titles = np.array(titles)[idx]

    nframe=all_spins.shape[0]
    shape0=list(sites.shape)
    shape0[-1]=3
    all_spins = all_spins.reshape([nframe]+shape0)
    if site_plot_idx == -1:
        sites_to_plot = sites[x0::xs,y0::ys]
        all_spins_to_plot = all_spins[:,x0::xs,y0::ys]
    else:
        sites_to_plot = sites[x0::xs,y0::ys,np.array(site_plot_idx,int)]
        all_spins_to_plot = all_spins[:,x0::xs,y0::ys,np.array(site_plot_idx,int)]

    print ('\nMake animation: {0} frames in total'.format(len(all_spins)))
    print ('Color mapping quantity: {0}'.format(color_mapping))

    if latt is not None: superlatt = np.dot([[sites.shape[0],0],[0,sites.shape[1]]],latt)
    if titles is not None: title = titles[0]
    else: title = None

    if 'phi' in color_mapping: colormap='hsv'

    spin_plot_kws=dict(
    scatter_size=scatter_size,verbosity=verbosity,title=title,
    color_mapping=color_mapping,mapping_all_sites=True,framework=framework,
    colormap=colormap,quiver_kws=quiver_kws,colorful_quiver=colorful_quiver,latt=latt,superlatt=superlatt,
    colorbar=colorbar,colorbar_shrink=colorbar_shrink,colorbar_orientation=colorbar_orientation,
    colorbar_axes_position=colorbar_axes_position,
    width_ratios=width_ratios,height_ratios=height_ratios,
    figsize=figsize)

    fig,ax,scat,qv,tl = plot_spin_2d(sites,all_spins[0],xs,ys,x0,y0,site_plot_idx,**spin_plot_kws)

    anim = FuncAnimation(fig, update, frames=range(nframe), interval=interval, repeat=False,
    fargs=[qv, scat, all_spins_to_plot, titles, tl, all_spins])
    if savegif:
        print ('save animation to {}.gif'.format(gif_name))
        anim.save('{}.gif'.format(gif_name), dpi=gif_dpi, writer='imagemagick')
    else: plt.show()


def make_ani_from_ovf(sites,fils,xs=1,ys=1,site_plot_idx=-1,interval=0.5e3,scatter_size=1,quiver_kws={},jump=1,
    gif_name='LLG_ani',verbosity=1,sort_fils=True,titles=None,savegif=False):
    if sort_fils:
        indice_int = np.array([fil.split('_')[-1].rstrip('.ovf') for fil in fils],int)
        fils = [fils[np.where(indice_int==i)[0][0]] for i in sorted(indice_int)]
    if titles is None: titles=[fil.split('_')[-1].rstrip('.ovf') for fil in fils]
    all_spins = np.array([parse_ovf_1(fil)[1].reshape(sites.shape) for fil in fils])
    make_ani(sites,all_spins,titles,xs,ys,site_plot_idx,interval,scatter_size,quiver_kws,gif_name,verbosity,jump,savegif)
