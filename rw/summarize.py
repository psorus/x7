import numpy as np

fin_a=np.load("fin/auc.npz")["auc"]
fin_o=np.load("fin/oauc.npz")["auc"]
mfin_a=np.load("mfin/auc.npz")["auc"]
mfin_o=np.load("mfin/oauc.npz")["auc"]
raw_a=np.load("raw/auc.npz")["auc"]
raw_o=np.load("raw/oauc.npz")["auc"]

ae=np.load("ae/auc.npz")

np.savez_compressed("result",fina=fin_a,fino=fin_o,mfina=mfin_a,mfino=mfin_o,rawa=raw_a,rawo=raw_o,ae_o=ae["oauc"],ae_a=ae["auc"])





