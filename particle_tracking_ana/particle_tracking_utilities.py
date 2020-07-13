# particle_tracking_utilities.py
# Mike Wallbank, July 2020
#
# Common utility functions which may be used in
# analyzing simulated particle tracks

import numpy

def LinesIntersect(a1, l1, a2, l2):
    n = numpy.cross(l1, l2)
    n1 = numpy.cross(l1, n)
    n2 = numpy.cross(l2, n)

    p1 = numpy.dot((a2-a1),n2)/numpy.dot(l1,n2)
    p2 = numpy.dot((a1-a2),n1)/numpy.dot(l2,n1)

    point1 = a1 + (p1*l1)
    point2 = a2 + (p2*l2)

    return point1, point2

def PointsDistance(p1, p2):
    return numpy.linalg.norm(p1-p2)
