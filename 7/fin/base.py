# -*- coding: utf-8 -*-
"""oneoff6 complexity times 5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dYfVLzOqaicSOWhzm1dJG1CpeXe7fZQj
"""


with open("../dex","r") as f:
    index=int(f.read().strip())

import sys
dex=0

if len(sys.argv)>1:
    dex=int(sys.argv[1])

pth=f"results/{dex}/"

import os
import shutil

if os.path.isdir(pth):
    shutil.rmtree(pth)

os.makedirs(pth, exist_ok=False)

log={}


import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.losses import mse
from tensorflow.keras.optimizers import Adam,SGD,RMSprop

import numpy as np
import matplotlib.pyplot as plt
import json


seed=dex

tf.random.set_seed(seed)
np.random.seed(seed)

def statinf(q):
  return {"shape":q.shape,"mean":np.mean(q),"std":np.std(q),"min":np.min(q),"max":np.max(q)}

from tensorflow.keras.datasets import mnist

#(x_train, y_train), (x_test, y_test) = mnist.load_data()
f=np.load("../ae/output.npz")
x_train,y_train,x_test,y_test=f["e_train"],f["y_train"],f["e_test"],f["y_test"]
seed=np.random.randint(10000000)
np.random.seed(seed)
x_train=x_train.transpose()
np.random.shuffle(x_train)
x_train=x_train.transpose()
np.random.seed(seed)
x_test=x_test.transpose()
np.random.shuffle(x_test)
x_test=x_test.transpose()


x_train=x_train[:,:128]
x_test=x_test[:,:128]
dim=int(x_train.shape[-1])
print(x_train.shape)
print(y_train.shape)
print(y_train[:100])

def normalise(q):
  ret=[]
  for aq in q:
    ret.append((aq-np.mean(aq))/255)#bild interresiertes normieres->egal das anders bei at
  qq=np.array(ret)
  return qq

def getdata(x,y,norm=True,normdex=7,n=1000):
  if norm:
    ids=np.where(y==normdex)
  else:
    ids=np.where(y!=normdex)
  qx=x[ids][:n]
  qy=np.reshape(qx,(int(qx.shape[0]),dim))
  return normalise(qy),qx

normdex=index
train,rawtrain=getdata(x_train,y_train,norm=True,normdex=normdex,n=600000)
at,rawat=getdata(x_test,y_test,norm=False,normdex=normdex,n=2000000)
t,rawt=getdata(x_test,y_test,norm=True,normdex=normdex,n=20000000)




print(statinf(t))
print(statinf(rawt))

#def getmodel(qc,q,reg=None,act="relu",mean=1.0,seed=None):
def getmodel(q,reg=None,act="relu",mean=1.0,seed=None):
  np.random.seed(seed)
  tf.random.set_seed(seed)
  #inn=Input(shape=(28,28,1))
  inn=Input(shape=(dim,))
  w=inn
  #w=inn
  #for a in qc:
  #  if a["typ"]=="conv":
  #    w=Conv2D(filters=a["newsize"],kernel_size=a["kernel"],activation=act)(w)
  #  if a["typ"]=="pool":
  #    w=MaxPooling2D((a["pool"],a["pool"]))(w)

  #w=Flatten()(w)
  for aq in q[1:]:
    w=Dense(aq,activation=act,use_bias=False,kernel_initializer=keras.initializers.TruncatedNormal(),kernel_regularizer=reg)(w)
  m=Model(inn,w,name="oneoff")
  zero=K.ones_like(w)*mean
  loss=mse(w,zero)
  loss=K.mean(loss)
  m.add_loss(loss)
  m.compile(Adam(lr=0.01))
  return m

def regulariser(q):
  qt=K.transpose(q)
  return K.mean(K.abs(K.dot(q,qt)-1))

l=[dim,dim,dim,dim]
#m=getmodel(l,reg=regulariser,act="relu")
mo=getmodel(l,reg=None,act="relu",mean=1.0,seed=seed)
mp=np.mean(mo.predict(t))
m=getmodel(l,reg=None,act="relu",mean=1.0,seed=seed)
print(m)

cb=[keras.callbacks.EarlyStopping(monitor='val_loss',patience=20,restore_best_weights=True),
                   keras.callbacks.TerminateOnNaN()]
