# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 22:34:32 2020

@author: MSI
"""
import pandas as pd 
import time
import numpy as np

def model_mnb(file_training, file_testing):
    data_training = pd.read_csv(file_training) 
    class_url = data_training.Class
    class_count = class_url.count()
    count_y = 0
    count_n = 0
    
    for i in class_url:
        if i==1:
            count_y += 1
        else:
            count_n += 1

    # Prior P(c) = Nc / N
    py = (count_y/class_count)
    pn = (count_n/class_count)
    
    class_y = []
    class_n = []
    page_relevance = []
    for i in range(class_count):
        url_word = data_training.URL_Word[i]
        parent_page = data_training.Parent_Page[i]
        anchor_text = data_training.Anchor_Text[i]
        surrounding_text = data_training.Surrounding_Text[i]
        page_relevance.extend((url_word,parent_page,anchor_text,surrounding_text))
        if data_training.Class[i]==1:
            #  bobot parameter di class y (y = 1)
            class_y.extend((url_word,parent_page,anchor_text,surrounding_text))
        elif data_training.Class[i]==0:
            # bobot parameter di class n (y = 0)
            class_n.extend((url_word,parent_page,anchor_text,surrounding_text))

    # |V| Jumlah kosa kata (tidak berulang) dalam dokumen training
    vocab = list(dict.fromkeys(page_relevance))
    v = len(vocab)
    
    count_class_y = len(class_y)
    count_class_n = len(class_n)

    data_testing = pd.read_csv(file_testing)
    class_url_testing = data_testing.Seed_URL
    class_count_testing = class_url_testing.count()
    write_class = []
    for i in range(class_count_testing):
        url_word = data_testing.URL_Word[i]
        parent_page = data_testing.Parent_Page[i]
        anchor_text = data_testing.Anchor_Text[i]
        surrounding_text = data_testing.Surrounding_Text[i] 
        
        # mencari bobot tiap parameter diclass y
        find_uw_y = np.where(class_y == url_word)
        find_pp_y = np.where(class_y == parent_page)
        find_at_y = np.where(class_y == anchor_text)
        find_st_y = np.where(class_y == surrounding_text)
        count_uw_y = np.count_nonzero(find_uw_y)
        count_pp_y = np.count_nonzero(find_pp_y)
        count_at_y = np.count_nonzero(find_at_y)
        count_st_y= np.count_nonzero(find_st_y)
        
        # Conditional Probabilities
        # P(tk|c) = count(tk|c)+1/count(tc)+|V| dengan c=1
        # tk merupakan berapa kali bobot muncul dalam dokumen training diclass 1
        cal_uw_y = (count_uw_y) / (count_class_y)
        cal_pp_y = (count_pp_y) / (count_class_y)
        cal_at_y = (count_at_y) / (count_class_y)
        cal_st_y = (count_st_y) / (count_class_y)
        
        # mencari bobot tiap parameter diclass n
        find_uw_n = np.where(class_n == url_word)
        find_pp_n = np.where(class_n == parent_page)
        find_at_n = np.where(class_n == anchor_text)
        find_st_n = np.where(class_n == surrounding_text)
        count_uw_n = np.count_nonzero(find_uw_n)
        count_pp_n = np.count_nonzero(find_pp_n)
        count_at_n = np.count_nonzero(find_at_n)
        count_st_n= np.count_nonzero(find_st_n)
        
        # Conditional Probabilities
        # P(tk|c) = count(tk|c)+1/count(tc)+|V| dengan c=0
        # tk merupakan berapa kali bobot muncul dalam dokumen training diclass 0
        cal_uw_n = (count_uw_n) / (count_class_n)
        cal_pp_n = (count_pp_n) / (count_class_n)
        cal_at_n = (count_at_n) / (count_class_n)
        cal_st_n = (count_st_n) / (count_class_n)
        
        # Pilih class
        choose_class_y = py*(cal_uw_y*cal_pp_y*cal_at_y*cal_st_y)
        choose_class_n = pn*(cal_uw_n*cal_pp_n*cal_at_n*cal_st_n)
        if(choose_class_y > choose_class_n):
            write_class.append(1)
        else:
            write_class.append(0)
    
    data_testing['Class'] = write_class
    data_testing.to_csv(file_testing,index=False)
    

def performance(file_testing):
    data = pd.read_csv(file_testing) 
    seed_url = data.Seed_URL.count()
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in range(seed_url):        
        actual = data.Actual_Class[i]
        predicted = data.Class[i]
        if(actual == 1 and predicted==1):
            TP +=1
        elif(actual == 0 and predicted==0):
            TN +=1
        elif(actual == 0 and predicted==1):
            FP +=1
        elif(actual == 1 and predicted==0):
            FN +=1
    
    accuracy =(TP+TN)/(TP+TN+FP+FN)
    precision = TP/(TP+FP)
    recall = TP/(TP+FN)
    f1 = 2*((precision*recall)/(precision+recall))
    print("\nHasil Uji Coba Performa")
    print("---------------------------------")
    print("Confussion Matrix :")
    print("TP : " + str(TP))
    print("TN : " + str(TN))
    print("FP : " + str(FP))
    print("FN : " + str(FN))
    print("---------------------------------")
    print("Accuracy : " +str('%.2f'%(accuracy*100)))
    print("Precision : " +str('%.2f'%(precision*100)))
    print("Recall : " +str('%.2f'%(recall*100)))
    print("F1 : " +str('%.2f'%(f1*100)))
    print("---------------------------------\n")
    

start_time = time.time()
file_training = "dataset/data_training_2.csv"
file_testing = "dataset/testing_model_nb/data_testing_detik.csv"
model_mnb(file_training, file_testing)
performance(file_testing)
print("--- %s seconds ---" % (time.time() - start_time))   