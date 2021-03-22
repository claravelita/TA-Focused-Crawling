# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 20:51:12 2020

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
    scrap = []
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        for s in soup.select('script'):
            s.extract()
        for s in soup.select('style'):
            s.extract()
        pages = soup.find('div', attrs={'class':'detail_text'})
        if not pages:
            pages = soup.find('div', attrs={'class':'content_detail'})
            if not pages:
                scrap.append("none")
            else:
                page = pages.find('span')
                scrap.append(page.getText())
        else:
            scrap.append(pages.getText())

    data['Parent'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Parent Page, Data Tersimpan di file " + file )


def AnchorText(file, scrap):
    data = pd.read_csv(file, encoding= 'unicode_escape')
    data_count = data.Seed_URL.count()
    spasi = " "
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        for s in soup.select('script'):
            s.extract()
        pages = soup.select('div.detail_text strong a')
        if not pages:
            pages = soup.select('div.detail_tag a')
            if not pages:
                pages = soup.find_all('a', attrs={'class':'gtm_baca_juga'})
                if not pages:
                    pages = soup.find('div', attrs={'class':'list-topik-terkait'})
                    if not pages:
                        pages = soup.find('table', attrs={'class':'topiksisip'})
                        if not pages:
                            scrap.append("none")
                        else:
                            anchor_text = []
                            tags = pages.find_all('a')
                            for tag in tags:
                                anchor_text.append(tag.getText())
                            scrap.append(spasi.join(anchor_text))
                    else:
                        scrap.append(pages.get("name"))
                else:
                    anchor_text = []
                    for page in pages:
                        tags = page.find('h2')
                        anchor_text.append(tags.getText())
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
        pages = soup.select('div.detail_text strong a')
        if not pages:
            pages = soup.select('div.detail_tag a')
            if not pages:
                pages = soup.find_all('a', attrs={'class':'gtm_baca_juga'})
                if not pages:
                    pages = soup.find('div', attrs={'class':'list-topik-terkait'})
                    if not pages:
                        pages = soup.find('table', attrs={'class':'topiksisip'})
                        if not pages:
                            surround_text = ""
                            return surround_text
                        else:
                            tags = pages.find_all('a')
                            for tag in tags:
                                surround_text.append(tag.getText())
                            return surround_text
                    else:
                        surround_text.append(pages.getText())
                        return surround_text
                else:
                    for page in pages:
                        tags = page.find('h2')
                        surround_text.append(tags.getText())
                    return surround_text
            else:
                for page in pages:
                    surround_text.append(page.getText())
                return surround_text
        else:
            for page in pages:
                surround_text.append(page.getText())
            return surround_text
        
    data = pd.read_csv(file, encoding= 'unicode_escape')
    data_count = data.Seed_URL.count()
    spasi = " "
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        for s in soup.select('script'):
            s.extract()
        for s in soup.select('style'):
            s.extract()
        pages = soup.select('div.detail_text strong a')
        if not pages:
            pages = soup.select('div.detail_tag a')
            if not pages:
                pages = soup.find_all('a', attrs={'class':'gtm_baca_juga'})
                if not pages:
                    pages = soup.find('div', attrs={'class':'list-topik-terkait'})
                    if not pages:
                        pages = soup.find('table', attrs={'class':'topiksisip'})
                        if not pages:
                            scrap.append("none")
                        else:
                            surround_text = []
                            tags = pages.find_all('a')
                            for tag in tags:
                                try:
                                    req_tag = requests.get(tag.get("href"))
                                    soup_tag = BeautifulSoup(req_tag.text, "lxml")
                                    for s in soup_tag.select('script'):
                                        s.extract()
                                    for s in soup_tag.select('style'):
                                        s.extract()
                                    surround_anchor = SurroundingAnchor(soup_tag, surround_text)
                                except requests.ConnectionError as e:
                                    surround_anchor = ""
                            scrap.append(spasi.join(surround_anchor))
                    else:
                        surround_text = []
                        tags = pages.find_all('a')
                        for tag in tags:
                            try:
                                req_tag = requests.get("https://www.cnnindonesia.com"+tag.get("href"))
                                soup_tag = BeautifulSoup(req_tag.text, "lxml")
                                for s in soup_tag.select('script'):
                                    s.extract()
                                for s in soup_tag.select('style'):
                                    s.extract()
                                links = soup_tag.select('article a')
                                for link in links:
                                    try:
                                        req_link = requests.get(link.get("href"))
                                        soup_link = BeautifulSoup(req_link.text, "lxml")
                                        for s in soup_link.select('script'):
                                            s.extract()
                                        for s in soup_link.select('style'):
                                            s.extract()
                                        surround_anchor = SurroundingAnchor(soup_link, surround_text)
                                    except requests.ConnectionError as e:
                                        surround_anchor = ""
                            except requests.ConnectionError as e:
                                surround_anchor = ""
                        scrap.append(spasi.join(surround_anchor))
                else:
                    surround_text = []
                    for page in pages:
                        try:
                            req_tag = requests.get(page.get("href"))
                            soup_tag = BeautifulSoup(req_tag.text, "lxml")
                            for s in soup_tag.select('script'):
                                s.extract()
                            for s in soup_tag.select('style'):
                                s.extract()
                            surround_anchor = SurroundingAnchor(soup_tag, surround_text)
                        except requests.ConnectionError as e:
                            surround_anchor = ""
                    scrap.append(spasi.join(surround_anchor))
            else:
                surround_text = []
                for page in pages:
                    try:
                        req_tag = requests.get(page.get("href"))
                        soup_tag = BeautifulSoup(req_tag.text, "lxml")
                        links = soup_tag.select('div.list article a')
                        for link in links:
                            try:
                                req_link = requests.get(link.get("href"))
                                soup_link = BeautifulSoup(req_link.text, "lxml")
                                for s in soup_link.select('script'):
                                    s.extract()
                                for s in soup_link.select('style'):
                                    s.extract()
                                surround_anchor = SurroundingAnchor(soup_link, surround_text)
                            except requests.ConnectionError as e:
                                surround_anchor = ""
                    except requests.ConnectionError as e:
                        surround_anchor = ""
                scrap.append(spasi.join(surround_anchor))
        else:
            surround_text = []
            for page in pages:
                try:
                    req_tag = requests.get(page.get("href"))
                    soup_tag = BeautifulSoup(req_tag.text, "lxml")
                    links = soup_tag.select('div.list article a')
                    for link in links:
                        try:
                            req_link = requests.get(link.get("href"))
                            soup_link = BeautifulSoup(req_link.text, "lxml")
                            for s in soup_link.select('script'):
                                s.extract()
                            for s in soup_link.select('style'):
                                s.extract()
                            surround_anchor = SurroundingAnchor(soup_link, surround_text)
                        except requests.ConnectionError as e:
                            surround_anchor = ""
                except requests.ConnectionError as e:
                    surround_anchor = ""
            scrap.append(spasi.join(surround_anchor))
    data['Surrounding'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Surrounding Text, Data Tersimpan di file " + file )
            
def Tahun(file, scrap):
    data = pd.read_csv(file, encoding= 'unicode_escape')
    data_count = data.Seed_URL.count()
    for i in range(data_count):
        article = Article(data.Seed_URL[i])
        article.download()
        article.parse()
        scrap.append(article.publish_date)

    data['Tanggal_Publish'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping, Data Tersimpan di file " + file )

            
start_time = time.time()
file = "../dataset/data_training/cnn.csv" 
scrap = []
#ParentPage(file, scrap)
#AnchorText(file, scrap)
#SurroundingText(file, scrap)
Tahun(file, scrap)
print("--- %s seconds ---" % (time.time() - start_time))