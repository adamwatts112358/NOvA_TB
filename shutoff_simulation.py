# shutoff_simulation.py
# Mike Wallbank <wallbank@fnal.gov> (University of Cincinnati), August 2020
#
# Simulate the shut-offs of the front-end boards

import sys
import ROOT
import random

class Particle:
#x y z Px Py Pz t PDGid EventID TrackID ParentID Weight
    def __init__(self, x, y, z, px, py, pz, t, pdg, eventid, trackid, parentid):
        self.X = x
        self.Y = y
        self.Z = z
        self.Px = px
        self.Py = py
        self.Pz = pz
        self.T = t
        self.PDG = pdg
        self.EventID = eventid
        self.TrackID = trackid
        self.ParentID = parentid

def LoadParticle(particles, particle):
    while particles[particle].startswith('#'):
        particle += 1
    particle_line = particles[particle].split()
    return Particle(float(particle_line[0]) + 1374.4731770833332,
                    float(particle_line[1]) - 724.8144,
                    float(particle_line[2]),
                    float(particle_line[3]),
                    float(particle_line[4]),
                    float(particle_line[5]),
                    float(particle_line[6]),
                    int(particle_line[7]),
                    int(particle_line[8]),
                    int(particle_line[9]),
                    int(particle_line[10])), particle

def GetFEBs(particle):
    febs = []
    if particle.X < 0 and particle.X > -1300:
        febs.append(0)
    if particle.X > 0 and particle.X < 1300:
        febs.append(1)
    if particle.Y > 0 and particle.Y < 1300:
        febs.append(2)
    if particle.Y < 0 and particle.Y > -1300:
        febs.append(3)
    return febs

# read in the particles from the text files
filename = '{}'.format(sys.argv[1])
with open(filename,'r') as f:
    all_particles = f.readlines()

# read in the spill structure
spillFile = ROOT.TFile("../../tb_commissioning/RateShutOffAna_1spill.root", "READ")
spillHist = spillFile.Get("rateshutoffana/Plane0Profile")

# start the 32 MHz clock
clock = 3
tick = 1./32e6

# DAQ re-enable
last_reenable = 0

# initiate all buffers
buffers = [0] * 4
feb_on = [True] * 4

# get the first particle
current_particle = 0
last_particle_time = 0

# save information about shut-offs
shut_off_times = [[]] * 4

# start the spill
while clock < 5:

    # re-enable DAQ
    if clock - last_reenable > 0.1:
        print "Reenabling at", clock
        print "Buffers:", buffers
        for feb in range(len(feb_on)):
            feb_on[feb] = True
        for feb in range(len(buffers)):
            buffers[feb] = 0
        last_reenable = clock

    # add the next particles
    #if clock - last_particle_time > 4.2/1e9:
    #if clock - last_particle_time > 4.2/2264500:
    num_new_particles = spillHist.GetBinContent(int(clock/tick)+1)
    additional_new_particles = random.randint(1,80)
    if additional_new_particles == 1: num_new_particles += 1
    new_particles = []
    while num_new_particles > 0:

        # next particle
        particle, current_particle = LoadParticle(all_particles, current_particle)
        new_particles.append(particle)

        # find any other particles from the same primary proton
        while current_particle+1 < len(all_particles) and \
                particle.EventID == LoadParticle(all_particles, current_particle+1)[0].EventID:
            new_particles.append(LoadParticle(all_particles, current_particle+1)[0])
            current_particle += 1

        # increment particle, if we run out look through again
        current_particle += 1
        if current_particle >= len(all_particles):
            current_particle = 0
        last_particle_time = clock

        num_new_particles -= 1

    # simulate hits
    for p in new_particles:
        febs = GetFEBs(p)
        for feb in febs:
            if feb_on[feb]:
                buffers[feb] += 140

    # check size of buffers
    for feb_buffer in range(len(buffers)):
        if buffers[feb_buffer] > 140000:
            print "FEB", feb_buffer, "shut off at time", clock
            shut_off_times[feb_buffer].append(clock)
            feb_on[feb_buffer] = False
            buffers[feb_buffer] = 0

    # drain buffer
    for feb_buffer in range(len(buffers)):
        if buffers[feb_buffer] > 0:
            buffers[feb_buffer] -= 1

    clock += tick

print "End of spill, shut-offs:", shut_off_times

# save on canvas
spillBinFile = ROOT.TFile("../../tb_commissioning/RateShutOffAna_1ms.root", "READ")
spillBinHist = spillBinFile.Get("rateshutoffana/HitProfile")
canv = ROOT.TCanvas("canv", "", 800, 600)
spillBinHist.SetLineColor(ROOT.kBlack)
spillBinHist.Draw("hist")
marker = ROOT.TMarker()
marker.SetMarkerStyle(29)
marker.SetMarkerSize(3)
for feb in range(len(shut_off_times)):
    marker.SetMarkerColor(feb+1)
    for shutoff in shut_off_times[feb]:
        marker.DrawMarker(shutoff*1e9, 0)
canv.SaveAs("figs/ShutOffSim.png")
