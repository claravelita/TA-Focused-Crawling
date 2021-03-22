# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 22:34:32 2020

@author: MSI
"""
import pandas as pd 
import time
import numpy as np
def labeling(uw, pp, at, st):
    if(uw >= 0.31 and pp >= 0.67 and at >= 0.20 and st >= 0.20):
        class_param = 1
    elif(uw >= 0.31 and pp >= 0.67 and at >= 0.20 and st == 0):
        class_param = 1
    elif(uw >= 0.31 and pp >= 0.67 and at == 0 and st >= 0.20):
        class_param = 1
    elif(uw >= 0.31 and pp >= 0.67 and at == 0 and st == 0):
        class_param = 1
    elif(uw >= 0 and pp >= 0.75 and at >= 0 and st >= 0):
        class_param = 1
    elif(uw >= 0 and pp >= 0.50 and at >= 0.60 and st >= 0.50):
        class_param = 1
    elif(uw >= 0 and pp >= 0.50 and at >= 0.60 and st == 0):
        class_param = 1
    elif(uw >= 0.60 and pp >= 0.45 and at >= 0.30 and st >= 0):
        class_param = 1
    else:
        class_param = 0
    return class_param

def labeling_training(file):
    data = pd.read_csv(file, encoding= 'unicode_escape') 
    seed_url = data.Seed_URL.count()
    save_class = []
    for i in range(seed_url):
        uw = data.URL_Word[i]
        pp = data.Parent_Page[i]
        at = data.Anchor_Text[i]
        st = data.Surrounding_Text[i]
        class_param = labeling(uw, pp, at, st)
        save_class.append(class_param)        

    data['Class'] = save_class
    data.to_csv(file,index=False)
    print("Berhasil Melakukan Labeling Class " + file) 

def labeling_testing(file):
    data = pd.read_csv(file, encoding= 'unicode_escape') 
    seed_url = data.Seed_URL.count()
    save_class = []
    for i in range(seed_url):
        uw = data.URL_Word[i]
        pp = data.Parent_Page[i]
        at = data.Anchor_Text[i]
        st = data.Surrounding_Text[i]
        class_param = labeling(uw, pp, at, st)
        save_class.append(class_param)        

    data['Actual_Class'] = save_class
    data.to_csv(file,index=False)
    print("Berhasil Melakukan Labeling Class " + file) 

start_time = time.time()
file_training = "dataset/data_proposal/dataset/data_training.csv"
file_testing = "dataset/data_proposal/dataset/kompas.csv"
#labeling_training(file_training)
labeling_testing(file_testing)
print("--- %s seconds ---" % (time.time() - start_time))  