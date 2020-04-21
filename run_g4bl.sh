# Magic  incantations so we can copy our tarball over from PNFS
. /cvmfs/fermilab.opensciencegrid.org/products/common/etc/setup
setup ifdhc
IFGH=`which ifdh`
export IFDH_CP_MAXRETRIES=2

# Copy the G4BL and Geant4 tarball over from PNFS                                                                                  
${IFGH} cp -D /pnfs/ebd/persistent/g4bl/NOvA_TB.tgz .
tar -xf NOvA_TB.tgz
cd G4BL

# Copy input file over
${IFGH} cp -D /pnfs/ebd/persistent/g4bl/NOvA_TB.in .

# Setup G4BL run parameters
MOMENTUM=64
EVENT_COUNT_PER_JOB=20000
FIRST=$((((${PROCESS_START} + ${PROCESS}))* ${EVENT_COUNT_PER_JOB}))
LAST=$((${FIRST} + $EVENT_COUNT_PER_JOB - 1))

# Point G4BL to the GEANT4 data from our tarball
export G4BL_DIR=./G4beamline-3.06
export G4ENSDFSTATEDATA=./Geant4Data/G4ENSDFSTATE2.2
export G4LEDATA=./Geant4Data/G4EMLOW7.7
export G4LEVELGAMMADATA=./Geant4Data/PhotonEvaporation5.3
export G4SAIDXSDATA=./Geant4Data/G4SAIDDATA2.0
export G4NEUTRONHPDATA=./Geant4Data/G4NDL4.5
export G4NEUTRONXSDATA=./Geant4Data/G4NEUTRONXS1.4
export G4PIIDATA=./Geant4Data/G4PII1.3
export G4RADIOACTIVEDATA=./Geant4Data/RadioactiveDecay5.3
export G4REALSURFACEDATA=./Geant4Data/RealSurface2.1.1
export G4ABLADATA=./Geant4Data/G4ABLA3.1
export G4PARTICLEXSDATA=./Geant4Data/G4PARTICLEXS1.1
export G4INCLDATA=./Geant4Data/G4INCL1.0
export G4TENDLDATA=./Geant4Data/G4TENDL1.3.2

# Run G4BL
./G4beamline-3.06/bin/g4bl NOvA_TB.in p=$MOMENTUM nParticles=$EVENT_COUNT_PER_JOB first=$FIRST last=$LAST > $FIRST.out.txt

# Copy output files back over to PNFS                                                                                                                  
cluster=$CLUSTER
process=$PROCESS
user=$GRID_USER
strProcess=`printf "%4.4d" $process`
outstagebase=/pnfs/ebd/persistent/g4bl
${IFGH} mkdir ${outstagebase}/${cluster}
${IFGH} mkdir ${outstagebase}/${cluster}/${user}_run_${strProcess}
${IFGH} cp -D *.txt ${outstagebase}/${cluster}/${user}_run_${strProcess}