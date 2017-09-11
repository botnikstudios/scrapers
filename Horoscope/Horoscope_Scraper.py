# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 19:53:07 2017
This script scrapes horoscopes.com
@author: Elle
"""

from bs4 import BeautifulSoup
import requests
import string
from datetime import datetime, timedelta


numdays = 365
base = datetime.today()
date_list = [base - timedelta(days=x) for x in range(0, numdays)]

# Make horoscope dictionary
#hdict = {'aries':'1','taurus':'2','gemini':'3','cancer':'4','leo':'5', 'virgo':'6', \
#         'libra':'7','scorpio':'8','sagittarius':'9','capricorn':'10','aquarius':'11','pisces':'12'}
hlist = ['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio',\
         'sagittarius','capricorn','aquarius','pisces']
for h in range(0,len(hlist)):
    corpus = []
    for i in range(0,len(date_list)):
        d = date_list[i]
        search_date = d.strftime("%Y%m%d")
        page_link = "https://www.horoscope.com/us/horoscopes/general/horoscope-archive.aspx?sign=" + str(h+1) + "&laDate=" + search_date
        #page_link = "https://cnn.com"
        page = requests.get(page_link)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        horoscope_tag = soup.find_all(class_="horoscope-content")
        horoscope_text = horoscope_tag[0].get_text().encode('utf-8')
        
        # Use regular expression to clean out anything but the horoscope
        split_date = horoscope_text.split('-')
        date = split_date[0].strip().translate(None, string.punctuation)
        body = split_date[1].split('\n')[0]
        
        corpus.append(body)
        
    ##### Print it!
    file_base = "./Results/" + hlist[h] + "_" + str(numdays) + "_days"
    f = open(file_base + ".txt","w")
    for item in corpus:
        f.write(item + '\n')
    f.close()