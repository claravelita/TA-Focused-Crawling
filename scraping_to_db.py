# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 05:11:39 2020

@author: MSI
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import time
from datetime import datetime
import mysql.connector
import threading 
import re
from nltk.tokenize import word_tokenize

def preprocessing(text): 
    remove_enter = re.compile('\n')
    text = re.sub(remove_enter, " ", str(text))
    encoded_string = text.encode("ascii", "ignore")
    text = encoded_string.decode()

    return text

def bulan(argument): 
	switcher = { 
		"Jan" : "01",
        "Feb" : "02",
        "Mar" : "03",
        "Apr" : "04",
        "Mei" : "05",
        "Jun" : "06",
        "Jul" : "07",
        "Agu" : "08",
        "Sep" : "09",
        "Okt" : "10",
        "Nov" : "11",
        "Des" : "12",
        "Januari" : "01",
        "Februari" : "02",
        "Maret" : "03",
        "April" : "04",
        "Mei" : "05",
        "Juni" : "06",
        "Juli" : "07",
        "Agustus" : "08",
        "September" : "09",
        "Oktober" : "10",
        "November" : "11",
        "Desember" : "12",
	} 

	return switcher.get(argument, argument) 

def save_berita(mydb, judul, waktu_pemuatan, rubrik, link, waktu_akses, penulis, editor, sumber_berita, keterangan, isi_berita, gambar_berita, id_media_online, id_geopark, created_at, updated_at): 
    mycursor = mydb.cursor()
