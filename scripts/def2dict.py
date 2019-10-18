import numpy as np
import json


txt = open('defn/unique_2.txt', 'r', encoding='latin1').read()
lines = txt.split('\n')
lines = [l for l in lines if l.startswith(' ') and ('ID' in l or 'NAME' in l)]
lines = [l[19:] for l in lines]
lines = np.char.strip(np.array(lines).reshape(-1, 3, 2))
lines = np.char.replace(lines, '(null)', '-999')
idx = lines[:, :, 0].astype('i')
name = lines[:, :, 1]
max0, max1, max2 = idx.max(0)
mul2 = np.int32(10**np.ceil(np.log10(max2)))
mul1 = np.int32(10**np.ceil(np.log10(max1)))
level0id = idx[:, 0] * max(mul1, mul2)
level0name = name[:, 0]
level1id = level0id + idx[:, 1]
level1name = np.char.add(
    np.char.add(level0name, ', '),
    name[:, 1]
)
level2id = level0id + idx[:, 2]
level2name = np.char.add(
    np.char.add(level1name, ', '),
    name[:, 2]
)
level0dict = dict([(int(i), n) for i, n in zip(level0id, level0name)])
level1dict = dict([(int(i), n) for i, n in zip(level1id, level1name)])
level2dict = dict([(int(i), n) for i, n in zip(level2id, level2name)])
json.dump(level0dict, open('defn/defn_0.txt', 'w'), indent=4)
json.dump(level1dict, open('defn/defn_1.txt', 'w'), indent=4)
json.dump(level2dict, open('defn/defn_2.txt', 'w'), indent=4)
