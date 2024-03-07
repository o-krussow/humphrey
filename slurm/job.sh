#!/bin/bash

#SBATCH --job-name=stock-test
#SBATCH -o outdir/output_%A_%a.txt
#SBATCH --mem 2G

PARAMS=$(sed "${SLURM_ARRAY_TASK_ID}q;d" params.txt)

python3 manager.py $PARAMS


