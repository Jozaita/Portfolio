import numpy as np
import random
from matplotlib import pyplot as plb
t=0.2
u=-1
v=1
m=np.linspace(-1,1,100)
plb.plot(m,t*0.5*m**2+u*m**4+v*m**6)