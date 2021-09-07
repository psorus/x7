# -*- coding: utf-8 -*-
"""oneoff6 complexity times 5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dYfVLzOqaicSOWhzm1dJG1CpeXe7fZQj
"""

import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.losses import mse
from tensorflow.keras.optimizers import Adam,SGD,RMSprop

import numpy as np
import matplotlib.pyplot as plt

def statinf(q):
  return {"shape":q.shape,"mean":np.mean(q),"std":np.std(q),"min":np.min(q),"max":np.max(q)}

from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(x_train.shape)
print(y_train.shape)
print(y_train[:100])

def normalise(q):
  ret=[]
  for aq in q:
    ret.append((aq-np.mean(aq))/255)
  qq=np.array(ret)
  return qq

def getdata(norm=True,normdex=7,n=1000):
  if norm:
    ids=np.where(y_train==normdex)
  else:
    ids=np.where(y_train!=normdex)
  qx=x_train[ids][:n]
  qy=np.reshape(qx,(int(qx.shape[0]),28*28))
  return normalise(qy),qx

normdex=7
t,rawt=getdata(norm=True,normdex=normdex,n=5000)
at,rawat=getdata(norm=False,normdex=normdex,n=5000)

print(statinf(t))
print(statinf(rawt))

#def getmodel(qc,q,reg=None,act="relu",mean=1.0,seed=None):
def getmodel(q,reg=None,act="relu",mean=1.0,seed=None):
  np.random.seed(seed)
  tf.random.set_seed(seed)
  #inn=Input(shape=(28,28,1))
  inn=Input(shape=(784,))
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

l=[784,1568,3920,3920,1568,784]
#m=getmodel(l,reg=regulariser,act="relu")
seed=15
mo=getmodel(l,reg=None,act="relu",mean=1.0,seed=seed)
mp=np.mean(mo.predict(t))
m=getmodel(l,reg=None,act="relu",mean=1.0,seed=seed)
print(m)

cb=[keras.callbacks.EarlyStopping(monitor='val_loss',patience=20,restore_best_weights=True),
                   keras.callbacks.TerminateOnNaN()]
cb.append(keras.callbacks.ModelCheckpoint("model1.tf", monitor='val_loss', verbose=1, save_best_only=True,save_weights_only=True))

m.summary()

mp=m.predict(t)
print(statinf(mp))
mop=mo.predict(t)
print(statinf(mop))

