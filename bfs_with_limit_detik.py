# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 16:21:55 2020

@author: MSI
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd 
import time

def crawl_level_satu(file, page, max_page, keyword, limit_crawl):
    count_url = 0
    with open(file,'a') as f:
        f.write("Seed_URL" + "\n")
        while page < max_page:
            if count_url >= limit_crawl:
                print("Crawling diberhantikan karena sudah melebihi batas maksimal crawling")
                break
            else:
                # cari berdasarkan keyword dan page
                url = "https://www.detik.com/search/searchall?query="+keyword+"&siteid=2&sortby=time&page="+str(page)
                try:
                    req = requests.get(url)
                    soup = BeautifulSoup(req.text, "lxml")
        
                    # cek apakah page saat ini adalah page paling terakhir
                    selected_page = soup.find('a', attrs={'class':'selected'})
                    if not selected_page:
                        print("Berhasil Melakukan Crawling URL Level 1\n")
                        break
                    
                    # mencari seluruh tag article
                    print("Crawling Halaman "+str(page))
                    artikel = soup.find_all('article')
                    for a in artikel:
                        if count_url >= limit_crawl:
                            print("Crawling diberhentikan karena sudah melebihi batas maksimal crawling")
                            break
                        else:
                            # melakukan URL dari tag a dan disimpan kedalam difrontier (file csv)
                            link = a.find('a')
                            f.write(link.get('href') + "\n")
                            count_url += 1
                except requests.ConnectionError:
                    pass
                page +=1
                if page == max_page:
                    print("Berhasil Melakukan Crawling URL Level 1\n")
    return count_url

def crawl_level_dua(file, count_url, limit_crawl):
    # membuka file csv hasil crawling level ke-1             
    data = pd.read_csv(file) 
    data_count = data.Seed_URL.count()
    with open(file,'a') as f:
        for i in range(data_count):
            if count_url >= limit_crawl:
                print("Crawling diberhentikan karena sudah melebihi batas maksimal crawling")
                break
            else:
                url = (data.Seed_URL[i])
                try:
                    print("Crawling dari URL ke-"+str(i+1)+ " URL : ")
                    print(url + "\n")
                    req = requests.get(url)
                    soup = BeautifulSoup(req.text, "lxml") 
                    artikel = soup.find_all('a', attrs={'class':'gtm_beritaterkait_artikel'})
                    for a in artikel:
                        if count_url >= limit_crawl:
                            print("Crawling diberhantikan karena sudah melebihi batas maksimal crawling")
                            break
                        else:
                            f.write(a.get('href') + "\n")
                            count_url += 1
                except requests.ConnectionError:
                     pass
    print("\nBerhasil Melakukan Crawling URL Level 2\n")
    
def drop_duplicate(file):
    data = pd.read_csv(file)
    # menghapus URL yang duplikat
    data.drop_duplicates(subset ="Seed_URL", 
    					keep = "first", inplace = True) 
    data.to_csv(file, index=True)

start_time = time.time()
keyword = "Geopark Ciletuh"
file = "dataset/crawling/bfs_with_limit_detik.csv"
page = 1
max_page = 100
limit_crawl = 200
count_url = crawl_level_satu(file, page, max_page, keyword, limit_crawl)
if count_url >= limit_crawl:
    print("Selesai melakukan crawling, URL tesimpan di " + file)
else:
    crawl_level_dua(file, count_url, limit_crawl)
drop_duplicate(file)
print("--- %s seconds ---" % (time.time() - start_time))