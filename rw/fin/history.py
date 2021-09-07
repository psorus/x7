import os
import numpy as np

import sys

from simplestat import statinf
import json

import matplotlib.pyplot as plt


pwr=0
if len(sys.argv)>1:
    pwr=float(sys.argv[1])

cmax=100000
if len(sys.argv)>2:
    cmax=int(sys.argv[2])


fns=["results/"+zw+"/result.npz" for zw in os.listdir("results")[:1000]]
fns=[zw for zw in fns if os.path.isfile(zw)]

from sklearn.metrics import roc_auc_score as auc


fs=[np.load(fn,allow_pickle=True) for fn in fns]


y_true=fs[0]["y_true"]
y_scores=[f["y_score"] for f in fs]

y_scores=y_scores[:cmax]




y_scores=[np.sqrt(np.mean([(y_score)**2 for y_score in y_scores[:i]],axis=0)) for i in range(1,len(y_scores))]



#auc_score=auc(y_true,y_score)
aucs=[auc(y_true,y_score) for y_score in y_scores]

print(statinf(aucs))

max_auc=max(aucs)


#print("----------",auc_score)

plt.plot([max_auc-auc for auc in aucs])
plt.yscale("log",nonpositive="clip")
plt.savefig("history.png")
plt.show()



