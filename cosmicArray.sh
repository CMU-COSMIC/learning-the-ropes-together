#!/bin/bash
#SBATCH -n 64
#SBATCH -t 168:00:00
#SBATCH -J cosmic_run_%a 
#SBATCH -o cosmic_run_%a
#SBATCH -A phy230054p
#SBATCH -p HENON
#SBATCH --array=0-29
#SBATCH --mail-type=ALL
# use the bash shell
set -x 
date
# echo each command to standard out before running it

metVals=(0.0001 0.00012174 0.0001482 0.00018041 0.00021962
       0.00026736 0.00032547 0.00039621 0.00048233 0.00058717
       0.00071479 0.00087016 0.00105929 0.00128954 0.00156983
       0.00191104 0.00232642 0.00283208 0.00344765 0.00419702
       0.00510928 0.00621981 0.00757174 0.00921751 0.011221
       0.01365996 0.01662905 0.02024349 0.02464355 0.03)
met=${metVals[$SLURM_ARRAY_TASK_ID]}

cosmic-pop --final-kstar1 14 15 --final-kstar2 14 15 --inifile Params.ini --porb_model log_uniform --apply_convergence_limits True --Nstep 100000 --Niter 10000000000 --metallicity $met --seed 1209 --nproc 64 

date