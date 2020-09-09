# sim_rates.py
# Mike Wallbank (University of Cincinnati) <wallbank@fnal.gov>, August 2020
#
# Analyze the rates of particles in the simulation

import sys
import matplotlib.pyplot as plt

infile = str(sys.argv[1])

# plotting
pz_plot = {}
locations = ['All', 'Tertiary', 'Plume', 'Punch-Through', 'East', 'West', 'Top', 'Bottom']
particles = [0,2212,211,-211,13,-13]
PDGName = {0:'all', 2212:'proton', 211:'pi+', -211:'pi-', 13:'mu-', -13:'mu+'}
for location in locations:
    for particle in particles:
        pz_plot[location+'_'+str(particle)] = []        

detwidth = 1300

# read in the particles from the input file
with open(infile,'r') as f:
    lines = f.readlines()
    for line in lines:
        if not line.startswith('#'):

            line_split = line.split()
            x = float(line_split[0]) + 1374.4731770833332 
            y = float(line_split[1]) - 724.8144
            pdg = int(line_split[7])
            pz = float(line_split[5])

            # collect both protons and antiprotons
            if pdg == -2212:
                pdg = 2212

            pz /= 1000

            if pdg not in particles:
                continue

            # only count things hitting the detector
            if x < -1*detwidth or x > detwidth or y < -1*detwidth or y > detwidth:
                continue

            # define properties of the hits
            east = False; west = False; top = False; bottom = False
            tertiary = False; plume = False; punchthrough = False
            if x < 0: east = True
            else: west = True
            if y > 0: top = True
            else: bottom = True

            if x < 100 and x > -100 and y < 100 and y > -100 and pz < 2:
                tertiary = True
            if x > 650 and y > 200 and y < 1000:
                plume = True
            if not tertiary and not plume:
                punchthrough = True

            # print "Particle at ({},{}) is East? {}, West? {}, Top? {}, Bottom? {}, Tertiary? {}, Plume? {}, Punch-Through? {}" \
            #     .format(x, y, east, west, top, bottom, tertiary, plume, punchthrough)

            # fill lists
            for pdgIt in [0, pdg]:
                pz_plot['All_'+str(pdgIt)].append(pz)
                if east: pz_plot['East_'+str(pdgIt)].append(pz)
                if west: pz_plot['West_'+str(pdgIt)].append(pz)
                if top: pz_plot['Top_'+str(pdgIt)].append(pz)
                if bottom: pz_plot['Bottom_'+str(pdgIt)].append(pz)
                if tertiary: pz_plot['Tertiary_'+str(pdgIt)].append(pz)
                if plume: pz_plot['Plume_'+str(pdgIt)].append(pz)
                if punchthrough: pz_plot['Punch-Through_'+str(pdgIt)].append(pz)

# Print numberzzz
print "Tertiary {}, Plume {}, Punch-Through {}" \
    .format(len(pz_plot['Tertiary_0']), len(pz_plot['Plume_0']), len(pz_plot['Punch-Through_0']))
print "East {}, West {}, Top {}, Bottom {}" \
    .format(len(pz_plot['East_0']), len(pz_plot['West_0']), len(pz_plot['Top_0']), len(pz_plot['Bottom_0']))
print "West/East {}".format(float(len(pz_plot['West_0']))/float(len(pz_plot['East_0'])))

# Plot momenta
fig, axs = plt.subplots(2, 4, figsize=(20,10))
for locationIt,location in enumerate(locations):
    ax = axs[locationIt%2, int(locationIt/2)]
    for particle in particles:
        #if particle == 0: continue
        key = location+'_'+str(particle)
        ax.hist(pz_plot[key], bins=100, histtype='step', label="{} ({})".format(PDGName[particle], len(pz_plot[key])))
        ax.set_xlabel('Momentum (GeV)')
    ax.legend(title=location)
fig.savefig('./figs/particle_rates.png')
