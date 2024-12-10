#!/usr/bin/env python

import time
import pickle
import glob
from asd.utility.asd_arguments import *
from asd.utility.spirit_tool import *
from asd.utility.spin_visualize_tools import *
from asd.utility.Swq import *
from asd.core.geometry import *
from spirit import state,geometry
from string import ascii_uppercase

default_color_set = [ 
'#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
'#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
'#bcbd22', '#17becf'
]


def gen_args():
    import argparse
    prog='analyze_Spirit_results.py'
    description = 'post-processing of Spirit LLG simulations'
    parser = argparse.ArgumentParser(prog=prog,description=description)
    add_switch_arguments(parser)
    add_llg_arguments(parser)
    add_spirit_arguments(parser)
    add_quiver_arguments(parser)
    add_spin_plot_arguments(parser)
    add_common_arguments(parser)
    args = parser.parse_args()
    return args


def plot_spin_corrs(ax,disps,corrs,colors=default_color_set,label_prefix='',sublattice_groups=None,
    component_label=True,component_label_height=0.9,component_label_left=0.5):

    corrs_dp = np.sum(corrs,axis=-1)         # generic correlation
    corrs_xy = np.sum(corrs[...,:2],axis=-1) # correlations of in-plane components, see PRL 2021, 127, 037204
    corrs_zz  = corrs[...,2]
    dists = np.linalg.norm(disps,axis=-1)
    nat = disps.shape[-2]
    if sublattice_groups is not None:
        for jj,isub in enumerate(sublattice_groups):  # treat the two sublattices separately
            sort_idx = np.argsort(dists[:,:,isub,isub].flatten())
            RR = dists[:,:,isub,isub].flatten()[sort_idx]
            corrs_xy_sort = corrs_xy[:,:,isub,isub].flatten()[sort_idx]
            corrs_zz_sort = corrs_zz[:,:,isub,isub].flatten()[sort_idx]
            corrs_dp_sort = corrs_dp[:,:,isub,isub].flatten()[sort_idx]
            label = label_prefix
            if len(sublattice_groups)>1: label +=' Sub {}'.format(ascii_uppercase[jj])
            corrs_set = [corrs_xy_sort,corrs_zz_sort,corrs_dp_sort]
            for ii in range(3): ax[ii].plot(RR,corrs_set[ii],'-',label=label,markersize=2,c=colors[ii])
    else:
        for isub in range(nat):  # treat the two sublattices separately
            sort_idx = np.argsort(dists[:,:,isub,isub].flatten())
            RR = dists[:,:,isub,isub].flatten()[sort_idx]
            corrs_xy_sort = corrs_xy[:,:,isub,isub].flatten()[sort_idx]
            corrs_zz_sort = corrs_zz[:,:,isub,isub].flatten()[sort_idx]
            corrs_dp_sort = corrs_dp[:,:,isub,isub].flatten()[sort_idx]
            label = label_prefix
            if nat>1: label +=' Sub {}'.format(ascii_uppercase[isub])
            corrs_set = [corrs_xy_sort,corrs_zz_sort,corrs_dp_sort]
            for ii in range(3): ax[ii].plot(RR,corrs_set[ii],'-',label=label,markersize=2,c=colors[ii])

    ylabel_xy = '$\langle S^+(\mathbf{r}_i) S^-(\mathbf{r}_j) \\rangle$'
    ylabel_zz = '$\langle S^z(\mathbf{r}_i) S^z(\mathbf{r}_j) \\rangle$'
    ylabel_dp = '$\langle \mathbf{S}(\mathbf{r}_i) \cdot \mathbf{S}(\mathbf{r}_j) \\rangle$'
    ylabels = [ylabel_xy,ylabel_zz,ylabel_dp]
    xlabel  ='$\\vert \mathbf{r}_i-\mathbf{r}_j \\vert \ \mathrm{(\AA)}$'
    ax[2].set_xlabel(xlabel,fontsize=12)
    ax[1].set_ylabel('spin-spin correlations',fontsize=12)

    for ii,axx in enumerate(ax):
        if nat>1: axx.legend()
        axx.axhline(0,ls='--',c='grey',alpha=0.5,zorder=-1)
        xlim = axx.get_xlim()
        ylim = axx.get_ylim()
        if component_label: 
            axx.text(xlim[1]*component_label_left,ylim[1]*component_label_height,
            ylabels[ii],fontsize=12,va='top',ha='center')


