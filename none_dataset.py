# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 03:50:36 2020

@author: MSI
"""

import pandas as pd
import numpy as np
df = pd.read_csv('dataset/data_training/data_training.csv', encoding= 'unicode_escape')   
df.isnull() 
df.replace(np.nan,"none", inplace=True)
df.to_csv('dataset/cnn_new.csv')
print(df.isnull())