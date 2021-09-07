import numpy as np

f=np.load("result.npz")


for fil in f.files:
    print(f"{fil}: {f[fil]}")

