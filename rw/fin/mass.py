import os
import time

with open("../rounds","r") as f:
    rounds=int(f.read().strip())

for i in range(0,rounds):
#for i in range(124,rounds):
    os.system(f"python3 base.py {i}")
    time.sleep(1)

