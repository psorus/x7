import numpy as np
import sys
pref=""
if len(sys.argv)>1:
    pref=sys.argv[1]

f=np.load(f"auc{pref}.npz")

for fil in f.files:
    print(f"{fil}:{f[fil]}")

