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
    data = pd.read_csv(file, encoding= 'unicode_escape')
    data_count = data.Seed_URL.count()
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        for s in soup.select('script'):
            s.extract()
        pages = soup.find('div', attrs={'class':'entry-content'})
        if not pages:
            pages = soup.find('div', attrs={'class':'post-content'})
            if not pages:
                pages = soup.find('div', attrs={'class':'flex-caption'})
                if not pages:
                    scrap.append("none")
                else:
                    scrap.append(pages.getText())
            else:
                scrap.append(pages.getText())
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
        pages = soup.find_all('ul', attrs={'class':'tags-widget'})
        if not pages:
            pages = soup.find_all('a', attrs={'class':'play-button'})
            if not pages:
                pages = soup.find('div', attrs={'class':'post-content'})
                if not pages:
                    pages = soup.find('div', attrs={'class':'related-posts'})
                    if not pages:
                        scrap.append("none")
                    else:
                        anchor_text = []
                        pages_posts = pages.find_all('h2', attrs={'class':'post-title'})
                        for page in pages_posts:
                            tags = page.find('a')
                            anchor_text.append(tags.get("title"))
                        scrap.append(spasi.join(anchor_text))
                else:
                    pages_posts = pages.find_all('a')
                    anchor_text = []
                    for page in pages_posts:
                        anchor_text.append(page.getText())
                    scrap.append(spasi.join(anchor_text))
            else:
                anchor_text = []
                for page in pages:
                    anchor_text.append(page.get("title"))
                scrap.append(spasi.join(anchor_text))
        else:
            anchor_text = []
            for page in pages:
                tags = page.find_all('a')
                for tag in tags:
                    anchor_text.append(tag.getText())
            scrap.append(spasi.join(anchor_text))
            
    data['Anchor'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan Scraping Anchor Text, Data Tersimpan di file " + file )
                
def SurroundingText(file, scrap):
    def SurroundingAnchor(soup, surround_text):
        pages = soup.find_all('ul', attrs={'class':'tags-widget'})
        if not pages:
            pages = soup.find_all('a', attrs={'class':'play-button'})
            if not pages:
                pages = soup.find('div', attrs={'class':'post-content'})
                if not pages:
                    pages = soup.find('div', attrs={'class':'related-posts'})
                    if not pages:
                        print("none")
                    else:
                        pages_posts = pages.find_all('h2', attrs={'class':'post-title'})
                        for page in pages_posts:
                            tags = page.find('a')
                            surround_text.append(tags.get("title"))
                        return surround_text
                else:
                    pages_posts = pages.find_all('a')
                    for page in pages_posts:
                        surround_anchor.append(page.getText())
                    return surround_text
            else:
                for page in pages:
                    surround_text.append(page.get("title"))
                return surround_text
        else:
            for page in pages:
                tags = page.find_all('a')
                for tag in tags:
                    surround_text.append(tag.getText())
            return surround_text
    data = pd.read_csv(file, encoding= 'unicode_escape') 
    data_count = data.Seed_URL.count()
    spasi = " "
    for i in range(data_count):
        req_news = requests.get(data.Seed_URL[i])
        soup = BeautifulSoup(req_news.text, "lxml")
        for s in soup.select('script'):
            s.extract()
        pages = soup.find_all('ul', attrs={'class':'tags-widget'})
        if not pages:
            pages = soup.find_all('a', attrs={'class':'play-button'})
            if not pages:
                pages = soup.find('div', attrs={'class':'post-content'})
                if not pages:
                    pages = soup.find('div', attrs={'class':'related-posts'})
                    if not pages:
                        scrap.append("none")
                    else:
                        # related-posts
                        surround_text = []      
                        posts = pages.find_all('div', attrs={'class':'post-thumb'})
                        for post in posts:
                            url = post.find('a')
                            req_tag = requests.get(url.get("href"))
                            soup_tag = BeautifulSoup(req_tag.text, "lxml")
                            surround_anchor = SurroundingAnchor(soup_tag, surround_text)
                        scrap.append(spasi.join(surround_anchor))
                else:
                    # post-content
                    pages_posts = pages.find_all('a')
                    surround_text = []
                    for page in pages_posts:
                        req_tag = requests.get(page.get("href"))
                        soup_tag = BeautifulSoup(req_tag.text, "lxml")
                        surround_anchor = SurroundingAnchor(soup_tag, surround_text)
                    scrap.append(spasi.join(surround_anchor))
            else:
                # play-button
                surround_text = []
                for page in pages:
                    req_tag = requests.get(page.get("href"))
                    soup_tag = BeautifulSoup(req_tag.text, "lxml")
                    surround_anchor = SurroundingAnchor(soup_tag, surround_text)
                scrap.append(spasi.join(surround_anchor))
        else:
            surround_text = []
            for page in pages:
                tags = page.find_all('a')
                for tag in tags:
                    req_tag = requests.get("https://www.antaranews.com"+tag.get("href"))
                    soup_tag = BeautifulSoup(req_tag.text, "lxml")
                    pages_tag = soup_tag.find_all('article', attrs={'class':'simple-post'})
                    for page_tag in pages_tag:
                        urls = page_tag.find_all('div', attrs={'class':'simple-thumb'})
                        for url in urls:
                            link = url.find('a')
                            req_link = requests.get(link.get("href"))
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
        article = Article(data.Seed_URL[i])
        article.download()
        article.parse()
        scrap.append(article.publish_date)

    data['Tanggal_Publish'] = scrap 
    data.to_csv(file, index=False)
    print("Berhasil melakukan scrapping, Data Tersimpan di file " + file )

           
start_time = time.time()
file = "../dataset/data_training/antaranews.csv"  
scrap = []
#ParentPage(file, scrap)
#AnchorText(file, scrap)
#SurroundingText(file, scrap)
Tahun(file, scrap)
print("--- %s seconds ---" % (time.time() - start_time))