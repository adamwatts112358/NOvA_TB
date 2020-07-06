# Run G4BL on worker node
# This version uses the build of G4beamline in ups

# Configurable parameters
PROCESS_START=$1
EVENT_COUNT_PER_JOB=$2
OUTPUT_DIR_TAG=$3

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

# Copy the required input files into the working directory
cp $CONDOR_DIR_INPUT/EPB.in .
cp $CONDOR_DIR_INPUT/QQM.in .
cp $CONDOR_DIR_INPUT/RQB.in .
cp $CONDOR_DIR_INPUT/EPB_fieldmap.txt .
cp $CONDOR_DIR_INPUT/3Q120_fieldmap.txt .
cp $CONDOR_DIR_INPUT/4Q120_fieldmap.txt .

echo "Running g4bl from event $FIRST to $LAST"

# Run G4BL
g4bl $CONDOR_DIR_INPUT/NOvA_TB.in p=$MOMENTUM nParticles=$EVENT_COUNT_PER_JOB first=$FIRST last=$LAST &> out_${FIRST}.txt

# Remove the input files from the working dir
rm -f EPB.in
rm -f QQM.in
rm -f RQB.in
rm -f EPB_fieldmap.txt
rm -f 3Q120_fieldmap.txt
rm -f 4Q120_fieldmap.txt

# Copy output files which we need to the directory which will be copied back
OUTPUT_DIR_ENV=CONDOR_DIR_${OUTPUT_DIR_TAG}
OUTPUT_DIR=${!OUTPUT_DIR_ENV}
cp *.txt ${OUTPUT_DIR}
cp g4beamline.root ${OUTPUT_DIR}/g4beamline_${FIRST}.root