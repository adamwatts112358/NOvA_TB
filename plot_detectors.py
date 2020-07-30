import matplotlib.pyplot as plt
import matplotlib.patches as patches
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

def FormatPlot(plt, title, xlabel, ylabel, xmin, xmax, ymin, ymax, color, log, draw_face, bgcolor):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(xmin, xmax)
    if log:
        plt.gca().set_yscale('log')
    if ymin != -1 or ymax != -1:
        plt.ylim(ymin, ymax)
    if color:
        plt.colorbar()
    plt.gca().set_facecolor(bgcolor)
    if draw_face:
        if ymin == -1 and ymax == -1:
            if 'x' in xlabel: mean = -1374.47
            else: mean = 0
            plt.axvline(x=mean-1300, color='r')
            plt.axvline(x=mean+1300, color='r')
            plt.axvline(x=mean-200, color='black')
            plt.axvline(x=mean+200, color='black')
        else:
            nova_face = patches.Rectangle((-1374.47-1300,-1300),2600,2600,linewidth=3,edgecolor='r',facecolor='none')
            tertiary_spot = patches.Rectangle((-1374.47-100,-100),200,200,linewidth=3,edgecolor='black',facecolor='none')
            plt.gca().add_patch(nova_face)
            plt.gca().add_patch(tertiary_spot)

def PlotIntegral2D(x, y, pz, xmean, ymean, plotlim, tertiarylim, tertiarymom):
    plot_integral = sum(x[i] > xmean-plotlim and x[i] < xmean+plotlim \
                            and y[i] > ymean-plotlim and y[i] < ymean+plotlim for i in range(len(x)))
    tertiary_integral = sum(x[i] > xmean-tertiarylim and x[i] < xmean+tertiarylim \
                                and y[i] > ymean-tertiarylim and y[i] < ymean+tertiarylim for i in range(len(x)))
    tertiary_integral_mom = sum(x[i] > xmean-tertiarylim and x[i] < xmean+tertiarylim \
                                and y[i] > ymean-tertiarylim and y[i] < ymean+tertiarylim \
                                and pz[i] < tertiarymom for i in range(len(x)))
    return plot_integral, tertiary_integral, tertiary_integral_mom

def PlotIntegral1D(x, pz, xmean, plotlim, tertiarylim, tertiarymom):
    plot_integral = sum(x[i] > xmean-plotlim and x[i] < xmean+plotlim for i in range(len(x)))
    tertiary_integral = sum(x[i] > xmean-tertiarylim and x[i] < xmean+tertiarylim for i in range(len(x)))
    tertiary_integral_mom = sum(x[i] > xmean-tertiarylim and x[i] < xmean+tertiarylim \
                                    and pz[i] < tertiarymom for i in range(len(x)))
    return plot_integral, tertiary_integral, tertiary_integral_mom

