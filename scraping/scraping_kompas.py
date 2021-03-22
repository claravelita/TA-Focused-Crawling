# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 13:05:04 2020

@author: MSI
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd 
import time
from newspaper import Article
from requests.exceptions import MissingSchema

def ParentPage(file, scrap):
    data = pd.read_csv(file)
    data_count = data.Seed_URL.count()
    for i in range(data_count):
        try:
            req_news = requests.get(data.Seed_URL[i])
            soup = BeautifulSoup(req_news.text, "lxml")
            for s in soup.select('script'):
                s.extract()
            for s in soup.select('style'):
                s.extract()
            pages = soup.find('div', attrs={'class':'read__content'}) 
            if not pages:
                pages = soup.find('div', attrs={'class':'main-artikel-paragraf'}) 
                if not pages:
                    pages = soup.find('div', attrs={'class':'articleRead'}) 
                    if not pages:
                        pages = soup.find('div', attrs={'class':'read__article'}) 
                        if not pages:
                            pages = soup.find('div', attrs={'class':'articleContent'})
                            if not pages:
                                scrap.append("none")
                            else:
                                parent_page = pages.getText()
                                scrap.append(parent_page)
                        else:
                            parent_page = pages.getText()
                            scrap.append(parent_page)
                    else:
                        parent_page = pages.getText()
                        scrap.append(parent_page)
                else:
                    parent_page = pages.getText()
                    scrap.append(parent_page)
            else:
                parent_page = pages.getText()
                scrap.append(parent_page)
        except requests.ConnectionError as e:
            scrap.append("none")

    data['Parent'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Parent Page, Data Tersimpan di file " + file )


def AnchorText(file, scrap):
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
            pages = soup.find_all('a', attrs={'class':'inner-link-tag'})
            if not pages:
                pages = soup.find_all('a', attrs={'class':'tag__article__link'})
                if not pages:
                    pages = soup.find_all('a', attrs={'class':'inner-link-baca-juga'})
                    if not pages:
                        pages = soup.select('h4[class~=related__inline__title] a')
                        if not pages:
                            pages = soup.find_all('a', attrs={'class':'inner-link'})
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
                    anchor.append(page.getText())
                scrap.append(spasi.join(anchor))
        except requests.ConnectionError as e:
            scrap.append("none")
            
    data['Anchor'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Anchor Text, Data Tersimpan di file " + file )
                
def SurroundingText(file, scrap):
    def SurroundingAnchor(soup, surround):
        pages = soup.find_all('a', attrs={'class':'inner-link-tag'})
        if not pages:
            pages = soup.find_all('a', attrs={'class':'tag__article__link'})
            if not pages:
                pages = soup.find_all('a', attrs={'class':'inner-link-baca-juga'})
                if not pages:
                    pages = soup.select('h4[class~=related__inline__title] a')
                    if not pages:
                        pages = soup.find_all('a', attrs={'class':'inner-link'})
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
                        surround.append(page.getText())
                    return surround
            else:
                for page in pages:
                    surround.append(page.getText())
                return surround
        else:
            for page in pages:
                surround.append(page.getText())
            return surround

    data = pd.read_csv(file, encoding= 'unicode_escape') 
    data_count = data.Seed_URL.count()
    spasi = " "
    for i in range(data_count):
        print(i)
        try:
            req_news = requests.get(data.Seed_URL[i])
            soup = BeautifulSoup(req_news.text, "lxml")
            for s in soup.select('script'):
                s.extract()
            for s in soup.select('style'):
                s.extract()
            pages = soup.find_all('a', attrs={'class':'inner-link-tag'})
            if not pages:
                pages = soup.find_all('a', attrs={'class':'tag__article__link'})
                if not pages:
                    pages = soup.find_all('a', attrs={'class':'inner-link-baca-juga'})
                    if not pages:
                        pages = soup.select('h4[class~=related__inline__title] a')
                        if not pages:
                            pages = soup.find_all('a', attrs={'class':'inner-link'})
                            if not pages:
                                scrap.append("none")
                            else:
                                surround = []
                                for page in pages:
                                    try:
                                        req_tag = requests.get(page.get("href"))
                                        soup_link = BeautifulSoup(req_tag.text, "lxml")
                                        surround_anchor = SurroundingAnchor(soup_link, surround)
                                    except requests.ConnectionError as e:
                                        surround_anchor = ""
                                    except MissingSchema:
                                        surround_anchor = ""
                                scrap.append(spasi.join(surround_anchor))
                        else:
                            surround = []
                            for page in pages:
                                try:
                                    req_tag = requests.get(page.get("href"))
                                    soup_link = BeautifulSoup(req_tag.text, "lxml")
                                    surround_anchor = SurroundingAnchor(soup_link, surround)
                                except requests.ConnectionError as e:
                                    surround_anchor = ""
                                except MissingSchema:
                                    surround_anchor = ""
                            scrap.append(spasi.join(surround_anchor))
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
                        try:
                            req_tag = requests.get(page.get("href"))
                            soup_tag = BeautifulSoup(req_tag.text, "lxml")
                            links = soup_tag.find_all('a', attrs={'class':'article__link'})
                            for link in links:
                                try:
                                    req_link = requests.get(link.get("href"))
                                    soup_link = BeautifulSoup(req_link.text, "lxml")
                                    surround_anchor = SurroundingAnchor(soup_link, surround)
                                except requests.ConnectionError as e:
                                    surround_anchor = ""
                                except MissingSchema:
                                    surround_anchor = ""
                        except requests.ConnectionError as e:
                            surround_anchor = ""
                        except MissingSchema:
                            surround_anchor = ""
                    scrap.append(spasi.join(surround_anchor))
            else:
                surround = []
                for page in pages:
                    try:
                        req_tag = requests.get(page.get("href"))
                        soup_tag = BeautifulSoup(req_tag.text, "lxml")
                        links = soup_tag.find_all('a', attrs={'class':'article__link'})
                        for link in links:
                            try:
                                req_link = requests.get(link.get("href"))
                                soup_link = BeautifulSoup(req_link.text, "lxml")
                                surround_anchor = SurroundingAnchor(soup_link, surround)
                            except requests.ConnectionError as e:
                                surround_anchor = ""
                            except MissingSchema:
                                surround_anchor = ""
                    except requests.ConnectionError as e:
                        surround_anchor = ""
                    except MissingSchema:
                        surround_anchor = ""
                scrap.append(spasi.join(surround_anchor))
        except requests.ConnectionError as e:
            scrap.append("none")
        except MissingSchema:
            scrap.append("none")
    data['Surrounding'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Surrounding Text, Data Tersimpan di file " + file )
 
def Tahun(file, scrap):
    data = pd.read_csv(file, encoding= 'unicode_escape')
    data_count = data.Seed_URL.count()
    for i in range(data_count):
        try:
            article = Article(data.Seed_URL[i])
            article.download()
            article.parse()
            scrap.append(article.publish_date)
        except:
            scrap.append("none")
    data['Tanggal_Publish'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping, Data Tersimpan di file " + file )

              
start_time = time.time()
file = "../dataset/data_testing/kompas.csv" 
scrap = []
#ParentPage(file, scrap)
#AnchorText(file, scrap)
#SurroundingText(file, scrap)
Tahun(file, scrap)
print("--- %s seconds ---" % (time.time() - start_time))