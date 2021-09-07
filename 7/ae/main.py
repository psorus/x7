import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, losses
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Model

from tensorflow import keras

with open("../dex","r") as f:
    index=int(f.read().strip())

from loaddata import loaddata
(x_train, y_train), (x_test, y_test) = loaddata()


x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.

x_train=np.expand_dims(x_train,axis=-1)
x_test=np.expand_dims(x_test,axis=-1)

print (x_train.shape)
print (x_test.shape)

#x_train=np.reshape(x_train,(x_train.shape[0],784))
#x_test=np.reshape(x_test,(x_test.shape[0],784))


train=x_train[np.where(y_train==index)]



latent_dim = 192

denses=[800,400,latent_dim]


i=keras.Input(x_train.shape[1:])

q=i

convs=[1,2,3]
    #-6 in dimension

for c in convs[1:]:
    q=layers.Conv2D(c,3,activation="relu",padding="same")(q)

q=layers.Flatten()(q)

for d in denses:
    q=layers.Dense(d)(q)

encoder=Model(i,q)

encoder.summary()

adenses=denses[::-1]
aconvs=convs[::-1]

for d in adenses:
    q=layers.Dense(d)(q)

q=layers.Dense(3136*3/4)(q)

q=layers.Reshape((28,28,convs[-1]))(q)

for c in aconvs[1:]:
    q=layers.Conv2D(c,3,activation="relu",padding="same")(q)

q=layers.Dense(28*28)(q)

model=Model(i,q)

model.summary()
#exit()


model.compile("adam","mse")

model.fit(train,train,epochs=50,validation_split=0.15,
        callbacks=[keras.callbacks.EarlyStopping(patience=5),
                   keras.callbacks.CSVLogger("history.csv")])


e_train=encoder.predict(x_train)
e_test=encoder.predict(x_test)

t_train=model.predict(x_train)
t_test=model.predict(x_test)

np.savez_compressed("output",x_test=x_test,x_train=x_train,e_train=e_train,e_test=e_test,y_test=y_test,y_train=y_train,t_train=t_train,t_test=t_test)







