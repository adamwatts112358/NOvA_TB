#!/bin/bash

JOBS_PER_BATCH=1000
EVENTS_PER_JOB=400000
OUTPUT_DIR='/pnfs/nova/scratch/users/wallbank/testbeam_sim/200MeVcut/64GeV-12mm-correct/'

if [ "$#" == 1 ] && [[ "$1" = "nova" ]]; then
    for BATCH in {0..4}
    do
	BATCH_PROCESS_START=$((JOBS_PER_BATCH*BATCH))
	BATCH_EVENT_START=$((EVENTS_PER_JOB*BATCH_PROCESS_START))

	touch ${OUTPUT_DIR}/${BATCH_EVENT_START}
	rm -rf ${OUTPUT_DIR}/${BATCH_EVENT_START}
	mkdir ${OUTPUT_DIR}/${BATCH_EVENT_START}
	chmod g+w ${OUTPUT_DIR}/${BATCH_EVENT_START}

	jobsub_submit --resource-provides=usage_model=OPPORTUNISTIC --OS=SL6 -G nova -N ${JOBS_PER_BATCH} -f dropbox://NOvA_TB.in -f dropbox://EPB.in -f dropbox://QQM.in -f dropbox://RQB.in -f dropbox://EPB_fieldmap.txt -f dropbox://3Q120_fieldmap.txt -f dropbox://4Q120_fieldmap.txt -d OUTDIR ${OUTPUT_DIR}/${BATCH_EVENT_START} file://run_g4bl_nova.sh ${BATCH_PROCESS_START} ${EVENTS_PER_JOB} OUTDIR
    done

else
    jobsub_submit  --resource-provides=usage_model=OPPORTUNISTIC --expected-lifetime=2h --disk=4GB -G ebd -N 50 file://run_g4bl.sh

fi