import matplotlib.pyplot as plt
import numpy as np
from os import listdir
import sys

def plotDet(name, ymean, plotlim):
    det_name = name.strip('_0.txt')
    print("Plotting detector {}".format(det_name))
    filename = './'+name
    pdgID = []
    x = []
    px = []
    y = []
    py = []
    pz = []
    with open(filename,'r') as f:
        lines = f.readlines()
        #for line in lines[2:]:
        for line in lines:
            if not line.startswith('#'):
                try:
                    x.append(float(line.split()[0]))
                    y.append(float(line.split()[1]))
                    px.append(float(line.split()[3]))
                    py.append(float(line.split()[4]))
                    pz.append(float(line.split()[5]))
                    pdgID.append(float(line.split()[7]))
                except:
                    pass
    
    # Remove the target height for y
    y = np.asarray(y)-724.8144
    
    proton_p = []
    protonx = []
    protony = []
    
    p_pion_p = []
    p_pionx = []
    p_piony = []
    
    n_pion_p = []
    n_pionx = []
    n_piony = []
    
    p_muon_p = []
    p_muonx = []
    p_muony = []
    
    n_muon_p = []
    n_muonx = []
    n_muony = []
    

    for i in range(len(pdgID)):
        if pdgID[i] == 2212.0:
            proton_p.append(pz[i])
            protonx.append(x[i])
            protony.append(y[i])
        elif pdgID[i] == 211.0:
            p_pion_p.append(pz[i])
            p_pionx.append(x[i])
            p_piony.append(y[i])
        elif pdgID[i] == -211.0:
            n_pion_p.append(pz[i])
            n_pionx.append(x[i])
            n_piony.append(y[i])
        elif pdgID[i] == 13.0:
            p_muon_p.append(pz[i])
            p_muonx.append(x[i])
            p_muony.append(y[i])
        elif pdgID[i] == -13.0:
            n_muon_p.append(pz[i])
            n_muonx.append(x[i])
            n_muony.append(y[i])
    
    # Plot all particles together, color code by type
    fig = plt.figure(figsize=(20,14))
    plt.suptitle('Detector {}'.format(name.strip('.txt')),fontsize=16)
    
    markersize = 8.0
    alpha = 0.85
    colormap = 'rainbow'
    mom_bins = 200
    bgcolor = '#FFFFFF' # '#e0e0eb' or '#F2F2F2'
    
    if '26' in det_name:
        xmean = -1374.4731770833332
    else:
        xmean = 0.0
    
    # Protons
    plt.subplot2grid((6,6), (0,0), rowspan=2, colspan=2)
    plt.title('protons: %.2e'%(len(protonx)))
    plt.scatter(protonx,protony,c=proton_p,marker='o',s=markersize,lw=0,label='protons',alpha=alpha,cmap=colormap)
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.xlim(xmean-plotlim, xmean+plotlim)
    plt.ylim(ymean-plotlim,ymean+plotlim)
    plt.colorbar()
    plt.gca().set_facecolor(bgcolor)
    plt.subplot2grid((6,6), (2,0), rowspan=1, colspan=2)
    plt.hist(proton_p, bins=mom_bins, alpha=1.0, color='#004C97')[0]
    plt.xlabel('Momentum [MeV/c]')
    plt.xlim(0,120000)
    plt.gca().set_yscale('log')
    plt.ylim(0,1E5)
    plt.gca().set_facecolor(bgcolor)
    
    # Pi+
    plt.subplot2grid((6,6), (0,2), rowspan=2, colspan=2)
    plt.title('pi+: %.2e'%(len(p_pionx)))
    plt.scatter(p_pionx,p_piony,c=p_pion_p,marker='o',s=markersize,lw=0,label='pi+',alpha=alpha,cmap=colormap)
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.xlim(xmean-plotlim, xmean+plotlim)
    plt.ylim(ymean-plotlim,ymean+plotlim)
    plt.colorbar()
    plt.gca().set_facecolor(bgcolor)
    plt.subplot2grid((6,6), (2,2), rowspan=1, colspan=2)
    plt.hist(p_pion_p, bins=mom_bins, alpha=1.0, color='#36573B')[0]
    plt.xlabel('Momentum [MeV/c]')
    plt.xlim(0,120000)
    plt.gca().set_yscale('log')
    plt.ylim(0,1E5)
    plt.gca().set_facecolor(bgcolor)

    # Pi-
    plt.subplot2grid((6,6), (3,2), rowspan=2, colspan=2)
    plt.title('p-: %.2e'%(len(n_pionx)))
    plt.scatter(n_pionx,n_piony,c=n_pion_p,marker='o',s=markersize,lw=0,label='pi-',alpha=alpha,cmap=colormap)
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.xlim(xmean-plotlim, xmean+plotlim)
    plt.ylim(ymean-plotlim,ymean+plotlim)
    plt.colorbar()
    plt.gca().set_facecolor(bgcolor)
    plt.subplot2grid((6,6), (5,2), rowspan=1, colspan=2)
    plt.hist(n_pion_p, bins=mom_bins, alpha=1.0, color='#78BE20')[0]
    plt.xlabel('Momentum [MeV/c]')
    plt.xlim(0,120000)
    plt.gca().set_yscale('log')
    plt.ylim(0,1E5)
    plt.gca().set_facecolor(bgcolor)

    # Mu+
    plt.subplot2grid((6,6), (0,4), rowspan=2, colspan=2)
    plt.title('mu+: %.2e'%(len(p_muonx)))
    plt.scatter(p_muonx,p_muony,c=p_muon_p,marker='o',s=markersize,lw=0,label='mu+',alpha=alpha,cmap=colormap)
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.xlim(xmean-plotlim, xmean+plotlim)
    plt.ylim(ymean-plotlim,ymean+plotlim)
    plt.colorbar()
    plt.gca().set_facecolor(bgcolor)
    plt.subplot2grid((6,6), (2,4), rowspan=1, colspan=2)
    plt.hist(p_muon_p, bins=mom_bins, alpha=1.0, color='#643335')[0]
    plt.xlabel('Momentum [MeV/c]')
    plt.xlim(0,120000)
    plt.gca().set_yscale('log')
    plt.ylim(0,1E5)
    plt.gca().set_facecolor(bgcolor)
    
    # Mu-
    plt.subplot2grid((6,6), (3,4), rowspan=2, colspan=2)
    plt.title('mu-: %.2e'%(len(p_muonx)))
    plt.scatter(n_muonx,n_muony,c=n_muon_p,marker='o',s=markersize,lw=0,label='mu-',alpha=alpha,cmap=colormap)
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.xlim(xmean-plotlim, xmean+plotlim)
    plt.ylim(ymean-plotlim,ymean+plotlim)
    plt.colorbar()
    plt.gca().set_facecolor(bgcolor)
    plt.subplot2grid((6,6), (5,4), rowspan=1, colspan=2)
    plt.hist(p_muon_p, bins=mom_bins, alpha=1.0, color='#AF272F')[0]
    plt.xlabel('Momentum [MeV/c]')
    plt.xlim(0,120000)
    plt.gca().set_yscale('log')
    plt.ylim(0,1E5)
    plt.gca().set_facecolor(bgcolor)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig('./p_particles_{}.png'.format(name.strip('.txt')))
    plt.close()
    
    protons = len(protonx)
    p_pions = len(p_pionx)
    n_pions = len(n_pionx)
    p_muons = len(p_muonx)
    n_muons = len(n_muonx)

protons_array = []
p_pions_array = []
n_pions_array = []
p_muons_array = []
n_muons_array = []

y_array = np.asarray([147.5, 224.3, 299.6, 361.8, 414.8328, 414.8328, 472.745, 499.871, 515.417, 529.6234, 568.15, 568.15, 610.2096, 622.7064, 648.0048, 681.8376, 705.612, 720.5472, 724.8144, 724.8144, 724.8144, 724.8144, 724.8144, 724.8144, 724.8144, 724.8144])-724.8144
plotlim_array = [2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E2,2.0E3,2.0E3,2.0E3,2.0E3,2.0E3,2.0E3]


for i in range(21,27):
    filename = '{}_0.txt'.format(i)
    plotDet('{}'.format(filename), y_array[i-1], plotlim_array[i-1])
