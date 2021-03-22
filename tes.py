# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 10:30:35 2020

@author: MSI
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd 
import time
from datetime import datetime
import mysql.connector
import threading 
from newspaper import Article

def Performance_Tahun(file_testing):
    data = pd.read_csv(file_testing) 
    tahun = data.Tahun.value_counts().sort_index().keys().tolist()
    jumlah_data = data.Tahun.value_counts().tolist()
    print(tahun)
    print(jumlah_data)
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    accuracy = {}
    precision = {}
    recall = {}
    for t in tahun:
        for i in range(data.Seed_URL.count()):
            if data.Tahun[i] == t:
                actual = data.Class_Train[i]
                predicted = data.Class[i]
                if(actual == 1 and predicted==1):
                    TP +=1
                elif(actual == 0 and predicted==0):
                    TN +=1
                elif(actual == 0 and predicted==1):
                    FP +=1
                elif(actual == 1 and predicted==0):
                    FN +=1
#    
        accuracy[t] =(TP+TN)/(TP+TN+FP+FN)
        
        
        try:
            precision[t] = TP/(TP+FP)
        except ZeroDivisionError:
            precision[t] = TP
            
        try:
            recall[t] = TP/(TP+FN)
        except ZeroDivisionError:
            recall[t] = TP
    
#        print("TP = " + str(TP))
#        print("TN = " + str(TN))
#        print("FP = " + str(FP))
#        print("FN = " + str(FN))
        print("\n---------------------------------")
        print("Accuracy :" +str('%.2f'%(accuracy[t])))
        print("Precision :" +str('%.2f'%(precision[t])))
        print("Recall :" +str('%.2f'%(recall[t])))
        print("\n---------------------------------")
    
    a = list(accuracy.values())
    p = list(precision.values())
    r = list(recall.values())
    import matplotlib.pyplot as plt
    plt.plot(tahun, r)
    plt.xlabel('Tahun')
    plt.ylabel('Akurasi')
    plt.show()

def plot_performace():
    import matplotlib.pyplot as plt
#    x = [2015,2016,2017,2018,2019,2020]
#    print('Skema 1: Detik')
#    akurasi = [1, 0.68, 0.98,0.92,0.93, 0.91]
#    presisi = [1,0.88,1,1,0.91,0.53]
#    recall = [1,0.39, 0.96, 0.86, 0.94, 0.82]
#    plt.plot(x, akurasi,'lightskyblue', x, presisi, 'palegreen', x, recall, 'lightcoral')
#    plt.plot(x, akurasi,'lightskyblue', x, presisi, 'palegreen', x, recall, 'lightcoral')
#    plt.xlabel('Tahun')
#    plt.ylabel('Akurasi')
#    plt.show()
    
    names = ['Detik', 'Kompas']
    accuracy = [0.91, 0.81]
    precision = [1, 0.97]
    recall = [0.89, 0.88]
    
    plt.figure(figsize=(6, 3))
    plt.plot(names, accuracy,'lightskyblue', names, precision, 'palegreen', names, recall, 'lightcoral')
#    plt.subplot(131)
#    plt.plot(names, accuracy)
#    plt.subplot(132)
#    plt.plot(names, accuracy)
#    plt.subplot(133)
#    plt.plot(names, recall)
    plt.xlabel('Media Online')
    plt.ylabel('Akurasi')
    plt.suptitle('Hasil Uji Testing')
    plt.show()
