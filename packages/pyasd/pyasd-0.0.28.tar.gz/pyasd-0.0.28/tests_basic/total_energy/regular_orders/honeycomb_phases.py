#!/usr/bin/env python

import numpy as np

# for calculate the exchange energy of regular magnetic orders
try:
    from asd.core.spin_configurations import regular_order
    from asd.core.geometry import build_latt
    from asd.core.shell_exchange import exchange_shell
    from asd.core.hamiltonian import spin_hamiltonian
except:
    print ('Fail to import some modules for the "calc_energy_numerical" function')
 
import matplotlib.pyplot as plt
from matplotlib import rcParams
#rcParams['font.family'] = 'sans-serif'
#rcParams['font.family'] = 'DejaVu Sans'
rcParams['font.family'] = 'Times New Roman'
rcParams['text.usetex'] = True

 

# calculate the exchange energy analytically by counting the number of couplings for each J
# Here positive/negative J represents AFM/FM exchange 
def calc_energy_analytic(J1,J2,J3,conf='FM',SIA=0,S=1/2,Neel_vec=np.array([0,0,1])):
    tetra_cosine = np.dot([1,1,-1],[-1,-1,-1])/3
    E={
    'FM':         ( 12*J1 + 24*J2 + 12*J3) * S**2,
    'Neel':       (-12*J1 + 24*J2 - 12*J3) * S**2,
    'Zigzag':     (  4*J1 -  8*J2 - 12*J3) * S**2,
    'Stripy':     ( -4*J1 -  8*J2 + 12*J3) * S**2,
    'super-Neel': (           - 12*J3) * S**2,
    'Tetrahedra': ( 12*J1*tetra_cosine + 24*J2*tetra_cosine + 12*J3) * S**2,
    'Cubic':      (  4*J1*tetra_cosine -  8*J2*tetra_cosine - 12*J3) * S**2
    }
    en = E[conf]
    sp_lat, latt, sites_muc = regular_order('honeycomb',conf,Neel_vec=Neel_vec)
    en -= np.sum(sp_lat[...,2]**2) * SIA
    return en


# calculate the exchange energy numerically 
# can take care of more complex spin Hamiltonians
def calc_energy_numerical(J1,J2,J3,conf='FM',SIA=0,S=1/2,Neel_vec=np.array([0,0,1])):
    latt,sites,neigh_idx,rotvecs = build_latt('honeycomb',2,2,1)
    SIA = np.ones(2)*SIA
    ones = np.ones(2)*S**2
    exch_1 = exchange_shell(neigh_idx[0],-J1*ones, shell_name='1NN')
    exch_2 = exchange_shell(neigh_idx[1],-J2*ones, shell_name='2NN')
    exch_3 = exchange_shell(neigh_idx[2],-J3*ones, shell_name='3NN')
    ham = spin_hamiltonian(S_values=np.ones(2)*S,
    BL_SIA=[SIA],BL_SIA_axis=[Neel_vec],
    BL_exch=[exch_1,exch_2,exch_3],iso_only=True)
    sp_lat, latt, sites_muc = regular_order('honeycomb',conf,Neel_vec=Neel_vec)
    E = ham.calc_total_E(sp_lat,average_on_sites=False)
    return E


# J1s, J2s, J3s are two-dim ndarray with the same shape
def calculate_phase_diagram_analytic(J1s,J2s,J3s,confs,S=1/2,SIA=0,Neel_vec=np.array([0,0,1])):
    energies = np.array([calc_energy_analytic(J1s,J2s,J3s,conf,S=S,SIA=SIA,Neel_vec=Neel_vec) for conf in confs])
    # determine which config has the lowest energy for each set of [J2,J3]
    ground_state_iconf = np.argmin(energies,axis=0)
    return energies,ground_state_iconf


def calculate_phase_diagram_numerical(J1s,J2s,J3s,confs,S=1/2,SIA=0,Neel_vec=np.array([0,0,1])):
    m,n = J1s.shape
    nconf = len(confs)
    energies = np.zeros((nconf,m,n))
    for iconf in range(nconf):
        print ('{}'.format(confs[iconf]))
        for i,j in np.ndindex(m,n): 
            energies[iconf,i,j] = calc_energy_numerical(J1s[i,j],J2s[i,j],J3s[i,j],confs[iconf],S=S,SIA=SIA,Neel_vec=Neel_vec) 
    # determine which config has the lowest energy for each set of [J2,J3]
    ground_state_iconf = np.argmin(energies,axis=0)
    return energies,ground_state_iconf


