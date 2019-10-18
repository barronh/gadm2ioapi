#!/work/ROMO/anaconda3/envs/dev/bin/python
import os
import json
import argparse
import numpy as np
import PseudoNetCDF as pnc

parser = argparse.ArgumentParser()
parser.add_argument('-O', '--clobber', default=False, action='store_true')
parser.add_argument('--fractional', default=False, action='store_true')
parser.add_argument('--variable', default=None)
parser.add_argument('definitions')
parser.add_argument('inpath')
parser.add_argument('outpath')
parser.epilog = """
cat << EOF > config.json
{
    "NorthAmerica": ["United States", "Canada", "Mexico"],
    "USA": ["United States"],
    "CAN": ["Canada"],
    "MEX": ["Mexico"]
}
EOF
./customregions.py customregions.json ioapi/gadm36_12US1.IOAPI.nc custom/gadm36_12US1_testcustomf.nc
./customregions.py --fractional customregions.json ioapi_frac/gadm36_4US1_12US1_ID_0.IOAPI.nc custom/gadm36_12US1_testcustomf.nc
"""
args = parser.parse_args()

if not args.clobber and os.path.exists(args.outpath):
    print(args.outpath + ' exits')
    exit()

def getfmask(fracf, vark, namelist):
    var = fracf.variables[vark]
    tf = fracf.variables['TFLAG'][:, 0, 0]
    i2k = eval(var.description)
    k2i = {k: i for i, k in i2k.items()}
    idlist = [k2i[k] for k in namelist if k in k2i]
    include = [ti for ti, t in enumerate(tf) if t in idlist]
    if len(include) == 0:
        print('No ids found')
        return fracf.eval('{} = np.ma.filled({}[:][[0]], 0) * 0'.format('NA', vark)).variables['NA']
    elif len(include) < len(namelist):
        print('Found some')

    tmpf = fracf.copy()
    del tmpf.variables['TFLAG']
    tmpf = fracf.subsetVariables([vark])
    tmpf = tmpf.slice(TSTEP=include)
    return np.ma.filled(tmpf.variables[vark], 0).sum(0, keepdims=True)
    
    
def getmask(idf, vark, namelist):
    var = idf.variables[vark]
    i2k = eval(var.description)
    k2i = {k: i for i, k in i2k.items()}
    idlist = [k2i[k] for k in namelist]
    outvar = np.in1d(var[:], idlist).reshape(var.shape)
    return outvar

gadmf = pnc.pncopen(args.inpath, format='ioapi')
if args.variable is None:
    for vark in ['ID_0', 'ID_1', 'ID_2']:
        if vark in gadmf.variables:
            args.variable = vark
            break
    else:
        print('Could not find variable ID_0, ID_1, ID_2')
        exit()

outf = gadmf.slice(TSTEP=0).subsetVariables([args.variable])
configd = json.load(open(args.definitions, mode='r', encoding='utf-8'))
for outvark, namelist in configd.items():
    outv = outf.createVariable(outvark, 'f', ('TSTEP', 'LAY', 'ROW', 'COL'))
    outv.units = '1'
    outv.long_name = outvark.ljust(16)
    outv.var_desc = outvark.ljust(80)
    if args.fractional:
        vals = getfmask(gadmf, args.variable, namelist)
    else:
        vals = getmask(gadmf, args.variable, namelist)
    outv[:] = vals

del outf.variables[args.variable]
delattr(outf, 'VAR-LIST')    
outf.updatemeta()
outf.save(args.outpath, format='NETCDF4_CLASSIC', complevel=1)
