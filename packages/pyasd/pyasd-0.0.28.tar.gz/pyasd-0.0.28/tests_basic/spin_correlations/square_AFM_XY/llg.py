#!/usr/bin/env python


from spirit import io,log,state,geometry,system,hamiltonian,simulation,parameters,configuration
import os
import glob

# in the convention of Spirit code
# negative for AFM, positive for FM
J1 = -1

# The DM intereaction strength
# if you use set_dmi, the DM vector
# always points along the bond, which
# favors Bloch-type skyrmions or other 
# chiral magnetic structures
DMI = 0

# for Single-ion anisotropy (SIA)
# negative (positive) favors in-plane (out-of-plane)
SIA = -0.1

temp=5
nx=60
ny=60
quiet = False

zeeman = 0.05

def main(nx,ny,J1,SIA,DMI,zeeman,temp):
    if len(glob.glob('*ovf'))>0: 
        for file in glob.glob('*ovf'): os.remove(file)
    if len(glob.glob('Log*'))>0:
        for file in glob.glob('Log*'): os.remove(file)
 
    tag = 'T_{:.2f}'.format(temp)
    with state.State(quiet = quiet) as p_state:
        geometry.set_n_cells(p_state,[nx,ny,1])
        geometry.set_mu_s(p_state, 1)
        hamiltonian.set_boundary_conditions(p_state,[1,1,0])
        hamiltonian.set_exchange(p_state, 1, [J1])
        hamiltonian.set_anisotropy(p_state, SIA, [0,0,1])
        hamiltonian.set_dmi(p_state, 1, [DMI])
        hamiltonian.set_field(p_state, zeeman, [0,0,1])

        configuration.random(p_state)
        parameters.llg.set_output_tag(p_state, tag)
        parameters.llg.set_output_folder(p_state, '.')
        parameters.llg.set_iterations(p_state, 30000, 300)
        parameters.llg.set_output_configuration(p_state, 0, 1, 3)
        parameters.llg.set_output_energy(p_state, 0, 1)
        parameters.llg.set_output_general(p_state, 1, 0, 0)
        parameters.llg.set_temperature(p_state, temp)
        parameters.llg.set_damping(p_state, 0.05)
        parameters.llg.set_timestep(p_state, 0.001)
        system.update_data(p_state)
        simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_DEPONDT)

# in the convention of Spirit code
# negative for AFM, positive for FM
J1 = -1

# The DM intereaction strength
# if you use set_dmi, the DM vector
# always points along the bond, which
# favors Bloch-type skyrmions or other 
# chiral magnetic structures
DMI = 0

# for Single-ion anisotropy (SIA)
# negative (positive) favors in-plane (out-of-plane)
SIA = 0.1

temp=5
nx=60
ny=60
quiet = False

zeeman = 0.05

if __name__=='__main__':
    main(nx,ny,J1,SIA,DMI,zeeman,temp)
 
