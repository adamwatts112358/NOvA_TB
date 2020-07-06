import matplotlib.pyplot as plt
import numpy as np
from os import listdir
import sys

class Particle:
    def __init__(self, pdg, x, y, z, px, py, pz):
        self.PDG = pdg
        self.X = x
        self.Y = y
        self.Z = z
        self.Px = px
        self.Py = py
        self.Pz = pz

class ParticleProperties:
    def __init__(self, pdg, mom_bin):
        self.PDG = pdg
        self.MomBin = mom_bin
    def __eq__(self, other):
        return self.PDG == other.PDG and self.MomBin == other.MomBin
    def __hash__(self):
        return hash((self.PDG, self.MomBin))

def MomentumBin(pz):
    if pz < 40000: return 0
    if pz < 80000: return 1
    else: return 2

def FormatPlot(plt, title, xlabel, ylabel, xmin, xmax, ymin, ymax, color, log, bgcolor):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(xmin, xmax)
    if log:
        plt.gca().set_yscale('log')
    plt.ylim(ymin, ymax)
    if color:
        plt.colorbar()
    plt.gca().set_facecolor(bgcolor)

def plotDet(det_name, filename, ymean, plotlim):

    print("Plotting detector {}".format(det_name))

    # set up containers
    x = {}
    y = {}
    z = {}
    px = {}
    py = {}
    pz = {}
    for pdg in [-1,2212,211,-211,13,-13]:
        for mombin in [-1,0,1,2]:
            x[ParticleProperties(pdg, mombin)] = []
            y[ParticleProperties(pdg, mombin)] = []
            z[ParticleProperties(pdg, mombin)] = []
            px[ParticleProperties(pdg, mombin)] = []
            py[ParticleProperties(pdg, mombin)] = []
            pz[ParticleProperties(pdg, mombin)] = []

    # read in the particles from the text files
    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith('#'):
                try:
                    line_split = line.split()
                    pdg_line = int(line_split[7])
                    pz_line = float(line_split[5])
                    for pdgIt in [-1, pdg_line]:
                        for momBinIt in [-1, MomentumBin(pz_line)]:
                            properties = ParticleProperties(pdgIt, momBinIt)
                            x[properties].append(float(line_split[0]))
                            y[properties].append(float(line_split[1]) - 724.8144) # remove target height
                            z[properties].append(float(line_split[2]))
                            px[properties].append(float(line_split[3]))
                            py[properties].append(float(line_split[4]))
                            pz[properties].append(pz_line)
                except:
                    pass

    # Plotting
    markersize = 8.0
    alpha = 0.85
    colormap = 'rainbow'
    mom_bins = 200
    bgcolor = '#FFFFFF' # '#e0e0eb' or '#F2F2F2'
    pdgLabels = {-1:'all',2212:'proton',211:'pi+',-211:'pi-',13:'mu-',-13:'mu+'}
    pdgColors = {-1:'#000000',2212:'#004C97',211:'#36573B',-211:'#78BE20',13:'#AF272F',-13:'#643335'}
    momBinLabels = {-1:'all',0:'<40 GeV',1:'40-80 GeV',2:'>80 GeV'}

    if det_name in [24,25,26]:
        xmean = -1374.4731770833332
    else:
        xmean = 0.0

    # Plot all particles together, color code by type
    fig = plt.figure(figsize=(20,14))
    plt.suptitle('Detector {}'.format(det_name),fontsize=16)
    for pdgIt,pdg in enumerate([-1,2212,211,-211,13,-13]):
        row = (pdgIt%2) * 3
        column = int(pdgIt/2) * 2
        plt.subplot2grid((6,6), (row,column), rowspan=2, colspan=2)
        plt.scatter(x[ParticleProperties(pdg, -1)],y[ParticleProperties(pdg, -1)],c=pz[ParticleProperties(pdg, -1)],
                    marker='o',s=markersize,lw=0,label=pdgLabels[pdg],alpha=alpha,cmap=colormap)
        FormatPlot(plt, '{}: {:.2e}'.format(pdgLabels[pdg], len(x[ParticleProperties(pdg, -1)])), 'x [mm]', 'y [mm]',
                   xmean-plotlim, xmean+plotlim, ymean-plotlim, ymean+plotlim, True, False, bgcolor)
        plt.subplot2grid((6,6), (row+2,column), rowspan=1, colspan=2)
        plt.hist(pz[ParticleProperties(pdg, -1)], bins=mom_bins, alpha=1.0, color=pdgColors[pdg])[0]
        FormatPlot(plt, '', 'Momentum [MeV/c]', '', 0, 120000, 0, 1E5, False, True, bgcolor)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig('./p_particles_{}.png'.format(det_name))
    plt.close()

    # Plot all particles, binned by momentum
    fig = plt.figure(figsize=(20,10))
    plt.suptitle('Detector {}'.format(det_name),fontsize=16)
    for pdgIt,pdg in enumerate([-1,2212,211,-211,13,-13]):
        for momBinIt,momBin in enumerate([0,1,2]):
            plt.subplot2grid((3,6), (momBinIt,pdgIt), rowspan=1, colspan=1)
            plt.scatter(x[ParticleProperties(pdg, momBin)],y[ParticleProperties(pdg, momBin)],c=pz[ParticleProperties(pdg, momBin)],
                        marker='o',s=markersize,lw=0,label='{} ({})'.format(pdgLabels[pdg], momBinLabels[momBin]),alpha=alpha,cmap=colormap)
            FormatPlot(plt, '{} ({}): {:.2e}'.format(pdgLabels[pdg], momBinLabels[momBin], len(pz[ParticleProperties(pdg, momBin)])),
                       'x [mm]', 'y [mm]', xmean-plotlim, xmean+plotlim, ymean-plotlim, ymean+plotlim, True, False, bgcolor)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig('./p_bin_particles_{}.png'.format(det_name))
    plt.close()


if len(sys.argv) != 2:
    print '''Example usage: python plot_detectors.py <path_to_files>
  Script expects path to input files to be passed as argument.
  These files are the text files produced from g4bl, named <det_number>_all.txt.'''
    exit(1)

y_array = np.asarray([147.5, 224.3, 299.6, 361.8, 414.8328, 414.8328, 472.745, 499.871, 515.417, 529.6234, 568.15, 568.15, 610.2096, 622.7064, 648.0048, 681.8376, 705.612, 720.5472, 724.8144, 724.8144, 724.8144, 724.8144, 724.8144, 724.8144, 724.8144, 724.8144])-724.8144
#plotlim_array = [2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E3,2.0E3,2.0E3,2.0E3,2.0E3]
plotlim_array = [2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E3,2.0E3,2.0E3,2.0E3,2.0E3,2.0E3,2.0E3]

for det_num in range(20,27):
    filename = '{}/{}_all.txt'.format(sys.argv[1], det_num)
    plotDet(det_num, '{}'.format(filename), y_array[det_num-1], plotlim_array[det_num-1])
