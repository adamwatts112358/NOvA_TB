# particle_tracking_ana
# Mike Wallbank, July 2020
#
# Analyze the particles which have been previously tracked

import sys
sys.path.append("..")
from particle_structures import ParticleID, DetectorHit, ParticleFlow
import matplotlib.pyplot as plt
import pickle, numpy

particles = pickle.load(open("{}".format(sys.argv[1]), "rb"))

# information to save
h_num_det_hits = []
momentum_of_stopped_particles = []
further_sameparticle_hits = []
descendant_detector_hits = []

for particleIt in particles:
    particle = particles[particleIt]
    particle.PrintBasic()

    for detector in particle.Detectors:
        print "  Hit detector {} with momentum {}".format(detector, particle.Detectors[detector].Pz)

    for daughter_det in particle.DaughterDetectors:
        daughter_info = particle.DaughterDetectors[daughter_det]
        print "  Daughter {} ({}) hit detector {} with momentum {}" \
            .format(daughter_info[1], daughter_info[2], daughter_det, daughter_info[0].Pz)

    num_det_hits = len(particle.Detectors)+len(particle.DaughterDetectors)
    h_num_det_hits.append(num_det_hits)
    if num_det_hits == 1:
        momentum_of_stopped_particles.append(particle.Detectors[21].Pz)
    else:
        further_sameparticle_hits.append(len(particle.Detectors)-1)
        descendant_detector_hits.append(len(particle.DaughterDetectors))

fig = plt.figure(figsize=(10, 10))
plt.hist(h_num_det_hits, bins=6, range=(0,6))
plt.xlabel("Number of detector hits", fontsize=18)
plt.savefig('./figs/number_of_detector_hits.png')
plt.tight_layout()
plt.close()

fig = plt.figure(figsize=(10, 10))
plt.hist(momentum_of_stopped_particles)
plt.xlabel("Momentum of Particles Stopped by Collimator (MeV)", fontsize=18)
plt.savefig('./figs/momentum_of_stopped_particles.png')
plt.tight_layout()
plt.close()

fig = plt.figure(figsize=(10, 10))
plt.hist(further_sameparticle_hits, bins=6, range=(0,6))
plt.xlabel("Further Hits by Same Incident Particle (Not Daughter)", fontsize=18)
plt.savefig('./figs/further_particle_hits.png')
plt.tight_layout()
plt.close()

fig = plt.figure(figsize=(10, 10))
plt.hist(descendant_detector_hits, bins=6, range=(0,6))
plt.xlabel("Number of Detectors Hit by Descendants", fontsize=18)
plt.savefig('./figs/descendant_detector_hits.png')
plt.tight_layout()
plt.close()
