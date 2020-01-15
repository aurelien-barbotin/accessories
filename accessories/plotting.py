#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 17:33:14 2019

@author: aurelien
"""
import matplotlib.pyplot as plt
import glob
import numpy as np
import os

from matplotlib.colors import ListedColormap

FIJI_PATH = r"C:\Users\univ4208\Documents\software\fiji-win64\Fiji.app\luts/"

def fiji_luts_available():
    luts = glob.glob(FIJI_PATH+"*.lut")
    lutsnames=""
    for lut in luts:
        lutsnames+= lut.split(".lut")[0].split(os.sep)[-1]
    return lutsnames

def fiji_lut(lut_name, debug = False):
    
    lname = FIJI_PATH + lut_name+".lut"
    all_bytes = list()
    
    if not os.path.isfile(lname):
        raise KeyError(lut_name+
                       " is not available in Fiji. Please use one of the following:\n"+
                       fiji_luts_available())
        
    with open(lname, "rb") as f:
        byte = f.read(1)
        while byte:
            # Do stuff with byte.
            byte = f.read(1)
            all_bytes.append(byte)
        r = [int.from_bytes(w,"big") for w in all_bytes[:255]]
        g = [int.from_bytes(w,"big") for w in all_bytes[256:511]]
        b = [int.from_bytes(w,"big") for w in all_bytes[512:767]]
    if debug:
        plt.figure()
        plt.plot(r, color="red")
        plt.plot(g, color="g")
        plt.plot(b, color="b")
    newcolors = np.array([r, g, b]).T.astype(float)
    newcolors/=newcolors.max()
    new_cmap = ListedColormap(newcolors)
    return new_cmap