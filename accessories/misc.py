#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:23:23 2020

@author: aurelien
"""
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

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