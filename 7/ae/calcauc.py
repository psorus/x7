import numpy as np
import sys

pref=""
if len(sys.argv)>1:
    pref=sys.argv[1]


with open("../dex","r") as f:
    dex=int(f.read())

try:
    f=np.load(f"output{pref}.npz")
except:
    exit()
x=f["x_test"]
y=f["y_test"]
t=f["t_test"]


d=np.mean((t-x)**2,axis=-1)

lab=(y!=dex).astype("int")


from sklearn.metrics import roc_auc_score as cauc

oauc=cauc(lab,d)

#print(oauc)


d0=d[np.where(lab==0)]
d1=d[np.where(lab==1)]

d1=d1[:len(d0)]

d=np.concatenate((d0,d1))
lab=np.concatenate((np.zeros(len(d0)),np.ones(len(d1))))

auc=cauc(lab,d)

#print(auc)


np.savez_compressed(f"auc{pref}",auc=auc,oauc=oauc)



