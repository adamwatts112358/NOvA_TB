# particle_tracking_ana
# Mike Wallbank, July 2020
#
# Analyze the particles which have been previously tracked

import sys
sys.path.append("..")
from particle_structures import ParticleID, DetectorHit, ParticleFlow
import pickle, numpy
from particle_tracking_utilities import FindIntersect

particles = pickle.load(open("../particle_tracking_output/particles_highp-protons-collimator-ds.pickle", "rb"))

for particleIt in particles:
    particleIt.Print()
    particle = particles[particleIt]
    if particle.ParentID == 1:
        print "  Primary"
    for detector in particle.Detectors:
        print "  Hit detector {} with momentum {}".format(detector, particle.Detectors[detector].Pz)
    for daughter_det in particle.DaughterDetectors:
        daughter_info = particle.DaughterDetectors[daughter_det]
        print "  Daughter {} ({}) hit detector {} with momentum {}" \
            .format(daughter_info[1], daughter_info[2], daughter_det, daughter_info[0].Pz)
