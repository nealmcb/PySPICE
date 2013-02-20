#!/usr/bin/env python

import os
import sys
import spice
import unittest
from matplotlib import pyplot as plt

class TestHorizons(unittest.TestCase):
  def setUp(self):
    ### Load default kernels
    mydir = os.path.dirname(__file__)
    self.kernels = [ os.path.join( mydir,i.strip()) for i in
      """
kernels/naif0010.tls
kernels/spk_drm239_WithBurn-full.bsp
      """.strip().split('\n') ]
    for kernel in self.kernels: spice.furnsh( kernel )

  def tearDown(self):
    ### Unload any kernels
    for kernel in self.kernels: spice.unload( kernel )

  def test_horizons(self):
    import horizons

    target = 'C/2013 S1'
    target = 'C/2011 L4'

    spkFilename,spiceId,status = horizons.gomain(target)

    spice.furnsh( spkFilename )
    self.kernels += [spkFilename]

    target_ = '_'.join( target.split() )

    et0 = spice.utc2et( '2013-01-10T12:00:00' )

    ls2au = spice.convrt( spice.clight(), 'KM', 'AU' )
    dpr = spice.dpr()
    spd = spice.spd()

    deltatime = None

    while deltatime is None or abs(deltatime) > 5e-7:
      stS2I,lsS2I = spice.spkgeo( spiceId, et0, 'J2000', 10 )
      posn, veloc = stS2I[:3], stS2I[3:]
      deltatime = - spice.vdot( posn, veloc ) / spice.vdot( veloc, veloc )
      et0 += deltatime


    valarrs = [ ]
    print( (deltatime,spice.et2utc(et0,'ISOC',3),) )

    deltatime = 1.0
    sixmonths = spice.pi() * 1e7

    while deltatime < sixmonths:
      for pmdet in (-deltatime,deltatime):
        et = et0 + pmdet
        utc = spice.et2utc(et,'ISOC',1)

        stD2I,lsD2I = spice.spkgeo( spiceId, et, 'J2000', -140)
        stI2S,lsI2S = spice.spkgeo( 10, et, 'J2000', spiceId )
        stD2S,lsD2S = spice.spkgeo( 10, et, 'J2000', -140 )

        rD2I, rI2S = [ ls * ls2au for ls in [lsD2I,lsI2S] ]
        aDIS, aSDI = [ ang * dpr for ang in 
                       [ spice.vsep( spice.vminus(stD2I[:3]), stI2S[:-3] )
                       , spice.vsep( stD2S[:3], stD2I[:-3] )
                       ]
                     ]
        valarrs += [ (et,pmdet,rD2I,rI2S,aDIS,aSDI,utc,) ]

      deltatime *= 1.2

    valarrs.sort()
    for valarr in valarrs:
      print( '%12.1f %9.3f %9.3f %7.2f %7.2f %s' % valarr[1:] )

    days = [i[1]/spd for i in valarrs]

    titles = [ i % (target_,) for i in """
    Range, %s-DI, AU
    Range, %s-Sun, AU
    Phase, DI-%s-Sun, deg
    Elongation, Sun-DI-%s, deg
    """.strip().split('\n')]

    plt.figure(1)
    for idx in range(len(titles)):
      ordinate = [i[idx+2] for i in valarrs]
      plt.subplot( 221+idx )
      plt.plot( days, ordinate )
      plt.plot( days, ordinate, '.')
      plt.title( titles[idx] )
      plt.ylabel( titles[idx] )
      if idx>1: plt.xlabel( 'T-Tperi, d' )

    plt.show()


if __name__=="__main__":
  unittest.main()
