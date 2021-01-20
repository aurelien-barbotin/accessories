#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:23:23 2020

@author: aurelien
"""
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
import h5py

def cres(res1,res2):
    """compares two resolutions"""
    return (np.array(res1) == np.array(res2)).all()

def gaussian(x,x0,sigma,a,c):
    return a*np.exp(-(x-x0)**2/(2*sigma))+c

def gaussian_fit(line,offset=True, x = None, plot = False):
    assert(line.ndim==1)
    if x is None:
        x = np.arange(line.size)
    xunit = np.abs(np.diff(x)[0])
    
    if offset:
        ff = gaussian
        bounds = ((x.min(),0.1*xunit,0,-line.max()/3),
                  (x.max(), (x.max()-x.min())/2, line.max()*1.5,line.max()/3) )
        
        popt, _ = curve_fit(ff, x, line, bounds = bounds)
        
    else:
        def ff(x,x0,sigma,a):
            return gaussian(x,x0,sigma,a,0)
        bounds = ((x.min(),0.1*xunit,0),
                  (x.max(), (x.max()-x.min())/2, line.max()*1.5) )
        
        popt, _ = curve_fit(ff, x, line, bounds = bounds)
    yh = ff(x, *popt)
    if plot:
        plt.figure()
        plt.plot(x,line)
        plt.plot(x,yh,"k--")
    return popt

def gaussian_fwhm(*args,**kwargs):
    popt = gaussian_fit(*args, **kwargs)
    sigma = popt[1]
    fwhm = np.sqrt(8*np.log(2)*sigma)
    return fwhm

class AberrationNames(object):
    def __init__(self):
        self.names = ['High NA defocus','tip','tilt','defocus','Oblique astigmatism'\
                    ,'Vertical astigmatism','Vertical coma','Horizontal coma'\
                    ,'Vertical trefoil','Oblique trefoil','1st spherical',\
                    'Vertical secondary astigmatism',\
                    'Oblique scondary astigmatism',\
                    'Vertical quadrafoil','Oblique quadrafoil']
    def __getitem__(self,nb):
        if isinstance(nb,(int,np.integer)):
            if nb<0:
                return "Not a zernike mode"
            elif nb<len(self.names):
                return self.names[nb]
            elif nb==21:
                return "2nd spherical"
            elif nb==36:
                return "3rd spherical"
            else:
                return "mode "+str(nb)
            
        elif type(nb)==list or type(nb)==np.ndarray:
            out=[]
            for elt in nb:
                out.append(self.__getitem__ (elt) )
            return out
        
aberration_names = AberrationNames()

def file_extractor(file, open_stacks=True):
    h5f = h5py.File(file, 'r')
    out = {} 
    for key in h5f['modal/'].keys():
        if key=="log_images" and not open_stacks:
            continue
        out[key] = h5f['modal/'][key][()]
    return out

def comparison_file_extractor(file,open_stacks=True):
    """Opens the result of a comparison experiment.
    Parameters:
        file: str, path to file
        open_stacks: bool, if False does not load the stacks (for less memory consumption)"""
    out={}
    h5f = h5py.File(file, 'r')
    for k in h5f.keys():
        if k!="filenames":
            if k=="stacks" and not open_stacks:
                continue
            out[k] = h5f[k].value
        else:
            fn = {}
            for kk in h5f["filenames/"]:
                nr = int(kk[4:])
                fn[nr] = h5f["filenames"][kk].value
                # print(kk,fn[nr])
            fn = sorted(fn.items())
            nrs = np.array([x[0] for x in fn])
            fn = [x[1] for x in fn]
            assert(np.all(nrs==np.arange(1,nrs.size+1)) )
            out["filenames"] = fn
    h5f.close()
    return out