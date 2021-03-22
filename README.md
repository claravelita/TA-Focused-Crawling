# Implementasi Focused Crawling dengan Topic-Specific, Multinomial Naive Bayes, dan Breadth First Search guna Pengumpulan Data Media Monitoring Geopark Ciletuh

Ini merupakan _source code_ dari Tugas Akhir Implementasi Focused Crawling dengan Topic-Specific, Multinomial Naive Bayes, dan Breadth First Search guna Pengumpulan Data Media Monitoring Geopark Ciletuh.

## Abstrak
Sebagai bagian dari UNESCO Global Geopark (UGG), wisata Geopark Ciletuh memiliki praktisi Public Relations (PR) yang mempunyai tujuan dalam hal membangun, mengembangkan, dan mempertahankan reputasi serta citra dari kawasan wisata Geopark Ciletuh. Untuk mencapai tujuan tersebut, praktisi PR melakukan media monitoring dengan mencari dan memilih berita dari berbagai sumber media online, lalu mengumpulkannya kedalam kliping berita untuk diidentifikasi dan dianalisis. Dalam media monitoring, proses ini disebut data back-end. Penelitian ini mengusulkan focused crawling untuk diimplementasikan pada data back-end media monitoring Geopark Ciletuh supaya proses pengumpulan data lebih cepat. Focused crawling diimplementasikan dengan menggunakan tiga metode yaitu metode crawler dengan Algoritma Breadth First Search (BFS) untuk mendapatkan URL berita yang lebih banyak, metode distiller dengan Topic-Specific Weight Table dan Page Relevance untuk fitur parameter dataset, serta metode klasifikasi dengan Multinomial Na ̈ıve Bayes untuk menentukan berita yang relevan. Hasil penelitian dengan algoritma BFS dapat melakukan crawling sebanyak 470 URL untuk Detik dan 290 URL untuk Kompas. Sedangkan dalam menentukan berita yang relevan akurasi yang didapatkan model Multinomial Na ̈ıve Bayes dengan Page Relevance yaitu 83.46% untuk dataset Detik, 89% untuk dataset Kompas dan diatas 88.16% untuk kedua gabungan dataset Detik dan Kompas.

## Teknologi
- Python 3.7

## Penggunaan
1. Crawling URL.
2. Scraping Parent Page, Anchor Text, dan Surrounding Text.
3. Menghitung Page Relevance URL Word Parent Page, Anchor Text, dan Surrounding Text.
4. Melakukan Labeling dataset.
5. Melakukan Klasifikasi Dataset.
6. Melakukan Scraping ke dalam Database.

### Crawling URL
Crawling URL menggunakan metode BFS, peneliti membuat dua cara bfs tanpa limit dan bfs dengan limit. 
Crawling dengan Limit :
- bfs_kompas.py
- bfs_detik.py

Crawling dengan Limit :
- bfs_with_limit_kompas.py
- bfs_with_limit_detik.py

### Scraping Parent Page, Anchor Text, dan Surrounding Text
Selanjutnya melakukan scraping Parameter Page Relevance (Parent Page, Anchor Text, dan Surrounding Text) berdasarkan URL yang sudah dilakukan crawling, file scraping tersedia didalam folder **scraping**. Untuk hasil BFS, bisa dilakukan scraping pada :
- scraping_kompas.py
- scraping_detik.py

PS : Sewaktu-waktu scraping tidak dapat berjalan dengan baik dikarenakan scraping bergantung pada Element dari DOM HTML. Element yang ada pada saat ini dapat berubah sesuai masing-masing media online.

### Menghitung Page Relevance URL Word Parent Page, Anchor Text, dan Surrounding Text
Setelah semua data di-scraping, selanjutnya hasil scraping dihitung page relevancenya di page_relevance.py

### Melakukan Labeling dataset
Dataset dilakukan labeling guna klasifikasi data di labeling_dataset.py

### Melakukan Klasifikasi Dataset
Peneliti melakukan eksperimen dengan beberapa metode klasifikasi yaitu :
- model_mnb.py (Multinomial Naive Bayes)
- model_mnb_improved.py (Improved Multinomial Naive Bayes berdasarkan parameter)
- model_nb.py (Naive Bayes)

### Melakukan Scraping ke dalam Database
Scraping dilakukan kedalam database, dengan menggunakan scraping_to_db.py

## Data Training
Data Training yang digunakan berdasarkan URL yang sudah dikumpulkan oleh PR Geopark Ciletuh. pada penelitian ini, data training yang digunakan ada pada dataset/data_training_2.csv

## Data Testing
Data Testing yang digunakan tersedia pada dataset/testing_model
