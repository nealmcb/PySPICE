SMAP NAIF IDs and Frames

History at end

\begindata

NAIF_BODY_NAME += ( 'SMAP'                    )
NAIF_BODY_CODE += (  -205                     )

NAIF_BODY_NAME += ( 'SMAP_BUS'                )
NAIF_BODY_CODE += (  1420500                  )

NAIF_BODY_NAME += ( 'SMAP_REFLECTOR_BASE'     )
NAIF_BODY_CODE += (  1420510                  )

NAIF_BODY_NAME += ( 'SMAP_FEFLECTOR_ROTATING' )
NAIF_BODY_CODE += (  1420511                  )

NAIF_BODY_NAME += ( 'SMAP_FEFLECTOR'          )
NAIF_BODY_CODE += (  1420512                  )
\begintext

SMAP Spacecraft bus frame:  dynamic (Class 5) two-vector TK frame

    Primary: +X to earth nadir
  Secondary: +Z near direction to Sun

\begindata
 
FRAME_SMAP_BUS              =  1420500
FRAME_1420500_NAME          = 'SMAP_BUS'
FRAME_1420500_CLASS         =  5
FRAME_1420500_CENTER        = -205
FRAME_1420500_CLASS_ID      =  1420500

FRAME_1420500_RELATIVE       =  'J2000'
FRAME_1420500_DEF_STYLE      =  'PARAMETERIZED'
FRAME_1420500_FAMILY         =  'TWO-VECTOR'

FRAME_1420500_PRI_AXIS       = '+X'
FRAME_1420500_PRI_VECTOR_DEF = 'OBSERVER_TARGET_POSITION'
FRAME_1420500_PRI_OBSERVER   = -205
FRAME_1420500_PRI_TARGET     = 399
FRAME_1420500_PRI_ABCORR     = 'NONE'

FRAME_1420500_SEC_AXIS       = '+Z'
FRAME_1420500_SEC_VECTOR_DEF = 'OBSERVER_TARGET_POSITION'
FRAME_1420500_SEC_OBSERVER   = -205
FRAME_1420500_SEC_TARGET     = 10
FRAME_1420500_SEC_ABCORR     = 'NONE'
 
\begintext

SMAP Reflector base frame:  static (Class 4) TK frame

  Expresses instrument base alignment wrt S/C bus:  initially aligned

\begindata
 
FRAME_SMAP_REFLECTOR_BASE    =  1420510
FRAME_1420510_NAME           = 'SMAP_REFLECTOR_BASE'
FRAME_1420510_CLASS          =  4
FRAME_1420510_CENTER         = -205
FRAME_1420510_CLASS_ID       =  1420510

TKFRAME_1420510_SPEC         =  'MATRIX'
TKFRAME_1420510_RELATIVE     =  'SMAP_BUS'
TKFRAME_1420510_MATRIX       =  ( 1.0 0.0 0.0
                                  0.0 1.0 0.0
                                  0.0 0.0 1.0 )
 
\begintext

SMAP Reflector rotating frame:  dynamic (Class 5) Euler frame

  Rotates around nominal Nadir at 14.6 rpm = 87.6 deg/s

\begindata
 
FRAME_SMAP_REFLECTOR_ROTATING =  1420511
FRAME_1420511_NAME            = 'SMAP_REFLECTOR_ROTATING'
FRAME_1420511_CLASS           =  5
FRAME_1420511_CENTER          = -205
FRAME_1420511_CLASS_ID        =  1420511

FRAME_1420511_RELATIVE        =  'SMAP_REFLECTOR_BASE'
FRAME_1420511_DEF_STYLE       =  'PARAMETERIZED'
FRAME_1420511_FAMILY          =  'EULER'

FRAME_1420511_EPOCH           = @2015-JAN-01/12:00:00
FRAME_1420511_AXES            = ( 1 3 1 )
FRAME_1420511_UNITS           = 'DEGREES'
FRAME_1420511_ANGLE_1_COEFFS  = ( 0.0 87.6 )
FRAME_1420511_ANGLE_2_COEFFS  = ( 0.0 0.0 )
FRAME_1420511_ANGLE_3_COEFFS  = ( 0.0 0.0 )
 
\begintext

SMAP Reflector:  static (Class 4) TK frame

  SMAP_REFLECTOR_ROTATING rotated 40deg around +Y
  => nominal +X (boresight) is 40deg off-nadir

\begindata
 
FRAME_SMAP_REFLECTOR          =  1420512
FRAME_1420512_NAME            = 'SMAP_REFLECTOR'
FRAME_1420512_CLASS           =  4
FRAME_1420512_CENTER          = -205
FRAME_1420512_CLASS_ID        =  1420512

TKFRAME_1420512_RELATIVE      =  'SMAP_REFLECTOR_ROTATING'
TKFRAME_1420512_SPEC          = 'ANGLES'
TKFRAME_1420512_UNITS         = 'DEGREES'
TKFRAME_1420512_ANGLES        =  ( 50.0  0.0  0.0 )
TKFRAME_1420512_AXES          =  ( 2     1    2   )

\begintext

\begindata
 
FRAME_MYEARTH_FIXED  =  399
FRAME_399_NAME       = 'MYEARTH_FIXED'
FRAME_399_CLASS      =  2
FRAME_399_CLASS_ID   =  399
FRAME_399_CENTER     =  399
 
OBJECT_EARTH_FRAME   = 'MYEARTH_FIXED'
OBJECT_399_FRAME     = 'MYEARTH_FIXED'
 
\begintext

BTCarcich
2013-02
Initial version for testing
