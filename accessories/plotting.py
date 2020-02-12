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
    
    custom = ["Magenta", "Cyan", "Green", "Red" ,"Blue"]
    
    if lut_name in custom:
        u = np.arange(256)
        nu = np.zeros(256)
        if lut_name == "Magenta":
            r = u
            b = u
            g = nu
        elif lut_name == "Cyan":
            r = nu
            g = u
            b = u
        elif lut_name == "Green":
            r = nu
            g = u
            b = nu
        elif lut_name == "Red":
            r = u
            g = nu
            b = nu
        elif lut_name == "Blue":
            r = nu
            g = nu
            b = u
    else:
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

def get_extent(img,res):
    """Returns the extent of an image for the imshow method
    Parameters:
        img (ndarray): 2D numpy array
        res (list): x and z resolutions
    Returns:
        list: 4-items list to be fed in the extent imshow method"""
    u,v = img.shape
    extent = [0, v * res[1],0,u*res[0]]
    return extent

def plot_scalebar(img,res,pos = [0.5,0.98],axis = 0, nline = 50, size = 1):
    """
    img: 2D array
    res: list of 2 elements, res along axis (0,1)
    pos: x,y initial position of scalebar
    axis: int
    size: in microns, should be same as resolution"""
    u,v = img.shape
    if axis==0:
        x0sbar = v * pos[1] * res[1]
        xsbar = np.ones(nline) * x0sbar  
        z0sbar = u*pos[0]*res[0]
        zsbar = np.linspace(0,1,nline) * size + z0sbar
        
    if axis==1:
        x0sbar = v * pos[1] * res[1]
        xsbar = np.linspace(0,1,nline) * size + x0sbar
        z0sbar = u*pos[0]*res[0]
        zsbar = np.ones(nline) * z0sbar  
    return xsbar,zsbar
