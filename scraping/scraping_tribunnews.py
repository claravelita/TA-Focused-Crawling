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
        pages = soup.select('div[class~=txt-article] p')
        if not pages:
            pages = soup.find('div', attrs={'class':'side-article txt-article'})
            if not pages:
                scrap.append("none")
            else:
                scrap.append(pages.getText())
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
        pages = soup.select('div.txt-article p a')
        if not pages:
            pages = soup.select('h5[class~=tagcloud3] a')
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
            
    data['Anchor'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Anchor Text, Data Tersimpan di file " + file )
                
def SurroundingText(file, scrap):
    def SurroundingAnchor(soup, surround):
        pages = soup.select('div.txt-article p a')
        if not pages:
            pages = soup.select('h5[class~=tagcloud3] a')
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
        pages = soup.select('div.txt-article p a')
        if not pages:
            pages = soup.select('h5[class~=tagcloud3] a')
            if not pages:
                scrap.append("none")
            else:
                surround = []
                for page in pages:
                    if "http" not in page.get("href"):
                        req_tag = requests.get("http:"+page.get("href"))
                    else:
                        req_tag = requests.get(page.get("href"))
                    soup_tag = BeautifulSoup(req_tag.text, "lxml")
                    links = soup_tag.find_all('div', attrs={'class':'fr mt3 pos_rel'})
                    for link in links:
                        href = link.find('a')
                        link_tag = href.get("href")
                        if "http" not in link_tag:
                            new_href = "http:"+link_tag
                        else:
                            new_href = link_tag
                        try:
                            req_link = requests.get(new_href)
                            soup_link = BeautifulSoup(req_link.text, "lxml")
                            surround_anchor = SurroundingAnchor(soup_link, surround)
                        except requests.ConnectionError as e:
                            print("Error Connecting")
                scrap.append(spasi.join(surround_anchor))
        else:
            surround = []
            for page in pages:
                link_tag = page.get("href")
                if "http" not in link_tag:
                    new_href = "http:"+link_tag
                else:
                    new_href = link_tag
                try:
                    req_tag = requests.get(new_href)
                    soup_tag = BeautifulSoup(req_tag.text, "lxml")
                    links = soup_tag.find_all('div', attrs={'class':'fr mt3 pos_rel'})
                    for link in links:
                        href = link.find('a')
                        if "http" not in href.get("href"):
                            req_link = requests.get("http:"+href.get("href"))
                        else:
                            req_link = requests.get(href.get("href"))
                        soup_link = BeautifulSoup(req_link.text, "lxml")
                        surround_anchor = SurroundingAnchor(soup_link, surround)
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
        pages = soup.find('div', attrs={'id':'article'})
        if not pages:
            scrap.append("none")
        else:
            page = pages.find('time')
            scrap.append(page.getText())

    data['Tanggal_Publish'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping, Data Tersimpan di file " + file )
          
           
start_time = time.time()
file = "../dataset/data_proposal/data_training/tribunnews.csv" 
scrap = []
#ParentPage(file, scrap)
#AnchorText(file, scrap)
#SurroundingText(file, scrap)
Tahun(file, scrap)
print("--- %s seconds ---" % (time.time() - start_time))