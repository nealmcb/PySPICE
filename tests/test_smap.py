#!/usr/bin/env python

import os
import sys
import spice
from collections import OrderedDict as OD
import unittest

class TestSMAP(unittest.TestCase):
  def setUp(self):
    ### Load default kernels
    mydir = os.path.dirname(__file__)
    self.kernels = [ os.path.join( mydir,i.strip()) for i in
      """
kernels/naif0010.tls
kernels/smap_v00.tf
kernels/pck00009.tpc
kernels/spk_drm239_WithBurn-full.bsp
kernels/SMAP_ref_150529_180529.bsp
###
### That last SMAP SPK kernel, or one like it, should be under this URL:
###
###   http://naif.jpl.nasa.gov/pub/naif/SMAP/kernels/spk/
###
###
      """.strip().split('\n') if i[0]!='#' ]
    for kernel in self.kernels: spice.furnsh( kernel )

  def tearDown(self):
    ### Unload any kernels
    for kernel in self.kernels: spice.unload( kernel )

  def test_smap(self):

    target = 'SMAP'

    et0 = spice.utc2et( '2016-01-01T12:00:00' )

    dpr = spice.dpr()
    spd = spice.spd()

    a,b,c = [spice.gdpool('BODY399_RADII',i,1)[1] for i in range(3)]

    ods = []

    for deltatime in [0.1 * i for i in range(601)]:
      stSmap,lsSmap = spice.spkezr( target, et0+deltatime, 'MYEARTH_FIXED', 'NONE', 'EARTH' )
      posn, veloc = stSmap[:3], stSmap[3:]
      mtx = spice.pxform( 'SMAP_REFLECTOR', 'MYEARTH_FIXED', et0+deltatime)
      boreEbf = spice.mxv( mtx, [1.0,0,0] )
      point = spice.surfpt( posn, boreEbf, a, b, c)
      radius,lon,lat = spice.reclat( point )
      utc = spice.et2utc( et0+deltatime, 'ISOC', 3 )
      ods += [ OD(deltatime=deltatime,posn=posn,veloc=veloc,boreEbf=boreEbf
                 ,utc=utc,point=point,radius=radius,lat=lat,lon=lon 
                 ,raynge=spice.vnorm(spice.vsub(point,posn))
                 )
             ]

    try:
      ### Moved matplotlib import to here so test runs to here at least
      from matplotlib import pyplot as plt
      plt.figure(1)
      keys = 'lat lon'.split()
      secs = [od['deltatime'] for od in ods]
      for idx in range(len(keys)):
        ordinate = [od[keys[idx]]*dpr for od in ods]
        plt.subplot( 221+idx )
        plt.plot( secs, ordinate )
        plt.plot( secs, ordinate, '.')
        plt.title( keys[idx] )
        plt.ylabel( '%s, deg' % (keys[idx],) )
        if idx>1: plt.xlabel( 'T-T0, s' )

      abscissa = [od['lon']*dpr for od in ods]
      ordinate = [od['lat']*dpr for od in ods]
      plt.subplot( 221+2 )
      plt.title( 'lon vs. lat' )
      plt.plot( abscissa, ordinate )
      plt.xlabel( 'lon, deg' )
      plt.ylabel( 'lat, deg' )
      plt.show()

    except:
      print( "Bypassed, or failed, matplotlib tests" )


if __name__=="__main__":
  unittest.main()
