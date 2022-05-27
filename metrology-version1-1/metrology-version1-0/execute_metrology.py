from hashlib import new
import pandas as pd
import sys
from subprocesses.metrology_functions import *
import glob
import os
from collections import defaultdict,OrderedDict
import subprocess
import datetime

### this part creates a list of lists [[xyz_file, measurement_file]] in respect to its current path

dirname=os.path.dirname(os.path.realpath(__file__))
datadir=dirname+"\\data\\"
datas=glob.glob(datadir+"*")
group_dict = defaultdict(list)
for fn in datas:
    key = reduce_key(fn)
    group_dict[key].append(fn)

group_list=list(group_dict.values())

### for every measurement, we run a subprocess of callibrated metrology script. This script is to be universal
### for any given measurement (sensor left-top, right-bottom etc), but dissimilar behaviour of measurement data
### forced us to use multiple scripts in this version (v1.0)

with open('res_raw{}.csv'.format(datetime.date.today()),'w') as f:
    for i in range(0,len(group_list)):
        print("Running metrology on: {}".format(group_list[i][1]))
        subprocess.run("python {0}\\subprocesses\\script_{1}.py {2} {3}".format(dirname,i,group_list[i][0],group_list[i][1]), shell=True,stdout=f)

### results are processed here (moved to origin and rotated) and output csv file is created with current date
### format may later be changed in compliance with ITk standard

df_raw = pd.read_csv('res_raw{}.csv'.format(datetime.date.today()),sep=',', comment='#',names=["x","y"])
x = df_raw.loc[:,"x"].values
x = [float(i) for i in x]
x_raw = np.array(x)
x=(x_raw-x_raw[0])*(-1)

y = df_raw.loc[:,"y"].values
y = [float(i) for i in y]
y_raw = np.array(y)
y=(y_raw-y_raw[0])*(-1)
order=["sensor R01", "sensor R07", "hybrid R09", "hybrid R11"]
#"PB R13", "PB R15", "PB R17"

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

### we keep some manually checked values as 'expected'. These values are raw (not rotated ...) but can be compared
### with raw values from out new measurement. Expected values are not precisely calculated from technical drawings (yet)

expected_raw_x=np.array([138.24749,23.3565,145.05431081081082,22.081777777777777])
#,144.92998648648648,80.40501501501501,78.57360887
expected_raw_y=np.array([59.343,67.0875,106.28801276281627,102.65549200970786])
#,107.72243054054054,116.36685888116371,121.36556958

new_dict={"x":x_new,"y":y_new,"order":order,"raw_x":x_raw,"expected_raw_x":expected_raw_x,"raw_y":y_raw,"expected_raw_y":expected_raw_y}
df = pd.DataFrame(data=new_dict)
print("Results:")
print(df)
df.to_csv('RESULTS{}.csv'.format(datetime.date.today()), header=True, index=None, sep='\t')

plt.show()