def energy_analytic_vs_numerical(J1,J2,J3,confs,S=1/2,SIA=0,Neel_vec=np.array([0,0,1])):
    for ii,conf in enumerate(confs):
        energies1 = calc_energy_analytic(J1,J2,J3,conf,S=S,SIA=SIA,Neel_vec=Neel_vec)
        energies2 = calc_energy_numerical(J1,J2,J3,conf,S=S,SIA=SIA,Neel_vec=Neel_vec)
        np.testing.assert_allclose(energies1,energies2,atol=1e-6)
        print ('{:>15s} passed'.format(confs[ii]))


def calc_phase_diagram(J1,J2,J3,confs,S=1/2,SIA=0,Neel_vec=np.array([0,0,1]),method='analytic',degenerate_threshold=1e-2):
    if method=='analytic':     energies,ground_state_iconf = calculate_phase_diagram_analytic(J1,J2,J3,confs,S=S,SIA=SIA,Neel_vec=Neel_vec)
    elif method=='numerical':  energies,ground_state_iconf = calculate_phase_diagram_numerical(J1,J2,J3,confs,S=S,SIA=SIA,Neel_vec=Neel_vec)
    min_energies = energies.min(axis=0)
    full_idx = [[np.where(abs(energies[:,ix,iy]-min_energies[ix,iy])<degenerate_threshold)[0] for iy in range(ny)] for ix in range(nx)]
    deg = np.array([[len(full_idx[ix][iy]) for iy in range(ny)] for ix in range(nx)])
    ground_state_confs_type = list(set([tuple(ii) for item in full_idx for ii in item]))
    ground_state_confs_maps = {}
    for idx in ground_state_confs_type:
        ground_state_confs_maps.setdefault( idx, '+'.join([confs[ii] for ii in idx]) )
    ground_state_iconf  = np.array([[sorted(ground_state_confs_type).index(tuple(full_idx[ix][iy])) for iy in range(ny)] for ix in range(nx)])
    return energies, ground_state_confs_maps, ground_state_iconf


def map_phase_diagram(J1,J2,J3,energies,confs_maps,ground_state_iconf,show=True,mark_datapoints=None,labels=None,mark_phase=False,
    colors=['lightgreen','khaki','lightyellow','royalblue','m','C1','C2','C3'],
    method='analytic',unit='J3',normalize=True):

    if unit=='J3':
        if normalize:
            J_X = J1/J3
            J_Y = J2/J3
            xlabel = '$J_1/J_3$'
            ylabel = '$J_2/J_3$'
        else:
            J_X = J1
            J_Y = J2
            xlabel = '$J_1$'
            ylabel = '$J_2$'
        title = '$J_3={}$'.format(J3[0,0])
        if J3[0,0]<0: title += ' (FM)'
        else: title += ' (AF)'
        idxJ = 3
    elif unit=='J1':
        if normalize:
            J_X = J2/J1
            J_Y = J3/J1
            xlabel = '$J_2/J_1$'
            ylabel = '$J_3/J_1$'
        else:
            J_X = J2
            J_Y = J3
            xlabel = '$J_2$'
            ylabel = '$J_3$'
        title = '$J_1={}$'.format(J1[0,0])
        if J1[0,0]<0: title += ' (FM)'
        else: title += ' (AF)'
        idxJ = 1
    if SIA!=0: title += ', SIA = {:.2f}'.format(SIA)

    sorted_confs = sorted(confs_maps.keys())
    fig,ax=plt.subplots(1,1,figsize=(6,5))
    for i,conf in enumerate(sorted_confs):
        idx = np.where(ground_state_iconf==i)
        fc = colors[i]
        if mark_phase==False: ax.scatter(J_X[idx],J_Y[idx],facecolor=fc,edgecolor='none',s=5,label=confs_maps[conf])
        else: ax.scatter(J10[idx],J20[idx],facecolor=fc,edgecolor='none',s=5)

    if mark_phase:
        txt_kws=dict(ha='center',fontsize=12)
        ax.text(-1.5,-0.7,'FM',**txt_kws)
        ax.text( 3.5,-0.7,'Neel',**txt_kws)
        ax.text(-1.5,1.75,'Zigzag',**txt_kws)
        ax.text( 3.5,1.75,'Stripy',**txt_kws)
 
    if mark_datapoints is not None:
        markers = ['o','s','^']
        colors = ['g','r','royalblue']
        lab=None
        for ii,scatt in enumerate(mark_datapoints):
            if labels is not None: lab = labels[ii]
            if unit=='J3':
                mpoint = np.array([scatt[0],scatt[1]])
                if normalize: mpoint /= scatt[2]
            elif unit=='J1': 
                mpoint = np.array([scatt[1],scatt[2]])
                if normalize: mpoint /= scatt[0]
 
            ax.scatter(*tuple(mpoint.T),marker=markers[ii],s=40,c=colors[ii],label=lab)
    if not mark_phase: ms=5
    else: ms=1
    lg = ax.legend(markerscale=ms,loc='center left')
    #for ii,tt in enumerate(lg.get_texts()): tt.set_color(colors[ii])
    lg.get_frame().set_alpha(1)
    if unit=='J3':
        ax.set_xlim(min_J1,max_J1)
        ax.set_ylim(min_J2,max_J2)
    if unit=='J1':
        ax.set_xlim(min_J2,max_J2)
        ax.set_ylim(min_J3,max_J3)
 
    ax.set_xlabel(xlabel,fontsize=16)
    ax.set_ylabel(ylabel,fontsize=16)
    ax.set_title(title,fontsize=18)
    ax.axvline(0,ls='--',c='gray',alpha=0.5)
    ax.axhline(0,ls='--',c='gray',alpha=0.5)
    fig.tight_layout()
    figname = 'Honeycomb_Heisenberg_phase_diagram'
    if np.max(J3)>0: figname += '_positive_J{}'.format(idxJ)
    else: figname += '_negative_J{}'.format(idxJ)
    fig.savefig(figname,dpi=250)
    if show: plt.show()
    return fig


