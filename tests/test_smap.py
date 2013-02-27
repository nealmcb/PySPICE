#!/usr/bin/env python

import os
import sys
import math
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

    et0 = spice.utc2et( '2015-06-01T12:00:00' )

    dpr = spice.dpr()
    spd = spice.spd()
    twopi = spice.twopi()

    a,b,c = [spice.gdpool('BODY399_RADII',i,1)[1] for i in range(3)]

    ods = []

    for deltatime in [spd * i for i in range(1080)]:
      et = et0 + deltatime
      stSmap,lsSmap = spice.spkezr( target, et, 'IAU_EARTH', 'NONE', 'EARTH' )
      posn, veloc = stSmap[:3], stSmap[3:]
      stSun,lsSun = spice.spkezr( 'SUN', et0, 'IAU_EARTH', 'LT', 'EARTH' )
      mtx = spice.pxform( 'SMAP_REFLECTOR', 'IAU_EARTH', et)
      boreEbf = spice.mxv( mtx, [1.0,0,0] )
      point = spice.surfpt( posn, boreEbf, a, b, c)
      rsurfpt,lon,lat = spice.reclat( point )
      utc = spice.et2utc( et, 'ISOC', 3 )
      eccsum = 0.0
      asum = 0.0
      Psum = 0.0
      ct = 0.0
      for j in range(5400,-1,-540):
        rp,ecc,inc,lnode,argp,m0,t0,mu = spice.oscelt( spice.spkezr( target, et+j,'EARTH_SUN_ORBIT', 'NONE', 'EARTH')[0]
                                                   , et, 398600.4418
                                                   )
        a = rp / (1.0-ecc)
        P = twopi * math.sqrt( a*a*a / mu )
        eccsum += ecc
        asum += a
        Psum += P
        ct += 1.0

      ods += [ OD(deltatime=deltatime,posn=posn,veloc=veloc,boreEbf=boreEbf
                 ,utc=utc,point=point,rsurfpt=rsurfpt
                 ,rsmap=spice.vnorm(posn),lat=lat,lon=lon 
                 ,raynge=spice.vnorm(spice.vsub(point,posn))
                 ,sunsep=spice.vsep( spice.ucrss(posn,veloc), stSun[:3] )
                 ,rp=rp,ecc=ecc,inc=inc,lnode=lnode,argp=argp,m0=m0,t0=t0,mu=mu
                 ,a=a,P=P,eccmean=eccsum/ct,amean=asum/ct,Pmean=Psum/ct
                 )
             ]

    try:
      ### Moved matplotlib import to here so test runs to here at least
      from matplotlib import pyplot as plt
      plt.figure(1)
      keys = 'lnode inc argp'.split()
      secs = [od['deltatime'] for od in ods]
      for idx in range(len(keys)):
        scal = 1.0 if keys[idx] in 'rsurfpt rsmap raynge sunsep rp ecc t0 mu a P eccmean amean Pmean'.split() else dpr
        ordinate = [od[keys[idx]]*scal for od in ods]
        plt.subplot( 221+idx )
        plt.plot( secs, ordinate )
        ###plt.plot( secs, ordinate, '.')
        plt.title( keys[idx] )
        plt.ylabel( '%s, deg' % (keys[idx],) )
        if idx>1: plt.xlabel( 'T-T0, s' )

      abscissa = [od['lon']*dpr for od in ods]
      ordinate = [od['lat']*dpr for od in ods]
      plt.subplot( 221+idx+1 )
      plt.title( 'lon vs. lat' )
      plt.plot( abscissa, ordinate )
      plt.xlabel( 'lon, deg' )
      plt.ylabel( 'lat, deg' )
      plt.show()

    except:
      print( "Bypassed, or failed, matplotlib tests" )


if __name__=="__main__":
  unittest.main()
