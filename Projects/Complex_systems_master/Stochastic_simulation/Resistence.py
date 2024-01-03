from matplotlib import pyplot as plb
import numpy as np
tiempo=np.arange(0,100)

f1=plb.figure(figsize=(10,8))
plb.plot(tiempo,fraccop4,label='removed=8')
plb.plot(tiempo,data000,label='removed=9')
plb.plot(tiempo,fraccop3,label='removed=10')
plb.plot(tiempo,data,label='removed=11')
plb.title('Adaptability',fontsize=16)
plb.xlabel('Time',fontsize=16)
plb.ylabel('Fraction of Cooperators',fontsize=16)
plb.legend()
f1.savefig('Resistence.jpg')