def plotDet(det_num, filename, ymean, plotlim):

    print("Plotting detector {}".format(det_num))

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

                # get pdg and momentum for binning
                line_split = line.split()
                pdg_line = int(line_split[7])
                pz_line = float(line_split[5])

                # collect both protons and antiprotons
                if pdg_line == -2212:
                    pdg_line = 2212

                # save this particle in both the pdg and momentum bin (if it exists), and also in all
                for pdgIt in [-1, pdg_line]:
                    for momBinIt in [-1, MomentumBin(pz_line)]:
                        properties = ParticleProperties(pdgIt, momBinIt)
                        if properties not in x:
                            continue
                        x[properties].append(float(line_split[0]))
                        y[properties].append(float(line_split[1]) - 724.8144) # remove target height
                        z[properties].append(float(line_split[2]))
                        px[properties].append(float(line_split[3]))
                        py[properties].append(float(line_split[4]))
                        pz[properties].append(pz_line)

    # Plotting
    markersize = 8.0
    alpha = 0.85
    colormap = 'rainbow'
    mom_bins = 200
    density_bins = int((2*plotlim)/41)
    bgcolor = '#FFFFFF' # '#e0e0eb' or '#F2F2F2'
    pdgLabels = {-1:'all',2212:'proton',211:'pi+',-211:'pi-',13:'mu-',-13:'mu+'}
    pdgColors = {-1:'#000000',2212:'#004C97',211:'#36573B',-211:'#78BE20',13:'#AF272F',-13:'#643335'}
    momBinLabels = {-1:'all',0:'<40 GeV',1:'40-80 GeV',2:'>80 GeV'}

    if det_num in [24,25,26]:
        xmean = -1374.4731770833332
    else:
        xmean = 0.0

    # Plot particle momentum, color coded by type
    fig = plt.figure(figsize=(20,14))
    plt.suptitle('Detector {}'.format(det_num),fontsize=16)
    for pdgIt,pdg in enumerate([-1,2212,211,-211,13,-13]):
        row = (pdgIt%2) * 3
        column = int(pdgIt/2) * 2
        plot_integral,tertiary_integral,tmp = PlotIntegral2D(x[ParticleProperties(pdg, -1)],
                                                             y[ParticleProperties(pdg, -1)],
                                                             pz[ParticleProperties(pdg, -1)],
                                                             xmean, ymean, 1300, 100, 2000)
        plt.subplot2grid((6,6), (row,column), rowspan=2, colspan=2)
        plt.scatter(x[ParticleProperties(pdg, -1)],y[ParticleProperties(pdg, -1)],c=pz[ParticleProperties(pdg, -1)],
                    marker='o',s=markersize,lw=0,label=pdgLabels[pdg],alpha=alpha,cmap=colormap)
        FormatPlot(plt, '{}: {:.2e} ({} tertiary)'.format(pdgLabels[pdg], plot_integral, tertiary_integral), 'x [mm]', 'y [mm]',
                   xmean-plotlim, xmean+plotlim, ymean-plotlim, ymean+plotlim, True, False, det_num==26, bgcolor)
        plt.subplot2grid((6,6), (row+2,column), rowspan=1, colspan=2)
        plt.hist(pz[ParticleProperties(pdg, -1)], bins=mom_bins, alpha=1.0, color=pdgColors[pdg])[0]
        FormatPlot(plt, '', 'Momentum [MeV/c]', '', 0, 120000, 0, 1E5, False, True, False, bgcolor)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig('./figs/p_particles_{}.png'.format(det_num))
    plt.close()

    # Plot particle momentum, in bins of momentum
    fig = plt.figure(figsize=(20,10))
    plt.suptitle('Detector {}'.format(det_num),fontsize=16)
    for pdgIt,pdg in enumerate([-1,2212,211,-211,13,-13]):
        for momBinIt,momBin in enumerate([0,1,2]):
            plot_integral,tertiary_integral,tmp = PlotIntegral2D(x[ParticleProperties(pdg, momBin)],
                                                                 y[ParticleProperties(pdg, momBin)],
                                                                 pz[ParticleProperties(pdg, momBin)],
                                                                 xmean, ymean, 1300, 100, 2000)
            plt.subplot2grid((3,6), (momBinIt,pdgIt), rowspan=1, colspan=1)
            plt.scatter(x[ParticleProperties(pdg, momBin)],y[ParticleProperties(pdg, momBin)],c=pz[ParticleProperties(pdg, momBin)],
                        marker='o',s=markersize,lw=0,label='{} ({})'.format(pdgLabels[pdg], momBinLabels[momBin]),alpha=alpha,cmap=colormap)
            FormatPlot(plt, '{} ({}): {:.2e}\n({} tertiary)'.format(pdgLabels[pdg], momBinLabels[momBin], plot_integral, tertiary_integral),
                       'x [mm]', 'y [mm]', xmean-plotlim, xmean+plotlim, ymean-plotlim, ymean+plotlim, True, False, det_num==26, bgcolor)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig('./figs/p_bin_particles_{}.png'.format(det_num))
    plt.close()

    # Plots for just detector face
    if det_num != 26:
        return

    # Plot occupancy/hit density -- 2D
    fig = plt.figure(figsize=(20, 12))
    plt.suptitle('Detector {}'.format(det_num),fontsize=16)
    for pdgIt,pdg in enumerate([-1,2212,211,-211,13,-13]):
        plot_integral,tertiary_integral,tertiary_integral_mom \
            = PlotIntegral2D(x[ParticleProperties(pdg, -1)],
                             y[ParticleProperties(pdg, -1)],
                             pz[ParticleProperties(pdg, -1)],
                             xmean, ymean, 1300, 100, 2000)
        plt.subplot2grid((2,3), (pdgIt%2,int(pdgIt/2)), rowspan=1, colspan=1)
        plt.hist2d(x[ParticleProperties(pdg, -1)],y[ParticleProperties(pdg, -1)],
                   bins=(density_bins,density_bins), cmap=colormap,
                   range=[[xmean-plotlim, xmean+plotlim], [ymean-plotlim, ymean+plotlim]])
        FormatPlot(plt, '{}: {:.2e} (Tertiary: {} (all), {} (<2 GeV))' \
                       .format(pdgLabels[pdg], plot_integral, tertiary_integral, tertiary_integral_mom),
                   'x [mm]', 'y [mm]', xmean-plotlim, xmean+plotlim, ymean-plotlim, ymean+plotlim, True, False, True, bgcolor)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig('./figs/xy_2d_particles_{}.png'.format(det_num))
    plt.close()

    # Plot occupancy/hit density -- 1D
    fig = plt.figure(figsize=(20, 12))
    plt.suptitle('Detector {}'.format(det_num),fontsize=16)
    for pdgIt,pdg in enumerate([-1,2212,211,-211,13,-13]):
        plot_integral_x,tertiary_integral_x,tertiary_integral_mom_x \
            = PlotIntegral1D(x[ParticleProperties(pdg, -1)],
                             pz[ParticleProperties(pdg, -1)],
                             xmean, 1300, 100, 2000)
        plt.subplot2grid((4,3), (2*(pdgIt%2),int(pdgIt/2)), rowspan=1, colspan=1)
        plt.hist(x[ParticleProperties(pdg, -1)], bins=density_bins, range=[xmean-plotlim, xmean+plotlim])
        FormatPlot(plt, '{}: {:.2e} (Tertiary: {} (all), {} (<2 GeV))' \
                       .format(pdgLabels[pdg], plot_integral_x, tertiary_integral_x, tertiary_integral_mom_x),
                   'x [mm]', '', xmean-plotlim, xmean+plotlim, -1, -1, False, False, True, bgcolor)
        plot_integral_y,tertiary_integral_y,tertiary_integral_mom_y \
            = PlotIntegral1D(y[ParticleProperties(pdg, -1)],
                             pz[ParticleProperties(pdg, -1)],
                             xmean, 1300, 100, 2000)
        plt.subplot2grid((4,3), ((2*(pdgIt%2))+1,int(pdgIt/2)), rowspan=1, colspan=1)
        plt.hist(y[ParticleProperties(pdg, -1)], bins=density_bins, range=[ymean-plotlim, ymean+plotlim])
        FormatPlot(plt, '{}: {:.2e} (Tertiary: {} (all), {} (<2 GeV))' \
                       .format(pdgLabels[pdg], plot_integral_y, tertiary_integral_y, tertiary_integral_mom_y),
                   'y [mm]', '', ymean-plotlim, ymean+plotlim, -1, -1, False, False, True, bgcolor)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig('./figs/xy_1d_particles_{}.png'.format(det_num))
    plt.close()

    # Plot occupancy/hit density, binned by momentum
    fig = plt.figure(figsize=(20, 10))
    plt.suptitle('Detector {}'.format(det_num),fontsize=16)
    for pdgIt,pdg in enumerate([-1,2212,211,-211,13,-13]):
        for momBinIt,momBin in enumerate([0,1,2]):
            plot_integral,tertiary_integral,tmp = PlotIntegral2D(x[ParticleProperties(pdg, momBin)],
                                                                 y[ParticleProperties(pdg, momBin)],
                                                                 pz[ParticleProperties(pdg, momBin)],
                                                                 xmean, ymean, 1300, 100, 2000)
            plt.subplot2grid((3,6), (momBinIt,pdgIt), rowspan=1, colspan=1)
            plt.hist2d(x[ParticleProperties(pdg, momBin)],y[ParticleProperties(pdg, momBin)],
                       bins=(density_bins,density_bins), cmap=colormap,
                       range=[[xmean-plotlim, xmean+plotlim], [ymean-plotlim, ymean+plotlim]])
            FormatPlot(plt, '{} ({}): {:.2e}\n({} tertiary)' \
                .format(pdgLabels[pdg], momBinLabels[momBin], plot_integral, tertiary_integral),
                       'x [mm]', 'y [mm]', xmean-plotlim, xmean+plotlim, ymean-plotlim, ymean+plotlim, True, False, True, bgcolor)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig('./figs/xy_bin_particles_{}.png'.format(det_num))
    plt.close()


if len(sys.argv) != 2:
    print '''Example usage: python plot_detectors.py <path_to_files>
  Script expects path to input files to be passed as argument.
  These files are the text files produced from g4bl, named <det_number>_all.txt.'''
    exit(1)

y_array = np.asarray([147.5, 224.3, 299.6, 361.8, 414.8328, 414.8328, 472.745, 499.871, 515.417, 529.6234, 568.15, 568.15, 610.2096, 622.7064, 648.0048, 681.8376, 705.612, 720.5472, 724.8144, 724.8144, 724.8144, 724.8144, 724.8144, 724.8144, 724.8144, 724.8144])-724.8144
#plotlim_array = [2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E3,2.0E3,2.0E3,2.0E3,2.0E3]
plotlim_array = [2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E3,2.0E3,2.0E3,2.0E3,2.0E3,2.0E3,2.0E3]

for det_num in range(26,27):
    filename = '{}/{}_all.txt'.format(sys.argv[1], det_num)
    plotDet(det_num, '{}'.format(filename), y_array[det_num-1], plotlim_array[det_num-1])
