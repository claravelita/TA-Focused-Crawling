# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 13:05:04 2020

@author: MSI
"""


from bs4 import BeautifulSoup
import requests
import pandas as pd 
import time

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
        pages = soup.find('div', attrs={'class':'article-content-body__item-content'})
        if not pages:
            scrap.append("none")
        else:
            parent_page = []
            for s in pages.select('div'):
                s.extract()
            tags = pages.find_all('p')
            for tag in tags:
                parent_page.append(tag.getText())
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
        pages = soup.find_all('a', attrs={'class':'tags--snippet__link'})
        if not pages:
            scrap.append("none")
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
        pages = soup.find_all('a', attrs={'class':'tags--snippet__link'})
        if not pages:
            surround_text = ""
            return surround_text
        else:
            for page in pages:
                surround_text.append(page.getText())
            return surround_text
            
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
        pages = soup.find_all('a', attrs={'class':'tags--snippet__link'})
        if not pages:
            scrap.append("none")
        else:
            surround_text = []
            for page in pages:
                req_tag = requests.get(page.get("href"))
                soup_tag = BeautifulSoup(req_tag.text, "lxml")
                links = soup_tag.find_all('a', attrs={'class':'articles--iridescent-list--text-item__title-link'})
                for link in links:
                    req_link = requests.get(link.get("href"))
                    soup_link = BeautifulSoup(req_link.text, "lxml")
                    surround_anchor = SurroundingAnchor(soup_link, surround_text)
            scrap.append(spasi.join(surround_anchor))
    data['Surrounding'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan scrap Surrounding Text, Data Tersimpan di file " + file )

def Tahun(file, scrap):
    data = pd.read_csv(file, encoding= 'unicode_escape')
    data_count = data.Seed_URL.count()
    spasi = " "
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        pages = soup.find_all('time', attrs={'itemprop':'datePublished'})
        if not pages:
            scrap.append("none")
        else:
            parent_page = []
            for page in pages:
                parent_page.append(page.getText())
            scrap.append(spasi.join(parent_page))

    data['Tanggal_Publish'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping, Data Tersimpan di file " + file )

            
start_time = time.time()
file = "../dataset/data_proposal/data_training/liputan6.csv" 
scrap = []
#ParentPage(file, scrap)
#AnchorText(file, scrap)
#SurroundingText(file, scrap)
Tahun(file, scrap)
print("--- %s seconds ---" % (time.time() - start_time))