#!/work/ROMO/anaconda3/envs/dev/bin/python
import numpy as np
import PseudoNetCDF as pnc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inpath')
parser.add_argument('varkey', help='Variable to output')
parser.add_argument('newres', type=float)
parser.add_argument('outpath')

args = parser.parse_args()

inf = pnc.pncopen(args.inpath, format='ioapi')
old2new = int(round(args.newres // inf.XCELL, 0))
vark = args.varkey

i2k = eval(inf.variables[vark].description)
inVAR = inf.variables[vark]
inSHAPE = inVAR.shape
outSHAPE = [
    inSHAPE[0], inSHAPE[1],
    inSHAPE[2] // old2new, old2new,
    inSHAPE[3] // old2new, old2new
]
inID = inVAR[:].reshape(*outSHAPE)
uID = np.unique(np.array(inID))
uniquevals = sorted([k for k in i2k if k in uID])
i2k = {k: i2k[k] for k in uniquevals}
print(vark, len(i2k), flush=True)
lvlf = inf.subsetVariables([vark]).slice(
    ROW=slice(None, None, 3), COL=slice(None, None, 3)
).eval(
    '{0} = 1. * {0}[:].repeat({1}, 0)'.format(vark, len(i2k))
)
d = lvlf.createDimension('TSTEP', len(i2k))
d.setunlimited(True)
lvlf.XCELL = float(args.newres)
lvlf.YCELL = float(args.newres)
outID = lvlf.copyVariable(lvlf.variables[vark], key=vark, dtype='f')
tf = lvlf.copyVariable(lvlf.variables['TFLAG'], key='TFLAG')
outID.description = '{}'.format(i2k)
for ui, uv in enumerate(uniquevals):
    print(i2k[uv].encode('latin1'), flush=True)
    tmp = (inID[:] == uv).astype('f').filled(0).sum((3, 5)) / 9.
    outID[ui] = tmp[:]
    tf[ui, 0, 0] = uv
    tf[ui, 0, 1] = 0
    
lvlf.save(args.outpath, complevel=1, verbose=0)
