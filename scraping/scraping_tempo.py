# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 20:51:12 2020

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
        pages = soup.find_all('div', attrs={'itemprop':'articleBody'})
        if not pages:
            scrap.append("none")
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
        pages = soup.select('div[class~=tags] a')
        if not pages:
            pages = soup.select('div[itemprop~=articleBody] a')
            if not pages:
                pages = soup.find_all('h2', attrs={'class':'title terkait'})
                if not pages:
                    scrap.append("none")
                else:
                    anchor = []
                    for page in pages:
                        anchor.append(page.getText())
                    scrap.append(spasi.join(anchor))
            else:
                anchor = []
                for page in pages:
                    anchor.append(page.getText())
                scrap.append(spasi.join(anchor))
        else:
            anchor = []
            for page in pages:
                if "Info Tempo" in page.getText():
                    another_pages = soup.find_all('h2', attrs={'class':'title terkait'})
                    if not another_pages:
                        scrap.append("none")
                    else:
                        anchor = []
                        for another_page in another_pages:
                            anchor.append(another_page.getText())
                else:
                    anchor.append(page.getText())
            scrap.append(spasi.join(anchor))
            
    data['Anchor'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Anchor Text, Data Tersimpan di file " + file )
                
def SurroundingText(file, scrap):
    def SurroundingAnchor(soup, surround):
        pages = soup.select('div[class~=tags] a')
        if not pages:
            pages = soup.select('div[itemprop~=articleBody] a')
            if not pages:
                pages = soup.find_all('h2', attrs={'class':'title terkait'})
                if not pages:
                    surround = ""
                    return surround
                else:
                    for page in pages:
                        surround.append(page.getText())
                    return surround
            else:
                for page in pages:
                    surround.append(page.getText())
                return surround
        else:
            for page in pages:
                if "Info Tempo" in page.getText():
                    another_pages = soup.find_all('h2', attrs={'class':'title terkait'})
                    if not another_pages:
                        surround = ""
                    else:
                        for another_page in another_pages:
                            surround.append(another_page.getText())
                else:
                    surround.append(page.getText())
            return surround
            
        
    data = pd.read_csv(file) 
    data_count = data.Seed_URL.count()
    spasi = " "
    for i in range(data_count):
        try:
            req_news = requests.get(data.Seed_URL[i])
            soup = BeautifulSoup(req_news.text, "lxml")
            for s in soup.select('script'):
                s.extract()
            for s in soup.select('style'):
                s.extract()
            pages = soup.select('div[class~=tags] a')
            if not pages:
                pages = soup.select('a[class~=col terkait] h2')
                if not pages:
                    scrap.append("none")
                else:
                    surround = []
                    for page in pages:
                        req_tag = requests.get(page.get("href"))
                        soup_link = BeautifulSoup(req_tag.text, "lxml")
                        surround_anchor = SurroundingAnchor(soup_link, surround)
                    scrap.append(spasi.join(surround_anchor))
            else:
                surround = []
                for page in pages:
                    if "Info Tempo" in page.get("href"):
                        another_pages = soup.select('a[class~=col terkait]')
                        if not another_pages:
                            surround_anchor = ""
                        else:
                            for another_page in another_pages:
                                req_link = requests.get(another_page.get("href"))
                                soup_link = BeautifulSoup(req_link.text, "lxml")
                                surround_anchor = SurroundingAnchor(soup_link, surround)
                    else:
                        req_tag = requests.get(page.get("href"))
                        soup_tag = BeautifulSoup(req_tag.text, "lxml")
                        links = soup_tag.select('section.list a.col')
                        for link in links:
                            req_link = requests.get(link.get("href"))
                            soup_link = BeautifulSoup(req_link.text, "lxml")
                            surround_anchor = SurroundingAnchor(soup_link, surround)
                scrap.append(spasi.join(surround_anchor))
        except requests.ConnectionError as e:
            print("Error Connecting")
    data['Surrounding'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Surrounding Text, Data Tersimpan di file " + file )
  
def Tahun(file, scrap):
    data = pd.read_csv(file, encoding= 'unicode_escape')
    data_count = data.Seed_URL.count()
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        pages = soup.find('span', attrs={'itemprop':'datePublished'})
        if not pages:
            scrap.append("none")
        else:
            scrap.append(pages.getText())

    data['Tanggal_Publish'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping, Data Tersimpan di file " + file )
            
          
start_time = time.time()
file = "../dataset/data_proposal/data_training/tempo.csv" 
scrap = []
#ParentPage(file, scrap)
#AnchorText(file, scrap)
#SurroundingText(file, scrap)
Tahun(file, scrap)
print("--- %s seconds ---" % (time.time() - start_time))