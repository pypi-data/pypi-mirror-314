#!/usr/bin/env python

from asd.core.random_vectors import *

def hist_small_step(nn=10000):
    import matplotlib.pyplot as plt
    import asd.mpi.mpi_tools as mt
    comm,size,rank,node = mt.get_mpi_handles()

    sigmas = np.arange(0,2,0.05)
    nsigma = len(sigmas)
    start,last = mt.assign_task(nsigma,size,rank)
    thetas = np.zeros(last-start)

    for i,sigma0 in enumerate(sigmas[start:last]):
        if rank==0: print ('{:3d} of {}, sigma = {:4.2f}'.format(i+1,last-start,sigma0))
        vec0 = gen_normal_random_spin()
        spins = np.array([gen_small_step_random_spin(vec0,sigma0) for i in range(nn)])
        thetas[i] = np.max(abs(calc_azimuthal_angle(spins,vec0)))

    thetas = comm.gather(thetas,root=0)

    if rank==0:
        thetas = np.concatenate(thetas,axis=0)
        idx1 = np.where(sigmas<=1)
        idx2 = np.where(sigmas>=1)
        fig,ax=plt.subplots(1,1,figsize=(6,5))
        thetas = np.rad2deg(thetas)
        ax.plot(sigmas[idx1],thetas[idx1],'go-')
        ax.plot(sigmas[idx2],thetas[idx2],'ro-')
        #xx = np.linspace(0,1,1000)
        #yy = np.arccos(np.sqrt(0.5-xx/2))
        #yy = np.rad2deg(yy)
        #ax.plot(xx,yy,ls='--',c='b')
        ax.set_xlabel('$\sigma$')
        ax.set_ylabel('$\\theta_{max}$')
        for xx in [0,90,180]:
            ax.axhline(xx,ls='--',c='gray',alpha=0.5)
        ax.axvline(1,ls='--',alpha=0.5,zorder=-1)
        ax.set_yticks(np.arange(0,200,30))
        fig.tight_layout()
        plt.show()



def hist_spins_by_area():
    import matplotlib.pyplot as plt

    def statistics_spins(ax,spins,ls='-',tag='normal'):
        thetas = np.rad2deg(np.arccos(spins[:,2]))
        hist,bins = np.histogram(thetas,bins=18)
        cum_areas = 2*np.pi*(1-np.cos(np.deg2rad(bins)))
        cum_count = np.append(0,np.cumsum(hist))
        ax.plot(cum_areas/(np.pi),cum_count/nn,ls=ls,label='n = {:>6d}'.format(nn))
        ax.set_title(tag)
        ax.set_xticks(np.arange(5))
        ax.legend(loc='upper left')

    tags = {
    'Cubic_random': 'Cubic: incorrect',
    'Spherical_random':'Spherical: incorrect',
    'Modified_cubic':'modified cubic: correct but inefficient',
    'MultivarNormal':'Gaussian: correct and efficient'}

    fig,ax=plt.subplots(2,2,sharex=True,sharey=True,figsize=(10,10))
    for nn in [10000,20000]:
        for ii,key in enumerate(tags.keys()):
            spins = gen_random_spins_misc(nn,method=key)
            statistics_spins(ax[ii//2,ii%2],spins, tag=tags[key])
    for i in range(2): 
        ax[i,0].set_ylabel('$n\ (\\theta)\ /\ n_{tot}$')
        ax[1,i].set_xlabel('$S\ /\ \pi$')
    fig.tight_layout()
    plt.show()


if __name__=='__main__':
    #hist_small_step()
    #hist_spins_by_theta()
    hist_spins_by_area()
