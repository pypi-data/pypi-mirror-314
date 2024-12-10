#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from asd.utility.Swq import analytic_spin_wave_FM
from asd.core.geometry import build_latt, get_BZ_path_labels, generate_q_vec
from asd.core.constants import Hbar

meV_to_THz = 1e-3/(Hbar*1e12*2*np.pi)


def test_spin_wave(lat_type,J1=1,J2=0,SIA=0.1,nx=1,ny=1,nq=100,plot_en_axis=True,
    save=False,show=False,freq_unit='THz'):

    latt, sites = build_latt(lat_type,nx,ny,1,return_neigh=False, vacuum=10)
    rcell = np.linalg.inv(latt).T  # in 2pi
    q_path, xlabels, BZ = get_BZ_path_labels(lat_type, latt_choice=2)
    q_vec, q_dist, q_node, q_cart =  generate_q_vec(q_path, nq, rcell)
    analytic_spectra = analytic_spin_wave_FM(lat_type,q_cart[:,:2], J1, J2, SIA, freq_unit=freq_unit)

    fmt = '$J_1$={:4.2f} meV, $J_2$={:4.2f} meV, $A_z$={:4.2f} meV'
    params = fmt.format(J1,J2,SIA)
    title = '{} lattice\n{}'.format(lat_type,params)

    fig,ax=plt.subplots(1,1)
    #ax.text(0.1,0.8,params)
    ax.set_title(title)
    ax.set_xticks(q_node)
    ax.set_xticklabels(['${}$'.format(item) for item in xlabels.split()])
    for q in q_node: ax.axvline(q,c='grey',alpha=0.5,zorder=-1)
    ax.set_xlim(q_dist[0],q_dist[-1])
    ax.set_ylabel('$\omega\ \mathrm{(THz)}$')
    ax.plot(q_dist,analytic_spectra.T)
    ax.axhline(0,ls='--',c='grey',zorder=-1)
    if plot_en_axis:
        tax = ax.twinx()
        tax.plot(q_dist,analytic_spectra.T/meV_to_THz,ls='--')
        ylim=ax.get_ylim()
        tax.set_ylim(ylim[0]/meV_to_THz,ylim[1]/meV_to_THz)
        tax.set_ylabel('$\\hbar \omega\ \mathrm{(meV)}$')
        tax.axhline(SIA,ls='--',c='grey',alpha=0.5)
    fig.tight_layout()
    figname = '{}_FM_spin_wave'.format(lat_type)
    if save: fig.savefig(figname,dpi=400)
    if show: plt.show()
    return fig




if __name__=='__main__':
    print ('Running {}'.format(__file__.split('/')[-1]))
    print ('Testing magnon spectra of some ferromagnetic lattices')
    print ('Based on linear spin wave theory\n')

    test_spin_wave('chain',J2=0.,SIA=0)
    test_spin_wave('kagome',SIA=0)
    test_spin_wave('honeycomb',SIA=0)
    test_spin_wave('square',SIA=0,show=True)
