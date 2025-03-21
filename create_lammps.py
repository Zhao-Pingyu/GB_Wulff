import numpy as np
import os
from shutil import copy, move

mis = 30 # misorientation angle
inc = np.arange(0,46,1) # inclination angle
a = 3.52 # lattice constant
x = 62 # simulation box length along x (in lattice units)
y = 62
z = 62
inner_r = 15 # inner sphere radius (in lattice units)

for inc_ in inc:
    name_string = '{}-{}'.format(mis,inc_)
    with open('{}.in'.format(name_string), 'w') as outfile:
        outfile.write('clear\n')
        outfile.write('log log-{}.lammps\n'.format(name_string))
        outfile.write('variable i loop 66\n')
        outfile.write('label loop\n')
        outfile.write('clear\n')
        outfile.write('variable b equal ($i+4)*0.01*$a\n')
        outfile.write('units metal\n')
        outfile.write('atom_style atomic\n')
        outfile.write('dimension 3\n')
        outfile.write('boundary s s s\n')
        outfile.write('lattice fcc $a\n')
        outfile.write('region total block 0 $x 0 $y 0 $z\n')
        outfile.write('create_box 1 total\n')
        outfile.write('read_data {}-{}-s.lmp add append\n'.format(mis,inc_))
        outfile.write('region r sphere ${x}/2 ${y}/2 ${z}/2 ${inner_r}\n')
        outfile.write('group r region r\n')
        #------------ Define Interatomic Potential ---------------------
        outfile.write('pair_style eam/alloy\n')
        outfile.write('pair_coeff * * ni1.set 1\n')
        outfile.write('timestep 0.001\n')
        outfile.write('delete_atoms overlap $b all all\n')
        outfile.write('neighbor 2.0 bin\n')
        outfile.write('neigh_modify delay 10 check yes\n')
        #- ---------- Define Settings --------------------- 
        outfile.write('compute er r pe/atom\n')
        outfile.write('compute Er r  reduce sum c_er\n')
        # ---------- Run Minimization --------------------- 
        outfile.write('fix 1 all box/relax iso 0.0 vmax 0.001\n')
        outfile.write('thermo_style custom step pe lx ly lz press pxx pyy pzz c_Er15\n')
        outfile.write('thermo 100\n')
        outfile.write('min_style cg\n')
        outfile.write('minimize 1.0e-15 1.0e-15 100000 1000000\n')
        outfile.write('variable nr equal "count(r)"\n')
        outfile.write('variable Er equal "c_Er"\n')
        outfile.write('variable length equal "lx"\n')
        outfile.write('print "b = ${b};"\n')
        outfile.write('print "Sphere energy (eV) = ${Er};"\n')
        outfile.write('print "Number of atoms = ${nr};"\n')
        outfile.write('next i\n')
        outfile.write('jump SELF loop\n')
os.mkdir('{}'.format(mis))
for inc_ in inc:
    move('{}-{}.in'.format(mis,inc_), '{}'.format(mis))