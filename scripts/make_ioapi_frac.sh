#!/bin/bash

INPATH=ioapi/gadm36_4US1.IOAPI.nc
for lvl in {1..3}
do
  OUTPATH=ioapi_frac/gadm36_4US1_12US1.ID_${lvl}.IOAPI.nc
  ./scripts/make_ioapi_frac.py ${INPATH} ID_${lvl} 12000 ${OUTPATH}
done

