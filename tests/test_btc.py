import spice
import unittest
"""
This string contains a SPICE text kernel which can be loaded
via

  spice.furnsh(__file__)

\begindata

D = 10.0
I = ( 1, 2 )
C = ( 'abc', 'def', 'ghi' )

BODY399_VARS = ( 1000.0 2000.0 3000.0 )
BODY99_VARS = ( 1099.5 2099.25 3099.125, 4099.0625 )

\begintext
"""

### Test routines that work with kernel pool variables
class TestKernelPool(unittest.TestCase):
  def setUp(self):
    ### Variables for comparison
    self.Ddtp = ( 1, 'N', )
    self.Idtp = ( 2, 'N', )
    self.Cdtp = ( 3, 'C', )
    self.var399 = ( 3, ( 1000.0, 2000.0, 3000.0, ), )
    self.var99 = (4, ( 1099.5, 2099.25, 3099.125, 4099.0625, ), )

    ### Load the kernel
    spice.furnsh( __file__ )

    ### Load a private name/code pair
    spice.boddef( 'MYBOD', 99 )

  def tearDown(self):
    ### Unload the kernel
    spice.unload( __file__ )

  ### Test bodvcd and bodvrd
  def test_bodvXds(self):
    self.assertEqual( spice.bodvcd( 399, 'VARS', 10), self.var399 )
    self.assertEqual( spice.bodvcd( 99, 'VARS', 10), self.var99 )
    self.assertEqual( spice.bodvrd( 'earth', 'VARS', 10), self.var399 )
    self.assertEqual( spice.bodvrd( 'mybod', 'VARS', 10), self.var99 )

  ### Test dtpool
  def test_dtpool(self):
    self.assertEqual( spice.dtpool( 'D' ), self.Ddtp )
    self.assertEqual( spice.dtpool( 'I' ), self.Idtp )
    self.assertEqual( spice.dtpool( 'C' ), self.Cdtp )

  ### Test bodc2n, bodn2c, bods2c, bodc2s
  def test_bodX2Y(self):
    self.assertEqual( spice.bodc2n( 99, ), 'MYBOD' )
    self.assertEqual( spice.bodn2c( 'MYBOD', ), 99 )

    self.assertEqual( spice.bodc2s( -99, ), '-99' )
    self.assertEqual( spice.bods2c( '-99', ), -99 )
    self.assertEqual( spice.bods2c( '99', ), 99 )
    self.assertEqual( spice.bods2c( 'MYBOD', ), 99 )

    self.assertEqual( spice.bodc2n( 999, ), 'PLUTO' )
    self.assertEqual( spice.bodn2c( 'PLUTO', ), 999 )
    self.assertEqual( spice.bods2c( '999', ), 999 )
    self.assertEqual( spice.bods2c( 'PLUTO', ), 999 )


### Test routins that work with SpiceCell's
class TestSpiceCells(unittest.TestCase):

  def setUp(self):
    pass

  def test_cells(self):
    for typ,appnd,item in ((spice.DataType.CHR,spice.appndc,'63',)
                          ,(spice.DataType.INT,spice.appndi,-99,)
                          ,(spice.DataType.DP,spice.appndd,-99.0,)
                          ,):

      ### items will be [n,2n,3n,<empty>]
      ### comparison object, first three items
      cmp = [ item, item+item, item+item+item ]

      a=spice.copy(spice.Cell(typ,4),spice.Cell(typ,4))

      ### comparison object, last item
      cmp += a.data[-1:]

      ### pad with nulls for character cells
      if typ==spice.DataType.CHR:
        cmp = [ (i[:5]+('\x00'*6))[:6] for i in cmp ]

      ### Assign two items, set cardinality, append a third item
      a.data[0]=item
      a.data[1]=item+item
      a=spice.scard(2,a)
      a=appnd(item+item+item,a)

      ### Check structure contents
      self.assertEqual( a.dtype, typ )
      self.assertEqual( a.size, 4 )
      self.assertEqual( a.card, 3 )
      self.assertEqual( a.init, True )

      ### Length is minimum of 6 for char cells, else 0
      if typ==spice.DataType.CHR:
        self.assertEqual( a.length, 6 )
      else:
        self.assertEqual( a.length, 0 )

      ### Compare data
      self.assertEqual( a.data, cmp )


if __name__=="__main__":
  unittest.main()
