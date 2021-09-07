import os
import numpy as np

addp=[]

if os.path.isfile("../contamination"):
    with open("../contamination","r") as f:
        addp.append(float(f.read().strip()))


addp=[str(zw) for zw in addp]

def lastsl(q):
    return q[q.rfind("/")+1:]

print(f"       {lastsl(os.getcwd())}:{' '.join(addp)}")
if os.path.isfile("ae/auc.npz"):
    print("        finished ae",end="")
    if os.path.isfile("ae/aucs.npz"):
        fae=np.load("ae/aucs.npz")
        print(f"        ae:{fae['m_auc']:.4f}+-{fae['s_auc']:.4f} oae:{fae['m_oauc']:.4f}+-{fae['s_oauc']:.4f}")
    
    else:
        fae=np.load("ae/auc.npz")
        print(f"        ae:{fae['auc']} oae:{fae['oauc']}")
if os.path.isdir("raw/results"):
    print(f"        Ran {len(os.listdir('raw/results'))} raw",end='')
    if os.path.isfile("raw/auc.npz") and os.path.isfile("raw/oauc.npz"):
        print(f"        raw:{np.load('raw/auc.npz')['auc']} oraw:{np.load('raw/oauc.npz')['auc']}")
    else:
        if os.path.isfile("raw/auc.npz"):
            print(f"        raw:{np.load('raw/auc.npz')['auc']}")
        if os.path.isfile("raw/oauc.npz"):
            print(f"        oraw:{np.load('raw/oauc.npz')['auc']}")
if os.path.isdir("fin/results"):
    print(f"        Ran {len(os.listdir('fin/results'))} fin",end='')
    if os.path.isfile("fin/auc.npz") and os.path.isfile("fin/oauc.npz"):
        print(f"        fin:{np.load('fin/auc.npz')['auc']} ofin:{np.load('fin/oauc.npz')['auc']}")
    else:
        if os.path.isfile("fin/auc.npz"):
            print(f"        fin:{np.load('fin/auc.npz')['auc']}")
        if os.path.isfile("fin/oauc.npz"):
            print(f"        ofin:{np.load('fin/oauc.npz')['auc']}")
if os.path.isdir("mfin/results"):
    print(f"        Ran {len(os.listdir('mfin/results'))} mfin",end='')
    if os.path.isfile("mfin/auc.npz") and os.path.isfile("mfin/oauc.npz"):
        print(f"        mfin:{np.load('mfin/auc.npz')['auc']} omfin:{np.load('mfin/oauc.npz')['auc']}")
    else:
        if os.path.isfile("mfin/auc.npz"):
            print(f"        mfin:{np.load('mfin/auc.npz')['auc']}")
        if os.path.isfile("mfin/oauc.npz"):
            print(f"        omfin:{np.load('mfin/oauc.npz')['auc']}")
