#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 14:18:33 2017

@author: eobrien
"""
import requests
from bs4 import BeautifulSoup
import string

# What is the page base?
page_name = "https://en.wikipedia.org/wiki/Aaron_Carter"

page = requests.get(page_name)
soup = BeautifulSoup(page.content, 'html.parser')

# Get headlines
header_tags = soup.find_all("h2")
head_tag = soup.h2 # This is always contents

page_title = soup.h1.get_text().encode('utf-8', errors='ignore')
page_title= page_title.translate(None, string.punctuation).lower()
page_title_formatted = page_title.replace(" ", "_")

# Remove that it says wikipedia



for i in range(0, len(header_tags)-1):
    head_tag = head_tag.find_next('h2')
    head_text = head_tag.get_text().encode('utf-8', errors='ignore').replace('[edit]', '')
    head_text_formatted = head_text.replace(" ", "_").lower()
    
    
    # Get the text below that header and save it as a corpus.
    a = head_tag.find_next()
    advance = 0
    text = []
    while advance == 0 and a:
        if a.name == 'p' or a.name == 'li':
            
            text.append(a.get_text().encode('utf-8', errors= 'ignore'))
            a = a.find_next()
        elif a.name == 'h2':
            advance = 1
        else:
            a = a.find_next()
        
    # Write this to a corpus- format is subject, header, text.
    if text:
        file_base = "./Results/" + page_title_formatted +  '_' + head_text_formatted + ".txt"
        f = open(file_base,"w")
        for item in text:
          f.write("%s\n" % item)  
        f.close()
