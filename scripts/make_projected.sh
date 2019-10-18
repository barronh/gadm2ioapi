#!/bin/bash

conda deactivate >& /dev/null
source /work/ROMO/anaconda3/bin/activate geo

for DOM in global_0.1 #12US1 12US2 4US1 HEMIS
do

OPTS="-lco ENCODING=UTF-8"
if [ ${DOM} == global_0.1 ]; then
  PROJ4="+proj=lonlat +lat_0=-90 +lon_0=-180 +no_defs"
  NX=3600
  NY=1800
  CLIP="-180 -90 180, 90"
  OPTS=" -wrapdateline ${OPTS}"
elif [ ${DOM} == 4US1 ]; then
  PROJ4="+proj=lcc +lat_1=33.0 +lat_2=45.0 +lat_0=40.0 +lon_0=-97.0 +y_0=1728000.0 +x_0=2556000.0 +a=6370000.0 +b=6370000.0 +to_meter=4000.0 +no_defs"
  NX=1377
  NY=897
  CLIP="-140 10 -40 60"
elif [ ${DOM} == 12US1 ]; then
  PROJ4="+proj=lcc +lat_1=33.0 +lat_2=45.0 +lat_0=40.0 +lon_0=-97.0 +y_0=1728000.0 +x_0=2556000.0 +a=6370000.0 +b=6370000.0 +to_meter=12000.0 +no_defs"
  NX=459
  NY=299
  CLIP="-140 10 -40 60"
elif [ ${DOM} == 12US2 ]; then
  PROJ4="+proj=lcc +lat_1=33.0 +lat_2=45.0 +lat_0=40.0 +lon_0=-97.0 +y_0=1620000.0 +x_0=2412000.0 +a=6370000.0 +b=6370000.0 +to_meter=12000.0 +no_defs"
  NX=396
  NY=246
  CLIP="-140 10 -40 60"
elif [ ${DOM} == HEMIS ]; then
  PROJ4="+proj=stere +lat_0=90.0 +lat_ts=45.0 +lon_0=-98.0 +y_0=10098000.0 +x_0=10098000.0 +a=6370000.0 +b=6370000.0 +to_meter=108000.0 +no_defs"
  NX=187
  NY=187
  CLIP="-180 -20 180 91"
  OPTS=" -wrapdateline ${OPTS}"
else
  echo "Unknown dom:" ${DOM}
  exit
fi
echo "Start ogr2ogr"
ogr2ogr -skipfailures -dim XY -clipsrc ${CLIP} ${OPTS} -t_srs "${PROJ4}" projected/gadm36_${DOM}.shp original/gadm36.shp
echo "End ogr2ogr"

for i in 0 1 2
do
echo "Start ${i}"

gdal_rasterize -of netCDF -at -a ID_${i}  -ts ${NX} ${NY} -te 0 0 ${NX} ${NY} -l gadm36_${DOM} projected/gadm36_${DOM}.shp projected/gadm36_${DOM}_ID_${i}.nc

echo "End ${i}"
done # i

done # DOM
