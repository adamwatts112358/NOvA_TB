#!/bin/bash

if [ "$#" == 1 ] && [[ "$1" = "nova" ]]; then
    jobsub_submit --resource-provides=usage_model=OPPORTUNISTIC --OS=SL6 -G nova -N 10000 -f dropbox://NOvA_TB.in -d OUTDIR /pnfs/nova/scratch/users/wallbank/testbeam_sim/ file://run_g4bl_nova.sh 400000 OUTDIR

else
    jobsub_submit  --resource-provides=usage_model=OPPORTUNISTIC --expected-lifetime=2h --disk=4GB -G ebd -N 50 file://run_g4bl.sh

fi