#!/usr/bin/env python

import re
import os
import sys
import urllib
import pexpect

nl='\n'

def horizons(target):
  pe = pexpect.spawn('telnet horizons.jpl.nasa.gov 6775')
  ex = pe.expect
  sl = pe.sendline
  ex( 'Horizons>',timeout=3 )

  sl( 'PAGE' )
  rtn = ex( ['PAGING toggled OFF','PAGING toggled ON',pexpect.TIMEOUT], timeout=3)

  if rtn>0:
    sl( 'PAGE' )
    rtn = ex( ['PAGING toggled OFF','PAGING toggled ON',pexpect.TIMEOUT], timeout=3)

  if rtn == 2: return rtn,pe.before

  sl( target+nl )
  rtn = ex( ['\[S]PK', pexpect.TIMEOUT], timeout=3)
  if rtn > 0: return rtn,pe.before

  sl( 'SPK' )
  rtn = ex( ['e-mail address', pexpect.TIMEOUT], timeout=3)
  if rtn > 0: return rtn,pe.before

  sl( 'pexpect@python.org'+nl )
  rtn = ex( ['text transfer.*YES, NO,', pexpect.TIMEOUT], timeout=3)
  if rtn > 0: return rtn,pe.before

  sl( 'NO' )
  rtn = ex( ['START', pexpect.TIMEOUT], timeout=3)
  if rtn > 0: return rtn,pe.before

  sl( '2000-01-01' )
  rtn = ex( ['STOP', pexpect.TIMEOUT], timeout=3)
  if rtn > 0: return rtn,pe.before

  sl( '2020-01-01' )
  rtn = ex( ['Add more objects to file', pexpect.TIMEOUT], timeout=3)
  if rtn > 0: return rtn,pe.before

  sl( 'NO' )
  rtn = ex( [nl+' *Full path *:', pexpect.TIMEOUT], timeout=3)
  if rtn > 0: return rtn,pe.before

  rtn = ex( ['[\r\n]', pexpect.TIMEOUT], timeout=3)
  if rtn > 0: return rtn,pe.before

  url = pe.before.strip('\n\r ')

  rtn = ex( ['\n *Select ', pexpect.TIMEOUT], timeout=3)
  if rtn > 0: return -1,url

  sl( '' )
  rtn = ex( ['Horizons>', pexpect.TIMEOUT], timeout=3)
  if rtn > 0: return -2,url

  sl( 'quit' )
  rtn = ex( ['Connection closed', pexpect.TIMEOUT], timeout=3)
  if rtn > 0: return -3,url

  return rtn,url

def brief(fn):
  pe = pexpect.spawn( 'brief -n -t -c %s' % (fn,) )
  ex = pe.expect
  rtn = ex( ['\n-+ +-+ +-+\r*\n',pexpect.TIMEOUT], timeout=1)
  if rtn > 0: return 1,pe.before
  rtn = ex( [' w[.]r[.]t[.] ',pexpect.TIMEOUT], timeout=1)
  if rtn > 0: return 1,pe.before
  return int(pe.before),'SUCCESS'
  
def gomain(target):
  fn = '_'.join( re.split('[^-a-zA-Z0-9]',target) )+'_pexpect.bsp'
  spiceId = 0
  msgs = ['Horizons lookup FAILED'
         ,'SPK retrieval not attempted'
         ,'SPICE Body ID not attempted'
         ]

  try:

    r,url = horizons(target)

    if r>0:
      msgs[0] = 'Horizons lookup FAILED status=%d, URL=%s' % (r,url,)
    else:
      msgs[0] = 'Horizons lookup status=%d, URL=%s' % (r,url,)

      msgs[1] = 'SPK retrieval FAILED'
      msgs[1] = '### Retrieved SPK (URL=%s) as %s' % (url, urllib.urlretrieve(url,fn)[0],)

      msgs[2] = 'SPICE Body ID FAILED'
      spiceId,status = brief(fn)
      msgs[2] = '### Retrieved SPICEID %d; status=%s' % (spiceId,status,)

  except:
    pass

  return fn,spiceId,msgs

if __name__=="__main__":
  for itarget in sys.argv[1:]:
    itarget = itarget.strip()
    print( gomain(itarget) )
    
