# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 20:51:12 2020

@author: MSI
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd 
import time
from nltk.tokenize import sent_tokenize, word_tokenize
from urllib.parse import urlparse


def ParentPage(file, scrap):
    data = pd.read_csv(file)
    data_count = data.Seed_URL.count()
    spasi = " "
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        for s in soup.select('script'):
            s.extract()
        for s in soup.select('style'):
            s.extract()
        pages = soup.find_all('div', attrs={'class':'entry-content'})
        if not pages:
            scrap.append("none")
        else:
            parent_page = []
            for page in pages:
                for s in page.select('div'):
                    s.extract()
                parent_page.append(page.getText())
            scrap.append(spasi.join(parent_page))

    data['Parent'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Parent Page, Data Tersimpan di file " + file )


def AnchorText(file, scrap):
    data = pd.read_csv(file)
    data_count = data.Seed_URL.count()
    spasi = " "
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        for s in soup.select('script'):
            s.extract()
        for s in soup.select('style'):
            s.extract()
        pages = soup.select('div[class~=tags-links] a')
        if not pages:
            pages = soup.find('div', attrs={'class':'gmr-related-post gmr-gallery-related-insidepos'})
            if not pages:
                scrap.append("none")
            else:
                anchor_text = []
                tags = pages.find('a')
                for tag in tags:
                    anchor_text.append(tag.getText())
                scrap.append(spasi.join(anchor_text))
        else:
            anchor_text = []
            for page in pages:
                anchor_text.append(page.getText())
            scrap.append(spasi.join(anchor_text))
            
    data['Anchor'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Anchor Text, Data Tersimpan di file " + file )
                
def SurroundingText(file, scrap):
    def SurroundingAnchor(soup, surround_text):
        pages = soup.select('div[class~=tags-links] a')
        if not pages:
            pages = soup.find('div', attrs={'class':'gmr-related-post gmr-gallery-related-insidepos'})
            if not pages:
                surround_text = ""
                return surround_text
            else:
                tags = pages.find('a')
                for tag in tags:
                    surround_text.append(tag.getText())
                return surround_text
        else:
            for page in pages:
                surround_text.append(page.getText())
            return surround_text
            
        
    data = pd.read_csv(file) 
    data_count = data.Seed_URL.count()
    spasi = " "
    for i in range(data_count):
        url = data.Seed_URL[i]
        parse_object = urlparse(url)
        seed = "https://"+parse_object.netloc
        delete_seed = url.replace(seed, "")
        detele_slash = delete_seed.replace('/', " ")
        tokens = word_tokenize(detele_slash)
        seed_url = seed+tokens[0]
        req_news = requests.get(url)
        soup = BeautifulSoup(req_news.text, "lxml")
        for s in soup.select('script'):
            s.extract()
        for s in soup.select('style'):
            s.extract()
        pages = soup.select('div[class~=tags-links] a')
        if not pages:
            pages = soup.find('div', attrs={'class':'gmr-related-post gmr-gallery-related-insidepos'})
            if not pages:
                scrap.append("none")
            else:
                surround_text = []
                tags = pages.find('a')
                for tag in tags:
                    try:
                        req_tag = requests.get(page.get("href"))
                        print(url.get("href"))
                        soup_tag = BeautifulSoup(req_tag.text, "lxml")
                        surround_anchor = SurroundingAnchor(soup_tag, surround_text)
                    except requests.ConnectionError as e:
                        print("Error Connecting")
                scrap.append(spasi.join(surround_anchor))
        else:
            surround_text = []
            for page in pages:
                try:
                    req_tag = requests.get(page.get("href"))
                    soup_tag = BeautifulSoup(req_tag.text, "lxml")
                    links = soup_tag.find_all('h2', attrs={'class':'entry-title'})
                    for link in links:
                        url = link.find('a')
                        req_link = requests.get(url.get("href"))
                        print(url.get("href"))
                        soup_link = BeautifulSoup(req_link.text, "lxml")
                        surround_anchor = SurroundingAnchor(soup_link, surround_text)
                except requests.ConnectionError as e:
                    print("Error Connecting")
            scrap.append(spasi.join(surround_anchor))
    data['Surrounding'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Surrounding Text, Data Tersimpan di file " + file )
 
def Tahun(file, scrap):
    data = pd.read_csv(file, encoding= 'unicode_escape')
    data_count = data.Seed_URL.count()
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        pages = soup.find('div', attrs={'class':'posted-on'})
        if not pages:
            scrap.append("none")
        else:
            scrap.append(pages.getText())

    data['Tanggal_Publish'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping, Data Tersimpan di file " + file )

           
start_time = time.time()
file = "../dataset/data_proposal/data_training/radarsukabumi.csv" 
scrap = []
#ParentPage(file, scrap)
#AnchorText(file, scrap)
SurroundingText(file, scrap)
#Tahun(file, scrap)
print("--- %s seconds ---" % (time.time() - start_time))