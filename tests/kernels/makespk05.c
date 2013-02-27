// Create SMAP SPK smap_test.c

// Requires LSK and smap_v00.tf with EARTH_SUN_ORBIT reference frame

// build command assumes this file is in PySPICE/tests/kernels/,
// and that ../../cspice/ has CSPICE

// gcc -I../../cspice/include makespk05.c ../../cspice/lib/cspice.a -lm -o makespk05

#include <stdio.h>
#include "SpiceUsr.h"

int
main() {
SpiceChar body[] = { "SMAP" };
SpiceDouble a = 7058.0;
SpiceDouble ecc = .0142;
SpiceDouble rp = a * (1.0 - ecc);
SpiceDouble inc = 0.0;
SpiceDouble lnode = 0.0;
SpiceDouble argp = 0.0;
SpiceDouble m0 = 0.0;
SpiceDouble mu = 398600.4418;
SpiceDouble gm = mu;
SpiceDouble elts[8] = { rp,ecc,inc,lnode,argp,m0,0.0,mu };
SpiceInt iBody;
SpiceInt iCenter;
SpiceInt n = 2;
SpiceChar frame[] = { "EARTH_SUN_ORBIT" };
SpiceChar segid[] = { "SMAP test SPK; requires EARTH_SUN_ORBIT" };
SpiceChar ifname[] = { "SMAP test SPK; requires frame EARTH_SUN_ORBIT (1420599)" };
SpiceChar filename[] = { "smap_test.bsp" };
SpiceInt handle;
SpiceBoolean found;
SpiceDouble epochs[2];
SpiceDouble *first = epochs;
SpiceDouble *last = epochs+1;
SpiceDouble states[2][6];

  furnsh_c( "naif0010.tls" );
  furnsh_c( "smap_v00.tf" );

  bodn2c_c(body,&iBody,&found);
  bodn2c_c("EARTH",&iCenter,&found);

  utc2et_c( "2015-01-01T12:00:00", first );
  utc2et_c( "2020-01-01T12:00:00", last );

  elts[6] = *first;

  conics_c( elts, *first, states[0]);
  conics_c( elts, *last, states[1]);

  spkopn_c( filename, ifname, 0, &handle );
  spkw05_c( handle, iBody, iCenter, frame, *first, *last, segid, gm, n, states, epochs );
  spkcls_c( handle );

  unload_c( "tests/kernels/naif00010.tls" );
  unload_c( "tests/kernels/smap_v00.tf" );
  return 0;
}