#from bs4 import BeautifulSoup
#import requests
#import pandas as pd
#from itertools import chain
#import numpy as np
#import collections
#import math
#from nltk.tokenize import sent_tokenize, word_tokenize
#from nltk.corpus import stopwords
#from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
#import re
#import time
#import json
#from urllib.parse import urlparse
#start_time = time.time()
##file ="dataset/klasifikasi/testing_kompas_seluruh_tahun_coba.csv"
##data = pd.read_csv(file, encoding= 'unicode_escape')
##kalimat = data.Seed_URL
#file = open("dataset/test.txt") 
#dataset_workbank = open("dataset/wordbank.txt") 
#wordbank = dataset_workbank.read().split('\n')
#text = file.read()
##text = "https://news.detik.com/berita-jawa-barat/d-4553707/penampakan-sampah-menumpuk-di-pantai-loji-geopark-ciletuh"
#pisah = []
#factory = StemmerFactory()
#stemmer = factory.create_stemmer()
#listStopword =  set(stopwords.words('indonesian'))
#remove_enter = re.compile('\n')
#remove_div = re.compile('(?:#).*(?:{).*(?:})')
#remove_js_1 = re.compile('(?:.function).*(?:;)')
#remove_js_2 = re.compile('(?:loading...).*(?:;)')
#remove_js_3 = re.compile('(?:.adsbygoogle.).*(?:;)')
#remove_js_4 = re.compile('(?:window.).*(?:;)')
#remove_js_5 = re.compile('(?:googletag.).*(?:;)')
#remove_char = re.compile('[^\w\s]')
#remove_tab = re.compile('\t')
#pisah = []
#print(text)
#parse_object = urlparse(text) 
#if parse_object.netloc is not '':
#    text = parse_object.path
#    for w in wordbank:
#        if w in text:
#            text = text.replace(w, " ")
#    text = re.sub(r"d-[0-9]?", " ", text)
#else:
##             membersikan hasil scraping
#    text = re.sub(remove_enter, " ", str(text))
#    text = re.sub(remove_div, " ", text)
#    text = re.sub(remove_js_1, " ", text)
#    text = re.sub(remove_js_2, " ", text)
#    text = re.sub(remove_js_3, " ", text)
#    text = re.sub(remove_js_4, " ", text)
#    text = re.sub(remove_js_5, " ", text)
#    text = re.sub(remove_tab, " ", text)
#    encoded_string = text.encode("ascii", "ignore")
#    text = encoded_string.decode()
#print(text)
#text = re.sub(remove_char, " ", text)
#print(text)
#text = ''.join([i for i in text if not i.isdigit()])
#print(text)
#palabuhanratu = ['pelabuhanratu', 'Pelabuhanratu', 'Palabuanratu', 'pelabuhan ratu', 'Pelabuhan Ratu', 'Palabuhan Ratu', 'palabuhan ratu', 'pelabuanratu', 'Pelabuanratu', 'palabuanratu']
#for p in palabuhanratu:
#    text = text.replace(p, 'palabuhanratu')
#jawa_barat = ['jabar', 'Jabar']
#for jb in jawa_barat:
#    text = text.replace(jb, 'jawa barat')
#geopark = ['Geoparks', 'geoparks']
#for g in geopark:
#    text = text.replace(g, 'geopark')
#ciletuh = ['cileteuh', 'cileteh', 'Cileteuh', 'Cileteh']
#for c in ciletuh:
#    text = text.replace(c, 'ciletuh')
#ciletuh_pugg = ['cpugg', 'CPUGG', 'CPUGGp','cpuggp']
#for cpugg in ciletuh_pugg:
#    text = text.replace(cpugg, 'ciletuh palabuhanratu unesco global geopark')
#unesco_gg = ['ugg', 'UGG', 'uggp', 'UGGp']
#for ugg in unesco_gg:
#    text = text.replace(ugg, 'unesco global geopark')
#geopark_ciletuh = ['geoparkciletuh', 'ciletuhgeopark', 'Geoparkciletuh', 'Ciletuhgeopark', 'GeoparkCiletuh', 'CiletuhGeopark', 'GeoparksCiletuh', 'geoparksciletuh']
#for gc in geopark_ciletuh:
#    text = text.replace(gc, 'geopark ciletuh')
#print(text)
#tokens = word_tokenize(text)
#print(tokens)
#hasil = []
#for t in tokens:
#    #casefolding
#    casefolding = t.lower()
#    removed = []
#    #stopword
#    if t not in listStopword:
#        removed.append(casefolding)
#        #stemming
#    print(removed)
#    for r in removed: 
#        hasil.append(stemmer.stem(r))
#
#print(hasil)
#encoded_string = text.encode("ascii", "ignore")
#text = encoded_string.decode()
#
#
#
##
#hapus_karakter = re.sub(r'[^\w\s]', ' ', text)
#hapus_angka = ''.join([i for i in hapus_karakter  if not i.isdigit()])
#hapus_angka = re.sub(r'\s\s', ' ', hapus_angka)
#print(hapus_angka)
#palabuhanratu = ['pelabuhanratu', 'Pelabuhanratu', 'Palabuanratu', 'pelabuhan ratu', 'Pelabuhan Ratu', 'Palabuhan Ratu', 'palabuhan ratu', 'pelabuanratu', 'Pelabuanratu', 'palabuanratu']
#for p in palabuhanratu:
#    hapus_angka = hapus_angka.replace(p, 'palabuhanratu')
#jawa_barat = ['jabar', 'Jabar']
#for jb in jawa_barat:
#    hapus_angka = hapus_angka.replace(jb, 'jawa barat')
#ciletuh = ['cileteuh', 'cileteh', 'Cileteuh', 'Cileteh']
#for c in ciletuh:
#    hapus_angka = hapus_angka.replace(c, 'ciletuh')
#geopark_ciletuh = ['geoparkciletuh', 'ciletuhgeopark', 'Geoparkciletuh', 'Ciletuhgeopark', 'GeoparkCiletuh', 'CiletuhGeopark']
#for gc in geopark_ciletuh:
#    hapus_angka = hapus_angka.replace(gc, 'geopark ciletuh')
#
#tokens = word_tokenize(hapus_angka)
#
#
#hasil = []
#for t in tokens:
#    #casefolding
#    casefolding = t.lower()
#    removed = []
#    #stopword
#    if t not in listStopword:
#        removed.append(casefolding)
#        #stemming
#    
#    for r in removed: 
#        hasil.append(stemmer.stem(r))
#pisah.append(hasil)
#print(pisah)


