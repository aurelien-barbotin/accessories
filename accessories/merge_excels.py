#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 13:46:57 2023

@author: aurelienb
"""

import pandas as pd
import numpy as np
        
import glob
import os

def merge_excels(folder, extension=".xlsx", sheet_name=0, 
                 repeat_name = "repeat",
                 savename = None, remove_unnamed = True):
    """Merge several excel files located in a main folder. 
    Arborescence: folder -> subfolders (conditions) -> excel files"""
    subfolders = glob.glob(os.path.join(folder,'*/'))
    conditions = [w[len(folder):].replace('/','') for w in subfolders]

    dfs = []
    for j, subfolder in enumerate(subfolders):
        files = sorted(glob.glob(subfolder+"*"+extension))
        for k, file in enumerate(files):
            df = pd.read_excel(file,sheet_name=sheet_name)
            if remove_unnamed:
                to_remove = list(filter(lambda x: "Unnamed" in x,df.keys()))
                df = df.drop(labels=to_remove,axis="columns")
                df = df.dropna()
            df[repeat_name] = k
            df["condition"] = conditions[j]
            dfs.append(df)
    dfs = pd.concat(dfs)
    if savename is not None:
        dfs.to_excel(savename)
    return dfs

if __name__=='__main__':
    import argparse
    import glob
    import os
    
    parser = argparse.ArgumentParser(description=
         'Merge excel files located in subfolders')
    
    parser.add_argument("-f", "--folder", help="Folder")
    parser.add_argument("-e", "--extension", help="extension")
    parser.add_argument("-x", "--sheet_name", help="Name of the sheet to be considered",
                        default=0)
    parser.add_argument("-s", "--save_name", help="Output name",
                        default="merged.xlsx")
    
    args = parser.parse_args()
    folder = args.folder
    extension = args.extension
    sheet_name = args.sheet_name
    if extension is None:
        extension = ".xlsx"
    merge_excels(folder,extension=extension, sheet_name=sheet_name,savename=args.save_name)