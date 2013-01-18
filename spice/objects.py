# Released under the BSD license, see LICENSE for details

class DataType(object):
    """
    SPICE_* and * quantities must match enumeration _SpiceDataType from
      cspice/include/SpiceZdf.h
    """
    SPICE_CHR = 0
    SPICE_DP = 1
    SPICE_INT = 2
    SPICE_TIME = 3
    SPICE_BOOL = 4
    CHR = 0
    DP = 1
    INT = 2
    TIME = 3
    BOOL = 4
    def __init__(self):
        pass


class Cell(object):
    baseSize = 6
    minCharLen = 6
    def __init__(self, dtArg, szArg, lenArg=minCharLen):
        dtLcl = int(dtArg)
        lenLcl = 0
        if dtLcl==DataType.SPICE_CHR:
            lenLcl = int(lenArg)
            if lenLcl<Cell.minCharLen: lenLcl=Cell.minCharLen
            v = ' ' * (lenLcl-1)
        elif dtLcl==DataType.SPICE_DP: v = 0.0
        elif dtLcl==DataType.SPICE_INT: v = 0
        elif dtLcl==DataType.SPICE_TIME: v = 0.0
        elif dtLcl==DataType.SPICE_BOOL: v = True
        else: 
            raise TypeError, 'Invalid type:  %s' % (str(dtArg),)
        self.dtype = dtArg
        self.length = lenLcl
        self.size = szArg
        self.card = 0
        self.isSet = False
        self.adjust = False
        self.init = False
        self.base = [v,]*Cell.baseSize
        self.data = [v,]*szArg


class Ellipse(object):
    """Class representing the C struct SpiceEllipse"""
    def __init__(self, center=None, semi_major=None, semi_minor=None):
        self.center = center or [0.0] * 3
        self.semi_major = semi_major or [0.0] * 3
        self.semi_minor = semi_minor or [0.0] * 3

    def __repr__(self):
        return '<SpiceEllipse: center = %s, semi_major = %s, semi_minor = %s>' % \
            (self.center, self.semi_major, self.semi_minor)


# EK Attribute Description
class EkAttDsc(object):
    def __init__(self):
        self.cclass = 0
        self.dtype = DataType()
        self.strlen = 0
        self.size = 0
        self.indexd = False
        self.nullok = False

# EK Segment Summary
class EkSegSum(object):
    def __init__(self):
        self.tabnam = ''
        self.nrows = 0
        self.ncols = 0
        self.cnames = [] # list of strings
        self.cdescrs = [] # list of EkAttDsc


class Plane(object):
    def __init__(self, normal=[0.0]*3, constant=0.0):
        self.normal = normal
        self.constant = constant

    def __str__(self):
        return '<Plane: normal=%s; constant=%s>' % (', '.join([str(x) for x in self.normal]), self.constant)

