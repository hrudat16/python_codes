# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 16:23:15 2019

@author: hrudat
"""

import requests, zipfile, os, io,glob, pandas as pd
from datetime import datetime,timedelta,date
import holidays
import pandas as pd
import xlrd as xld

# Code to check public holiday in this case it's India You can extract data for other countries

FD = date.today() 
India_holidays = holidays.India()

if FD in India_holidays:
    yesterday = datetime.now() - timedelta(days=1)
else:
    yesterday = datetime.now()

# File Download code
mydate = datetime.now()
mth=mydate.strftime("%b")
ustr=str(mth)
Y = str(yesterday.year)
D = str(yesterday.day)
M = ustr.upper()

D1 =  yesterday.day

if D1 < 9:
    str1 = "https://www1.nseindia.com/content/historical/EQUITIES/"+Y+"/"+M+"/cm0"+D+M+Y+"bhav.csv.zip"
    
else:
    str1 = "https://www1.nseindia.com/content/historical/EQUITIES/"+Y+"/"+M+"/cm"+D+M+Y+"bhav.csv.zip"

# Extracting downloaded file
udownload = requests.get(str1,stream=True)
zfile = zipfile.ZipFile(io.BytesIO(udownload.content))
zfile.extractall()
zfile.extractall(path="E:/Bhavcopies/")
file=max(glob.glob("E:/Bhavcopies/*"), key=os.path.getctime)

#Pickup latest file and analysis code starts here
if D1 < 9:
    latest_file = glob.glob("E:/Bhavcopies/cm0"+D+M+Y+"bhav.csv.zip")

else:
    latest_file = glob.glob("E:/Bhavcopies/cm"+D+M+Y+"bhav.csv.zip")

cf =  pd.read_csv ("cm10JAN2020bhav.csv", usecols = ['SYMBOL','HIGH','LOW','CLOSE'])

df =  pd.DataFrame(cf)

df['PIVOT POINT'] = (df['HIGH']+df['LOW']+df['CLOSE'])/3
df['R1'] = (2*df['PIVOT POINT'])-df['LOW']
df['R2'] = df['PIVOT POINT'] - (df['LOW']-df['CLOSE'])
df['R3'] = df['HIGH']+(2*(df['PIVOT POINT']-df['LOW']))
df['S1'] = (2 * df['PIVOT POINT']) - df['HIGH'] 
df['S2'] = df['PIVOT POINT'] - (df['HIGH']-df['LOW'])
df['S3'] = df['LOW']+(2*(df['HIGH']-df['PIVOT POINT']))

final_excel = df.round()

final_excel.to_excel(r'E:\bhavcopies\Final_daily_data_'+D+M+Y+'.xlsx')