#import pandas as pd 
#file = "dataset/topic_spesific.csv"
#data = pd.read_csv(file)
#data.drop_duplicates(subset ="Seed_URL", 
#					keep = "first", inplace = True) 
#data.to_csv(file, index=True)
#import pandas as pd
#import numpy as np
#df = pd.read_csv('dataset/kompas.csv', encoding= 'unicode_escape')   
#df.isnull() 
#df.replace(np.nan,"none", inplace=True)
#df.to_csv('dataset/kompas.csv')
#print(df.isnull())



#import threading 
#  
#def print_cube(): 
#    import mysql.connector
#
#    mydb = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="",
#    database="test"
#    )
#    
#    mycursor = mydb.cursor()
#    
#    sql = "INSERT INTO tr_brand (brand, created_at) VALUES (%s, %s)"
#    val = ("John", "2020-08-18")
#    
#    mycursor.execute(sql, val)
#    
#    mydb.commit()
#    
#    print(mycursor.rowcount, "record inserted.")
#  
#def print_square(): 
#    import mysql.connector
#
#    mydb = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="",
#    database="test"
#    )
#    
#    mycursor = mydb.cursor()
#    
#    sql = "INSERT INTO tr_brand (brand, created_at) VALUES (%s, %s)"
#    val = ("John", "2020-08-18")
#    
#    mycursor.execute(sql, val)
#    
#    mydb.commit()
#    
#    print(mycursor.rowcount, "record inserted.")
#  
#if __name__ == "__main__": 
#    # creating thread 
#    t1 = threading.Thread(target=print_square) 
#    t2 = threading.Thread(target=print_cube) 
#  
#    # starting thread 1 
#    t1.start() 
#    # starting thread 2 
#    t2.start() 
#  
#    # wait until thread 1 is completely executed 
#    t1.join() 
#    # wait until thread 2 is completely executed 
#    t2.join() 
#  
#    # both threads completely executed 
#    print("Done!") 

#txt ="Kompas.com - 29/12/2018, 11:03 WIB"
#re_kompas = txt.replace("Kompas.com - ", "")
#re_koma = re_kompas.replace(",", "")
#re_wib = re_koma.replace(" WIB", "")
#
#from datetime import datetime
#a = datetime.strptime(txt, "Kompas.com - %d/%m/%Y, %H:%M WIB")
#print(a)


#import mysql.connector
#
#mydb = mysql.connector.connect(
#  host="localhost",
#  user="root",
#  password="",
#  database="test"
#)
#
#mycursor = mydb.cursor()
#
#sql = "SELECT * FROM profil_berita WHERE link = %s"
#adr = ("kompas.com", )
#
#mycursor.execute(sql, adr)
#
#myresult = mycursor.fetchall()
#
#hitung = len(myresult)
#
#if(hitung == 0):
#    print("jangan tambah")
#else:
#    print("tambah")
#from datetime import datetime

