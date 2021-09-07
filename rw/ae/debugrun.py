from mass import run
import numpy as np

for i in range(10):
    try:
        f=np.load(f"output{i}.npz")
    except:
        print("running",i)
        run(i)

