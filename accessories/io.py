#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 17:32:28 2019

@author: aurelien
"""

import numpy as np
from PIL import Image
from PIL.TiffTags import TAGS
from tifffile import imread
import glob
import os
from .calibration import sted_power

def get_tiff_img(file, preprocess = None):
    out_arr = imread(file) - 2**15
    if preprocess is not None:
        out_arr = preprocess(out_arr)
    with Image.open(file) as img:
        #out_arr = np.asarray(img) - 2**15
        meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.keys()}
    
    xres = meta_dict["XResolution"][0][1]/meta_dict["XResolution"][0][0]
    yres = meta_dict["YResolution"][0][1]/meta_dict["YResolution"][0][0]
    return out_arr, [yres, xres]

def generate_names_list_npy(path,output_dict=False,sted_keyword="correction"):
    """Given a path to a npy experiment, generates the necessary names list to
    feed fit_all method"""
    out_dict = {}
    confocal_files = glob.glob(path+"/*.npy")
    confocal_files.sort()
    out_dict[0] = confocal_files
    
    sted_folder = None
    sted_folders = glob.glob(path+"/*/")
    for sf in sted_folders:
        if sted_keyword in sf:
            sted_folder = sf
    if sted_folder is None:
        raise KeyError('Sted keyword not found')
    
    sted_power_folders = glob.glob(sted_folder+"/*/")
    sted_power_folders.sort()
    sted_files = [sorted(glob.glob(w+"/*.npy")) for w in sted_power_folders]
    sted_powers = [float(os.path.split(w)[-2].split("_")[-1][:-2] ) for w in sted_power_folders]
    sted_files = [x for _,x in sorted(zip(sted_powers,sted_files))]
    sted_powers = np.array([0]+sorted(sted_powers))
    if sted_powers.max()<100:
        sted_powers*=1000
    for pw,fls in zip(sted_powers[1:],sted_files):
        if len(fls)>0:
            out_dict[int(pw)] = fls
    if output_dict:
        return out_dict
    else:
        return confocal_files,sted_files,sted_powers

def sort_names(names_list):
    """Method used to sort SIN curves in order of acquisition"""
    fk = lambda x : int(os.path.split(x)[-1].split("rep")[-1].split(".")[0])
    return sorted(names_list,key = fk)

def generate_names_list_dict(path):
        """Given a path to a SIN experiment, generates a list of files in a dict.
        The keys are the STED powers, values are list of files.
        Parameters:
            path: string, path to data
        Returns:
            out: dictionary containing a link to all the files
        """
        files = glob.glob(path+"/*.SIN")
        files.sort()
        prfx = list(set([os.path.split(w)[-1].split("_")[0] for w in files]))     
        out = {}
        for prf in prfx:
            pw = int(prf) * 100
            if pw!=0:
               pw = int(sted_power(pw))
            if pw not in out:
                out[pw] = sort_names(glob.glob(path+"/"+prf+"_*"))
            else:
                out[pw].extend(glob.glob(path+"/"+prf+"_*"))
                out[pw] = sort_names(out[pw])
        return out
    