#    cari = "SELECT * FROM Profil_Berita WHERE Isi_Berita = %s"
#    adr = (isi_berita, )
#    
#    mycursor.execute(cari, adr)
#    
#    myresult = mycursor.fetchall()
#    
#    hitung = len(myresult)
#    if hitung == 0:
    sql = """INSERT IGNORE INTO  Profil_Berita(Judul, Waktu_Pemuatan, Rubrik, Link, Waktu_Akses, Penulis, Editor, Sumber_Berita, Keterangan, Isi_Berita, Gambar_Berita, Id_Media_Online, Id_Geopark, Created_at, Updated_at) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    val = (judul, waktu_pemuatan, rubrik, link, waktu_akses, penulis, editor, sumber_berita, keterangan, isi_berita, gambar_berita, id_media_online, id_geopark, created_at, updated_at)
    
    mycursor.execute(sql, val)
    
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")   


def scrap_kompas(awal, akhir, data_class, data, ciletuh):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="medmondb"
    )
    
    for i in range(awal,akhir):
        if (data_class[i]==1):
            try:
                req_berita = requests.get(data.Seed_URL[i])
                soup = BeautifulSoup(req_berita.text, "lxml")
                for s in soup.select('script'):
                    s.extract()
                for s in soup.select('style'):
                    s.extract()
                # isi_berita
                # .travel .regional .bandung .entertainment .biz .semarang
                find_isi = soup.find('div', attrs={'class':'read__content'})
                if not find_isi:
                    # .pesonaindonesia
                    find_isi = soup.find('div', attrs={'class':'main-artikel-paragraf'})
                    if not find_isi:
                        # .superapps
                        find_isi = soup.find('div', attrs={'class':'articleRead'})
                        if not find_isi:
                            # .pemilu
                            find_isi = soup.find('div', attrs={'class':'read__article'})
                            if not find_isi:
                                # .genbest
                                find_isi = soup.find('div', attrs={'class':'articleContent'})
                                if not find_isi:
                                    isi_berita = ""
                                else:
                                    isi_berita = find_isi.getText()
                            else:
                                isi_berita = find_isi.getText()
                        else:
                            isi_berita = find_isi.getText()
                    else:
                        isi_berita = find_isi.getText()
                else:
                    isi_berita = find_isi.getText()
                # judul 
                # .travel .regional .bandung .entertainment .biz .semarang .properti .sains .yogyakarta .bogor .surabaya .pemilu .otomotif .money .lifestyle .ekonomi .bola .nasional .megapolitan .internasional
                find_judul = soup.find('h1', attrs={'class':'read__title'})
                if not find_judul:
                    # .pesonaindonesia
                    find_judul = soup.find('h1', attrs={'class':'main-title'})
                    if not find_judul:
                        # .superapps .genbest
                        find_judul = soup.find('h1', attrs={'class':'articleTitle'})
                        if not find_judul:
                            judul = ""
                        else:
                            judul = find_judul.getText()
                    else:
                        judul = find_judul.getText()
                else:
                    judul = find_judul.getText()
                count_ciletuh = 0
                count_ciletuh_judul = 0
                for c in ciletuh:
                    if c in isi_berita:
                        count_ciletuh +=1
                for c in ciletuh:
                    if c in judul:
                        count_ciletuh_judul +=1
                if count_ciletuh > 0 or count_ciletuh_judul > 0:
                    
                    
                    # waktu_pemuatan
    #                    article = Article(data.Seed_URL[i])
    #                    article.download()
    #                    article.parse()
    #                    waktu_pemuatan = article.publish_date
                    find_waktu_pemuatan = soup.find('div', attrs={'class':'read__time'})
                    if not find_waktu_pemuatan:
                        find_waktu_pemuatan = soup.find('div', attrs={'class':'main-artikel-date'})
                        if not find_waktu_pemuatan:
                            find_waktu_pemuatan = soup.find('div', attrs={'class':'articleMetaShare iobitdev-grid'})
                            if not find_waktu_pemuatan:
                                waktu_pemuatan = None
                            else:
                                find_text_waktu_pemuatan = find_waktu_pemuatan.find('span', attrs={'class':'time'}) 
                                get_waktu_pemuatan = find_text_waktu_pemuatan.getText()
                                remove_char = re.sub(r"[^\w\s\.\:]", " ", get_waktu_pemuatan)
                                split_waktu = re.split("\s+", remove_char)
                                d = split_waktu[0]
                                m = split_waktu[1]
                                y = split_waktu[2]
                                t = split_waktu[3]
                                waktu_pemuatan = str(y)+"-"+str(m)+"-"+str(d)+" "+str(t)
                        else:
                            find_text_waktu_pemuatan = find_waktu_pemuatan.find('p')  
                            get_waktu_pemuatan = find_text_waktu_pemuatan.getText()
                            remove_char = re.sub(r"[^\w\s\.\:]", " ", get_waktu_pemuatan)
                            split_waktu = re.split("\s+", remove_char)
                            d = split_waktu[1]
                            m = bulan(split_waktu[2])
                            y = split_waktu[3]
                            t = split_waktu[4]
                            waktu_pemuatan = str(y)+"-"+str(m)+"-"+str(d)+" "+str(t)
                    else:
                        get_waktu_pemuatan = find_waktu_pemuatan.getText()
                        remove_char = re.sub(r"[^\w\s\.\:]", " ", get_waktu_pemuatan)
                        split_waktu = re.split("\s+", remove_char)
                        d = split_waktu[1]
                        m = bulan(split_waktu[2])
                        y = split_waktu[3]
                        t = split_waktu[4]
                        waktu_pemuatan = str(y)+"-"+str(m)+"-"+str(d)+" "+str(t)
    
                    
    
                    # rubrik
                    # .travel .regional .bandung .entertainment .semarang .properti .sains .yogyakarta .bogor .surabaya .pemilu .otomotif .money .lifestyle .ekonomi .bola .nasional .megapolitan .internasional
                    find_rubrik = soup.find_all('li', attrs={'class':'breadcrumb__item'})
                    if not find_rubrik:
                        # .pesonaindonesia
                        find_rubrik = soup.find('div', attrs={'class':'breadcrumb'})
                        if not find_rubrik:
                            find_rubrik = soup.find('ul', attrs={'class':'breadcrumb__wrap'})
                            if not find_rubrik:
                                rubrik = None
                            else:
                                nama_rubrik = []
                                find_nama_rubrik = find_rubrik.find_all('a')
                                for a_rubrik in find_nama_rubrik:
                                    txt_rubrik = a_rubrik.getText()
                                    nama_rubrik.append(txt_rubrik)
                                rubrik = " / ".join(nama_rubrik)
                        else:
                            nama_rubrik = []
                            find_nama_rubrik = find_rubrik.find_all('a')
                            for a_rubrik in find_nama_rubrik:
                                txt_rubrik = a_rubrik.getText()
                                nama_rubrik.append(txt_rubrik)
                            rubrik = " / ".join(nama_rubrik)
                    else:
                        nama_rubrik = []
                        for li_rubrik in find_rubrik:
                            find_nama_rubrik = li_rubrik.find('span', attrs={'itemprop':'name'})
                            if not find_nama_rubrik:
                                nama_rubrik.append("")
                            else:
                                txt_rubrik = find_nama_rubrik.getText()
                                nama_rubrik.append(txt_rubrik)
                        rubrik = " / ".join(nama_rubrik)
    
                    # link
                    link = data.Seed_URL[i]
                    
                    # waktu_akses
                    waktu_akses = datetime.now()
                    
                    # penulis
                    find_penulis = soup.find('div', attrs={'id':'penulis'})
                    if not find_penulis:
                        penulis = None
                    else:
                        txt_penulis = find_penulis.find('a')
                        if not txt_penulis:
                            penulis = None
                        else:
                            penulis = txt_penulis.getText()
                    
                    # editor
                    find_editor = soup.find('div', attrs={'id':'editor'})
                    if not find_editor:
                        editor = None
                    else:
                        txt_editor = find_editor.find('a')  
                        if not txt_editor:
                            editor = None
                        else:
                            editor = txt_editor.getText()
                    
                    # sumber_berita
                    sumber_berita = None
                    
                    # keterangan
                    keterangan = None
                    
                    # gambar_berita
                    # .travel .regional .bandung .entertainment .biz .semarang .properti .sains .yogyakarta .bogor .surabaya .pemilu .otomotif .money .lifestyle .ekonomi .bola .nasional .megapolitan .internasional
                    find_gambar = soup.find('div', attrs={'class':'photo'})
                    if not find_gambar:
                        # .pesonaindonesia
                        find_gambar = soup.find('img', attrs={'class':'main-artikel-img'})
                        if not find_gambar:
                            # .superapps .genbest
                            find_gambar = soup.find('div', attrs={'class':'articleImage'})
                            if not find_gambar:
                                gambar_berita = None
                            else:
                                gambar = find_gambar.find('img')  
                                gambar_berita = gambar.get("src")
                        else:
                            gambar_berita = find_gambar.get("src")
                    else:
                        gambar = find_gambar.find('img')  
                        gambar_berita = gambar.get("src")
    
                    created_at = datetime.now()
                    updated_at = datetime.now()
                    id_media_online = 1
                    id_geopark = 1
                    isi_berita = preprocessing(isi_berita)
                    save_berita(mydb, judul, waktu_pemuatan, rubrik, link, waktu_akses, penulis, editor, sumber_berita, keterangan, isi_berita, gambar_berita, id_media_online, id_geopark, created_at, updated_at)
            except requests.ConnectionError as e:
                print("error")

def scrap_detik(awal, akhir, data_class, data, ciletuh):
    mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="",
          database="medmondb"
        )
    
    for i in range(awal,akhir):
        if(data_class[i]==1):
            try:
                req_berita = requests.get(data.Seed_URL[i])
                soup = BeautifulSoup(req_berita.text, "lxml")
                for s in soup.select('script'):
                    s.extract()
                for s in soup.select('style'):
                    s.extract()
                # isi_berita
                find_isi = soup.find('div', attrs={'id':'detikdetailtext'}) 
                if not find_isi:
                    find_isi = soup.find('div', attrs={'class':'detail__body-text'}) 
                    if not find_isi:
                        find_isi = soup.find('div', attrs={'class':'read__content'})
                        if not find_isi:
                            find_isi = soup.find('div', attrs={'class':'parallax_detail'})
                            if not find_isi:
                                find_isi = soup.find('div', attrs={'class':'detail_text'})
                                if not find_isi:
                                    isi_berita = ""
                                else:
                                    for s in find_isi.select('div[class~=embedvideo]'):
                                        s.extract()
                                    for s in find_isi.select('div[class~=date]'):
                                        s.extract()
                                    isi_berita = find_isi.getText()
                            else:
                                isi_berita = find_isi.getText()
                        else:
                            for s in find_isi.select('div[class~=detail_tag]'):
                                s.extract()
                            isi_berita = find_isi.getText()
                    else:
                        for s in find_isi.select('div[class~=detail__body-tag]'):
                            s.extract()
                        for s in find_isi.select('table[class~=linksisip]'):
                            s.extract()
                        isi_berita = find_isi.getText()
                else:
                    for s in find_isi.select('div[class~=detail_tag]'):
                        s.extract()
                    for s in find_isi.select('table[class~=linksisip]'):
                        s.extract()
                    isi_berita = find_isi.getText()
    
                # judul
                # .travel
                find_head = soup.find('div', attrs={'class':'read__head'})
                if not find_head:
                    find_head = soup.find('div', attrs={'class':'detail__header'})
                    if not find_head:
                        # .20 (video)
                        find_head = soup.find('h1', attrs={'class':'title'})
                        if not find_head:
                            # .oto
                            find_head = soup.find('div', attrs={'class':'jdl'})
                            if not find_head:
                                judul = ""
                            else:
                                find_judul = find_head.find('h1')
                                judul = find_judul.getText()
                        else:
                            judul = find_head.getText()
                    else:
                        find_judul = find_head.find('h1', attrs={'class':'detail__title'})
                        judul = find_judul.getText()
                else:
                    find_judul = find_head.find('h1')
                    judul = find_judul.getText()
                        
                count_ciletuh = 0
                count_ciletuh_judul = 0
                for c in ciletuh:
                    if c in isi_berita:
                        count_ciletuh +=1
                for c in ciletuh:
                    if c in judul:
                        count_ciletuh_judul +=1
                if count_ciletuh > 0 or count_ciletuh_judul > 0:
    
                    
                    # waktu_pemuatan
    #                    article = Article(data.Seed_URL[i])
    #                    article.download()
    #                    article.parse()
    #                    waktu_pemuatan = article.publish_date
    
                    find_waktu_pemuatan = soup.find('div', attrs={'class':'detail__date'})
                    if not find_waktu_pemuatan:
                        find_waktu_pemuatan = soup.find('div', attrs={'class':'date'})
                        if not find_waktu_pemuatan:    
                            waktu_pemuatan = None
                        else:
                            get_waktu_pemuatan = find_waktu_pemuatan.getText()
                            remove_comma = re.split(", ", get_waktu_pemuatan)
                            remove_wib = re.split(" WIB", remove_comma[1])
                            split_waktu = re.split("\s+", remove_wib[0])
                            d = split_waktu[0]
                            m = bulan(split_waktu[1])
                            y = split_waktu[2]
                            t = split_waktu[3]
                            waktu_pemuatan = str(y)+"-"+str(m)+"-"+str(d)+" "+str(t)
                        
                    else:
                        get_waktu_pemuatan = find_waktu_pemuatan.getText()
                        remove_comma = re.split(", ", get_waktu_pemuatan)
                        remove_wib = re.split(" WIB", remove_comma[1])
                        split_waktu = re.split("\s+", remove_wib[0])
                        d = split_waktu[0]
                        m = bulan(split_waktu[1])
                        y = split_waktu[2]
                        t = split_waktu[3]
                        waktu_pemuatan = str(y)+"-"+str(m)+"-"+str(d)+" "+str(t)
    
    
                # rubrik
                # .travel
                    find_head= soup.find('div', attrs={'class':'read__head'})
                    if not find_head:
                        find_head = soup.find('div', attrs={'class':'page__header'})
                        if not find_head:
                            # .oto
                            find_head = soup.find('div', attrs={'class':'breadcrumb'})
                            if not find_head:
                                rubrik = None
                            else:
                                find_rubrik = find_head.find_all('a')
                                nama_rubrik = []
                                for li_rubrik in find_rubrik:
                                    txt_rubrik = li_rubrik.getText()
                                    nama_rubrik.append(txt_rubrik)
                                rubrik = " / ".join(nama_rubrik)
                        else:
                            find_breadcrumb = find_head.find('div', attrs={'class':'page__breadcrumb'})
                            if not find_breadcrumb:
                                rubrik = None
                            else:
                                find_rubrik = find_breadcrumb.find_all('a')
                                nama_rubrik = []
                                for li_rubrik in find_rubrik:
                                    txt_rubrik = li_rubrik.getText()
                                    nama_rubrik.append(txt_rubrik)
                                rubrik = " / ".join(nama_rubrik)
                    else:
                        find_breadcrumb = find_head.find('div', attrs={'class':'breadcrumb'})
                        if not find_breadcrumb:
                            rubrik = None
                        else:
                            find_rubrik = find_breadcrumb.find_all('a')
                            nama_rubrik = []
                            for li_rubrik in find_rubrik:
                                txt_rubrik = li_rubrik.getText()
                                nama_rubrik.append(txt_rubrik)
                            rubrik = " / ".join(nama_rubrik)
    
                    # link
                    link = data.Seed_URL[i]
                
                    # waktu_akses
                    waktu_akses = datetime.now()
                
                    # penulis
                    # .travel
                    find_penulis = soup.find('div', attrs={'class':'ugc__block__name'})
                    if not find_penulis:
                        # .news .finance
                        find_penulis = soup.find('div', attrs={'class':'detail__author'})
                        if not find_penulis:
                            # .20 (video)
                            find_penulis = soup.find('div', attrs={'class':'meta'})
                            if not find_penulis:
                                # .oto
                                find_penulis = soup.find('div', attrs={'class':'jdl'})
                                if not find_penulis:
                                    penulis = None
                                else:
                                    find_div = find_penulis.find('div', attrs={'class':'author'})
                                    txt_penulis = find_div.getText()
                                    if "detikOto" in txt_penulis:
                                        penulis = txt_penulis.replace(" - detikOto", "")
                                    else:
                                        penulis = txt_penulis
                            else:
                                txt_penulis = find_penulis.getText()
                                if "20DETIK" in txt_penulis:
                                    penulis = txt_penulis.replace(" - 20DETIK", "")
                                else:
                                    penulis = txt_penulis
                        else:
                            txt_penulis = find_penulis.getText()
                            if "detikNews" in txt_penulis:
                                penulis = txt_penulis.replace(" - detikNews", "")
                            elif "detikFinance" in txt_penulis:
                                 penulis = txt_penulis.replace(" - detikFinance", "")
                            else:
                                penulis = txt_penulis
                    else:
                        txt_penulis = find_penulis.find('a')
                        if not txt_penulis:
                            penulis = None
                        else:
                            penulis = txt_penulis.getText()
                    
                    # editor
                    editor = None
                    
                    # sumber_berita
                    sumber_berita = None
                    
                    # keterangan
                    # .20 (video)
                    find_ket = soup.find('div', attrs={'class':'embedvideo'})
                    if not find_ket:
                        keterangan = None
                    else:
                        find_input = find_ket.find('input')
                        keterangan = find_input.get("value")
                    
                    # gambar_berita
                    # .travel
                    find_gambar = soup.find('div', attrs={'class':'read__photo'})
                    if not find_gambar:
                        # .news .finance
                        find_gambar = soup.find('div', attrs={'class':'detail__media'})
                        if not find_gambar:
                            find_gambar = soup.find('div', attrs={'class':'detail__author'})
                            if not find_gambar:
                                # .oto
                                find_gambar = soup.find('div', attrs={'class':'media_artikel'})
                                if not find_gambar:
                                    gambar_berita = None
                                else:
                                    gambar = find_gambar.find('img') 
                                    if not gambar:
                                        gambar_berita = None
                                    else:
                                        gambar_berita = gambar.get("src")
                            else:
                                gambar = find_gambar.find('img') 
                                if not gambar:
                                    gambar_berita = None
                                else:
                                    gambar_berita = gambar.get("src")
                        else:
                            find_detail_gambar = find_gambar.find('figure', attrs={'class':'detail__media-image'})
                            if not find_detail_gambar:
                                gambar_berita = None
                            else:
                                gambar = find_detail_gambar.find('img') 
                                if not gambar:
                                    gambar_berita = None
                                else:
                                    gambar_berita = gambar.get("src")
                    else:
                        find_detail_gambar = find_gambar.find('div', attrs={'class':'read__photo__big'})
                        if not find_detail_gambar:
                            gambar = find_gambar.find('img') 
                            if not gambar:
                                gambar_berita = None
                            else:
                                gambar_berita = gambar.get("src")
                            
                        else:
                            gambar = find_detail_gambar.find('img')  
                            if not gambar:
                                gambar_berita = None
                            else:
                                gambar_berita = gambar.get("src")
        
                    created_at = datetime.now()
                    updated_at = datetime.now()
                    id_media_online = 2
                    id_geopark = 1
                    isi_berita = preprocessing(isi_berita)
                    save_berita(mydb, judul, waktu_pemuatan, rubrik, link, waktu_akses, penulis, editor, sumber_berita, keterangan, isi_berita, gambar_berita, id_media_online, id_geopark, created_at, updated_at)
            except requests.ConnectionError as e:
                print("error")

def t1(media_online,data,data_count,data_class,bagi_data,ciletuh):
    if(media_online == "kompas"):
        scrap_kompas(0, data_count, data_class, data, ciletuh)
    elif(media_online == "detik"):
        scrap_detik(0, data_count, data_class, data, ciletuh)
    else:
        print("Scraping untuk media online " + media_online + "tidak tersedia")

def t2(media_online,data,data_count,data_class,bagi_data,ciletuh):
    if(media_online == "kompas"):
        t1 = threading.Thread(target=scrap_kompas, args=(0, bagi_data, data_class, data, ciletuh,)) 
        t2 = threading.Thread(target=scrap_kompas, args=(bagi_data+1, data_count, data_class, data, ciletuh,))
    elif(media_online == "detik"):
        t1 = threading.Thread(target=scrap_detik, args=(0, bagi_data, data_class, data, ciletuh,)) 
        t2 = threading.Thread(target=scrap_detik, args=(bagi_data+1, data_count, data_class, data, ciletuh,))
    else:
        print("Scraping untuk media online " + media_online + "tidak tersedia")
    
    t1.start() 
    t2.start()
    t1.join()  
    t2.join()

start_time = time.time()
#file = "dataset/testing_model_mnb/data_testing_kompas.csv"
data = pd.read_csv(file)
data_count = data.Seed_URL.count()
data_class = data.Class
thread = 2
bagi_data = int(data_count/thread)
media_online = "kompas"
ciletuh = ['ciletuh', 'Ciletuh', 'CILETUH', 'cileteuh', 'Cileteuh', 'CILETEUH', 'Ciletuh-Palabuhanratu', 'Ciletuh-Palabuhan Ratu', 'cpugg', 'CPUGG', 'CPUGGp','cpuggp','cileteh']
if(thread == 1):
    t1(media_online,data,data_count,data_class,bagi_data,ciletuh)
elif(thread == 2):
    t2(media_online,data,data_count,data_class,bagi_data,ciletuh)
else:
    print("Multithread hanya dari 1-2")  
print("Done!")
print("--- %s seconds ---" % (time.time() - start_time))             

