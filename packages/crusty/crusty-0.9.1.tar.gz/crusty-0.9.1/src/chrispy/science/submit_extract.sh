#!/bin/bash -x
#SBATCH --job-name=extract_py
#SBATCH --account=jibg31
#SBATCH --ntasks=5
#SBATCH --time=24:00:00


source /p/scratch/cjibg31/jibg3105/Data/EDWUE/code_edwue/modulesEDWUE.sh

name=FERNAND_all
src=COSMOREA6
stations_file=FERNAND_stations.csv
variables='FLDS FSDS TBOT PSRF RH PRECTmms WIND'
year0=2009
year1=2018

#echo python extract.py -n $name -s $source -p $path -v $variables -x $unit_x

for y in $(seq $year0 2 $year1); do

	y1=$(($y+1))
	newname="${name}_${y}"

	srun -n 1 --mem 5256000 python extract.py -n $newname -s $src -v $variables -fs $stations_file -y0 $y -y1 $y1

done
