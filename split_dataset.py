# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 02:05:41 2020

@author: MSI
"""

import pandas as pd 

def split_by_class_testing(data,save_file_as,c_y,c_n):
    class_y = data['Actual_Class']==1
    get_data_y = data[class_y]
    sample_y = get_data_y.sample(n=c_y)
    class_n = data['Actual_Class']==0
    get_data_n = data[class_n]
    sample_n = get_data_n.sample(n=c_n)
    join_yn = pd.concat([sample_y, sample_n], ignore_index=True)
    join_yn.to_csv(save_file_as, index=False)
    print("Selesai melakukan split data by class")
    
def split_by_class_training(data,save_file_as,c_y,c_n):
    class_y = data['Class']==1
    get_data_y = data[class_y]
    sample_y = get_data_y.sample(n=c_y)
    class_n = data['Class']==0
    get_data_n = data[class_n]
    sample_n = get_data_n.sample(n=c_n)
    join_yn = pd.concat([sample_y, sample_n], ignore_index=True)
    join_yn.to_csv(save_file_as, index=False)
    print("Selesai melakukan split data by class")

def split_by_class_pembagian(data,save_file_as,c_y,c_n):
    class_y = data['Pembagian']==c_y
    get_data_y = data[class_y]
    get_data_y.to_csv(save_file_as, index=False)
    print("Selesai melakukan split data by class")

def split_by_year(data,year,save_file_as):
    tahun = data['Tahun']==year
    get_data_tahun = data[tahun]
    get_data_tahun.to_csv(save_file_as, index=False)
    print("Selesai melakukan split data by year")

def split_by_class(data,actual_class,save_file_as):
    ac = data['Actual_Class']==actual_class
    get_data_ac = data[ac]
    get_data_ac.to_csv(save_file_as, index=False)
    print("Selesai melakukan split data by class")

def count_data(data):
    data_count = data.Seed_URL.count()
    tahun = data.Tahun.value_counts()
    jumlah_data_pertahun = data.Tahun.value_counts().sort_index()
#    jumlah_data_perclass = data.Class.value_counts().sort_index()
    jumlah_data_peractual = data.Actual_Class.value_counts().sort_index()
    print(jumlah_data_peractual)
    print("Selesai melakukan count data")

#file = "dataset/parameter2/02_testing_kompas.csv"
#save_file_as = "dataset/parameter2/skenario_4/SK4_02_testing_kompas_5.csv"
file = "dataset/data_proposal/dataset/kompas.csv"
save_file_as = "dataset/data_proposal/dataset/testing_kompas.csv"
data = pd.read_csv(file) 
year = 2016
c_y = 100
c_n = 50
actual_class = 1
#split_by_class_training(data,save_file_as,c_y,c_n)
#split_by_class_testing(data,save_file_as,c_y,c_n)
#split_by_class_pembagian(data,save_file_as,c_y,c_n)
#split_by_year(data,year,save_file_as)
#split_by_class(data,actual_class,save_file_as)
#count_data(data)