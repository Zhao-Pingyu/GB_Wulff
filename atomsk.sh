#!/bin/bash
angle="30"
radius="70.4"
a="3.52"
mkdir -p $angle
cd $angle
'atomsk.exe' --create fcc $a Ni Ni.xsf
for ((i=0;i<=45;i+=1))
do 
	'atomsk.exe' --polycrystal Ni.xsf ${angle}-$i.txt ${angle}-$i.lmp;
	'atomsk.exe' ${angle}-$i.lmp -select out sphere 0.5*box 0.5*box 0.5*box ${radius} -rmatom select ${angle}-$i-s.lmp;
done
rm -f ${angle}-*grains-com.xsf
rm -f ${angle}-*nodes.xsf
rm -f ${angle}-*size-dist.txt
rm -f ${angle}-*id-size.txt
cd ..