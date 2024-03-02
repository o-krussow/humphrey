#!/bin/bash

NUMPARAMS=$(cat params.txt | wc -l)

sbatch --array=1-"$NUMPARAMS" job.sh
