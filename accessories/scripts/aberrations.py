# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 17:17:57 2020
Script used to compare the aberrations in two different SLM files
"""

import numpy as np
import matplotlib.pyplot as plt

import sys
import json
if len(sys.argv)!=3:
    print("Invalid number of arguments")
  
reference_file = sys.argv[1]
correction_file = sys.argv[2]
"""
reference_file = "C:/Users/univ4208/Documents/Data/2020_01_10_Valentin/session3/SLM settings/correction_3microns_kk114.json"
correction_file = "C:/Users/univ4208/Documents/Data/2020_01_10_Valentin/session3/SLM settings/reference_fluorescence.json"
"""
with open(correction_file,"r") as f:
    dd1 = json.load(f)
    
with open(reference_file,"r") as f:
    dd2 = json.load(f)
    

aberration = np.array(dd2["aberration"]) - np.array(dd1["aberration"])
aberration = aberration.reshape(-1)
modes = np.arange(aberration.size)

xx = aberration!=0
aberration = aberration[xx]
modes = modes[xx]

# fig,ax = plt.subplots(1,1)
plt.figure()
plt.bar(list(range(aberration.size)), aberration)
plt.xticks(list(range(aberration.size)),modes)
plt.show()