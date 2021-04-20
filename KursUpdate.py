#!/usr/bin/env python3

# Skriptu napravio  Miodrag Mijatovic  2020

import cx_Oracle
import smtplib 
from email.mime.text import MIMEText 
import requests as req 
import datetime
from bs4 import BeautifulSoup
import re

# Datumi
now = datetime.datetime.now() 
current_time = now.strftime("%Y-%m-%d") 
print("Current Time =", current_time,now) 
datum = now.strftime("%d-%m-%Y") 
datum1 = "Kurs eura na dan: ", datum 
datumsubject = ''.join(map(str, datum1)) #spajanje u string
datumsql = now.strftime("%Y-%m-%d")


# Scraping NBS Broj oznacava poziciju zeljene vrednost (broj celije u 
# kojojse nalazi kurs)
# Kupovni_kurs _kk   Prodajni_kurs  _pk  


#=============================================================================
page = req.get("https://www.nbs.rs/kursnaListaModul/zaDevize.faces?lang=lat")
soup = BeautifulSoup(page.content, 'html.parser')
rows = soup.select('tbody td')
kurse = soup.find_all(style=True)
kursEUR_kk3 = str(rows[5])
kursEUR_pk3 = str(rows[6])
kursCHF_kk3 = str(rows[83])
kursCHF_pk3 = str(rows[84])
kursUSD_kk3 = str(rows[95])
kursUSD_pk3 = str(rows[96])

kursEUR_kk2 = kursEUR_kk3.replace("<td>", "")
kursEUR_pk2 = kursEUR_pk3.replace("<td>", "")
kursCHF_kk2 = kursCHF_kk3.replace("<td>", "")
kursCHF_pk2 = kursCHF_pk3.replace("<td>", "")
kursUSD_kk2 = kursUSD_kk3.replace("<td>", "")
kursUSD_pk2 = kursUSD_pk3.replace("<td>", "")

kursEUR_kk0 = kursEUR_kk2.replace("</td>", "")
kursEUR_pk0 = kursEUR_pk2.replace("</td>", "")
kursCHF_kk0 = kursCHF_kk2.replace("</td>", "")
kursCHF_pk0 = kursCHF_pk2.replace("</td>", "")
kursUSD_kk0 = kursUSD_kk2.replace("</td>", "")
kursUSD_pk0 = kursUSD_pk2.replace("</td>", "")

kursEUR_kk = kursEUR_kk0.replace(",", ".")
kursEUR_pk = kursEUR_pk0.replace(",", ".")
kursCHF_kk = kursCHF_kk0.replace(",", ".")
kursCHF_pk = kursCHF_pk0.replace(",", ".")
kursUSD_kk = kursUSD_kk0.replace(",", ".")
kursUSD_pk = kursUSD_pk0.replace(",", ".")
print("Prodajni kurs Kupovni kurs",kursEUR_pk,kursEUR_kk,kursCHF_pk,kursCHF_kk,kursUSD_kk,kursUSD_pk)
#=============================================================================


page1 = req.get("https://www.nbs.rs/kursnaListaModul/srednjiKurs.faces?lang=lat",verify=False)
soup1 = BeautifulSoup(page1.content, 'html.parser')
rows1 = soup1.select('tbody td')
#kurse1 = soup1.find_all(style=True)
kursEUR3 = str(rows1[5])
kursCHF3 = str(rows1[70])
kursUSD3 = str(rows1[80])   

kursEUR2 = kursEUR3.replace("<td>", "")
kursCHF2 = kursCHF3.replace("<td>", "")
kursUSD2 = kursUSD3.replace("<td>", "")

kursEUR = kursEUR2.replace("</td>", "")
kursCHF = kursCHF2.replace("</td>", "")
kursUSD = kursUSD2.replace("</td>", "")

kursEUR_s = kursEUR.replace(",", ".")
kursCHF_s = kursCHF.replace(",", ".")
kursUSD_s = kursUSD.replace(",", ".")

print("Srednji Kurs",kursEUR_s,kursCHF_s,kursUSD_s)


#EUR
E_CURRENCY1 = "EUR" 
E_VALUE1 = 1 
E_CURRENCY2 = "RSD"
#E_CURRENCY_DATE = now
E_SYSTEMDATE = datumsql +" "+ current_time 
E_SYSTEMUSER = "SYSTEM" 
E_VALUE2_B = kursEUR_kk 
E_VALUE2_M = kursEUR_s
E_VALUE2_S = kursEUR_pk


