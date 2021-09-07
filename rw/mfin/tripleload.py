import numpy as np



def tripleload(n=3):
    fs=[np.load(f"../ae/output{i}.npz") for i in range(n)]
    x_train=np.concatenate([f["e_train"] for f in fs],axis=1)
    y_train=fs[0]["y_train"]
    x_test=np.concatenate([f["e_test"] for f in fs],axis=1)
    y_test=fs[0]["y_test"]
    return x_train,y_train,x_test,y_test
    print(x_train.shape)
    #x_train,y_train,x_test,y_test=f["e_train"],f["y_train"],f["e_test"],f["y_test"]



if __name__=="__main__":
    tripleload(3)
