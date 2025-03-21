## GB_Wulff
The GB_Wulff package is used for constructing the Wulff shapes of cylindrical [001] tilt boundaries with any misorientation angle around the tilt axis. It integrates Atomsk for constructing bicrystal structures containing grain boundaries, and LAMMPS for performing atomistic simulations to determine grain boundary energy.

**Files:**

*create_angle.py*: generates the input files for constructing the bicrystal structures of the grain boundaries covering the full circle of inclination angles (0-360 ̊ ) for the defined misorientation angle

*atomsk.sh*: utilizes the Atomsk software to generate the grain boundary structures, based on the input files generated by create_angle.py

*create_lammps.py*: generates the input files for the LAMMPS software, which is used to search for the ground states of the constructed grain boundaries, and compute the grain boundary energies

*wulff.py*: extracts the computed ground state grain boundary energies for the different inclination angles, and perform Wulff construction to obtain the Wulff shape
