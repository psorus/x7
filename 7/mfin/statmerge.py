#merge with each same number of normal and abnormal events

import os
import numpy as np

import sys

from simplestat import statinf
import json

ple=30
quiet=False
if len(sys.argv)>1:
    try:
        ple=int(sys.argv[1])
    except:
        quiet=sys.argv[1]=="quiet"
pwr=0.0
cmax=100000
if len(sys.argv)>2:
    cmax=int(sys.argv[2])

if not os.path.isdir("results"):exit()

fns=["results/"+zw+"/result.npz" for zw in os.listdir("results")[:1000]]
fns=[zw for zw in fns if os.path.isfile(zw)]

from sklearn.metrics import roc_auc_score as auc


fs=[np.load(fn,allow_pickle=True) for fn in fns]


y_true=fs[0]["y_true"]
le=int(2*(len(y_true)-sum(y_true)))
y_true=y_true[:le]
y_scores=[f["y_score"][:le] for f in fs]

y_scores=y_scores[:cmax]


#aucs=[auc(y_true,y_score) for y_score in y_scores]
#if not quiet:print(json.dumps([[statinf(aucs)]],indent=2))


def aucbyscore(y_scores):

    y_score=np.sqrt(np.mean([(y_score)**2 for y_score in y_scores],axis=0))


    auc_score=auc(y_true,y_score)

    return auc_score

#if not quiet:print("----------",auc_score)


#np.savez_compressed("auc.npz",auc=auc_score,aucs=aucs,wids=wids)


def insteps(q,step=ple):
    dex=0
    while True:
        ac= q[dex:dex+step]
        if len(ac)!=step:break
        yield ac
        dex+=step
        if dex>len(q):
            break

print(aucbyscore(y_scores))
#print(aucbyscore(y_scores[:100]))
print([len(zw) for zw in insteps(y_scores)])


subs=[aucbyscore(zw) for zw in insteps(y_scores)]

print(subs)


print(json.dumps([[statinf(subs)]],indent=2))