def tenary_phase_diagram(J10,J20,J30,ground_state_iconf,mark_datapoints=None):
    import ternary

    J1_min=np.min(J10)
    J1_max=np.max(J10)
    J2_min=np.min(J20)
    J2_max=np.max(J20)
    J3_min=np.min(J30)
    J3_max=np.max(J30)
    assert J1_max-J1_min == J2_max-J2_min == J3_max-J3_min, 'scale for three axes should be equal!'

    confs=['FM','Neel','Zigzag','stripy']
    colors=['c','pink','g','m']

    # Simple example:
    ## Boundary and Gridlines
    scale = J1_max-J1_min
    fig, tax = ternary.figure(scale=scale)
    tax.ax.axis("off")
    fig.set_facecolor('w')

    origin = np.array([J1_min,J2_min,J3_min])
    if mark_datapoints is not None:
        mark_datapoints = np.array([[0,0,0]])
        points = mark_datapoints - origin
        points = [tuple(point) for point in points]
        print (points)
        tax.scatter(points ,facecolor='r',edgecolor='none',s=20,zorder=2)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=1.0)
    tax.gridlines(color="black", multiple=1, linewidth=0.5, ls='-')

    # Set Axis labels and Title
    fontsize = 16
    tax.left_axis_label(  "$J_3$", fontsize=fontsize, offset=0.13)
    tax.right_axis_label( "$J_2$", fontsize=fontsize, offset=0.12)
    tax.bottom_axis_label("$J_1$", fontsize=fontsize, offset=0.06)

    # Set custom axis limits by passing a dict into set_limits.
    # The keys are b, l and r for the three axes and the vals are a list
    # of the min and max in data coords for that axis. max-min for each
    # axis must be the same as the scale i.e. 9 in this case.
    #tax.set_axis_limits({'b': [67, 76], 'l': [24, 33], 'r': [0, 9]})
    tax.set_axis_limits({'b': [J1_min, J1_max], 'r': [J2_min, J2_max], 'l': [J3_min, J3_max]})
 
    # get and set the custom ticks:
    tax.get_ticks_from_axis_limits()
    tax.set_custom_ticks(fontsize=10, offset=0.02)

    tax.ax.set_aspect('equal', adjustable='box')
    tax._redraw_labels()
    fig.tight_layout()
    fig.savefig('tri_axis_plots',dpi=300)
    plt.show()
    return fig



def test_energy_function(ntest=5):
    print ('Test the energy function')
    for itest in range(ntest):
        print ('\nTest {}'.format(itest+1))
        J1, J2, J3 = (np.random.random(size=3) - 0.5 )*2
        energy_analytic_vs_numerical(J1, J2, J3, confs, SIA=SIA, Neel_vec=Neel_vec)



# arguments specifically for the Gd2CX2 (X = Cl, Br or I) systems
S=7/2
Js_Cl = np.array([0.116,0.047,0.185])
Js_Br = np.array([0.105,0.042,0.188])
Js_I  = np.array([0.062,0.036,0.182])
mark_datapoints = [Js_Cl,Js_Br,Js_I]
labels = ['$\mathrm{Gd_2C'+halogen+'_2}$' for halogen in ['Cl','Br','I']]


S=5/2
Js_MnPSe3 = np.array([0.582,0.059,0.332])
labels = ['$\mathrm{MnPSe}_3$']
mark_datapoints = [Js_MnPSe3]



