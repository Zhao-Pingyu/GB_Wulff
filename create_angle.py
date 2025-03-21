import numpy as np
mis = 20 # misorientation angle
incs = np.arange(0,46,1) # inclination angles for [001] tilt gb with D4h symmetry
# create structure file for Atomsk to generate gb structure
x = 62 # box length along x direction
y = 62 # box length along y direction
z = 62 # box length along z direction
a = 3.52 # lattice constant
deg = '°'
for inc in incs:
    with open('{}-{}.txt'.format(mis,inc), 'w',encoding="utf-8") as outfile:
        outfile.write(f'box {x*a} {y*a} {z*a}\n')
        if mis>=2*inc:
            outfile.write('node 0.5*box 0.75*box 0.5*box 0{} 0{} {}{}\n'.format(deg,deg,mis/2-inc,deg))
            outfile.write('node 0.5*box 0.25*box 0.5*box 0{} 0{} -{}{}\n'.format(deg,deg,mis/2+inc,deg))
        else:
            outfile.write('node 0.5*box 0.75*box 0.5*box 0{} 0{} -{}{}\n'.format(deg,deg,-mis/2+inc,deg))
            outfile.write('node 0.5*box 0.25*box 0.5*box 0{} 0{} -{}{}\n'.format(deg,deg,mis/2+inc,deg))