# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 20:51:12 2020

@author: MSI
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import time
from urllib.parse import urlparse
from newspaper import Article

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
            pages = soup.find('div', attrs={'id':'detikdetailtext'}) 
            if not pages:
                pages = soup.find('div', attrs={'class':'detail__body-text'}) 
                if not pages:
                    pages = soup.find('div', attrs={'class':'read__content'})
                    if not pages:
                        pages = soup.find('div', attrs={'class':'parallax_detail'})
                        if not pages:
                            pages = soup.find('div', attrs={'class':'detail_text'})
                            if not pages:
                                scrap.append("none")
                            else:
                                for s in pages.select('div[class~=embedvideo]'):
                                    s.extract()
                                for s in pages.select('div[class~=date]'):
                                    s.extract()
                                scrap.append(pages.getText())
                        else:
                            scrap.append(pages.getText())
                    else:
                        for s in pages.select('div[class~=detail_tag]'):
                            s.extract()
                        scrap.append(pages.getText())
                else:
                    for s in pages.select('div[class~=detail__body-tag]'):
                        s.extract()
                    for s in pages.select('table[class~=linksisip]'):
                        s.extract()
                    scrap.append(pages.getText())
            else:
                for s in pages.select('div[class~=detail_tag]'):
                    s.extract()
                for s in pages.select('table[class~=linksisip]'):
                    s.extract()
                scrap.append(pages.getText())
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
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        for s in soup.select('script'):
            s.extract()
        for s in soup.select('style'):
            s.extract()
        pages = soup.select('div[id~=detikdetailtext] a') 
        if not pages:
            pages = soup.select('div[class~=detail_tag] a')  
            if not pages:
                pages = soup.select('div[class~=detail__body-tag] a')
                if not pages:
                    pages = soup.select('article[class~=list-content__item] a') 
                    if not pages:
                        pages = soup.select('div[class~=list__terkait] a')
                        if not pages:
                            pages = soup.select('a[class~=gtm_beritaterkait_artikel] h2')
                            if not pages:
                                pages = soup.select('div[class~=detail] a')
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
        pages = soup.select('div[id~=detikdetailtext] a') 
        if not pages:
            pages = soup.select('div[class~=detail_tag] a')  
            if not pages:
                pages = soup.select('div[class~=detail__body-tag] a')
                if not pages:
                    pages = soup.select('article[class~=list-content__item] a') 
                    if not pages:
                        pages = soup.select('div[class~=list__terkait] a')
                        if not pages:
                            pages = soup.select('a[class~=gtm_beritaterkait_artikel] h2')
                            if not pages:
                                pages = soup.select('div[class~=detail] a')
                                if not pages:
                                    surround.append("none")
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
        print(i+1)
        try:
            req_news = requests.get(data.Seed_URL[i])
            soup = BeautifulSoup(req_news.text, "lxml")
            for s in soup.select('script'):
                    s.extract()
            for s in soup.select('style'):
                    s.extract()
            pages = soup.select('div[id~=detikdetailtext] a') 
            if not pages:
                pages = soup.select('div[class~=detail_tag] a')  
                if not pages:
                    pages = soup.select('div[class~=detail__body-tag] a')
                    if not pages:
                        pages = soup.select('article[class~=list-content__item] a') 
                        if not pages:
                            pages = soup.select('div[class~=list__terkait] a')
                            if not pages:
                                pages = soup.select('a[class~=gtm_beritaterkait_artikel]')
                                if not pages:
                                    pages = soup.select('div[class~=detail] a')
                                    if not pages:
                                        scrap.append("none")
                                    else:
                                        surround = []
                                        for page in pages:
                                            if urlparse(page.get("href")).netloc is '' or 'None':
                                                surround_anchor = ""
                                            else:
                                                try:
                                                    req_tag = requests.get(page.get("href"))
                                                    soup_link = BeautifulSoup(req_tag.text, "lxml")
                                                    surround_anchor = SurroundingAnchor(soup_link, surround)
                                                except requests.ConnectionError as e:
                                                    surround_anchor = ""
                                        scrap.append(spasi.join(surround_anchor))
                                else:
                                    surround = []
                                    for page in pages:
                                        if urlparse(page.get("href")).netloc is '' or 'None':
                                            surround_anchor = ""
                                        else:
                                            try:
                                                req_tag = requests.get(page.get("href"))
                                                soup_link = BeautifulSoup(req_tag.text, "lxml")
                                                surround_anchor = SurroundingAnchor(soup_link, surround)
                                            except requests.ConnectionError as e:
                                                surround_anchor = ""
                                    scrap.append(spasi.join(surround_anchor))
                            else:
                                surround = []
                                for page in pages:
                                    if urlparse(page.get("href")).netloc is ''  or 'None':
                                        surround_anchor = ""
                                    else:
                                        try:
                                            req_tag = requests.get(page.get("href"))
                                            soup_link = BeautifulSoup(req_tag.text, "lxml")
                                            surround_anchor = SurroundingAnchor(soup_link, surround)
                                        except requests.ConnectionError as e:
                                            surround_anchor = ""
                                scrap.append(spasi.join(surround_anchor))
                        else:
                            surround = []
                            for page in pages:
                                if urlparse(page.get("href")).netloc is ''  or None:
                                    surround_anchor = ""
                                else:
                                    try:
                                        req_tag = requests.get(page.get("href"))
                                        soup_link = BeautifulSoup(req_tag.text, "lxml")
                                        surround_anchor = SurroundingAnchor(soup_link, surround)
                                    except requests.ConnectionError as e:
                                        surround_anchor = ""
                            scrap.append(spasi.join(surround_anchor))
                    else:
                        surround = []
                        for page in pages:
                            if urlparse(page.get("href")).netloc is ''  or 'None':
                                surround_anchor = ""
                            else:
                                try:
                                    req_tag = requests.get(page.get("href"))
                                    soup_tag = BeautifulSoup(req_tag.text, "lxml" or 'None')
                                    links = soup_tag.select("article a")
                                    for link in links:
                                        if urlparse(link.get("href")).netloc is '':
                                            surround_anchor = ""
                                        else:
                                            try:
                                                req_link = requests.get(link.get("href"))
                                                soup_link = BeautifulSoup(req_link.text, "lxml")
                                                surround_anchor = SurroundingAnchor(soup_link, surround)
                                            except requests.ConnectionError as e:
                                                surround_anchor = ""
                                except requests.ConnectionError as e:
                                    surround_anchor = ""
                        scrap.append(spasi.join(surround_anchor))
                else:
                    surround = []
                    for page in pages:
                        if urlparse(page.get("href")).netloc is '' or 'None':
                            surround_anchor = ""
                        else:
                            try:
                                req_tag = requests.get(page.get("href"))
                                soup_tag = BeautifulSoup(req_tag.text, "lxml")
                                links = soup_tag.select("article a")
                                for link in links:
                                    if urlparse(link.get("href")).netloc is '' or 'None':
                                        surround_anchor = ""
                                    else:
                                        try:
                                            req_link = requests.get(link.get("href"))
                                            soup_link = BeautifulSoup(req_link.text, "lxml")
                                            surround_anchor = SurroundingAnchor(soup_link, surround)
                                        except requests.ConnectionError as e:
                                            surround_anchor = ""
                            except requests.ConnectionError as e:
                                surround_anchor = ""
                    scrap.append(spasi.join(surround_anchor))
            else:
                surround = []
                for page in pages:
                    if urlparse(page.get("href")).netloc is '' or 'None':
                        surround_anchor = ""
                    else:
                        try:
                            req_tag = requests.get(page.get("href"))
                            soup_tag = BeautifulSoup(req_tag.text, "lxml")
                            links = soup_tag.select("article a")
                            for link in links:
                                if urlparse(link.get("href")).netloc is ''  or 'None':
                                    surround_anchor = ""
                                else:
                                    try:
                                        req_link = requests.get(link.get("href"))
                                        soup_link = BeautifulSoup(req_link.text, "lxml")
                                        surround_anchor = SurroundingAnchor(soup_link, surround)
                                    except requests.ConnectionError as e:
                                        surround_anchor = ""
                        except requests.ConnectionError as e:
                            surround_anchor = ""
                scrap.append(spasi.join(surround_anchor))
        except requests.ConnectionError as e:
               scrap.append("none")

    data['Surrounding'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Surrounding Text, Data Tersimpan di file " + file )
 
def Tahun(file, scrap):
    data = pd.read_csv(file, encoding= 'unicode_escape')
    data_count = data.Seed_URL.count()
    for i in range(data_count):
        print(str(i))
        try:
            article = Article(data.Seed_URL[i])
            article.download()
            article.parse()
            print(article.publish_date)
            scrap.append(article.publish_date)
        except:
            scrap.append("none")
    data['Tanggal_Publish'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping, Data Tersimpan di file " + file )           
start_time = time.time()
file = "../dataset/data_testing/detik.csv"  
scrap = []
#ParentPage(file, scrap)
#AnchorText(file, scrap)
#SurroundingText(file, scrap)
Tahun(file,scrap)
print("--- %s seconds ---" % (time.time() - start_time))