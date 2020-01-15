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

def get_tiff_img(file):
    out_arr = imread(file) - 2**15
    with Image.open(file) as img:
        #out_arr = np.asarray(img) - 2**15
        meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.keys()}
    
    xres = meta_dict["XResolution"][0][1]/meta_dict["XResolution"][0][0]
    yres = meta_dict["YResolution"][0][1]/meta_dict["YResolution"][0][0]
    return out_arr, [yres, xres]