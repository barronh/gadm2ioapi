gadm36
------

Contains gridded IOAPI-compliant rasterized versions of the global
administrative boundaries as defined by the gadm project version 3.6.

`ioapi/gadm_<DOM>.IOAPI.nc`:
  files have a time-independent raster where each grid is assigned an
  ID derived from gadm `ID_<x>` fields
`ioapi_frac/gadm_4US1_<DOM>.ID_<x>.IOAPI.nc`:
  files have a raster files where each time is a single feature and the
  TFLAG YYYYJJJ identifies the `ID_<x>` values.

## Globally Unique IDS

gadm v 3.6 level 1 and level 2 IDs were not unique, only unique within
Level 0, which led to duplicate counties within the 12US1 domain. Some in
Canada, some in Mexico, some in US. 

To make the levels unique, I modified the codes:
 * `ID_0 = ID_0_orig * 10000`
 * `ID_1 = ID_0 + ID_1_orig`
 * `ID_2 = ID_0 + ID_2_orig`

This applies to `ioapi/gadm36_<DOM>.IOAPI.nc` files.

## Fractional 12US1 assignments

I also created a set of files using fractional area overlap. I started
with 4US1, created masks (0: off; 1: on), and averaged neighboring grid
cells (3, 3).  This will obviously be limited to 9ths of a 12k cell, but
it may be better than binary -- particularly for counties at 12k. For
example, there is at least one county whose maximum cell coverage is 1/9.

Each country/state/county present within the domain. There are 7 countries,
110 states, and 3690 counties.  I stored each as a separate TSTEP and the
YYYYJJJ is actually the ID. Definitely violates the JJJ part for `ID_0`.
Because I am using TSTEP to store separate shapes, it was best to store each
variable separately. 

This applies to `ioapi_frac/gadm36_4US1_<DOM>.ID_<x>.IOAPI.nc`

## Making Custom Regions

There is a script to make custom regions. `./customregions.py -h` will give
details.
