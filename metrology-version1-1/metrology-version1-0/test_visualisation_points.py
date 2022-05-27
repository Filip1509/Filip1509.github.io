
from matplotlib import pyplot as plt
import numpy as np
import math
import pandas as pd

def rotate(pointX,pointY, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox=0
    oy=0
    px = pointX
    py=pointY

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

x=np.array([138.24749,23.3565,145.05431081081082,22.081777777777777,144.92998648648648,80.40501501501501,78.57360887])
x=(x-138.24749)*(-1)
y=np.array([59.343,67.0875,106.28801276281627,102.65549200970786,107.72243054054054,116.36685888116371,121.36556958])
y=(y-59.343)*(-1)
order=["sensor R01", "sensor R07", "hybrid R09", "hybrid R11", "PB R13", "PB R15", "PB R17"]
expected_value=[0 for x in order]

fig, ax = plt.subplots()
angle = math.atan2(y[1], x[1])
#print(angle)

x_new=[]
y_new=[]
for i,x_point in enumerate(x):
    result=rotate(x_point,y[i],-angle)
    x_new.append(round(result[0],5))
    y_new.append(round(result[1],5))

plt.scatter(x_new,y_new)
for i, txt in enumerate(order):
    ax.annotate(txt, (x_new[i], y_new[i]))

new_dict={"x":x_new,"y":y_new,"order":order,"expected value":expected_value}
df = pd.DataFrame(data=new_dict)
print(df)
df.to_csv('ok.txt', header=True, index=None, sep='\t')

plt.show()