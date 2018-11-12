# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 14:06:15 2018

@author: andro
"""

from bs4 import BeautifulSoup
import requests
import re

link_list = []
# Get a list of products to browse
for page_num in range(1,3):
    page_link = "https://www.sephora.com/search/search.jsp?keyword=lip%20gloss&mode=all&currentPage=" + str(page_num)
    page = requests.get(page_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    tags = soup.find_all(id="searchResult")
    tags_text = tags[0].get_text()
    link_list_tmp = re.findall('"product_url":"([^"]*)"', tags_text)
    # Append to list of links
    link_list.append(link_list_tmp)

# Flatten it
flat_list = [item for sublist in link_list for item in sublist]
col_list_long = []

for link in flat_list:
    page_link = "https://www.sephora.com" + link
    page = requests.get(page_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    color_tag = soup.find_all(class_="css-1o1r7cl")
    colors_tag = soup.find_all(type= "application/ld+json")
    if colors_tag and len(colors_tag) > 1:
        s = colors_tag[1].get_text()
        
        col_list = s.split('[', 1)[1].split(']')[0]
        
        col_list = col_list.replace('\"',"")
        col_list = col_list.split(",")
        col_list_long.append(col_list)

flat_list_col = [item for sublist in col_list_long for item in sublist]


f = open('sephora_lipgloss_out.txt','w')
for item in flat_list_col:
    f.write(item + '\n')
f.close()