Js_FePS3 = np.array([
-0.48837062499999995,
0.21694218749999994,
0.5938156250000007])
labels = ['$\mathrm{FePS}_3$']
mark_datapoints = [Js_FePS3]

confs=[
'FM',
'Neel',
'Zigzag',
'Stripy',
'super-Neel',
'Tetrahedra',
'Cubic']

colors=['lightgreen','khaki','lightyellow','royalblue','m','C1','C2']
 
# for some selective phases
#confs = np.array(confs)[np.array([0,1,-2,-1])]
#colors=['lightblue','lightgreen','lightyellow','lightcoral']

nx=300
ny=150
method='analytic'

# single-ion anisotropy which can break the O(3) symmetry
# positive for out-of-plane and negative for in-plane magnetization
SIA=-0.1*0
Neel_vec=np.array([0,0,1])
#Neel_vec=np.array([1,0,0])


if __name__=='__main__':
    #test_energy_function(ntest=5)

    print ('Calculate the energies for MnPSe3')
    for conf in confs:
        en = calc_energy_analytic(*tuple(Js_MnPSe3),conf=conf,S=S,SIA=SIA,Neel_vec=Neel_vec)
        print ('{:>15s} : {:10.5f} meV'.format(conf,en))

    # use J1 as unit, J1 = 1, AFM
    # reproduce Fig. 7 of Phys. Rev. B 83, 184401 (2011)
    # the black region (spiral phase) is not included
    min_J1=-2
    max_J1=4
    min_J2=-4
    max_J2=4
    min_J3=-4
    max_J3=4
    J20,J30 = np.mgrid[min_J2:max_J2:1j*nx,min_J3:max_J3:1j*ny]

    J1 = -np.ones_like(J20)
    J2 = J20*J1
    J3 = J30*J1
    energies,ground_state_confs_maps,ground_state_iconf = calc_phase_diagram(J1,J2,J3,confs,
    method=method,S=S,SIA=SIA,Neel_vec=Neel_vec)
    fig = map_phase_diagram(J1,J2,J3,energies,ground_state_confs_maps,ground_state_iconf,
    mark_datapoints=mark_datapoints,
    colors=colors,unit='J1',normalize=False)

 
    exit()

    min_J1=-2
    max_J1=4
    min_J2=-3
    max_J2=4
    min_J3=-4
    max_J3=4
    J10,J20 = np.mgrid[min_J1:max_J1:1j*nx,min_J2:max_J2:1j*ny]

    # J3 = -1, FM
    J3 = -np.ones_like(J10)
    J1 = J10*J3
    J2 = J20*J3
    energies,confs_maps,ground_state_iconf = calc_phase_diagram(J1,J2,J3,confs,method=method,S=S,SIA=SIA)
    fig = map_phase_diagram(J1,J2,J3,energies,confs_maps,ground_state_iconf,show=False,
    )

    # J3 = 1, AFM
    min_J1=-2
    max_J1=4
    min_J2=-1
    max_J2=2
    min_J3=-4
    max_J3=4
    J10,J20 = np.mgrid[min_J1:max_J1:1j*nx,min_J2:max_J2:1j*ny]

    J3 = np.ones_like(J10)
    J1 = J10*J3
    J2 = J20*J3
    energies,confs_maps,ground_state_iconf = calc_phase_diagram(J1,J2,J3,confs,method=method,S=S,SIA=SIA)
    fig = map_phase_diagram(J1,J2,J3,energies,confs_maps,ground_state_iconf,
    mark_datapoints=mark_datapoints,
    #labels=labels,mark_phase=True,
    show=False)

    exit()

    iconf = -2
    relative_en = np.zeros(ground_state_iconf.shape)
    for ix,iy in np.ndindex(nx,ny):
        relative_en[ix,iy] = energies[iconf,ix,iy] - energies[ground_state_iconf[ix,iy],ix,iy]
    fig,ax=plt.subplots(1,1)
    scat = ax.scatter(J2,J3,c=relative_en,s=2,cmap='bwr',vmin=-1000,vmax=1000)
    fig.colorbar(scat,shrink=0.5)
    ax.set_xlim(min_J2,max_J2)
    ax.set_ylim(min_J3,max_J3)
    fig.tight_layout()
    plt.show()
 
 
    exit()

    nx = 50
    ny = 50
    nz = 50
    max_J = max(max_J1,max_J2,max_J3)
    min_J = min(min_J1,min_J2,min_J3)
    J10,J20,J30 = np.mgrid[min_J:max_J:1j*nx,min_J:max_J:1j*ny,min_J:max_J:1.j*nz]
    energies, ground_state_iconf = calculate_phase_diagram(J10,J20,J30) 
    #tenary_phase_diagram(J10,J20,J30,ground_state_iconf,mark_datapoints)
