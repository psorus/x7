import numpy as np

def loaddata():
    f=np.load("../../../../../multiruff/data.npz")
    return (f["train_x"],f["train_y"]),(f["test_x"],f["test_y"])

if __name__=="__main__":
    (x,y),(tx,ty)=loaddata()

    print(x.shape)