def get_corrs_one_set(restart,args,latt,sites,start_conf,cutoff_x,cutoff_y):
    print ('\n\nCalculate spin-spin correlations from Spirit results')
    print ('Results from directory {}'.format(args.outdir))
    print ('restart = {}'.format(restart))
    if restart==0: print ('Start from ovf file')
    if restart==1: print ('Start from confs.pickle')
    if restart==2: print ('Start from corrs.pickle')
    print ('\nPLEASE MAKE SURE')
    print ('This is the right starting point you want!\n')

    #fil_cfg = '{}/{}'.format(args.outdir,args.spirit_input_file)
 
    if restart < 1:   # restart < 1, start from ovf file
        stime = time.time()
        files = glob.glob('{}/{}*Spins-archive.ovf'.format(args.outdir,args.prefix))
        assert len(files)==1, 'ovf file not found!'
        fil = files[0]
        print ('\nSpin configs from achive file {}'.format(fil))
        confs = parse_ovf(fil,parse_params=False)[1]
        nframe = confs.shape[0]
        confs = confs.reshape(nframe,args.ny,args.nx,-1,3)
        confs = np.swapaxes(confs,1,2)
        pickle.dump(confs,open('{}/confs.pickle'.format(args.outdir),'wb'))
        print ('Data read. Time used: {:8.3f} s'.format(time.time()-stime))

    if restart < 2:  # restart < 2, start from the loaded confs
        confs = pickle.load(open('{}/confs.pickle'.format(args.outdir),'rb'))
        print ('Data shape: {}'.format(confs.shape))
        confs_0 = confs[start_conf:]
        print ('Use the last {} configurations for sampling.\n'.format(confs_0.shape[0]))
        disps = calc_space_disp(latt,sites,cutoff_x,cutoff_y,cutoff_z=0,ndim=2,verbosity=1)
        corrs = calc_correlation_function(confs_0,confs_0,cutoff_x=cutoff_x,cutoff_y=cutoff_y,verbosity=1,substract_background=False)
        pickle.dump(disps,open('{}/disps.pickle'.format(args.outdir),'wb'))
        pickle.dump(corrs,open('{}/corrs.pickle'.format(args.outdir),'wb'))

    if restart < 3:   # restart < 3, start from the loaded disps and corr data
        disps = pickle.load(open('{}/disps.pickle'.format(args.outdir),'rb'))
        corrs = pickle.load(open('{}/corrs.pickle'.format(args.outdir),'rb'))

    return disps,corrs


args = gen_args()
args.nx=80
args.ny=80
args.nz=1
args.prefix='T'
args.spirit_input_file = 'input.cfg'

cutoff_x=25
cutoff_y=25

lat_type='honeycomb'
lat_type='square'

start_conf = -20  # use the last 20 configurations for sampling and statistics

restart=0

if __name__=='__main__':
    latt,sites = build_latt(lat_type,1,1,1,return_neigh=False)
 
    args.outdir='square_FM_XY'
    disps,corrs = get_corrs_one_set(restart,args,latt,sites,start_conf,cutoff_x,cutoff_y)

    args.outdir='square_FM_Ising'
    disps_Ising,corrs_Ising = get_corrs_one_set(restart,args,latt,sites,start_conf,cutoff_x,cutoff_y)

    fig,ax=plt.subplots(3,1,sharex=True,figsize=(6,7))
    plot_spin_corrs(ax,disps,corrs,label_prefix='XY') 
    plot_spin_corrs(ax,disps_Ising,corrs_Ising,colors=default_color_set[3:],component_label=False,label_prefix='Ising') 
    for axx in ax: axx.legend()
    fig.tight_layout()
    fig.savefig('Spin_correlations',dpi=400)
    plt.show()            

