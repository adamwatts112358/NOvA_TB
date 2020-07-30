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
plume_init = [0]*3
for dim in range(3):
    plume_init[dim] = {}
    for pdg in [2212, 211, 321, -1]:
        plume_init[dim][pdg] = []
primaries = 0
number_of_parents = {}
pdg_of_parent = {}
momentum = []

for particleIt in particles:
    particle = particles[particleIt]
    particle.PrintBasic()

    # print detectors the final particle hit
    for detector in particle.Detectors:
        print "  Hit detector {} with momentum {}".format(detector, particle.Detectors[detector].Pz)

    momentum.append(particle.Detectors[26].Pz)

    # analyze detectors parents hit
    parents = []
    for parent_det in particle.ParentDetectors:
        parent_info = particle.ParentDetectors[parent_det]
        print "  Parent {} ({}) hit detector {} with momentum {}" \
            .format(parent_info[1], parent_info[2], parent_det, parent_info[0].Pz)
        if [parent_info[1], parent_info[2]] not in parents:
            parents.append([parent_info[1], parent_info[2]])

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

    if particle.ParentID == 1:
        print "  Primary"
        primaries += 1
    else:
        print "  First detector hit by final particle is {}".format(particle.MostUpstreamDetector)
        if particle.MostUpstreamDetector-1 in particle.ParentDetectors:
            particle_det = particle.Detectors[particle.MostUpstreamDetector]
            parent_det = particle.ParentDetectors[particle.MostUpstreamDetector-1][0]
            p1, p2 = LinesIntersect(numpy.array([particle_det.X, particle_det.Y+724, particle_det.Z]),
                                    numpy.array([particle_det.Px, particle_det.Py, particle_det.Pz]),
                                    numpy.array([parent_det.X, parent_det.Y+724, parent_det.Z]),
                                    numpy.array([parent_det.Px, parent_det.Py, parent_det.Pz]))
            separation = PointsDistance(p1, p2)
            print "  Final particle was made near points {} and {}".format(p1, p2)
            print "    (Separation distance {} mm)".format(separation)
            if separation < 10:
                for dim in range(3):
                    plume_init[dim][abs(last_parent_pdg)].append(p1[dim])

print primaries, "primaries"
print "Number of parents:", number_of_parents
print "PDG of last parent:", pdg_of_parent

fig = plt.figure(figsize=(10, 10))
plt.bar(number_of_parents.keys(), number_of_parents.values())
plt.xlabel("Number of ancestors", fontsize=18)
plt.savefig('./figs/number_of_parents.png')

fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(111)
pdg_pos = [i for i,_ in enumerate(pdg_of_parent.keys())]
plt.bar(pdg_pos, pdg_of_parent.values())
plt.xticks(pdg_pos, pdg_of_parent.keys(), fontsize=18)
plt.xlabel("PDG of parent", fontsize=18)
plt.savefig('./figs/pdg_of_parent.png')

fig = plt.figure(figsize=(10, 10))
plt.hist(momentum, bins=100, range=(0,30000))
plt.xlabel("Momentum (MeV)", fontsize=18)
plt.savefig('./figs/plume_momentum.png')

fig = plt.figure(figsize=(20, 5))
colors = {2212:'b', 211:'r', 321:'g', -1: 'black'}
plt.subplot2grid((2,1), (0,0), rowspan=1, colspan=1)
for pdg in [2212, 211, 321, -1]:
    plt.scatter(plume_init[2][pdg], plume_init[0][pdg], marker='o', color=colors[pdg])
plt.xlim(-100, 122600)
plt.ylim(-1000, 4000)
plt.ylabel('x [mm]')
plt.subplot2grid((2,1), (1,0), rowspan=1, colspan=1)
for pdg in [2212, 211, 321, -1]:
    plt.scatter(plume_init[2][pdg], plume_init[1][pdg], marker='o', color=colors[pdg])
plt.xlim(-100, 122600)
plt.ylim(-1000, 2000)
plt.xlabel('z [mm]')
plt.ylabel('y [mm]')
plt.savefig('./figs/plume_particle_init.png')

# f_gen_point = fig.add_subplot(111, projection='3d')
# for pdg in [2212, 211, 321, -1]:
#     f_gen_point.scatter(plume_init[2][pdg], plume_init[0][pdg], plume_init[1][pdg], marker='o', color=colors[pdg])
# f_gen_point.set_xlabel('z [mm]')
# f_gen_point.set_ylabel('x [mm]')
# f_gen_point.set_zlabel('y [mm]')
# plt.show()
