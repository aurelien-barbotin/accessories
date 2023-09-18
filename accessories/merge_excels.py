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

# df = pd.read_excel(file,sheet_name=sheet_name)

def merged_df_by_mask(df,groupby_cols=["repeat",'label']):
    print(groupby_cols)
    dct = {
        'number': 'mean',
        'object': lambda col: col.mode() if col.nunique() == 1 else np.nan,
    }
    dct = {k: v for i in [
        {col: agg for col in df.select_dtypes(tp).columns.difference(groupby_cols)} for tp, agg in dct.items()] for
        k, v in i.items()}
    
    group=df.groupby(by=groupby_cols).agg(**{k: (k, v) for k, v in dct.items()})
    index=group.index
    index_int = np.array([ [int(i1),int(i2)] for i1,i2 in index])
    group[groupby_cols[1]] = index_int[:,1]
    return group

def merge_excels(folder, extension=".xlsx", sheet_name=0, 
                 repeat_name = "acquisition",
                 savename = None, remove_unnamed = True,
                 regroup_names = None):
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
                
            if regroup_names is not None:
                df = merged_df_by_mask(df, groupby_cols = regroup_names)
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
    parser.add_argument("-r", "--repeat_name", help="Name given to the parameter counting the number of\
independent acquisitions",
                        default="acquisition")
    
    parser.add_argument('-l','--list', nargs='+', help='List of parameter names to regroup dataset')
    args = parser.parse_args()
    folder = args.folder
    extension = args.extension
    sheet_name = args.sheet_name
    if extension is None:
        extension = ".xlsx"
    merge_excels(folder,extension=extension, sheet_name=sheet_name,
                 savename=args.save_name, regroup_names = args.list)