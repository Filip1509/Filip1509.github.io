import matplotlib.pyplot as plt
from statistics import mean
import pandas as pd
from scipy.interpolate import griddata
from scipy.stats import mode
import numpy as np
import os
import math
import sys
from collections import OrderedDict

def profile_selector(cut_x_desired,factor,verbose,plot,dataframe,z_params):
    """
    TROUBLESHOOTING PARAMETERS: factor: 1.3 or 0.9 depends on inversion of data. Weirdly, some measurements
    gave inverted heights, other did not. This function is universal for all measurements
    """
    global HEIGHT_PROTO
    df=dataframe
    df_sort = df.iloc[(df['x']-cut_x_desired).abs().argsort()[:1]]
    cut_x_found = df_sort["x"].values[0]
    df_cut = df[df['x'].isin([cut_x_found])]
    
    x = df_cut["y"]
    y = df_cut["z"]
    priemer = round(mean(y),2)
    HEIGHT_PROTO=priemer*factor 

    #OPTIONAL outputs for debugging
    if verbose:
        print("Your desired parameter is: ", cut_x_desired)
        print("Closest data found is for: ", cut_x_found)
        print("minz=",min(z_params), "maxz=",max(z_params),"most frequent=",mode(df_cut["z"]), "mean=",mean(y))
    
    if plot:
        cut_file = open('cut_%s.txt' % cut_x_found, 'w',newline='')
        df_cut.to_csv(cut_file, index=False, header=False)
        cut_file.close()
        print("Your cut is ready in file: cut_%s.txt" % (cut_x_found))
        plt.figure(figsize=(15,3))
        plt.plot(x, y, '.', color='blue')
        plt.xlabel("Y [mm.10]", fontsize=15)
        plt.ylabel("Z [mm]", fontsize=15)
        plt.plot([min(x),max(x)],[mean(y),mean(y)], c='red')
        plt.legend(["rez v x=%s" % cut_x_found, "average height: %s" % priemer], fontsize=15)
        plt.tick_params(axis='both', which='major', labelsize=15)
        plt.savefig('y_profile_%s.png' % cut_x_found)
        plt.show(block=True)
        print("Your profile scatter is ready in file: y_profile_%s.png\n" % (cut_x_found))

    return HEIGHT_PROTO


def plot_contour(x,y,z,z_r,resolution,contour_method):
    """
    creates contour data
    """
    resolution = str(resolution)+'j'
    X,Y = np.mgrid[min(x):max(x):complex(resolution),   min(y):max(y):complex(resolution)]
    points = [[a,b] for a,b in zip(x,y)]
    Z = griddata(points, z, (X, Y), method=contour_method)
    Z2 = griddata(points, z_r, (X, Y), method=contour_method)
    return X,Y,Z,Z2

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

def reduce_key(fn):
    return fn.replace("_Measurements","")