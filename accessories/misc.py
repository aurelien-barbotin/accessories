#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:23:23 2020

@author: aurelien
"""
import numpy as np


def cres(res1,res2):
    """compares two resolutions"""
    return (np.array(res1) == np.array(res2)).all()