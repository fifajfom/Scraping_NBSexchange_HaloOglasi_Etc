#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 08:32:48 2020

@author: m.mijatovic
"""
import requests as req
#import datetime
from bs4 import BeautifulSoup
from xlsxwriter import Workbook
import datetime
import mysql.connector
from mysql.connector import Error


now = datetime.datetime.now()
citydatenow = now.strftime("%d.%m.%Y") 
datum = now.strftime("%d-%m-%Y") 
datum1 = "Stanovi_", datum  
datumsubject = ''.join(map(str, datum1))
cc = ".xlsx"
datummysql = now.strftime("%Y-%m-%d") 



# Stranice sa weba
# Beograd

# Čukarica
page2 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-cukarica")
soupCUK = BeautifulSoup(page2.content, 'html.parser')
# Barajevo
page3 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-barajevo")
soupBAR = BeautifulSoup(page3.content, 'html.parser')
# Voždovac
page4 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-vozdovac")
soupVOZ = BeautifulSoup(page4.content, 'html.parser')
# Novi Beograd
page5 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-novi-beograd")
soupNBG = BeautifulSoup(page5.content, 'html.parser')
# Vračar
page6 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-vracar")
soupVR = BeautifulSoup(page6.content, 'html.parser')
# Zvezdara
page7 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-zvezdara")
soupZVE = BeautifulSoup(page7.content, 'html.parser')
# Palilula
page8 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-palilula")
soupPAL = BeautifulSoup(page8.content, 'html.parser')
# Borca
page9 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-palilula-borca")
soupBOR = BeautifulSoup(page9.content, 'html.parser')
# Krnjača
page10 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-palilula-krnjaca")
soupKRN = BeautifulSoup(page10.content, 'html.parser')
# Mladenovac
page11 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-mladenovac")
soupMLA = BeautifulSoup(page11.content, 'html.parser')
# Lazarevac
page12 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-lazarevac")
soupLAZ = BeautifulSoup(page12.content, 'html.parser')
# Grocka
page13 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-grocka")
soupGRO = BeautifulSoup(page13.content, 'html.parser')
# Stari Grad
page14 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-stari-grad")
soupSGR = BeautifulSoup(page14.content, 'html.parser')
# Mirijevo
page15 = req.get("https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-zvezdara-mirijevo")
soupMIR = BeautifulSoup(page15.content, 'html.parser')

gradsql = []
cenaD = []
final_average = []
final_average1 = []
broj_soba = []
m2 = []
m22 = []
cenam2 = []
ime_nekretnine = []
link = []
opis = []
bs = []
final_average = []
count=[]    
cena_nekretnine1 = []
cena_nekretnine = []
bs = []

def TruncateAdsCities():
        try:
            connection = mysql.connector.connect(host='localhost',
                                                  database='DB',
                                                  user='Username',
                                                  password='Password')
            cursor = connection.cursor()
            mySql_insert_query = """truncate ads_bgd """
            cursor.execute(mySql_insert_query)
            connection.commit()
            print("DB ads_cities now is empty")
    
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
    
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                


def insertAdsCities(grad, br_soba, m2, cenam2, cena_nekretnine, link, opis, datum):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                  database='DB',
                                                  user='Username',
                                                  password='Password')
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO ads_bgd (city, rooms, sq_m, price_sq_m, total_price, link, description, date) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """
    
            recordTuple = (grad, br_soba, m2, cenam2, cena_nekretnine, link, opis, datum)
            cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
            print("Record inserted successfully into opstine " + gradsql[0])
    
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
    
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                
                
