#!/bin/bash -x
#SBATCH --job-name=extract_py
#SBATCH --account=jibg31
#SBATCH --ntasks=256
#SBATCH --time=24:00:00

source /p/scratch/cjibg31/jibg3105/projects/venvs/2024_03/activate.sh

srun -n 256 python parallel.py


