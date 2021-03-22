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
        pages = soup.find_all('div', attrs={'class':'mdk-body-paragraph'})
        if not pages:
            pages = soup.find_all('div', attrs={'class':'body-paragraph'})
            if not pages:
                scrap.append("none")
            else:
                parent_page = []
                for page in pages:
                    parent_page.append(page.getText())
                scrap.append(spasi.join(parent_page))
        else:
            parent_page = []
            for page in pages:
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
        pages = soup.select('ol[class~=mdk-list-terkait] a')
        if not pages:
            pages = soup.select('div[class~=mdk-list-crosslink] a')
            if not pages:
                pages = soup.select('ol[class~=ol-tag] a')
                if not pages:
                    pages = soup.select('ul[class~=list-article-berita ] a')
                    if not pages:
                        scrap.append("none")
                    else:
                        anchor_text = []
                        for page in pages:
                            anchor_text.append(page.getText())
                        scrap.append(spasi.join(anchor_text))
                else:
                    anchor_text = []
                    for page in pages:
                        anchor_text.append(page.getText())
                    scrap.append(spasi.join(anchor_text))
            else:
                anchor_text = []
                for page in pages:
                    anchor_text.append(page.getText())
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
        pages = soup.select('ol[class~=mdk-list-terkait] a')
        if not pages:
            pages = soup.select('div[class~=mdk-list-crosslink] a')
            if not pages:
                pages = soup.select('ol[class~=ol-tag] a')
                if not pages:
                    pages = soup.select('ul[class~=list-article-berita ] a')
                    if not pages:
                        surround_text = ""
                        return surround_text
                    else:
                        for page in pages:
                            surround_text.append(page.getText())
                        return surround_text
                else:
                    for page in pages:
                        surround_text.append(page.getText())
                    return surround_text
            else:
                for page in pages:
                    surround_text.append(page.getText())
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
        pages = soup.select('ol[class~=mdk-list-terkait] a')
        if not pages:
            pages = soup.select('div[class~=mdk-list-crosslink] a')
            if not pages:
                pages = soup.select('ol[class~=ol-tag] a')
                if not pages:
                    scrap.append("none")
                else:
                    surround_text = []
                    for page in pages:
                        req_tag = requests.get(page.get("href"))
                        soup_tag = BeautifulSoup(req_tag.text, "lxml")
                        links = soup_tag.select('div[class~=list-article] a')
                        for link in links:
                            req_link = requests.get("https://bandung.merdeka.com"+link.get("href"))
                            soup_link = BeautifulSoup(req_link.text, "lxml")
                            surround_anchor = SurroundingAnchor(soup_link, surround_text)
                    scrap.append(spasi.join(surround_anchor))
            else:
                surround_text = []
                for page in pages:
                    req_tag = requests.get(page.get("href"))
                    soup_link = BeautifulSoup(req_tag.text, "lxml")
                    surround_anchor = SurroundingAnchor(soup_link, surround_text)
                scrap.append(spasi.join(surround_anchor))
        else:
            surround_text = []
            for page in pages:
                req_tag = requests.get(page.get("href"))
                soup_tag = BeautifulSoup(req_tag.text, "lxml")
                links = soup_tag.select('div[class~=mdk-tag-contg-rb-small] a')
                for link in links:
                    req_link = requests.get("https://www.merdeka.com"+link.get("href"))
                    soup_link = BeautifulSoup(req_link.text, "lxml")
                    surround_anchor = SurroundingAnchor(soup_link, surround_text)
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
        pages = soup.find('span', attrs={'class':'date-post'})
        if not pages:
            scrap.append("none")
        else:
            scrap.append(pages.getText())

    data['Tanggal_Publish'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping, Data Tersimpan di file " + file )

           
start_time = time.time()
file = "../dataset/data_proposal/data_training/merdeka.csv" 
scrap = []
#ParentPage(file, scrap)
#AnchorText(file, scrap)
#SurroundingText(file, scrap)
Tahun(file, scrap)
print("--- %s seconds ---" % (time.time() - start_time))