#import pandas as pd
#from itertools import chain
#import numpy as np
#import collections
#import math
#from nltk.tokenize import sent_tokenize, word_tokenize
#from nltk.corpus import stopwords
#from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
#import re
#import time
#from urllib.parse import urlparse


#def Preprocessing(bow):
#    hasil_pre = []
#    factory = StemmerFactory()
#    stemmer = factory.create_stemmer()
#    listStopword =  set(stopwords.words('indonesian'))
#    #tokenization
#    parse_object = urlparse(bow) 
##    website = ['https', 'http', 'www', 'com', 'co', 'id','antaranews', 'beritasatu', 'page', 'cnn', 'gatra', 'inews', 'jpnn', 'kontan', 'kumparan', 'liputan6', 'mediaindonesia', 'merdeka', 'okezone', 'pikiranrakyat', 'pikiran-rakyat', 'radarsukabumi', 'republika', 'sindonews', 'tempo', 'tribunnews', 'kompas', 'detik']
#    hapus_karakter = re.sub(r'[^\w\s]', ' ', str(parse_object.path))
##    for w in website:
##        if w in hapus_karakter:
##            hapus_karakter = hapus_karakter.replace(w, ' ')    
#    hapus_angka = ''.join([i for i in hapus_karakter  if not i.isdigit()])
#    palabuhanratu = ['pelabuhanratu', 'Pelabuhanratu', 'Palabuanratu', 'pelabuhan ratu', 'Pelabuhan Ratu', 'pelabuanratu', 'palabuanratu']
#    for p in palabuhanratu:
#        hapus_angka = hapus_angka.replace(p, 'palabuhanratu')
#    jawa_barat = ['jabar', 'Jabar']
#    for jb in jawa_barat:
#        hapus_angka = hapus_angka.replace(jb, 'jawa barat')
#    ciletuh = ['cileteuh', 'cileteh', 'Cileteuh', 'Cileteh']
#    for c in ciletuh:
#        hapus_angka = hapus_angka.replace(c, 'ciletuh')
#    geopark_ciletuh = ['geoparkciletuh', 'ciletuhgeopark', 'Geoparkciletuh', 'Ciletuhgeopark', 'GeoparkCiletuh', 'CiletuhGeopark']
#    for gc in geopark_ciletuh:
#        hapus_angka = hapus_angka.replace(gc, 'geopark ciletuh')
#    tokens = word_tokenize(hapus_angka)
#    hasil = []
#    for t in tokens:
#        #casefolding
#        casefolding = t.lower()
#        removed = []
#        #stopword
#        if t not in listStopword:
#            removed.append(casefolding)
#            #stemming
#            for r in removed: 
#                hasil.append(stemmer.stem(r))
#    print(hasil)

#text = "www.google.com"
#factory = StemmerFactory()
#stemmer = factory.create_stemmer()
#listStopword =  set(stopwords.words('indonesian'))
#parse_object = urlparse(text) 
#print(parse_object)
#if parse_object.netloc is not '':
#    print("url")
#else:
#    print("bukan")
#if 'di' in listStopword:
#    print("hapus")
#else:
#    print("jangan")
#print(stemmer.stem('disana'))
#unicode_string = parse_object.path
#encode_string = unicode_string.encode("ascii", "ignore")
#decode_string = encode_string.decode()
#hapus_karakter = re.sub(r'[^\w\s]', ' ', decode_string)
#hapus_karakter2 = hapus_karakter.replace('_', ' ')
#hapus_angka = ''.join([i for i in hapus_karakter  if not i.isdigit()])
#print(hapus_angka)
#tokens = word_tokenize(hapus_angka)
#hasil = []
#for t in tokens:
#    #casefolding
#    casefolding = t.lower()
#    removed = []
#    #stopword
#    if t not in listStopword:
#        removed.append(casefolding)
#        #stemming
#        for r in removed: 
#            hasil.append(stemmer.stem(r))
#print(listStopword)
