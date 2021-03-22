# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 10:19:50 2020

@author: MSI
"""

import pandas as pd
from itertools import chain
import numpy as np
import collections
import math
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import time
from urllib.parse import urlparse

def preprocessing(data_url):
    text_pre = []
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    listStopword =  set(stopwords.words('indonesian'))
    website = ['https', 'http', 'www', '_', '.com', '.net', '/sukabumi-update/', '.org', '.co', '.id', 'berita','news', 'travel', 'read',  'html', 'jabar.', 'travel.detik','bali.tribunnews','antaranews', 'beritasatu', 'cnn', 'gatra', 'inews', 'jpnn', 'kontan', 'kumparan', 'liputan6', 'mediaindonesia', 'merdeka', 'okezone', 'pikiranrakyat', 'pikiran-rakyat', 'radarsukabumi', 'republika', 'sindonews', 'tempo', 'tribunnews', 'kompas', 'detik']
    for text in data_url:
        for w in website:
            if w in text:
                text = text.replace(w, ' ')
        hapus_karakter = re.sub(r'[^\w\s]', ' ', text)
        hapus_angka = ''.join([i for i in hapus_karakter  if not i.isdigit()])
        palabuhanratu = ['pelabuhanratu', 'pelabuhan ratu', 'Pelabuhan Ratu']
        for p in palabuhanratu:
            hapus_angka = hapus_angka.replace(p, 'palabuhanratu')
        jawa_barat = ['jabar', 'Jabar']
        for jb in jawa_barat:
            hapus_angka = hapus_angka.replace(jb, 'jawa barat')
        ciletuh = ['cileteuh']
        for c in ciletuh:
            hapus_angka = hapus_angka.replace(c, 'ciletuh')
        geopark_ciletuh = ['geoparkciletuh']
        for gc in geopark_ciletuh:
            hapus_angka = hapus_angka.replace(gc, 'geopark ciletuh')
        tokens = word_tokenize(hapus_angka)
        stemming = []
        for t in tokens:
            #casefolding
            casefolding = t.lower()
            stopword = []
            #stopword
            if t not in listStopword:
                stopword.append(casefolding)
                #stemming
            for r in stopword: 
                stemming.append(stemmer.stem(r))
        text_pre.append(stemming)
    return text_pre

def topic_specific(text):
    DF = {}
    c_text = len(text)
    for i in range(c_text):
        tokens = text[i]
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
    all_key_tfidf = []
    for i in range(c_text):
        tokens = text[i] 
        counter = collections.Counter(tokens)
        key_tfidf = []
        for token in DF:
            tf = counter[token]
            df = doc_freq(token)
            idf = math.log10((c_text)/(df))+1
            tf_idf[token] = tf*idf
            key_tfidf.append(tf_idf[token])
        all_key_tfidf.append(key_tfidf)

    sum_key_tfidf = [sum(x) for x in zip(*all_key_tfidf)]

    bobotmax = max(sum_key_tfidf)
    i = 0
    bobot = {}
    for word in DF:
        bobot[word] = sum_key_tfidf[i]/bobotmax
        i +=1
    items = bobot.items()
    bobot_keyword = sorted(items, key = lambda kv:(kv[1], kv[0]), reverse=True)
    c_bobot_keyword = len(bobot_keyword)
    print("Topic-Specific Geopark Ciletuh  Weight Table")
    print("----------------------------------------------\n")
    print("(Keyword, Bobot)")
    for x in range(c_bobot_keyword):
        print(bobot_keyword[x])



start_time = time.time()
file ="dataset/topic_specific.csv"
data = pd.read_csv(file, encoding= 'unicode_escape')
data_url = data.Seed_URL
prep = preprocessing(data_url)
topic_specific(prep)
