#!/usr/bin/env python

from analyze_spin_correlations import *

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
        confs_A = np.zeros((confs_0.shape[0],args.nx//2,args.ny//2,2,3))
        confs_B = np.zeros((confs_0.shape[0],args.nx//2,args.ny//2,2,3))
        confs_A[:,:,:,:1] = confs_0[:,0::2,0::2]
        confs_A[:,:,:,1:] = confs_0[:,1::2,1::2]
        confs_B[:,:,:,:1] = confs_0[:,0::2,1::2]
        confs_B[:,:,:,1:] = confs_0[:,1::2,0::2]
        confs_0 = np.concatenate((confs_A,confs_B),axis=3)

        print ('Use the last {} configurations for sampling.\n'.format(confs_0.shape[0]))
        disps = calc_space_disp(latt,sites,cutoff_x,cutoff_y,cutoff_z=0,ndim=2,verbosity=1)
        corrs = calc_correlation_function(confs_0,confs_0,cutoff_x=cutoff_x,cutoff_y=cutoff_y,verbosity=1,substract_background=False)
        pickle.dump(disps,open('{}/disps.pickle'.format(args.outdir),'wb'))
        pickle.dump(corrs,open('{}/corrs.pickle'.format(args.outdir),'wb'))

    if restart < 3:   # restart < 3, start from the loaded disps and corr data
        disps = pickle.load(open('{}/disps.pickle'.format(args.outdir),'rb'))
        corrs = pickle.load(open('{}/corrs.pickle'.format(args.outdir),'rb'))

    return disps,corrs


args.nx=60
args.ny=60
cutoff_x=10
cutoff_y=10

restart=1

if __name__=='__main__':
    latt = np.diag([2,2])
    sites = np.array([[[[0,0],[0.5,0.5],[0.5,0],[0,0.5]]]])
    subgroups = np.array([[0,1],[2,3]])

    args.outdir='square_AFM_XY'
    disps,corrs = get_corrs_one_set(restart,args,latt,sites,start_conf,cutoff_x,cutoff_y)
    args.outdir='square_AFM_Ising'
    disps_Ising,corrs_Ising = get_corrs_one_set(restart,args,latt,sites,start_conf,cutoff_x,cutoff_y)

    fig,ax=plt.subplots(3,1,sharex=True,figsize=(6,7))
    plot_spin_corrs(ax,disps,corrs,label_prefix='XY',sublattice_groups=subgroups,component_label=False) 
    plot_spin_corrs(ax,disps_Ising,corrs_Ising,colors=default_color_set[3:],
    component_label=True,component_label_height=0.5,
    label_prefix='Ising',sublattice_groups=subgroups) 
    for axx in ax: axx.legend()
    fig.tight_layout()
    fig.savefig('Spin_correlations',dpi=400)
    plt.show()            

