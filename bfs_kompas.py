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


def search_keyword(url, keyword, driver):
    driver.get(url)
    elem = driver.find_element_by_name("q")
    elem.clear()
    # mengirimkan keyword ke text box pencarian kompas
    elem.send_keys(keyword)
    elem = driver.find_element_by_name("submit")
    elem.click()
    # mendapat url hasil pencarian
    current_url = driver.current_url
    return current_url       
          
def crawl_level_satu(current_url,file):
    print("Memulai Crawling URL Level Satu\n")
    driver.get(current_url)
    with open(file,'a') as f:
        f.write("Seed_URL" + "\n")
        # mencari banyaknya halaman pada hasil pencarian
        page = driver.find_elements_by_xpath('//div[@class="gsc-cursor-page"]')
        element = driver.find_elements_by_xpath('//div[@class="gs-title"]/a[@class="gs-title"]')
        sum_el = len(element)
        # melakukan crawling URL pada halaman pertama
        for e in range(sum_el-1):
            f.write(element[e].get_attribute("href"))
            f.write("\n")
        sum_page = len(page)
        print("Crawling Halaman 1")
        for p in range(sum_page):
            print("Crawling Halaman " + str(p+2))
            # menjelajahi halaman selanjutnya
            page = driver.find_elements_by_xpath('//div[@class="gsc-cursor-page"]')
            page[p].click()
            time.sleep(5)
            element = driver.find_elements_by_xpath('//div[@class="gs-title"]/a[@class="gs-title"]')
            sum_el = len(element)
            try:
                # melakukan crawling URL
                for e in range(sum_el-1):
                    f.write(element[e].get_attribute("href"))
                    f.write("\n")
            except StaleElementReferenceException:
                print('StaleElementReferenceException')
        print("Berhasil melakukan level satu crawling URL kedalam file " + file)
    
def crawl_level_dua(file, driver):
    print("Memulai Crawling URL Level Dua\n")
    data = pd.read_csv(file) 
    data_count = data.Seed_URL.count()
    for u in range(data_count):
        no = u+1
        url = (data.Seed_URL[u])
        print("Crawling dari URL ke-" + str(no)+ " URL : ")
        print(url + "\n")
        contains = re.search("https://www.kompas.com/tag/", url)
        time.sleep(5)
        driver.get(url)
        if contains:
            # jika URL merupakan kompas tag (bukan berita)
            element = driver.find_elements_by_xpath('//a[@class="article__link"]')
            time.sleep(5)
            sum_el = len(element)
            for e in range(sum_el): 
                with open(file,'a') as f:
                    f.write(element[e].get_attribute("href") + "\n")
        else:
            # jika URL berita
            element = driver.find_elements_by_xpath('//a[@class="inner-link-baca-juga"]')
            time.sleep(5)
            sum_el = len(element)
            for e in range(sum_el): 
                with open(file,'a') as f:
                    f.write(element[e].get_attribute("href") + "\n")
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
driver =webdriver.Firefox()
search = search_keyword(url, keyword, driver)
file = "dataset/crawling/bfs_kompas.csv"
crawl_level_satu(search, file)
crawl_level_dua(file,driver)
drop_duplicate(file)
driver.quit()
print("--- %s seconds ---" % (time.time() - start_time))

