# Run G4BL on worker node
# This version uses the build of G4beamline in ups

# Configurable parameters
EVENT_COUNT_PER_JOB=$1
OUTPUT_DIR_TAG=$2

# Setup G4beamline from NOvA ups area
source /cvmfs/nova.opensciencegrid.org/novasoft/slf6/novasoft/setup/setup_nova.sh -b maxopt
#source /cvmfs/nova.opensciencegrid.org/externals/setup
setup G4beamline v3_04
ups active

# Setup G4BL run parameters
MOMENTUM=64
#EVENT_COUNT_PER_JOB=20000
FIRST=$((((${PROCESS_START} + ${PROCESS}))* ${EVENT_COUNT_PER_JOB}))
LAST=$((${FIRST} + $EVENT_COUNT_PER_JOB - 1))

# Run G4BL
g4bl $CONDOR_DIR_INPUT/NOvA_TB.in p=$MOMENTUM nParticles=$EVENT_COUNT_PER_JOB first=$FIRST last=$LAST &> out_${FIRST}.txt

# Copy output files which we need to the directory which will be copied back
OUTPUT_DIR_ENV=CONDOR_DIR_${OUTPUT_DIR_TAG}
OUTPUT_DIR=${!OUTPUT_DIR_ENV}
cp *.txt ${OUTPUT_DIR}
cp g4beamline.root ${OUTPUT_DIR}/g4beamline_${FIRST}.root