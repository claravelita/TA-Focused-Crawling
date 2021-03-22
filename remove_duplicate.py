# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 20:22:35 2020

@author: MSI
"""
import pandas as pd 
file = "dataset/data_testing/detik_level_satu.csv"
data = pd.read_csv(file, encoding= 'unicode_escape')   
data.drop_duplicates(subset ="Seed_URL", 
					keep = "first", inplace = True) 
data.to_csv(file, index=True)