#CHF 
C_CURRENCY1 = "CHF" 
C_VALUE1 = 1 
C_CURRENCY2 = "RSD"
C_SYSTEMDATE = datumsql +" "+ current_time 
C_SYSTEMUSER = "SYSTEM" 
C_VALUE2_B = kursCHF_kk
C_VALUE2_M = kursCHF_s
C_VALUE2_S = kursCHF_pk

#USD
U_CURRENCY1 = "USD" 
U_VALUE1 = 1 
U_CURRENCY2 = "RSD"
U_SYSTEMDATE = datumsql +" "+ current_time 
U_SYSTEMUSER = "SYSTEM" 
U_VALUE2_B = kursUSD_kk
U_VALUE2_M = kursUSD_s
U_VALUE2_S = kursUSD_pk


def sendmail_Kurs():
   
    a = "EUR: "+ kursEUR_kk +' '+ kursEUR_s + ' '+kursEUR_pk +'\n'+ "CHF: "+ kursCHF_kk +' '+ kursCHF_s + ' '+kursCHF_pk +'\n'+ "USD: "+ kursUSD_kk +' '+ kursUSD_s + ' '+kursUSD_pk
    msg = MIMEText(a)
    me = "MAIL FROM"
    you = "MAIL TO"
    msg['Subject'] = "Kurs eura na dan: "+ datum
    msg['From'] = me
    msg['To'] = you
    s = smtplib.SMTP('ENTER YOUR SMTP')
    s.sendmail(me, [you], msg.as_string())
    s.quit()


def sendmail_error():
   
    a = "Problem sa Oracle kursom"
    msg = MIMEText(a)
    me = "MAIL FROM"
    you = "MAIL TO"
    msg['Subject'] = "Error Kurs eura na dan: "+ datum
    msg['From'] = me
    msg['To'] = you
    s = smtplib.SMTP('ENTER YOUR SMTP')
    s.sendmail(me, [you], msg.as_string())
    s.quit()


# Konekcija sa bazom
dsn_tns = cx_Oracle.makedsn('IP', 'PORT', service_name='S_NAME') 
conn = cx_Oracle.connect(user='user', password='password', dsn=dsn_tns)
c = conn.cursor()


c.execute(''' INSERT INTO MATRIX.CURRENCY_CONVERSION(CURRENCY1,VALUE1,CURRENCY2,CURRENCY_DATE,VALUE2_B,VALUE2_M,VALUE2_S)
          VALUES (:a1,:a2,:a3,TO_DATE(:a4, 'yyyy-mm-dd'),:a5,:a6,:a7) '''
          ,a1 = E_CURRENCY1, a2 = E_VALUE1, a3 = E_CURRENCY2, a4= current_time, a5 = E_VALUE2_B,a6 = E_VALUE2_M,a7 = E_VALUE2_S)
EE = c.rowcount

c.execute(''' INSERT INTO MATRIX.CURRENCY_CONVERSION(CURRENCY1,VALUE1,CURRENCY2,CURRENCY_DATE,VALUE2_B,VALUE2_M,VALUE2_S)
          VALUES (:a1,:a2,:a3,TO_DATE(:a4, 'yyyy-mm-dd'),:a5,:a6,:a7) '''
          ,a1 = C_CURRENCY1, a2 = C_VALUE1, a3 = C_CURRENCY2, a4= current_time, a5 = C_VALUE2_B,a6 = C_VALUE2_M,a7 = C_VALUE2_S)
CC = c.rowcount

c.execute(''' INSERT INTO MATRIX.CURRENCY_CONVERSION(CURRENCY1,VALUE1,CURRENCY2,CURRENCY_DATE,VALUE2_B,VALUE2_M,VALUE2_S)
          VALUES (:a1,:a2,:a3,TO_DATE(:a4, 'yyyy-mm-dd'),:a5,:a6,:a7) '''
          ,a1 = U_CURRENCY1, a2 = U_VALUE1, a3 = U_CURRENCY2, a4= current_time, a5 = U_VALUE2_B,a6 = U_VALUE2_M,a7 = U_VALUE2_S)
UU = c.rowcount

RowCount = EE+CC+UU 

if RowCount == 3:
    sendmail_Kurs() 
else:
    sendmail_error() 


conn.commit()
conn.close()
# hh24:mi:ss'