print(f"training on {t.shape}")
h=m.fit(t,None,
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
plt.show()

model=h.model
p=model.predict(t)
print(statinf(p))
print(np.corrcoef(np.transpose(p)))

plt.close()
pp=np.mean(p,axis=-1)
print(statinf(pp))

plt.hist(pp,bins=100,alpha=0.5)
plt.show()

plt.close()
pp2=p[0]
print(statinf(pp2))

plt.hist(pp2,bins=100,alpha=0.5)
plt.show()

w=model.predict(at)
print(statinf(w))

plt.close()
ww=np.mean(w,axis=-1)
print(statinf(ww))

plt.hist(ww,bins=100,alpha=0.5)
plt.show()

plt.close()

plt.hist(pp,bins=100,alpha=0.5,label="background")
plt.hist(ww,bins=100,alpha=0.5,label="signal")
plt.legend()
plt.yscale("log",nonposy="clip")
plt.show()

from sklearn.metrics import roc_auc_score as auc

pd=np.abs(pp-1)
wd=np.abs(ww-1)
y_score=np.concatenate((pd,wd))
y_true=np.concatenate((np.zeros_like(pp),np.ones_like(ww)))
print(statinf(y_score))
print(statinf(y_true))

auc_score=auc(y_true,y_score)
print(f"reached auc of {auc_score}")

plt.close()
plt.hist(pd,bins=100,alpha=0.5,label="background")
plt.hist(wd,bins=100,alpha=0.5,label="signal")
plt.legend()
plt.show()

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
plt.show()

auc_score=auc(y_true,y_score)
print(f"reached auc of {auc_score}")

pd=np.max(np.abs(p-m),axis=-1)
print(statinf(pd))

wd=np.max(np.abs(w-m),axis=-1)
print(statinf(wd))

plt.close()
plt.hist(pd,bins=100,alpha=0.5,label="background")
plt.hist(wd,bins=100,alpha=0.5,label="signal")
plt.legend()
plt.yscale("log",nonposy="clip")
plt.xscale("log",nonposx="clip")
plt.show()
auc_score=auc(y_true,y_score)
print(f"reached auc of {auc_score}")

m=getmodel(l,reg=None,act="relu")
s=m.predict(t)
print(statinf(s))
print(statinf(pp))

"""```
Deep one Class
0 98.6±0.0 97.1±0.0 98.0±0.3 97.6±0.7 96.6±1.3 97.8±0.7 98.0±0.7
1 99.5±0.0 98.9±0.0 97.3±0.4 98.3±0.6 99.2±0.6 99.6±0.1 99.7±0.1
2 82.5±0.1 79.0±0.0 88.6±0.5 85.4±2.4 85.0±2.9 89.5±1.2 91.7±0.8
3 88.1±0.0 86.2±0.0 89.9±0.4 86.7±0.9 88.7±2.1 90.3±2.1 91.9±1.5
4 94.9±0.0 87.9±0.0 92.7±0.6 86.5±2.0 89.4±1.3 93.8±1.5 94.9±0.8
5 77.1±0.0 73.8±0.0 85.5±0.8 78.2±2.7 88.3±2.9 85.8±2.5 88.5±0.9
6 96.5±0.0 87.6±0.0 95.6±0.3 94.6±0.5 94.7±2.7 98.0±0.4 98.3±0.5
7 93.7±0.0 91.4±0.0 92.0±0.4 92.3±1.0 93.5±1.8 92.7±1.4 94.6±0.9
8 88.9±0.0 79.2±0.0 89.9±0.4 86.5±1.6 84.9±2.1 92.9±1.4 93.9±1.6
9 93.1±0.0 88.2±0.0 93.5±0.3 90.4±1.8 92.4±1.1 94.9±0.6 96.5±0.3
```

"""

seed=16
m2=getmodel(l,reg=None,act="relu",mean=1.0,seed=seed)
print(m2)

m2.summary()

cb=[keras.callbacks.EarlyStopping(monitor='val_loss',patience=20,restore_best_weights=True),
                   keras.callbacks.TerminateOnNaN()]
cb.append(keras.callbacks.ModelCheckpoint("model2.tf", monitor='val_loss', verbose=1, save_best_only=True,save_weights_only=True))

print(f"training on {t.shape}")
h=m2.fit(t,None,
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
plt.show()

model2=h.model
p2=model2.predict(t)
print(statinf(p2))
print(np.corrcoef(np.transpose(p2)))
plt.close()
pp2=np.mean(p2,axis=-1)
print(statinf(pp2))

plt.hist(pp2,bins=100,alpha=0.5)
plt.show()

w2=model2.predict(at)
print(statinf(w2))

plt.close()
ww2=np.mean(w2,axis=-1)
print(statinf(ww2))

plt.hist(ww2,bins=100,alpha=0.5)
plt.show()

plt.close()

plt.hist(pp2,bins=100,alpha=0.5,label="background")
plt.hist(ww2,bins=100,alpha=0.5,label="signal")
plt.legend()
plt.yscale("log",nonposy="clip")
plt.show()

m2=np.mean(pp2)
pd2=np.abs(pp2-m2)
wd2=np.abs(ww2-m2)
y_score2=np.concatenate((pd2,wd2))
y_true2=np.concatenate((np.zeros_like(pp2),np.ones_like(ww2)))
print(statinf(pd2))
print(statinf(wd2))
print(statinf(y_score2))
print(statinf(y_true2))

auc_score2=auc(y_true2,y_score2)
print(f"reached auc of {auc_score2}")

wid=np.std(pd)
wid2=np.std(pd2)

def sumauc(f):
  score=y_score+y_score2*f
  return auc(y_true,score)

print(f"original auc 1 {auc_score}")
print(f"original auc 2 {auc_score2}")


print(f"simple sum auc {sumauc(1)}")
print(f"power1 auc {sumauc(wid/wid2)}")
print(f"power-1 auc {sumauc((wid/wid2)**(-1))}")
print(f"power3 auc {sumauc((wid/wid2)**(3))}")
print(f"power-3 auc {sumauc((wid/wid2)**(-3))}")

print(f"widfactor {wid/wid2}")
print(statinf(pd))
print(statinf(pd2))

np.corrcoef(pd,pd2)

seed=17
m3=getmodel(l,reg=None,act="relu",mean=1.0,seed=seed)
print(m3)

m3.summary()

b=[keras.callbacks.EarlyStopping(monitor='val_loss',patience=20,restore_best_weights=True),
                   keras.callbacks.TerminateOnNaN()]
cb.append(keras.callbacks.ModelCheckpoint("model3.tf", monitor='val_loss', verbose=1, save_best_only=True,save_weights_only=True))

print(f"training on {t.shape}")
h=m3.fit(t,None,
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
plt.show()

model3=h.model
p3=model3.predict(t)
print(statinf(p3))
print(np.corrcoef(np.transpose(p3)))
plt.close()
pp3=np.mean(p3,axis=-1)
print(statinf(pp3))

plt.hist(pp3,bins=100,alpha=0.5)
plt.show()

w3=model3.predict(at)
print(statinf(w3))

plt.close()
ww3=np.mean(w3,axis=-1)
print(statinf(ww3))

plt.hist(ww3,bins=100,alpha=0.5)
plt.show()

plt.close()

plt.hist(pp3,bins=100,alpha=0.5,label="background")
plt.hist(ww3,bins=100,alpha=0.5,label="signal")
plt.legend()
plt.yscale("log",nonposy="clip")
plt.show()

m3=np.mean(pp3)
pd3=np.abs(pp3-m3)
wd3=np.abs(ww3-m3)
y_score3=np.concatenate((pd3,wd3))
y_true3=np.concatenate((np.zeros_like(pp3),np.ones_like(ww3)))
print(statinf(pd3))
print(statinf(wd3))
print(statinf(y_score3))
print(statinf(y_true3))

auc_score3=auc(y_true3,y_score3)
print(f"reached auc of {auc_score3}")

wid=np.std(pd)
wid2=np.std(pd2)
wid3=np.std(pd3)

def sumauc3p(f,f2):
  score=y_score+y_score2*f+y_score3*f2
  return auc(y_true,score)

print(f"original auc 1 {auc_score}")
print(f"original auc 2 {auc_score2}")
print(f"original auc 3 {auc_score3}")



print(f"simple sum auc {sumauc3p(1,1)}")
print(f"power1 auc {sumauc3p(wid/wid2,wid/wid3)}")
print(f"power-1 auc {sumauc3p((wid/wid2)**(-1),(wid/wid3)**(-1))}")
print(f"power3 auc {sumauc3p((wid/wid2)**(3),(wid/wid3)**(3))}")
print(f"power-3 auc {sumauc3p((wid/wid2)**(-3),(wid/wid3)**(-3))}")

print(statinf(pd))
print(statinf(pd2))
print(statinf(pd3))

print(np.corrcoef([pd,pd2,pd3]))

seed=18
m4=getmodel(l,reg=None,act="relu",mean=1.0,seed=seed)
print(m4)

m4.summary()

b=[keras.callbacks.EarlyStopping(monitor='val_loss',patience=20,restore_best_weights=True),
                   keras.callbacks.TerminateOnNaN()]
cb.append(keras.callbacks.ModelCheckpoint("model4.tf", monitor='val_loss', verbose=1, save_best_only=True,save_weights_only=True))

print(f"training on {t.shape}")
h=m4.fit(t,None,
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
plt.show()

model4=h.model
p4=model4.predict(t)
print(statinf(p4))
print(np.corrcoef(np.transpose(p4)))
plt.close()
pp4=np.mean(p4,axis=-1)
print(statinf(pp4))

plt.hist(pp4,bins=100,alpha=0.5)
plt.show()

w4=model4.predict(at)
print(statinf(w4))

plt.close()
ww4=np.mean(w4,axis=-1)
print(statinf(ww4))

plt.hist(ww4,bins=100,alpha=0.5)
plt.show()

plt.close()

plt.hist(pp4,bins=100,alpha=0.5,label="background")
plt.hist(ww4,bins=100,alpha=0.5,label="signal")
plt.legend()
plt.yscale("log",nonposy="clip")
plt.show()

m4=np.mean(pp4)
pd4=np.abs(pp4-m4)
wd4=np.abs(ww4-m4)
y_score4=np.concatenate((pd4,wd4))
y_true4=np.concatenate((np.zeros_like(pp4),np.ones_like(ww4)))
print(statinf(pd4))
print(statinf(wd4))
print(statinf(y_score4))
print(statinf(y_true4))

auc_score4=auc(y_true4,y_score4)
print(f"reached auc of {auc_score4}")

wid=np.std(pd)
wid2=np.std(pd2)
wid3=np.std(pd3)
wid4=np.std(pd4)

def sumaucN(wids,scores,pwr=0.0):
  score=(wids[0]**pwr)*scores[0]
  for w,s in zip(wids[1:],scores[1:]):
    score+=(w**pwr)*s
  return auc(y_true,score)

print(f"original auc 1 {auc_score}")
print(f"original auc 2 {auc_score2}")
print(f"original auc 3 {auc_score3}")
print(f"original auc 4 {auc_score4}")

wids=[wid,wid2,wid3,wid4]
scores=[y_score,y_score2,y_score3,y_score4]

print(f"simple sum auc {sumaucN(wids,scores,pwr=0.0)}")
print(f"pwr1 {sumaucN(wids,scores,pwr=1.0)}")
print(f"pwr-1 {sumaucN(wids,scores,pwr=-1.0)}")
print(f"pwr3 {sumaucN(wids,scores,pwr=3.0)}")
print(f"pwr-3 {sumaucN(wids,scores,pwr=-3.0)}")

print(statinf(pd))
print(statinf(pd2))
print(statinf(pd3))
print(statinf(pd4))

print(np.corrcoef([pd,pd2,pd3,pd4]))

seed=19
m5=getmodel(l,reg=None,act="relu",mean=1.0,seed=seed)
print(m5)

m5.summary()

b=[keras.callbacks.EarlyStopping(monitor='val_loss',patience=20,restore_best_weights=True),
                   keras.callbacks.TerminateOnNaN()]
cb.append(keras.callbacks.ModelCheckpoint("model5.tf", monitor='val_loss', verbose=1, save_best_only=True,save_weights_only=True))

print(f"training on {t.shape}")
h=m5.fit(t,None,
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
plt.show()

model5=h.model
p5=model5.predict(t)
print(statinf(p5))
print(np.corrcoef(np.transpose(p5)))
plt.close()
pp5=np.mean(p5,axis=-1)
print(statinf(pp5))

plt.hist(pp5,bins=100,alpha=0.5)
plt.show()

w5=model5.predict(at)
print(statinf(w5))

plt.close()
ww5=np.mean(w5,axis=-1)
print(statinf(ww5))

plt.hist(ww5,bins=100,alpha=0.5)
plt.show()

plt.close()

plt.hist(pp5,bins=100,alpha=0.5,label="background")
plt.hist(ww5,bins=100,alpha=0.5,label="signal")
plt.legend()
plt.yscale("log",nonposy="clip")
plt.show()

m5=np.mean(pp5)
pd5=np.abs(pp5-m5)
wd5=np.abs(ww5-m5)
y_score5=np.concatenate((pd5,wd5))
y_true5=np.concatenate((np.zeros_like(pp5),np.ones_like(ww5)))
print(statinf(pd5))
print(statinf(wd5))
print(statinf(y_score5))
print(statinf(y_true5))

auc_score5=auc(y_true5,y_score5)
print(f"reached auc of {auc_score5}")

wid=np.std(pd)
wid2=np.std(pd2)
wid3=np.std(pd3)
wid4=np.std(pd4)
wid5=np.std(pd5)


print(f"original auc 1 {auc_score}")
print(f"original auc 2 {auc_score2}")
print(f"original auc 3 {auc_score3}")
print(f"original auc 4 {auc_score4}")
print(f"original auc 5 {auc_score5}")

wids=[wid,wid2,wid3,wid4,wid5]
scores=[y_score,y_score2,y_score3,y_score4,y_score5]

print(f"simple sum auc {sumaucN(wids,scores,pwr=0.0)}")
print(f"pwr1 {sumaucN(wids,scores,pwr=1.0)}")
print(f"pwr-1 {sumaucN(wids,scores,pwr=-1.0)}")
print(f"pwr3 {sumaucN(wids,scores,pwr=3.0)}")
print(f"pwr-3 {sumaucN(wids,scores,pwr=-3.0)}")

print(statinf(pd))
print(statinf(pd2))
print(statinf(pd3))
print(statinf(pd4))
print(statinf(pd5))

print(np.corrcoef([pd,pd2,pd3,pd4,pd5]))

plt.close()

def gromod(w,s):
  i=list(np.arange(len(w)).astype("int"))
  np.random.shuffle(i)
  qw=np.array(w)[i]
  qs=np.array(s)[i]
  x=np.arange(len(w))+1
  y=[]
  for j in range(len(w)):
    y.append(sumaucN(qw[:j+1],qs[:j+1],pwr=0.0))
  y=np.array(y)
  plt.plot(x,y,markersize=3,alpha=0.5)

for i in range(15):
  gromod(wids,scores)

plt.show()
