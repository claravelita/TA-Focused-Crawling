# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 20:50:15 2020

@author: MSI
"""

import pandas as pd
import numpy as np
import collections
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import time
from urllib.parse import urlparse
import validators

def preprocessing(data_param, dataset_wordbank): 
    wordbank = dataset_wordbank.read().split('\n')
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    listStopword =  set(stopwords.words('indonesian'))
    remove_enter = re.compile('\n')
    remove_char = re.compile('[^\w\s]')
    remove_tab = re.compile('\t')
    text_pre = []
     
    for text in data_param:
        url_validator = validators.url(str(text))
        if url_validator==True:
            parse_object = urlparse(text)
            text = parse_object.path
            for w in wordbank:
                if w in text:
                    text = text.replace(w, " ")
            text = re.sub(r"d-[0-9]?", " ", str(text))
        else:
            text = re.sub(remove_enter, " ", str(text))
            text = re.sub(remove_tab, " ", str(text))
            encoded_string = text.encode("ascii", "ignore")
            text = encoded_string.decode()
        text = re.sub(remove_char, " ", str(text))
        text = ''.join([i for i in text if not i.isdigit()])
        jawa_barat = ['jabar', 'Jabar']
        for jb in jawa_barat:
            text = text.replace(jb, 'jawa barat')
        palabuhanratu = ['pelabuhanratu', 'Pelabuhanratu', 'Palabuanratu', 'pelabuhan ratu', 'Pelabuhan Ratu', 'Palabuhan Ratu', 'palabuhan ratu', 'pelabuanratu', 'Pelabuanratu', 'palabuanratu']
        for p in palabuhanratu:
            text = text.replace(p, 'palabuhanratu')
        geopark = ['Geoparks', 'geoparks']
        for g in geopark:
            text = text.replace(g, 'geopark')
        ciletuh = ['cileteuh', 'cileteh', 'Cileteuh', 'Cileteh']
        for c in ciletuh:
            text = text.replace(c, 'ciletuh')
        geopark_ciletuh = ['geoparkciletuh', 'ciletuhgeopark', 'Geoparkciletuh', 'Ciletuhgeopark', 'GeoparkCiletuh', 'CiletuhGeopark', 'GeoparksCiletuh', 'geoparksciletuh']
        for gc in geopark_ciletuh:
            text = text.replace(gc, 'geopark ciletuh')
        ciletuh_pugg = ['cpugg', 'CPUGG', 'CPUGGp','cpuggp']
        for cpugg in ciletuh_pugg:
            text = text.replace(cpugg, 'ciletuh palabuhanratu unesco global geopark')
        unesco_gg = ['ugg', 'UGG', 'uggp', 'UGGp']
        for ugg in unesco_gg:
            text = text.replace(ugg, 'unesco global geopark')
    
        tokens = word_tokenize(text)
        stemming = []
        for t in tokens:
            #casefolding
            casefolding = t.lower()
            removed = []
            #stopword
            if t not in listStopword:
                removed.append(casefolding)
                #stemming
            for r in removed: 
                stemming.append(stemmer.stem(r))
        text_pre.append(stemming)
    return text_pre
    
def page_relevance(data, text_pre, topicspecific):
    DF = {}
    c_text = len(text_pre)
    for i in range(c_text):
        tokens = text_pre[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}
                
    for i in DF:
        DF[i] = len(DF[i])

    def doc_freq(word):
        c = 0
        try:
            c = DF[word]
        except:
            pass
        return c
        
    tf_idf = {}
    cosine = []
    for i in range(c_text):
        tokens = text_pre[i]
        counter = collections.Counter(tokens)
        words_count = len(tokens)
        key_tfidf = []
        for token in DF:
            try:
                tf = counter[token]/words_count
            except ZeroDivisionError:
                tf = counter[token]
            df = doc_freq(token)
            idf = math.log10((c_text)/(df))
            tf_idf[token] = tf*idf
            key_tfidf.append(tf_idf[token])
            
        topic = {}
        for t in topicspecific:
            if t in DF:
                topic[t] = tf_idf[t]
            else:
                topic[t] = 0.0
                
        topicword = {}
        for key, value in topic.items():
            if value==0.0:
                topicword[key] = 0.0
            else:
                topicword[key] = topicspecific[key]
        
        tswt=list(topicspecific.values())
        twt=list(topicword.values())
        if(all(v == 0 for v in twt)):
            val = 0
            cosine.append(val)
        else:
            dot = np.dot(tswt, twt)
            norma = np.linalg.norm(tswt)
            normb = np.linalg.norm(twt)
            cos = dot/(norma*normb)
            val = '%.2f'%(cos)
            cosine.append(val)
    return cosine


def url_word(dataset, data, dataset_wordbank, topicspecific):
    data_param = data.Seed_URL
    text_pre = preprocessing(data_param, dataset_wordbank)
    cal_page_relevance = page_relevance(data, text_pre, topicspecific)
    data['URL_Word'] = cal_page_relevance 
    data.to_csv(dataset, index=False)
    print("Berhasil melakukan perhitungan Page Relevance URL Word, Data Tersimpan di file " + dataset )
         
def parent_page(dataset, data, dataset_wordbank, topicspecific):
    data_param = data.Parent
    text_pre = preprocessing(data_param, dataset_wordbank)
    cal_page_relevance = page_relevance(data, text_pre, topicspecific)
    data['Parent_Page'] = cal_page_relevance 
    data.to_csv(dataset, index=False)
    print("Berhasil melakukan perhitungan Page Relevance Parent Page, Data Tersimpan di file " + dataset )

def anchor_text(dataset, data, dataset_wordbank, topicspecific):
    data_param = data.Anchor
    text_pre = preprocessing(data_param, dataset_wordbank)
    cal_page_relevance = page_relevance(data, text_pre, topicspecific)
    data['Anchor_Text'] = cal_page_relevance 
    data.to_csv(dataset, index=False)
    print("Berhasil melakukan perhitungan Page Relevance Anchor Text, Data Tersimpan di file " + dataset )

def surrounding_text(dataset, data, dataset_wordbank, topicspecific):
    data_param = data.Surrounding
    text_pre = preprocessing(data_param, dataset_wordbank)
    cal_page_relevance = page_relevance(data, text_pre, topicspecific)
    data['Surrounding_Text'] = cal_page_relevance 
    data.to_csv(dataset, index=False)
    print("Berhasil melakukan perhitungan Page Relevance Surrounding Text, Data Tersimpan di file " + dataset )

start_time = time.time() 
#dataset ="dataset/data_proposal/data_training/data_training.csv"
#dataset ="dataset/data_proposal/data_testing/detik.csv"
dataset ="dataset/data_proposal/data_testing/kompas.csv"
data = pd.read_csv(dataset, encoding= 'unicode_escape')   
dataset_wordbank = open("dataset/wordbank.txt")

#topicspecific = {'geopark': 1.0, 
#                     'ciletuh': 0.74, 
#                     'kawasan': 0.57,
#                     'taman': 0.51, 
#                     'palabuhanratu': 0.51, 
#                     'bumi': 0.51,
#                     'alam': 0.51, 
#                     'sukabumi': 0.48, 
#                     'nasional': 0.44,
#                     'wisata': 0.41}


topicspecific = {'ciletuh': 1.0, 
                 'geopark': 0.92, 
                 'sukabumi': 0.69,
                 'palabuhanratu': 0.57, 
                 'wisata': 0.35, 
                 'jawa': 0.35,
                 'unesco': 0.28, 
                 'taman': 0.28, 
                 'bumi': 0.28,
                 'barat': 0.28}



#url_word(dataset, data, dataset_wordbank, topicspecific)
#parent_page(dataset, data, dataset_wordbank, topicspecific)
#anchor_text(dataset, data, dataset_wordbank, topicspecific)
surrounding_text(dataset, data, dataset_wordbank, topicspecific)
print("--- %s seconds ---" % (time.time() - start_time))  