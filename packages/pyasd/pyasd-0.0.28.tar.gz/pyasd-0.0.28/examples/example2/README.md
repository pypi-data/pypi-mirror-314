# LLG simulation example 

Square lattice with nearest Ising-type ferromagnetic exchange coupling

##  To run the example

1. run the LLG simulation by command

> mpirun -np 2 ./llg.py

> "2" is the number of processors invoked and can be changed depending on your platform

2. post-processing, to visualize the simulation results

> run the command

> post_llg.py --scatter_size=30 --jump=1
