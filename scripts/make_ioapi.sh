#!/bin/bash

conda deactivate >& /dev/null
source /work/ROMO/anaconda3/bin/activate dev >& /dev/null

for DOM in 12US1 4US1 12US2 HEMIS
do
python -c "
import PseudoNetCDF as pnc
import json

inf0 = pnc.pncopen('projected/gadm36_${DOM}_ID_0.nc', format='netcdf')
inf1 = pnc.pncopen('projected/gadm36_${DOM}_ID_1.nc', format='netcdf')
inf2 = pnc.pncopen('projected/gadm36_${DOM}_ID_2.nc', format='netcdf')
tmpf = pnc.pncopen('GRIDDESC', format='griddesc', GDNAM='${DOM}')
tmpf.SDATE = 2019001
tmpf.STIME = 0
outf = tmpf.copy()
DUMMY = outf.variables['DUMMY']
DUMMY.missing_value = -999
for n in [0, 1, 2]:
    id = 'ID_{}'.format(n)
    var = outf.copyVariable(
        DUMMY, key=id, dtype='i',
    )
    var.long_name=id.ljust(16)
    var.var_desc=id.ljust(80)
    i2k = json.load(open('defn/defn_{}.txt'.format(n), encoding='latin1'))
    i2k = {int(i): k for i, k in i2k.items()}
    var.description = '{}'.format(i2k)

del outf.variables['DUMMY']
ID_0 = outf.variables['ID_0']
ID_1 = outf.variables['ID_1']
ID_2 = outf.variables['ID_2']
ID_0[:] = inf0.variables['Band1'][:] * 10000
ID_1[:] = ID_0[:] + inf1.variables['Band1'][:]
ID_2[:] = ID_0[:] + inf2.variables['Band1'][:]
outf.NVARS = 3
setattr(
    outf, 'VAR-LIST',
    ''.join([
        i.ljust(16) for i in ['ID_0', 'ID_1', 'ID_2']
    ])
)
outf.HISTORY = 'Made from gadm36'
outf.save('ioapi/gadm36_${DOM}.IOAPI.nc', verbose=0, complevel=1)
"
done
