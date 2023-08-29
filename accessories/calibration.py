#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:51:03 2020

@author: aurelien


"""
import numpy as np
from scipy.optimize import curve_fit
power_calibration = [0.0,4.04,10,15.5,21.9,33.3,46.5,56.1,71.2,86.8] #mW
power_calibration = list(map(float,power_calibration))
voltage = np.array([0,500,800,1000,
                    1200,1500,1800,2000,2300,2600]).astype(np.float) #mV

def quadr(x,a,b,c):
    return a*x**2+b*x+c

fit_calibration,_ = curve_fit(quadr,voltage,power_calibration)

def sted_power(voltage):
    """Converts the input STED power in millivolts fed to the AOM in power
    in mW measured with a powermeter"""
    out = quadr(voltage,*fit_calibration)
    return out