def insertAdsCitiesAverage(citydate,average,datum):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                  database='DB',
                                                  user='Username',
                                                  password='Password')
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO ads_bgd_average (city, avg_sq_m, date) 
                                    VALUES (%s, %s, %s)"""
    
            recordTuple = (citydate,average,datum)
            cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
            print("Record inserted successfully into opstine " + citydate[0])
    
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
    
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
 
def Average(cenam2): 
    return sum(cenam2) / len(cenam2)                

def Clear():
    cenaD.clear()
    broj_soba.clear()
    cenam2.clear()
    ime_nekretnine.clear()
    m2.clear();
    final_average.clear()
    final_average1.clear()
    count.clear()
    gradsql.clear()
    link.clear()
    cena_nekretnine.clear()
    cena_nekretnine1.clear()
    bs.clear()
    opis.clear()


def AdsCity(soupp,cityy):
# LINK  
    for section in soupp.findAll("div", class_="col-md-6 col-sm-5 col-xs-6 col-lg-6 sm-margin"):
        nextNode = section
        link.append("https://www.halooglasi.com"+section.find('a')['href'])
        while True:
            nextNode = nextNode.find_next_sibling()
            if nextNode and nextNode.name == 'a':
                print (nextNode)
            else:
                break
            
    if  not link:
      print(cityy, " is empty")
    else:   
        
    # M2
        for section in soupp.findAll("div", class_="value-wrapper"):
            nextNode = section
            #print (" %s " % section.text)
            m22.append("%s" % section.text)
            while True:
                nextNode = nextNode.find_next_sibling()
                if nextNode and nextNode.name == 'span':
                    print (nextNode)
                else:
                    break
                
    # odvajanje rezultata M2
        subs = '\xa0m2Kvadratura' 
        res = [i for i in m22 if subs in i ] 
        bs = res.copy()   
    
        if len(bs) == 0:
            m2.append("0")
        else: 
            for p in bs: 
                    cc = p.replace('\xa0m2Kvadratura','')
                    bb = cc.replace('+','.0')
                    m2.append(bb)   
    
                
    #OPIS
    
        for section in soupp.findAll('h3'):
            nextNode = section
            # print (" %s " % section.text)
            opis.append("%s" % section.text)
            while True:
                nextNode = nextNode.find_next_sibling()
                if nextNode and nextNode.name == 'li':
                    print (nextNode)
                else:
                    break
                
    # Priprema za broj soba       
        for section in soupp.findAll('div',class_="value-wrapper"):
            nextNode = section
            ime_nekretnine.append("%s" % section.text)
            while True:
                nextNode = nextNode.find_next_sibling()
                if nextNode and nextNode.name == 'li':
                    print (nextNode)
                else:
                    break
    # odvajanje rezultata tj biranje samo broj soba  
        subs = '\xa0Broj soba' 
        res = [i for i in ime_nekretnine if subs in i ] 
        bs = res.copy()   
    
        if len(bs) == 0:
            broj_soba.append("0.00")
        else: 
            for p in bs: 
                    cc = p.replace('\xa0Broj soba','')
                    bb = cc.replace('+','.0')
                    broj_soba.append(bb)   
    
    
    # Cena m2
        for section in soupp.findAll("div", class_="price-by-surface"):
                nextNode = section
                cenaD.append("%s" % section.text)
                while True:
                    nextNode = nextNode.find_next_sibling()
                    if nextNode and nextNode.name == 'span':
                        print (nextNode)
                    else:
                        break
    
        if len(cenaD) == 0:
            final_average.append("0.00")
        else: 
            for p in cenaD: 
                    aa = p.replace('.','')
                    bb = aa.replace(' €/m2','')
                    cenam2.append(int(bb))   
                    
    # CENA Full
    
        for section in soupp.findAll("div", class_="central-feature"):
            nextNode = section
            cena_nekretnine1.append("%s" % section.text)
            while True:
                nextNode = nextNode.find_next_sibling()
                if nextNode and nextNode.name == 'span':
                    print (nextNode)
                else:
                    break
                
        if len(cena_nekretnine1) == 0:
            final_average1.append("0.00")
        else: 
            for pp in cena_nekretnine1: 
                    aaa = pp.replace('.','')
                    bbb = aaa.replace('\xa0€','')
                    cena_nekretnine.append(int(bbb))             
        
    #    print(m2)     
                
        average2 = Average(cenam2)
        average =  round(average2, 2)
        citydate = cityy                            #+citydatenow
        try:
           
              insertAdsCitiesAverage(citydate,average,datummysql)
                    
        except:
                print('GREŠKA AVG ' + gradsql[0] )      
      
        gradsql.append(cityy)
        mysqll = []  
        brr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]      
        if len(mysqll) < len(broj_soba):
            try:
                for brb in brr:
                    insertAdsCities(gradsql[0], broj_soba[brb], m2[brb], cenam2[brb], cena_nekretnine[brb], link[brb], opis[brb], datummysql)
                    
            except:
                print('GREŠKA ' + gradsql[0] )
        # print(gradsql,broj_soba[0],cenam2[0], link[0])
        # print(opis[0],cena_nekretnine[0])
        Clear()

Clear()
TruncateAdsCities()
AdsCity(soupCUK,"Čukarica ")
AdsCity(soupBAR,"Barajevo ")
AdsCity(soupVOZ,"Voždovac ")
AdsCity(soupNBG,"NoviBeograd ")
AdsCity(soupVR,"Vračar ")
AdsCity(soupZVE,"Zvezdara ")
AdsCity(soupPAL,"Palilula ")
AdsCity(soupBOR,"Borča ")
AdsCity(soupKRN,"Krnjača ")
AdsCity(soupMLA,"Mladenovac ")
AdsCity(soupLAZ,"Lazarevac ")
AdsCity(soupGRO,"Grocka ")
AdsCity(soupSGR,"StariGrad ")
AdsCity(soupMIR,"Mirijevo ")
