# particle_tracking_ana
# Mike Wallbank, July 2020
#
# Analyze the particles which have been previously tracked

import sys
sys.path.append("..")
from particle_structures import ParticleID, DetectorHit, ParticleFlow
import pickle, numpy
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from particle_tracking_utilities import LinesIntersect, PointsDistance

particles = pickle.load(open("{}".format(sys.argv[1]), "rb"))

# information to track
plume_init_x = []
plume_init_y = []
plume_init_z = []
primaries = 0
number_of_parents = {}
pdg_of_parent = {}

for particleIt in particles:
    particle = particles[particleIt]
    particle.PrintBasic()

    # print detectors the final particle hit
    for detector in particle.Detectors:
        print "  Hit detector {} with momentum {}".format(detector, particle.Detectors[detector].Pz)

    # analyze detectors parents hit
    parents = []
    for parent_det in particle.ParentDetectors:
        parent_info = particle.ParentDetectors[parent_det]
        print "  Parent {} ({}) hit detector {} with momentum {}" \
            .format(parent_info[1], parent_info[2], parent_det, parent_info[0].Pz)
        if [parent_info[1], parent_info[2]] not in parents:
            parents.append([parent_info[1], parent_info[2]])

    if particle.ParentID == 1:
        print "  Primary"
        primaries += 1
    else:
        print "  First detector hit by final particle is {}".format(particle.MostUpstreamDetector)
        if particle.MostUpstreamDetector-1 in particle.ParentDetectors:
            particle_det = particle.Detectors[particle.MostUpstreamDetector]
            parent_det = particle.ParentDetectors[particle.MostUpstreamDetector-1][0]
            p1, p2 = LinesIntersect(numpy.array([particle_det.X, particle_det.Y, particle_det.Z]),
                                    numpy.array([particle_det.Px, particle_det.Py, particle_det.Pz]),
                                    numpy.array([parent_det.X, parent_det.Y, parent_det.Z]),
                                    numpy.array([parent_det.Px, parent_det.Py, parent_det.Pz]))
            separation = PointsDistance(p1, p2)
            print "  Final particle was made near points {} and {}".format(p1, p2)
            print "    (Separation distance {} mm)".format(separation)
            if separation < 10:
                plume_init_x.append(p1[0])
                plume_init_y.append(p1[1])
                plume_init_z.append(p1[2])

    if len(parents) not in number_of_parents: number_of_parents[len(parents)] = 0
    number_of_parents[len(parents)] += 1

    last_parent = 0
    last_parent_pdg = -1
    for parent in parents:
        if parent[0] > last_parent:
            last_parent = parent[0]
            last_parent_pdg = parent[1]

    if last_parent_pdg not in pdg_of_parent: pdg_of_parent[last_parent_pdg] = 0
    pdg_of_parent[last_parent_pdg] += 1

print primaries, "primaries"
print "Number of parents:", number_of_parents
print "PDG of last parent:", pdg_of_parent

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(plume_init_z, plume_init_x, plume_init_y, marker='o')
ax.set_xlabel('z [mm]')
ax.set_ylabel('x [mm]')
ax.set_zlabel('y [mm]')
plt.show()
