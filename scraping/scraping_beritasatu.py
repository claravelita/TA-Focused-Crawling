# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 02:40:36 2020

@author: MSI
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd 
import time
from newspaper import Article

def ParentPage(file, scrap):
    data = pd.read_csv(file)
    data_count = data.Seed_URL.count()
    spasi = " "
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        for s in soup.select('script'):
            s.extract()
        pages = soup.find_all('div', attrs={'class':'story'})
        if not pages:
            scrap.append("none")
        else:
            berita = []
            for page in pages:
                berita.append(page.getText())
            scrap.append(spasi.join(berita))
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
        pages = soup.find_all('div', attrs={'class':'story'})
        if not pages:
            scrap.append("none")
        else:
            anchor_text = []
            for page in pages:
                tags = page.find_all('a')
                for tag in tags:
                    anchor_text.append(tag.getText())
            scrap.append(spasi.join(anchor_text))
            
    data['Anchor'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scrapping Anchor Text, Data Tersimpan di file " + file )
                
def SurroundingText(file, scrap):
    def SurroundingAnchor(soup, surround_text):
        pages = soup.find_all('div', attrs={'class':'story'})
        if not pages:
            return surround_text
        else:
            for page in pages:
                tags = page.find_all('a')
                for tag in tags:
                    surround_text.append(tag.getText())
            return surround_text
        
    data = pd.read_csv(file) 
    data_count = data.Seed_URL.count()
    spasi = " "
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        print(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        for s in soup.select('script'):
            s.extract()
        pages = soup.find_all('div', attrs={'class':'story'})
        if not pages:
            scrap.append("none")
        else:
            surround_text = []
            for page in pages:
                tags = page.find_all('a')
                for tag in tags:
                    req_tag = requests.get(tag.get("href"))
                    req_link = BeautifulSoup(req_tag.text, "lxml")
                    posts = req_link.find_all('h1')
                    if not posts:
                        surround_anchor = "none"
                    else:
                        for post in posts:
                            urls = post.find('a')
                            if not urls:
                                surround_anchor = "none"
                            else:
                                req_url = requests.get(urls.get("href"))
                                soup_link = BeautifulSoup(req_url.text, "lxml")
                                surround_anchor = SurroundingAnchor(soup_link, surround_text)
            scrap.append(spasi.join(surround_anchor))
            
    data['Surrounding'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scrapping Surrounding Text, Data Tersimpan di file " + file )

def Tahun(file, scrap):
    data = pd.read_csv(file, encoding= 'unicode_escape')
    data_count = data.Seed_URL.count()
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        for s in soup.select('script'):
            s.extract()
        pages = soup.find('p', attrs={'class':'editor'})
        scrap.append(pages.getText())

    data['Tanggal_Publish'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scrapping Tahun, Data Tersimpan di file " + file )

            
start_time = time.time()
file = "../dataset/data_training/beritasatu.csv" 
scrap = []
#ParentPage(file, scrap)
#AnchorText(file, scrap)
#SurroundingText(file, scrap)
Tahun(file, scrap)
print("--- %s seconds ---" % (time.time() - start_time))