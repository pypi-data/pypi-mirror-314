#!/usr/bin/python

from asd.utility.mag_thermal import *


def display_log_magnetization_with_varying_beta(
    temperatures=np.linspace(0,20,100,),Tc=10,betas=[0.125,np.pi**2*3/128],show=False):

    fig,ax=plt.subplots(1,1,figsize=(6,4))
    for beta in betas:
        yy = exponent_magnetization(temperatures,Tc,beta)
        ax.plot(temperatures,yy,label='$\\beta\ =\ {:.3f}$'.format(beta))
    for beta,label in zip([0.125,np.pi**2*3/128],['Ising','XY']):
        yy = exponent_magnetization(temperatures,Tc,beta)
        ax.plot(temperatures,yy,lw=3,label='$\\beta\ =\ {0:.3f}$'.format(beta)+' 2D {}'.format(label))
    ax.legend()
    ax.set_xlabel('T (K)')
    ax.set_ylabel('M')
    fig.tight_layout()
    fig.savefig('Tc_beta_power',dpi=400)
    if show: plt.show()


if __name__=='__main__':
    print ('script to calculate spin related thermodynamic properties')
    betas = [0.15,0.3,0.6,1.2,1.8]
    display_log_magnetization_with_varying_beta(betas=betas,show=True)

