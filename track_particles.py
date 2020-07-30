# track_particles.py
# Mike Wallbank, July 2020
#
# From the full simulation, build up full tracking of all particles
# passing through MC6/MC7 in order to study behavior

# Useage:
#  The tracking works by selecting particles of interest in a given detector,
#  and then tracking them upstream or downstream.
#  Parent or daughter particles are added to the particle's attributes, along
#  with all detectors hit and the properties of the particle at each location.
#  The following is required:
#   -- define the selection in the PassSelection function
#   -- define the detector to start the tracking from, and the tracking direction (upstream or downstream)
#   -- define the output file name describing the particles being selected and tracked
#   -- define how much data to analyze, and the base directory to find the output of the simulation
#         (note the directory structure is assumed to be that made when running the simulation using the
#         set up defined in the configurations in this directory)

import os
from particle_structures import ParticleID, Particle, DetectorHit, ParticleFlow
import pickle

# define selection
def PassSelection(particle):
    #if particle.PDG == 2212 and particle.Pz > 80000:
    #if particle.PDG == 2212 and particle.Y > 200 and particle.X > -1000:
    if abs(particle.PDG) == 13 and particle.Y > 200 and particle.X > -1000:
    #if particle.PDG == 211 and particle.Y > 200 and particle.X > -1000:
    #if particle.PDG == -211 and particle.Y > 200 and particle.X > -1000:
        return True
    return False

# define where to start the selection and which way to track
start_detector = 26
track_upstream = True
# start_detector = 21
# track_upstream = False

# output file name
# selection (highp, plumeloc etc) - species - start (detplume, collimator etc) - direction (us, ds)
outtag = "plumeloc-mu-detplume-us"

# define how much data to analyze
num_batches = 1 # 5
jobs_per_batch = 10 # 1000
events_per_job = 400000

# define the base directory
base_dir = "/pnfs/nova/scratch/users/wallbank/testbeam_sim/full_fields/64GeV/mc6mc7/"

# Containers to hold objects of interest
particles = {}
particle_origin = {}
particle_daughter = {}

# Find particles to track
batch_start = 0
while batch_start < (num_batches*jobs_per_batch*events_per_job):
    job_start = 0
    while job_start < (batch_start+(jobs_per_batch*events_per_job)):
        print "Initial particle selection: {}%" \
            .format(float(job_start*100)/(float(num_batches*jobs_per_batch*events_per_job)))
        if not os.path.isfile("{}/{}/{}_{}.txt" \
                                  .format(base_dir, batch_start, start_detector, job_start)):
            job_start += events_per_job
            continue
        with open("{}/{}/{}_{}.txt" \
                      .format(base_dir, batch_start, start_detector, job_start)) as inFile:
            print inFile
            for line in inFile:
                # x y z Px Py Pz t PDGid EventID TrackID ParentID Weight
                if line.startswith('#'):
                    continue
                line_split = line.strip().split(' ')
                x = float(line_split[0])
                y = float(line_split[1])-724.8144
                z = float(line_split[2])
                px = float(line_split[3])
                py = float(line_split[4])
                pz = float(line_split[5])
                pdg = int(line_split[7])
                eventid = int(line_split[8])
                trackid = int(line_split[9])
                parentid = int(line_split[10])
                particle = Particle(eventid, trackid, pdg, x, y, z, px, py, pz, parentid)

                if PassSelection(particle):
                    particleid = ParticleID(eventid, trackid)
                    particles[particleid] = ParticleFlow(eventid, trackid, pdg, parentid)
                    particles[particleid].AddDetector(DetectorHit(start_detector, x, y, z, px, py, pz))
                    parentid = ParticleID(eventid, parentid)
                    particle_origin[particleid] = particleid
                    particle_daughter[parentid] = particleid
        job_start += events_per_job
    batch_start += (jobs_per_batch*events_per_job)

print "Particles to track ({}):".format(len(particles))
for particleid in particles.keys():
    particleid.Print()

# Find these particles, and the parents/daughters, in the detectors upstream or downstream
batch_start = 0
if track_upstream: detector_list = [i for i in reversed(range(1,start_detector))]
else: detector_list = [i+1 for i in range(start_detector,26)]
while batch_start < (num_batches*jobs_per_batch*events_per_job):
    job_start = 0
    while job_start < (batch_start+(jobs_per_batch*events_per_job)):
        print "Tracking upstream/downstream particles: {}%" \
            .format(float(job_start*100)/(float(num_batches*jobs_per_batch*events_per_job)))
        for detector in detector_list:
            if not os.path.isfile("{}/{}/{}_{}.txt" \
                                      .format(base_dir, batch_start, detector, job_start)):
                job_start += events_per_job
                continue
            with open("{}/{}/{}_{}.txt" \
                          .format(base_dir, batch_start, detector, job_start)) as inFile:
                print inFile
                for line in inFile:
                    # x y z Px Py Pz t PDGid EventID TrackID ParentID Weight
                    if line.startswith('#'):
                        continue
                    line_split = line.strip().split(' ')
                    x = float(line_split[0])
                    y = float(line_split[1])-724.8144
                    z = float(line_split[2])
                    px = float(line_split[3])
                    py = float(line_split[4])
                    pz = float(line_split[5])
                    pdg = int(line_split[7])
                    trackid = int(line_split[9])
                    eventid = int(line_split[8])
                    parentid = int(line_split[10])
                    particle = Particle(eventid, trackid, pdg, x, y, z, px, py, pz, parentid)

                    particleid = ParticleID(eventid, trackid)
                    if particleid in particles.keys():
                        particles[particleid].AddDetector(DetectorHit(detector, x, y, z, px, py, pz))
                    if particleid in particle_daughter.keys():
                        daughterid = particle_daughter[particleid]
                        particles[daughterid].AddParentDetector(DetectorHit(detector, x, y, z, px, py, pz), trackid, pdg)
                        particle_daughter[ParticleID(eventid, parentid)] = daughterid
                    if ParticleID(eventid, parentid) in particle_origin.keys():
                        originid = particle_origin[ParticleID(eventid, parentid)]
                        particles[originid].AddDaughterDetector(DetectorHit(detector, x, y, z, px, py, pz), trackid, pdg)
                        particle_origin[particleid] = originid

        job_start += events_per_job
    batch_start += (jobs_per_batch*events_per_job)

pickle.dump(particles, file = open("particle_tracking_output/particles_{}.pickle".format(outtag), "wb"))
