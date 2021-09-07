import os
import numpy as np
import re

fns=[zw for zw in os.listdir(".") if re.match("auc.?\.npz",zw)]

fs=[np.load(fn) for fn in fns if not "aucs" in fn]

aucs=[f["auc"] for f in fs]
oaucs=[f["oauc"] for f in fs]


m_auc=np.mean(aucs)
m_oauc=np.mean(oaucs)
s_auc=np.std(aucs)
s_oauc=np.std(oaucs)

print(m_auc,"+-",s_auc,"*",len(aucs))
print(m_oauc,"+-",s_oauc,"*",len(oaucs))

np.savez_compressed("aucs",aucs=aucs,oaucs=oaucs,fns=fns,m_auc=m_auc,m_oauc=m_oauc,s_auc=s_auc,s_oauc=s_oauc)



