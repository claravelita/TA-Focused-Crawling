# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 11:33:25 2020

@author: MSI
"""
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd 
import time
import re


def search_keyword(url, keyword, driverfirefox):
    driverfirefox.get(url)
    elem = driverfirefox.find_element_by_name("q")
    elem.clear()
    # mengirimkan keyword ke text box pencarian kompas
    elem.send_keys(keyword)
    elem = driverfirefox.find_element_by_name("submit")
    elem.click()
    # mendapat url hasil pencarian
    current_url = driverfirefox.current_url
    return current_url       
          
def crawl_level_satu(current_url,file,limit_crawl):
    driverfirefox.get(current_url)
    count_url = 0
    with open(file,'a') as f:
        f.write("Seed_URL" + "\n")
        # mencari banyaknya halaman pada hasil pencarian
        page = driverfirefox.find_elements_by_xpath('//div[@class="gsc-cursor-page"]')
        news = driverfirefox.find_elements_by_xpath('//div[@class="gs-title"]/a[@class="gs-title"]')
        sum_el = len(news)
        # melakukan crawling URL pada halaman pertama
        for e in range(sum_el-1):
            f.write(news[e].get_attribute("href"))
            f.write("\n")
            count_url += 1
        sum_page = len(page)
        print("Crawling Halaman 1")
        for p in range(sum_page):
            if count_url >= limit_crawl:
                print("Crawling diberhentikan karena sudah melebihi batas maksimal crawling")
                break
            else:
                print("Crawling Halaman " + str(p+2))
                # menjelajahi halaman selanjutnya
                page = driverfirefox.find_elements_by_xpath('//div[@class="gsc-cursor-page"]')
                page[p].click()
                time.sleep(5)
                news = driverfirefox.find_elements_by_xpath('//div[@class="gs-title"]/a[@class="gs-title"]')
                sum_el = len(news)
                try:
                    # melakukan crawling URL
                    for e in range(sum_el-1):
                        if count_url >= limit_crawl:
                            print("Crawling diberhentikan karena sudah melebihi batas maksimal crawling")
                            break
                        else:
                            f.write(news[e].get_attribute("href"))
                            f.write("\n")
                            count_url += 1
                except StaleElementReferenceException:
                    print('StaleElementReferenceException')
        print("Berhasil melakukan level satu crawling URL kedalam file " + file)
        return count_url
    
def crawl_level_dua(file, driverfirefox,count_url,limit_crawl):
    data = pd.read_csv(file) 
    data_count = data.Seed_URL.count()
    for u in range(data_count):
        no = u+1
        url = (data.Seed_URL[u])
        print("Crawling dari URL ke-" + str(no)+ " URL : ")
        print(url + "\n")
        contains = re.search("https://www.kompas.com/tag/", url)
        time.sleep(5)
        driverfirefox.get(url)
        if count_url >= limit_crawl:
            print("Crawling diberhentikan karena sudah melebihi batas maksimal crawling")
            break
        else:
            if contains:
                # jika URL merupakan kompas tag (bukan berita)
                news = driverfirefox.find_elements_by_xpath('//a[@class="article__link"]')
                time.sleep(5)
                sum_el = len(news)
                print(sum_el)
                for e in range(sum_el): 
                    if count_url >= limit_crawl:
                        print("Crawling diberhentikan karena sudah melebihi batas maksimal crawling")
                        break
                    else:
                        with open(file,'a') as f:
                            f.write(news[e].get_attribute("href") + "\n")
                            count_url += 1
            else:
                # jika URL berita
                
                news = driverfirefox.find_elements_by_xpath('//a[@class="inner-link-baca-juga"]')
                time.sleep(5)
                sum_el = len(news)
                for e in range(sum_el): 
                    if count_url >= limit_crawl:
                        print("Crawling diberhentikan karena sudah melebihi batas maksimal crawling")
                        break
                    else:
                        with open(file,'a') as f:
                            f.write(news[e].get_attribute("href") + "\n")
                            count_url += 1
    print("Selesai Melakukan Crawling level ke dua")

def drop_duplicate(file):
    data = pd.read_csv(file) 
    # menghapus URL yang duplikat
    data.drop_duplicates(subset ="Seed_URL", 
    					keep = "first", inplace = True) 
    data.to_csv(file, index=True)

start_time = time.time()
url = "https://www.kompas.com/"
keyword = "Geopark Ciletuh"
limit_crawl = 200
driverfirefox = webdriver.Firefox()
search = search_keyword(url, keyword, driverfirefox)
file = "dataset/crawling/bfs_with_limit_kompas.csv"
count_url = crawl_level_satu(search, file, limit_crawl)
if count_url >= limit_crawl:
    print("Selesai melakukan crawling, URL tesimpan di " + file)
else:
    crawl_level_dua(file,driverfirefox,count_url,limit_crawl)
#drop_duplicate(file)
driverfirefox.quit()
print("--- %s seconds ---" % (time.time() - start_time))
