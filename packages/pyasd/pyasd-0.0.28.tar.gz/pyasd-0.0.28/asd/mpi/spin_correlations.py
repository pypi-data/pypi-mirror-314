#!/usr/bin/env python

#=============================================
#
# structure factors of spin configs
# Shunhong Zhang
# Last modified: Nov 27, 2021
#
#=============================================

from asd.core.spin_correlations import *
import asd.mpi.mpi_tools as mt

 
def mpi_calc_static_structure_factor(spins,sites_cart,qpt_cart,dump=True):
    comm,size,rank,node = mt.get_mpi_handles()
    start,last = mt.assign_task(len(qpt_cart),size,rank)
    S_vector = calc_static_structure_factor(spins,sites_cart,qpt_cart[start:last],dump=False)
    S_vector = comm.allgather(S_vector)
    S_vector = np.concatenate(S_vector,axis=0)
    if dump and rank==0: pickle.dump(S_vector,open('S_vector.pickle','wb'))
    return S_vector


def mpi_calculate_correlation_function_dR(confs_t,confs_0,dx,dy,ave_on_confs=True):
    import mpi4py.MPI as MPI
    comm,size,rank,node = mt.get_mpi_handles()

    stime = time.time()
    if rank==0: shape = confs_t.shape
    else: shape=None
    shape = comm.bcast(shape)
    nsample,nx,ny,nat = shape[:4]

    itemsize = MPI.DOUBLE.Get_size()
    nbytes = itemsize*np.prod(shape)
    win1 = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm)
    buf1, itemsize0 = win1.Shared_query(0)
    assert itemsize0 == itemsize
    confs_0_shared = np.ndarray(buffer=buf1, dtype='float', shape=shape)
    if rank==0: confs_0_shared[:] = confs_0

    win2 = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm)
    buf2, itemsize0 = win2.Shared_query(0)
    assert itemsize0 == itemsize
    confs_t_shared = np.ndarray(buffer=buf2, dtype='float', shape=shape)
    if rank==0: confs_t_shared[:] = confs_t

    comm.barrier()
    start,last = mt.assign_task(nsample,size,rank)
    corr = np.zeros((nat,nat,3))
    for isample in range(start,last):
        confs_tmp = np.roll(confs_0_shared[isample],(-dy,-dx),axis=(1,0))
        cc = np.einsum('xyad,xybd->xyabd',confs_t_shared[isample],confs_tmp)
        corr += np.average(cc,axis=(0,1))
    corr = comm.allreduce(corr)
    corr = corr/nsample
    if rank==0: print('Time used: {:8.3f} s'.format(time.time()-stime)); sys.stdout.flush()
    win1.Free()
    win2.Free()
    return corr


def mpi_get_confs_t(nx,ny,nat,prefix='Ensemble',fil_key='spin_confs.ovf',start_conf=0):
    import glob
    from asd.utility.ovf_tools import parse_ovf
    comm,size,rank,node = mt.get_mpi_handles()
    if prefix=='': dirs=['.']
    else: dirs = sorted(glob.glob('{}_*'.format(prefix)))
    if dirs==[]:
        if rank==0: print ('Cannot find ovf files at directories with prefix "{}"!'.format(prefix))
        exit()
    nsample = len(dirs)
    start,last = mt.assign_task(nsample,size,rank)
    confs_t = []
    for i in range(start,last):
        fil = glob.glob('{}/{}'.format(dirs[i],fil_key))[0]
        spins = parse_ovf(fil)[1]
        confs = np.swapaxes(spins.reshape(spins.shape[0],ny,nx,nat,3),1,2)
        confs_t.append(confs[start_conf:])
    confs_t = comm.gather(confs_t)
    if rank==0: confs_t = np.array([conf for confs in confs_t for conf in confs if len(confs)>0])
    else: confs_t = None
    return confs_t


# a parallel version
def mpi_calc_dyn_structure_factor(confs,latt,sites,qpt_cart,time_spacing,omegas,
    cutoff_x=3,cutoff_y=3,cutoff_z=0,
    dump=True,pickle_name='Swq.pickle',verbosity=1):

    comm,size,rank,node = mt.get_mpi_handles()
    nx,ny = sites.shape[:2]
    nat,ndim = sites.shape[-2:]
    nsite = np.prod(sites.shape[:-1])
    nq = len(qpt_cart)
    nomega = len(omegas)
    if not rank: shape = confs.shape
    else: shape = None
    shape = comm.bcast(shape)
    nsample,nconf = shape[:2]

    times = (np.arange(nconf)-nconf//2)*time_spacing
    time_phases = np.exp(2.j*np.pi * np.einsum('w,t->wt',omegas,times) )

    if not rank: space_disp = calc_space_disp(latt,sites,cutoff_x,cutoff_y,cutoff_z,ndim)
    else: space_disp = None
    space_disp = comm.bcast(space_disp)
    space_phases = np.exp(2.j*np.pi * np.einsum('qi,xyabi-> qxyab',qpt_cart, space_disp) )

    stime = time.time()
    Swq = np.zeros((nq,nomega,3),complex)

    start,last = mt.assign_task(nconf,size,rank)

    confs_t = np.zeros((nsample,last-start,*tuple(shape[2:])))
    if rank==0:
        idx0 = np.where(times==0)[0][0]
        confs_0 = confs[:,idx0]
        if verbosity: verbose_Swq_setup(nsample,nconf,nsite,idx0,time_spacing,nq,nomega,np.max(omegas),cutoff_x,cutoff_y,size)
        confs_t = confs[:,start:last]
        for irank in range(1,size):
            start0,last0 = mt.assign_task(nconf,size,irank)
            comm.send(confs[:,start0:last0],dest=irank,tag=irank)
    else:
        confs_0 = None
        confs_t = comm.recv(source=0,tag=rank)
    confs_0 = comm.bcast(confs_0)
    

    mm = max(1,(last-start)//10)
    prog = 'Progress {:2d} / {}: Conf {:4d} of {}, time = {:10.3f} s'
    for iconf in range(last-start):
        if iconf%mm==0 and not rank and verbosity>1: 
            print (prog.format(iconf//mm,min(max(10,(last-start)//mm),last-start),iconf,last-start,time.time()-stime))
            sys.stdout.flush()
        Corr = calc_correlation_function(confs_t[:,iconf],confs_0,cutoff_x=cutoff_x,cutoff_y=cutoff_y)
        Swq0 = np.einsum('w,qxyab,xyabi->qwi',time_phases[:,iconf+start],space_phases,Corr)/np.prod(Corr.shape[:2])
        Swq += Swq0

    Swq = comm.allreduce(Swq)
    Swq *= time_spacing/(2*np.pi)
    if not rank and dump:  
        pickle.dump(Swq,open(pickle_name,'wb'))
        print ('\nFinished at {}\nTime used: {:8.2f} s'.format(time.ctime(),time.time()-stime))
    return Swq


if __name__=='__main__':
    print ('Running {}'.format(__file__.split('/')[-1]))

