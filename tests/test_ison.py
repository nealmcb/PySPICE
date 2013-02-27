import spice
import unittest
"""
This file contains a SPICE text kernel which can be loaded
via

  spice.furnsh(__file__)

    C/2012 S1 (ISON)
Epoch 2012 Sept. 30.0 TT = JDT 2456200.5
T 2013 Nov. 28.83943 TT                                 MPC
q   0.0125206            (2000.0)            P               Q
z  -0.0001416      Peri.  345.49752     +0.31396150     +0.52149342
 +/-0.0000061      Node   295.75673     -0.75950095     -0.36349391
e   1.0000018      Incl.   61.75288     -0.56972491     +0.77195647
From 1418 observations 2011 Dec. 28-2013 Jan. 12, mean residual 0".4.

    C/2012 S1 (ISON)
Epoch 2013 Dec. 14.0 TT = JDT 2456640.5
T 2013 Nov. 28.78376 TT                                 MPC
q   0.0124445            (2000.0)            P               Q
z  -0.0001246      Peri.  345.56415     +0.31512453     +0.51249745
 +/-0.0000061      Node   295.65420     -0.75894756     -0.36925673
e   1.0000016      Incl.   62.39057     -0.56982026     +0.77523921
From 1418 observations 2011 Dec. 28-2013 Jan. 12, mean residual 0".4.
"""

class MPC_HELIOCENTRIC_ISON:
    """
VECTORS: Heliocentric vectors/AU
Obj           JD_TT               X               Y               Z               X'              Y'              Z'
CK12S010 2456313.5000000     -1.838621582     3.996888204     2.473535871     0.003679388    -0.008412821    -0.005747084
CK12S010 2456323.5000000     -1.801610451     3.912290279     2.415774077     0.003722922    -0.008506895    -0.005805299
CK12S010 2456333.5000000     -1.764154611     3.826732067     2.357418790     0.003768496    -0.008605253    -0.005866032

Convert to ( jdtt, (X,Y,Z), (Xdot,Ydot,Zdot), )
    """
    def __init__(self):
        self.jpv=[ ( 'JD %s TDT' % (jdtt,)
                 , ( spice.convrt(float(x),'AU','KM'), spice.convrt(float(y),'AU','KM'), spice.convrt(float(z),'AU','KM'), )
                 , ( spice.convrt(float(xdot),'AU','KM')/spice.spd(), spice.convrt(float(ydot),'AU','KM')/spice.spd(), spice.convrt(float(zdot),'AU','KM')/spice.spd(), )
                 , )
                 for nm,jdtt,x,y,z,xdot,ydot,zdot
                 in [ i.strip().split() for i in self.__doc__.split('\n') if i[:9]=='CK12S010 ' ]
                 ]


class MPC_ISON_C_2012_S1:
    """Minor Planet Center orbital elements for
       Comet C/2012 S1 (ISON) per MPC 2013-A85

    """
    def __init__(self):
        self.source  = 'MPC 2013-A85'
        self.qAU     = 0.0125206
        self.e       = 1.0000018
        self.InclDEG = 61.75288
        self.NodeDEG = 295.75673
        self.PeriDEG = 345.49752
        self.M0      = 0.0
        self.T0_TDT  = ('2013-11-28 00:00:00 TDT',0.83943)
        self.MuM3S2  = 1.32712440018e+20   ### km**3 s**-2

        #self.qAU     = 0.0124445
        #self.e       = 1.0000016
        #self.InclDEG = 62.39057
        #self.NodeDEG = 295.65420
        #self.PeriDEG = 345.56415
        #self.M0      = 0.0
        #self.T0_TDT  = ('2013-11-28 00:00:00 TDT',0.78376)
        #self.MuM3S2  = 1.32712440018e+20   ### km**3 s**-2


### Test routins that work with kernel pool variables
class TestConics(unittest.TestCase):
  def setUp(self):

    ### Load the kernel
    spice.furnsh( __file__ )

    ### Convert MPC constants to CONICS_C elements
    ison = MPC_ISON_C_2012_S1()
    self.rpKM     = spice.convrt( ison.qAU, 'AU', 'KM')
    self.ecc      = ison.e
    self.incRAD   = spice.convrt( ison.InclDEG, 'DEGREES', 'RADIANS')
    self.lnodeRAD = spice.convrt( ison.NodeDEG, 'DEGREES', 'RADIANS')
    self.argpRAD  = spice.convrt( ison.PeriDEG, 'DEGREES', 'RADIANS')
    self.m0RAD    = spice.convrt( ison.M0, 'DEGREES', 'RADIANS')
    self.t0       = spice.str2et( ison.T0_TDT[0] ) + spice.convrt( ison.T0_TDT[1], 'DAYS', 'SECONDS' )
    self.mu       = ison.MuM3S2 * 1e-9
    self.elts = ( self.rpKM, self.ecc, self.incRAD, self.lnodeRAD, self.argpRAD, self.m0RAD, self.t0, self.mu )

    self.ditime       = spice.utc2et( '2013-01-16 12:00:00' )

  def tearDown(self):
    ### Unload the kernel
    spice.unload( __file__ )

  ### Test conics and others
  def test_bodvXds(self):
    periState = spice.conics( self.elts, self.t0)
    self.assertAlmostEqual( spice.vnorm(periState[:3]), self.rpKM, places=11)
    helioIson = MPC_HELIOCENTRIC_ISON()
    for jdtt,pos,vel in helioIson.jpv:
      et = spice.str2et( jdtt )
      conicState = spice.conics( self.elts, et )
      print( conicState )
      print( pos+vel )
      self.assertAlmostEqual( spice.vdist(conicState[:3], pos), 0.0, places=3)


