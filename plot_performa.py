# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 17:34:41 2020

@author: MSI
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 14
def simpleaxis(ax):
    ax.spines['top'].set_linestyle('--')
    ax.spines['top'].set_linewidth(1.5)
    ax.spines['top'].set_color('gainsboro')
    ax.spines['top'].set_zorder(0)
#    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

def plot_bfs():
    x = ["Node Awal", "Layer 1"," Layer 2"] 
    detik = [0, 222,470] 
    kompas = [0,100,290]
    plt.subplots(figsize =(8, 5)) 
    plt.plot(x, detik, label = "Detik" ,color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3)  
    plt.plot(x, kompas, label = "Kompas",color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.xlabel('Layer BFS') 
    plt.ylabel('Halaman yang di-crawling') 
#    plt.title('Hasil Uji Coba Breadth First Search (BFS)') 
    plt.grid(zorder=0,axis='y',color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.yticks(np.arange(0, 510, step=50)) 
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='center',
           ncol=2, borderaxespad=0.,frameon=False)
    
def plot_bfs_scraping():
    mnb_relevan_detik = [196, 198]
    mnb_relevan_kompas = [68,88]
    mnb_bfs_detik = [26, 272]
    mnb_bfs_kompas = [30, 151]
    mnb_relevan_dup_kompas = [70,139]
    
    imnb_relevan_detik = [206, 208]
    imnb_relevan_kompas = [71,94]
    imnb_relevan_dup_kompas = [74,146]
    imnb_bfs_detik = [16, 262]
    imnb_bfs_kompas = [26, 144]
    
    plt.subplots(figsize =(15, 6)) 
    r = [0,2]
    r2 = [1,3]

    barWidth = 0.8
    
    plt.subplot(211)
    plt.barh(r, mnb_relevan_detik, label = "Detik (Relevan)",color='orange', edgecolor='white', height=barWidth, zorder=2)
    plt.barh(r, mnb_bfs_detik, label = "Detik (Tidak Relevan)",left=mnb_relevan_detik, color='navajowhite', edgecolor='white', height=barWidth, zorder=2)
    plt.barh(r2, mnb_relevan_kompas, label = "Kompas (Relevan)", color='steelblue', edgecolor='white', height=barWidth, zorder=2)
    plt.barh(r2, mnb_bfs_kompas, label = "Kompas (Relevan namun duplikat)", left=mnb_relevan_kompas,  color='lightsteelblue', edgecolor='white', height=barWidth, zorder=2)
    plt.barh(r2, mnb_bfs_kompas, label = "Kompas (Tidak Relevan)", left=mnb_relevan_dup_kompas,  color='lightblue', edgecolor='white', height=barWidth, zorder=2)
    
#    plt.plot(mnb_relevan_detik, r, label = "Perbandingan",color='orangered', marker='o', markerfacecolor='lightcoral', markersize=10, zorder=3,linewidth=2) 
#    plt.plot(mnb_relevan_kompas, r2, color='orangered', marker='o', markerfacecolor='lightcoral', markersize=10, zorder=3,linewidth=2) 
    plt.text(98,-0.2,'196',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(99,1.8,'198',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(34,0.82,'68',fontsize=12,fontweight='bold',color ='white',horizontalalignment='center')
    plt.text(44,2.82,'88',fontsize=12,fontweight='bold',color ='white',horizontalalignment='center')
    plt.text(69,0.82,'2',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(113.5,2.82,'51',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(85,0.82,'30',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(214.5,2.82,'151',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(209,-0.2,'26',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(334,1.8,'272',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    
    plt.xticks(np.arange(0, 500, step=30)) 
    plt.grid(zorder=0,axis='x',color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.yticks([r + barWidth for r in range(len(mnb_relevan_detik))], 
    		['Layer 1', 'Layer 2']) 
    plt.xlabel('Halaman yang di-crawling') 
    plt.ylabel('Layer') 
    plt.title('Multinomial Naive Bayes')
    plt.legend(bbox_to_anchor=(0., 1.4, 1., .102), loc='center',
           ncol=3, borderaxespad=0.,frameon=False)
    
    plt.subplot(212)
    plt.barh(r, imnb_relevan_detik, label = "Detik (Relevan)",color='orange', edgecolor='white', height=barWidth, zorder=2)
    plt.barh(r, imnb_bfs_detik, label = "Detik (Tidak Relevan)",left=imnb_relevan_detik, color='navajowhite', edgecolor='white', height=barWidth, zorder=2)
    plt.barh(r2, imnb_relevan_kompas, label = "Kompas (Relevan)", color='steelblue', edgecolor='white', height=barWidth, zorder=2)
    plt.barh(r2, imnb_bfs_kompas, label = "Kompas (Relevan namun duplikat)", left=imnb_relevan_kompas, color='lightsteelblue', edgecolor='white', height=barWidth, zorder=2)
    plt.barh(r2, imnb_bfs_kompas, label = "Kompas (Tidak Relevan)", left=imnb_relevan_dup_kompas, color='lightblue', edgecolor='white', height=barWidth, zorder=2)
    
    
#    plt.plot(imnb_relevan_detik, r, label = "Perbandingan",color='orangered', zorder=3,linewidth=2) 
#    plt.plot(imnb_relevan_kompas, r2, color='orangered', zorder=3,linewidth=2) 
#    plt.plot(imnb_relevan_dup_kompas, r2, color='orangered', zorder=3,linewidth=2) 

    plt.text(103,-0.2,'206',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(104,1.8,'208',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(35.5,0.82,'71',fontsize=12,fontweight='bold',color ='white',horizontalalignment='center')
    plt.text(47,2.82,'94',fontsize=12,fontweight='bold',color ='white',horizontalalignment='center')
    plt.text(72,0.82,'3',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(120,2.82,'52',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(87,0.82,'26',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(218,2.82,'144',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(214,-0.2,'16',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(339,1.8,'262',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    
    plt.xticks(np.arange(0, 500, step=30)) 
    plt.grid(zorder=0,axis='x',color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.yticks([r + barWidth for r in range(len(imnb_relevan_detik))], 
    		['Layer 1', 'Layer 2'])
    plt.xlabel('Halaman yang di-crawling') 
    plt.ylabel('Layer') 
    plt.title('Improved Multinomial Naive Bayes')
    plt.subplots_adjust(hspace=0.65)
#    plt.suptitle('Hasil uji coba scraping berita berdasarkan hasil klasifikasi Multinomial Naive Bayes',y=1.05)
    plt.show()

    

def plot_mnb_sk_1():
    # Training data : Seluruh Tahun, Testing data : Seluruh Tahun    
    x = ["60","160","260","360","460","560","660","760"]
    accuracy_p = [90, 90.62, 89.62, 90.83, 90.22, 89.46, 89.55, 88.16]
    precision_p = [100, 100, 99, 96.12, 90.83, 90.14, 90.25, 86.29]
    recall_p = [89.83, 90.57, 88.79, 88.79, 88.79, 89.83, 90.5, 90.43]

    accuracy_m = [93.33, 95, 94.23, 95.28, 96.3, 95.36, 95.3, 93.82]
    precision_m = [100, 100, 100, 99.05, 99.05, 96.86, 96.32, 92.73]
    recall_m = [93.22, 94.97, 93.27, 93.27, 93.27, 94.24, 94.97, 94.95]

    plt.figure(figsize=(20, 5))
    plt.subplot(131)
    plt.title("Accuracy")
    plt.plot(x, accuracy_p, color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, accuracy_m, color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.xlabel('Halaman yang di-crawling')
    plt.ylabel('Accuracy (%)')
    plt.yticks(np.arange(84, 102, step=2)) 

    plt.subplot(132)
    plt.title("Precision")
    plt.plot(x, precision_p, label = "Multinomial Naive Bayes",  color='orange', marker='o',markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, precision_m, label = "Improved Multinomial Naive Bayes", color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.xlabel('Halaman yang di-crawling')
    plt.ylabel('Precision (%)')
    plt.yticks(np.arange(84, 102, step=2)) 
    plt.legend(bbox_to_anchor=(0., 1.08, 1., .102), loc='center',
           ncol=2, borderaxespad=0.,frameon=False)
    
    plt.subplot(133)
    plt.title("Recall")
    plt.plot(x, recall_p,  color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, recall_m, color='steelblue', marker='o', markerfacecolor='lightblue',  markersize=8,linewidth=3) 
    plt.xlabel('Halaman yang di-crawling')
    plt.ylabel('Recall (%)')
    plt.yticks(np.arange(84, 102, step=2)) 
    
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
#    plt.suptitle('Hasil Uji Coba Multiomial Naive Bayes - Skenario 1')
    
    plt.show() 

def plot_mnb_sk_2():
    # Training data : Pertahun, Testing data : Pertahun
    x = ["2016","2017","2018","2019","2020"] 
    mnb_accuracy_detik = [40,33.33,83.33,83.33,66.67]
    mnb_precision_detik = [100,66.67,100,83.33,100]
    mnb_recall_detik = [40,40,80,100,60]

    mnb_accuracy_kompas = [50,83.33,100,100,83.33]
    mnb_precision_kompas = [100,83.33,100,100,100]
    mnb_recall_kompas = [40,100,100,100,80]
    
    imnb_accuracy_detik = [100,83.33,83.33,83.33,83.33]
    imnb_precision_detik = [100,83.33,83.33,83.33,83.33]
    imnb_recall_detik = [100,100,100,100,100]

    imnb_accuracy_kompas = [83.33,83.33,83.33,83.33,83.33]
    imnb_precision_kompas = [83.33,83.33,83.33,83.33,83.33]
    imnb_recall_kompas = [100,100,100,100,100]
    
    plt.figure(figsize=(20, 5))
    
    plt.subplot(131)
    plt.title("Accuracy")
    plt.plot(x, mnb_accuracy_detik, label = "MNB (Detik)" ,color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, mnb_accuracy_kompas, label = "MNB (Kompas)",color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.plot(x, imnb_accuracy_detik, label = "Improved MNB (Detik)" ,color='darkorchid', marker='s', markerfacecolor='thistle', markersize=8,linewidth=3) 
    plt.plot(x, imnb_accuracy_kompas, label = "Improved MNB (Kompas)",color='orangered', marker='s', markerfacecolor='lightcoral', markersize=8,linewidth=3) 
    plt.xlabel('Tahun')
    plt.ylabel('Accuracy (%)')
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
#    plt.yticks(np.arange(0, 102, step=10)) 
    
    plt.subplot(132)
    plt.title("Precision")
    plt.plot(x, mnb_precision_detik, label = "MNB (Detik)" ,color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, mnb_precision_kompas, label = "MNB (Kompas)",color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.plot(x, imnb_precision_detik, label = "Improved MNB (Detik)" ,color='darkorchid', marker='s', markerfacecolor='thistle', markersize=8,linewidth=3) 
    plt.plot(x, imnb_precision_kompas, label = "Improved MNB (Kompas)",color='orangered', marker='s', markerfacecolor='lightcoral', markersize=8,linewidth=3) 
    plt.xlabel('Tahun')
    plt.ylabel('Precision (%)')
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.legend(bbox_to_anchor=(0., 1.08, 1., .102), loc='center',
           ncol=4, borderaxespad=0.,frameon=False)
    
    plt.subplot(133)
    plt.title("Recall")
    plt.plot(x, mnb_recall_detik, label = "MNB Detik" ,color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, mnb_recall_kompas, label = "MNB Kompas",color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.plot(x, imnb_recall_detik, label = "IMNB Detik" ,color='darkorchid', marker='s', markerfacecolor='thistle', markersize=8,linewidth=3) 
    plt.plot(x, imnb_recall_kompas, label = "IMNB Kompas",color='orangered', marker='s', markerfacecolor='lightcoral', markersize=8,linewidth=3) 
    
    plt.xlabel('Tahun')
    plt.ylabel('Recall (%)')
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
#    plt.suptitle('Hasil Uji Coba Multiomial Naive Bayes - Skenario 2')  
    plt.show()
    
def plot_mnb_sk_3():
    # Training data : Seluruh Tahun, Testing data : Pertahun
    x = ["2016","2017","2018","2019","2020"] 
    
    mnb_accuracy_detik = [60,80,96.67,83.33,83.33]
    mnb_precision_detik = [100,100,100,100,100]
    mnb_recall_detik = [60,77.78,96.3,81.48,81.48]

    mnb_accuracy_kompas = [96.67,90,80,96.67,90]
    mnb_precision_kompas = [100,96.15,95.65,100,87.5]
    mnb_recall_kompas = [96,92.59,81.48,96.3,100]
    
    imnb_accuracy_detik = [83.33,83.33,96.67,90,90]
    imnb_precision_detik = [100,89.29,96.43,96.15,100]
    imnb_recall_detik = [83.33,92.59,100,92.59,88.89]

    imnb_accuracy_kompas = [90,96.67,90,90,80]
    imnb_precision_kompas = [89.29,96.43,92.86,90,77.78]
    imnb_recall_kompas = [100,100,96.3,100,100]
    
    
    
    plt.figure(figsize=(20, 5))
    
    plt.subplot(131)
    plt.title("Accuracy")
    plt.plot(x, mnb_accuracy_detik, label = "MNB (Detik)" ,color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, mnb_accuracy_kompas, label = "MNB (Kompas)",color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.plot(x, imnb_accuracy_detik, label = "Improved MNB (Detik)" ,color='darkorchid', marker='s', markerfacecolor='thistle', markersize=8,linewidth=3) 
    plt.plot(x, imnb_accuracy_kompas, label = "Improved MNB (Kompas)",color='orangered', marker='s', markerfacecolor='lightcoral', markersize=8,linewidth=3) 
    plt.xlabel('Tahun')
    plt.ylabel('Accuracy (%)')
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
    
    plt.subplot(132)
    plt.title("Precision")
    plt.plot(x, mnb_precision_detik, label = "MNB (Detik)" ,color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, mnb_precision_kompas, label = "MNB (Kompas)",color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.plot(x, imnb_precision_detik, label = "Improved MNB (Detik)" ,color='darkorchid', marker='s', markerfacecolor='thistle', markersize=8,linewidth=3) 
    plt.plot(x, imnb_precision_kompas, label = "Improved MNB (Kompas)",color='orangered', marker='s', markerfacecolor='lightcoral', markersize=8,linewidth=3) 
    plt.xlabel('Tahun')
    plt.ylabel('Precision (%)')
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.legend(bbox_to_anchor=(0., 1.08, 1., .102), loc='center',
           ncol=4, borderaxespad=0.,frameon=False)
    
    plt.subplot(133)
    plt.title("Recall")
    plt.plot(x, mnb_recall_detik, label = "MNB (Detik)" ,color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, mnb_recall_kompas, label = "MNB (Kompas)",color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.plot(x, imnb_recall_detik, label = "Improved MNB (Detik)" ,color='darkorchid', marker='s', markerfacecolor='thistle', markersize=8,linewidth=3) 
    plt.plot(x, imnb_recall_kompas, label = "Improved MNB (Kompas)",color='orangered', marker='s', markerfacecolor='lightcoral', markersize=8,linewidth=3) 
    plt.xlabel('Tahun')
    plt.ylabel('Recall (%)')
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
#    plt.suptitle('Hasil Uji Coba Multiomial Naive Bayes - Skenario 3')  
    plt.show() 

def plot_mnb_sk_4():
    # Training data : Pertahun, Testing data : Seluruh Tahun
    x = ["2016","2017","2018","2019","2020"] 
    
    mnb_accuracy_detik = [88.89,86,93.55,88.89,66.67]
    mnb_precision_detik = [100,100,100,95.24,100]
    mnb_recall_detik = [88.89,85.42,93.55,90.91,65]

    mnb_accuracy_kompas = [100,86,98.39,85.19,95.24]
    mnb_precision_kompas = [100,97.67,100,95,100]
    mnb_recall_kompas = [100,87.5,98.39,86.36,95]
    
    imnb_accuracy_detik = [100,94,100,90.74,95.24]
    imnb_precision_detik = [100,100,100,97.56,95.24]
    imnb_recall_detik = [100,93.75,100,90.91,100]

    imnb_accuracy_kompas = [100,88,100,94.44,95.24]
    imnb_precision_kompas = [100,97.73,100,100,95.24]
    imnb_recall_kompas = [100,89.58,100,93.18,100]
    
  
    
    plt.figure(figsize=(20, 5))
    
    plt.subplot(131)
    plt.title("Accuracy")
    plt.plot(x, mnb_accuracy_detik, label = "MNB (Detik)" ,color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, mnb_accuracy_kompas, label = "MNB (Kompas)",color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.plot(x, imnb_accuracy_detik, label = "Improved MNB (Detik)" ,color='darkorchid', marker='s', markerfacecolor='thistle', markersize=8,linewidth=3) 
    plt.plot(x, imnb_accuracy_kompas, label = "Improved MNB (Kompas)",color='orangered', marker='s', markerfacecolor='lightcoral', markersize=8,linewidth=3) 
    plt.yticks(np.arange(60, 110, step=10)) 
    plt.xlabel('Tahun')
    plt.ylabel('Accuracy (%)')
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
 
    plt.subplot(132)
    plt.title("Precision")
    plt.plot(x, mnb_precision_detik, label = "MNB (Detik)" ,color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, mnb_precision_kompas, label = "MNB (Kompas)",color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.plot(x, imnb_precision_detik, label = "Improved MNB (Detik)" ,color='darkorchid', marker='s', markerfacecolor='thistle', markersize=8,linewidth=3) 
    plt.plot(x, imnb_precision_kompas, label = "Improved MNB (Kompas)",color='orangered', marker='s', markerfacecolor='lightcoral', markersize=8,linewidth=3) 
    plt.yticks(np.arange(95, 101, step=1)) 
    plt.xlabel('Tahun')
    plt.ylabel('Precision (%)')
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.legend(bbox_to_anchor=(0., 1.08, 1., .102), loc='center',
           ncol=4, borderaxespad=0.,frameon=False)
    
    plt.subplot(133)
    plt.title("Recall")
    plt.plot(x, mnb_recall_detik, label = "MNB (Detik)" ,color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, mnb_recall_kompas, label = "MNB (Kompas)",color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.plot(x, imnb_recall_detik, label = "Improved MNB (Detik)" ,color='darkorchid', marker='s', markerfacecolor='thistle', markersize=8,linewidth=3) 
    plt.plot(x, imnb_recall_kompas, label = "Improved MNB (Kompas)",color='orangered', marker='s', markerfacecolor='lightcoral', markersize=8,linewidth=3) 
    plt.yticks(np.arange(60, 105, step=10)) 
    plt.xlabel('Tahun')
    plt.ylabel('Recall (%)')
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
#    plt.suptitle('Hasil Uji Coba Multiomial Naive Bayes - Skenario 4')  
    plt.show() 

def plot_scraping():
    x = ["1", "2","3","4","5"] 
    single_detik = [249.23,106.09,266.49,214.68,118.07]
    multi_detik = [259.71,260.91,206.38,94.90,178.22] 
    single_kompas = [66.26,54.19,53.84,50.94,49.93]
    multi_kompas= [62.94,43.87,45.00,43.00,43.57] 
    
#    single_detik = [4.15,1.77,4.44,3.58,1.97]
#    multi_detik = [4.33,4.35,3.44,1.58,2.97] 
#    single_kompas = [1.10,0.90,0.90,0.85,0.83]
#    multi_kompas= [1.05,0.73,0.75,0.72,0.73] 
    plt.figure(figsize=(13, 12))
    
    plt.subplot(221)
    plt.plot(x, single_detik, label = "Single" ,color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3)  
    plt.plot(x, multi_detik, label = "Multithread",color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.xlabel('Percobaan') 
    
    
#    plt.yticks(np.arange(0, 300, step=20)) 
    plt.ylabel('Waktu Scraping (seconds)') 
    plt.title('Media Online Detik') 
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.yticks(np.arange(0, 350, step=50)) 
    plt.legend(bbox_to_anchor=(0., 1.08, 2.1, .102), loc='center',
           ncol=4, borderaxespad=0.,frameon=False)
    
    plt.subplot(222)
    plt.plot(x, single_kompas, label = "Single" ,color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3)  
    plt.plot(x, multi_kompas, label = "Multithread",color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.xlabel('Percobaan')
    
    
#    plt.yticks(np.arange(0, 100, step=10)) 
    plt.ylabel('Waktu Scraping (second)') 
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.yticks(np.arange(0, 80, step=15)) 
    plt.title('Media Online Kompas') 
#    plt.suptitle('Hasil Uji Coba Scraping berita dengan Multithread') 
#    plt.tight_layout(pad=5)
    plt.show()

def plot_bfs_real():
    mnb_relevan_detik = [219, 222]
    mnb_relevan_kompas = [74,97]
    mnb_bfs_detik = [3, 248]
    mnb_bfs_kompas = [23, 140]
    mnb_relevan_dup_kompas = [77,150]
    
    plt.subplots(figsize =(14, 2)) 
    r = [0,2]
    r2 = [1,3]

    barWidth = 0.8
    
    plt.barh(r, mnb_relevan_detik, label = "Detik (Relevan)",color='orange', edgecolor='white', height=barWidth, zorder=2)
    plt.barh(r, mnb_bfs_detik, label = "Detik (Tidak Relevan)",left=mnb_relevan_detik, color='navajowhite', edgecolor='white', height=barWidth, zorder=2)
    plt.barh(r2, mnb_relevan_kompas, label = "Kompas (Relevan)", color='steelblue', edgecolor='white', height=barWidth, zorder=2)
    plt.barh(r2, mnb_bfs_kompas, label = "Kompas (Relevan namun duplikat)", left=mnb_relevan_kompas,  color='lightsteelblue', edgecolor='white', height=barWidth, zorder=2)
    plt.barh(r2, mnb_bfs_kompas, label = "Kompas (Tidak Relevan)", left=mnb_relevan_dup_kompas,  color='lightblue', edgecolor='white', height=barWidth, zorder=2)
    
#    plt.plot(mnb_relevan_detik, r, label = "Perbandingan",color='orangered', marker='o', markerfacecolor='lightcoral', markersize=10, zorder=3,linewidth=2) 
#    plt.plot(mnb_relevan_kompas, r2, color='orangered', marker='o', markerfacecolor='lightcoral', markersize=10, zorder=3,linewidth=2) 
    plt.text(109.5,-0.2,'219',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(111,1.8,'222',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(37,0.82,'74',fontsize=12,fontweight='bold',color ='white',horizontalalignment='center')
    plt.text(48.5,2.82,'97',fontsize=12,fontweight='bold',color ='white',horizontalalignment='center')
    plt.text(75.5,0.82,'3',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(123.5,2.82,'53',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(88.5,0.82,'30',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(220,2.82,'140',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(220.5,-0.2,'3',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    plt.text(346,1.8,'248',fontsize=12,fontweight='bold',color ='black',horizontalalignment='center')
    
    plt.xticks(np.arange(0, 500, step=30)) 
    plt.grid(zorder=0,axis='x',color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.yticks([r + barWidth for r in range(len(mnb_relevan_detik))], 
    		['Layer 1', 'Layer 2']) 
    plt.xlabel('Halaman yang di-crawling') 
    plt.ylabel('Layer') 
    plt.legend(bbox_to_anchor=(0., 1.4, 1., .102), loc='center',
           ncol=3, borderaxespad=0.,frameon=False)
    
    plt.show()
    
def plot_mnb_sk_1_mnb():
    # Training data : Seluruh Tahun, Testing data : Seluruh Tahun    
    x = ["1","2","3","4","5"]
    accuracy_p = [90.91,88.1,86.82,83.46,84]
    precision_p = [100,99.05,99.06,98.13,96.43]
    recall_p = [90.38,88.14,86.78,84,86.17]

    accuracy_m = [89.09,91.27,90.7,93.98,89]
    precision_m = [97.92,99.08,98.23,100,95.6]
    recall_m = [90.38,91.53,91.74,93.6,92.55]

    plt.figure(figsize=(20, 5))
    plt.subplot(131)
    plt.title("Accuracy")
    plt.plot(x, accuracy_p, color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, accuracy_m, color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.xlabel('Pengujian')
    plt.ylabel('Accuracy (%)')
    plt.yticks(np.arange(82, 102, step=2)) 

    plt.subplot(132)
    plt.title("Precision")
    plt.plot(x, precision_p, label = "Detik",  color='orange', marker='o',markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, precision_m, label = "Kompas", color='steelblue', marker='o', markerfacecolor='lightblue', markersize=8,linewidth=3) 
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.xlabel('Pengujian')
    plt.ylabel('Precision (%)')
    plt.yticks(np.arange(82, 102, step=2)) 
    plt.legend(bbox_to_anchor=(0., 1.08, 1., .102), loc='center',
           ncol=2, borderaxespad=0.,frameon=False)
    
    plt.subplot(133)
    plt.title("Recall")
    plt.plot(x, recall_p,  color='orange', marker='o', markerfacecolor='navajowhite', markersize=8,linewidth=3) 
    plt.plot(x, recall_m, color='steelblue', marker='o', markerfacecolor='lightblue',  markersize=8,linewidth=3) 
    plt.xlabel('Pengujian')
    plt.ylabel('Recall (%)')
    plt.yticks(np.arange(82, 102, step=2)) 
    
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
#    plt.suptitle('Hasil Uji Coba Multiomial Naive Bayes - Skenario 1')
    
    plt.show()
    
def plot_mnb_sk_1_imnb():
    # Training data : Seluruh Tahun, Testing data : Seluruh Tahun    
    x = ["1","2","3","4","5"]
    accuracy_p = [94.55,92.86,90.7,93.23,94]
    precision_p = [100,100,100,98.33,95.83]
    recall_p = [94.23,92.37,90.08,94.4,97.87]

    accuracy_m = [90.91,97.62,96.12,96.24,93]
    precision_m = [96.08,100,98.33,98.39,94.85]
    recall_m = [94.23,97.46,97.52,97.6,97.87]

    plt.figure(figsize=(20, 5))
    plt.subplot(131)
    plt.title("Accuracy")
    plt.plot(x, accuracy_p ,color='darkorchid', marker='s', markerfacecolor='thistle', markersize=8,linewidth=3) 
    plt.plot(x, accuracy_m,color='orangered', marker='s', markerfacecolor='lightcoral', markersize=8,linewidth=3) 
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.xlabel('Pengujian')
    plt.ylabel('Accuracy (%)')
    plt.yticks(np.arange(82, 102, step=2)) 

    plt.subplot(132)
    plt.title("Precision")
    plt.plot(x, precision_p, label = "Detik",color='darkorchid', marker='s', markerfacecolor='thistle', markersize=8,linewidth=3) 
    plt.plot(x, precision_m, label = "Kompas",color='orangered', marker='s', markerfacecolor='lightcoral', markersize=8,linewidth=3) 
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
    plt.xlabel('Pengujian')
    plt.ylabel('Precision (%)')
    plt.yticks(np.arange(82, 102, step=2)) 
    plt.legend(bbox_to_anchor=(0., 1.08, 1., .102), loc='center',
           ncol=2, borderaxespad=0.,frameon=False)
    
    plt.subplot(133)
    plt.title("Recall")
    plt.plot(x, recall_p,color='darkorchid', marker='s', markerfacecolor='thistle', markersize=8,linewidth=3) 
    plt.plot(x, recall_m,color='orangered', marker='s', markerfacecolor='lightcoral', markersize=8,linewidth=3) 
    plt.xlabel('Pengujian')
    plt.ylabel('Recall (%)')
    plt.yticks(np.arange(82, 102, step=2)) 
    
    plt.grid(zorder=0,color='gainsboro', linestyle='--',linewidth=1.5) 
#    plt.suptitle('Hasil Uji Coba Multiomial Naive Bayes - Skenario 1')
    
    plt.show()
#plot_bfs()
#plot_bfs_scraping()
plot_mnb_sk_1()
#plot_mnb_sk_2()
#plot_mnb_sk_3()
#plot_mnb_sk_4()
#plot_scraping()
#plot_bfs_real()
plot_mnb_sk_1_imnb()