cb.append(keras.callbacks.ModelCheckpoint(f"{pth}/model.tf", monitor='val_loss', verbose=1, save_best_only=True,save_weights_only=True))

m.summary()

mp=m.predict(t)
print(statinf(mp))
mop=mo.predict(t)
print(statinf(mop))

print(f"training on {t.shape}")
h=m.fit(train,None,
        epochs=500,
        batch_size=100,
        validation_split=0.25,
        verbose=1,
        callbacks=cb)

hist=h.history
plt.close()
for key in hist.keys():
  ac=hist[key][1:]
  plt.plot(np.arange(len(ac)),ac,label=key,alpha=0.8)
plt.legend()
plt.yscale("log",nonposy="clip")
plt.savefig(f"{pth}/history.png")
plt.close()

model=h.model
p=model.predict(t)
print(statinf(p))
print(np.corrcoef(np.transpose(p)))

plt.close()
pp=np.mean(p,axis=-1)
print(statinf(pp))

plt.hist(pp,bins=100,alpha=0.5)
plt.savefig(f"{pth}/hist_mean.png")
plt.close()
#plt.show()

plt.close()
pp2=p[0]
print(statinf(pp2))

plt.hist(pp2,bins=100,alpha=0.5)
plt.savefig(f"{pth}/hist_normal.png")
plt.close()

w=model.predict(at)
print(statinf(w))

plt.close()
ww=np.mean(w,axis=-1)
print(statinf(ww))

plt.hist(ww,bins=100,alpha=0.5)
plt.savefig(f"{pth}/hist_abnormal.png")
plt.close()

plt.close()

plt.hist(pp,bins=100,alpha=0.5,label="background")
plt.hist(ww,bins=100,alpha=0.5,label="signal")
plt.legend()
plt.yscale("log",nonposy="clip")
plt.savefig(f"{pth}/hist_both.png")
plt.close()

from sklearn.metrics import roc_auc_score as auc

pd=np.abs(pp-1)
wd=np.abs(ww-1)
y_score=np.concatenate((pd,wd))
y_true=np.concatenate((np.zeros_like(pp),np.ones_like(ww)))
print(statinf(y_score))
print(statinf(y_true))

auc_score=auc(y_true,y_score)
print(f"reached auc of {auc_score}")

log["auc"]={"delta1":auc_score}


plt.close()
plt.hist(pd,bins=100,alpha=0.5,label="background")
plt.hist(wd,bins=100,alpha=0.5,label="signal")
plt.legend()
plt.savefig(f"{pth}/hist_delta1.png")
plt.close()

m=np.mean(pp)
pd=np.abs(pp-m)
wd=np.abs(ww-m)
y_score=np.concatenate((pd,wd))
y_true=np.concatenate((np.zeros_like(pp),np.ones_like(ww)))
print(statinf(pd))
print(statinf(wd))
print(statinf(y_score))
print(statinf(y_true))

plt.close()
plt.hist(pd,bins=100,alpha=0.5,label="background")
plt.hist(wd,bins=100,alpha=0.5,label="signal")
plt.legend()
plt.savefig(f"{pth}/hist_deltam.png")
plt.close()

auc_score=auc(y_true,y_score)
print(f"reached auc of {auc_score}")
log["auc"]["deltam"]=auc_score


pdm=np.max(np.abs(p-m),axis=-1)
print(statinf(pd))

wdm=np.max(np.abs(w-m),axis=-1)
print(statinf(wd))

plt.close()
plt.hist(pdm,bins=100,alpha=0.5,label="background")
plt.hist(wdm,bins=100,alpha=0.5,label="signal")
plt.legend()
plt.yscale("log",nonposy="clip")
plt.xscale("log",nonposx="clip")
plt.savefig(f"{pth}/hist_maxdelta.png")
plt.close()

m=getmodel(l,reg=None,act="relu")
s=m.predict(t)
print(statinf(s))
print(statinf(pp))





np.savez_compressed(f"{pth}/result.npz",y_true=y_true,y_score=y_score)#,pd=pd,wd=wd,pdm=pdm,wdm=wdm,t=t,at=at,rawt=rawt,rawat=rawat,train=train,rawtrain=rawtrain)






with open(f"{pth}/log.csv","w") as f:
    f.write(json.dumps(log,indent=2))






