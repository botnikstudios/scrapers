# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 12:35:07 2017
Savage Love Scraper
@author: Elle
"""

from bs4 import BeautifulSoup
import requests
import string
from datetime import datetime, timedelta
import re
import time



link_list = []

# Loop over every page on Dan Savage's archive
for page_num in range(10,61):
    page_link = "https://www.thestranger.com/archive/savage-love?page=" + str(page_num)
    page = requests.get(page_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    tags = soup.find_all(class_="article-list component")
    tags2 = tags[0].find_all(class_="headline")
    # Get the URL of every posting
    for i in range(0,len(tags2)):
        headline = tags2[i].find_all('a')
        link_tmp = headline[0]["href"]
        link_list.append(link_tmp)
    
# Now, go to each page and extract the text, then save to a text file
counter = 475
for index in range (0, len(link_list)):
    link = link_list[index]
    page = requests.get("https://thestranger.com" + link)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Tags- p, blockquote, name = more
    article = soup.find_all(class_="article-text category-slog")
    if article:
    # Quite difficult to suss out question and answer, so do it all
    #questions = article[0].find_all('blockquote')
    #answers = article[0].find_all(name="more")
        text_tags = article[0].find_all('p')
        text = [t.get_text().encode('utf-8') for t in text_tags]
        text = [t.replace("HUMP! 2017 Call for Submissions!","") for t in text]
        text = [t.replace("Listen to my podcast, the Savage Lovecast, at www.savagelovecast.com.","") for t in text]
        text = [t.replace("Impeach the motherfucker already! Get your ITMFA buttons, t-shirts, hats and lapel pins and coffee mugs at www.ITMFA.org!","") for t in text]
    
        filebase= "./Results/article_" + str(counter)
        f = open(filebase + ".txt","w")
        for item in text:
            f.write(item + '\n')
        f.close()
        
        counter += 1
        