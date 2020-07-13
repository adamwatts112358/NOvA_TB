# particle_structures.py
# Mike Wallbank, July 2020
#
# Define some custom structures to hold information about particle flow in the simulation

class ParticleID:
    def __init__(self, eventid, trackid):
        self.EventID = eventid
        self.TrackID = trackid
    def __eq__(self, other):
        return self.EventID == other.EventID and self.TrackID == other.TrackID
    def __hash__(self):
        return hash((self.EventID, self.TrackID))
    def Print(self):
        print "Event ID {}, Track ID {}".format(self.EventID, self.TrackID)

class Particle:
    def __init__(self, eventid, trackid, pdg, x, y, z, px, py, pz, parentid):
        self.EventID = eventid
        self.TrackID = trackid
        self.PDG = pdg
        self.X = x
        self.Y = y
        self.Z = z
        self.Px = px
        self.Py = py
        self.Pz = pz
        self.ParentID = parentid
    def Print(self):
        print "Event {}, particle {} (PDG {}) at ({}, {}, {}) with momentum ({}, {}, {}) and parent {}" \
            .format(self.EventID, self.TrackID, self.PDG, self.X, self.Y, self.Z, self.Px, self.Py, self.Pz, self.ParentID)

class DetectorHit:
    def __init__(self, detector, x, y, z, px, py, pz):
        self.Detector = detector
        self.X = x
        self.Y = y
        self.Z = z
        self.Px = px
        self.Py = py
        self.Pz = pz

class ParticleFlow:
    def __init__(self, eventid, trackid, pdg, parentid):
        self.EventID = eventid
        self.TrackID = trackid
        self.PDG = pdg
        self.ParentID = parentid
        self.Detectors = {}
        self.ParentDetectors = {}
        self.DaughterDetectors = {}
        self.MostUpstreamDetector = 1e6
    def AddDetector(self, detector):
        self.Detectors[detector.Detector] = detector
        if detector.Detector < self.MostUpstreamDetector:
            self.MostUpstreamDetector = detector.Detector
    def AddParentDetector(self, detector, trackid, pdg):
        self.ParentDetectors[detector.Detector] = [detector, trackid, pdg]
    def AddDaughterDetector(self, detector, trackid, pdg):
        self.DaughterDetectors[detector.Detector] = [detector, trackid, pdg]
    def PrintBasic(self):
        print "Event ID {}, Track ID {} ({})".format(self.EventID, self.TrackID, self.PDG)