if __name__=="__main__":
  unittest.main()
"""
naif0010.tls - leapseconds through mid-2012

KPL/LSK


LEAPSECONDS KERNEL FILE
===========================================================================

Modifications:
--------------

2012, Jan. 5    NJB  Modified file to account for the leapsecond that
                     will occur on June 30, 2012.
                     
2008, Jul. 7    NJB  Modified file to account for the leapsecond that
                     will occur on December 31, 2008.
                     
2005, Aug. 3    NJB  Modified file to account for the leapsecond that
                     will occur on December 31, 2005.
                     
1998, Jul  17   WLT  Modified file to account for the leapsecond that
                     will occur on December 31, 1998.
                     
1997, Feb  22   WLT  Modified file to account for the leapsecond that
                     will occur on June 30, 1997.
                     
1995, Dec  14   KSZ  Corrected date of last leapsecond from 1-1-95
                     to 1-1-96.

1995, Oct  25   WLT  Modified file to account for the leapsecond that
                     will occur on Dec 31, 1995.

1994, Jun  16   WLT  Modified file to account for the leapsecond on
                     June 30, 1994.

1993, Feb. 22  CHA   Modified file to account for the leapsecond on
                     June 30, 1993.

1992, Mar. 6   HAN   Modified file to account for the leapsecond on
                     June 30, 1992.

1990, Oct. 8   HAN   Modified file to account for the leapsecond on 
                     Dec. 31, 1990.  


Explanation:
------------

The contents of this file are used by the routine DELTET to compute the 
time difference

[1]       DELTA_ET  =  ET - UTC                                         
          
the increment to be applied to UTC to give ET. 

The difference between UTC and TAI,

[2]       DELTA_AT  =  TAI - UTC

is always an integral number of seconds. The value of DELTA_AT was 10
seconds in January 1972, and increases by one each time a leap second
is declared. Combining [1] and [2] gives

[3]       DELTA_ET  =  ET - (TAI - DELTA_AT)

                    =  (ET - TAI) + DELTA_AT

The difference (ET - TAI) is periodic, and is given by

[4]       ET - TAI  =  DELTA_T_A  + K sin E 

where DELTA_T_A and K are constant, and E is the eccentric anomaly of the 
heliocentric orbit of the Earth-Moon barycenter. Equation [4], which ignores 
small-period fluctuations, is accurate to about 0.000030 seconds.

The eccentric anomaly E is given by 

[5]       E = M + EB sin M

where M is the mean anomaly, which in turn is given by 

[6]       M = M  +  M t
               0     1

where t is the number of ephemeris seconds past J2000.

Thus, in order to compute DELTA_ET, the following items are necessary.

          DELTA_TA
          K
          EB
          M0
          M1
          DELTA_AT      after each leap second.

The numbers, and the formulation, are taken from the following sources.

     1) Moyer, T.D., Transformation from Proper Time on Earth to 
        Coordinate Time in Solar System Barycentric Space-Time Frame
        of Reference, Parts 1 and 2, Celestial Mechanics 23 (1981),
        33-56 and 57-68.

     2) Moyer, T.D., Effects of Conversion to the J2000 Astronomical
        Reference System on Algorithms for Computing Time Differences
        and Clock Rates, JPL IOM 314.5--942, 1 October 1985.

The variable names used above are consistent with those used in the 
Astronomical Almanac.

\begindata

DELTET/DELTA_T_A       =   32.184
DELTET/K               =    1.657D-3
DELTET/EB              =    1.671D-2
DELTET/M               = (  6.239996D0   1.99096871D-7 )

DELTET/DELTA_AT        = ( 10,   @1972-JAN-1
                           11,   @1972-JUL-1     
                           12,   @1973-JAN-1     
                           13,   @1974-JAN-1     
                           14,   @1975-JAN-1          
                           15,   @1976-JAN-1          
                           16,   @1977-JAN-1          
                           17,   @1978-JAN-1          
                           18,   @1979-JAN-1          
                           19,   @1980-JAN-1          
                           20,   @1981-JUL-1          
                           21,   @1982-JUL-1          
                           22,   @1983-JUL-1          
                           23,   @1985-JUL-1          
                           24,   @1988-JAN-1 
                           25,   @1990-JAN-1
                           26,   @1991-JAN-1 
                           27,   @1992-JUL-1
                           28,   @1993-JUL-1
                           29,   @1994-JUL-1
                           30,   @1996-JAN-1 
                           31,   @1997-JUL-1
                           32,   @1999-JAN-1
                           33,   @2006-JAN-1
                           34,   @2009-JAN-1
                           35,   @2012-JUL-1 )

\begintext
"""
