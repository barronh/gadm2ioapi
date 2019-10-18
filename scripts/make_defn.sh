#!/bin/bash

conda deactivate >& /dev/null
source /work/ROMO/anaconda3/bin/activate geo

ogrinfo -geom=no -dialect SQLite -sql "SELECT DISTINCT ID_0, NAME_0 FROM gadm36" gadm36.shp > defn/unique_0.txt
ogrinfo -geom=no -dialect SQLite -sql "SELECT DISTINCT ID_0, NAME_0, ID_1, NAME_1 FROM gadm36" gadm36.shp > defn/unique_1.txt
ogrinfo -geom=no -dialect SQLite -sql "SELECT DISTINCT ID_0, NAME_0, ID_1, NAME_1, ID_2, NAME_2 FROM gadm36" gadm36.shp > defn/unique_2.txt

python def2dict.py
