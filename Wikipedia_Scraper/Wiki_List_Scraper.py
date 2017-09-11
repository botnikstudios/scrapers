# -*- coding: utf-8 -*-
"""
WIKI LIST SCRAPER
Created on Sat Sep 09 17:13:30 2017

@author: Elle
"""

import requests
from bs4 import BeautifulSoup
import string

# What is the page base?
page_name = "https://en.wikipedia.org/wiki/List_of_people_who_were_beheaded"

page = requests.get(page_name)
soup = BeautifulSoup(page.content, 'html.parser')

header_tags = soup.find_all("h2")
head_tag = soup.h2 # This is always contents

links = []

for i in range(1, len(header_tags)-4):
    head_tag = header_tags[i]

    
    # Get the text below that header and save it as a corpus.
    a = head_tag.find_next()
    advance = 0
    while advance == 0 and a:
        entries = a.find_all('li')
        if a.name == 'ul' and entries:
            for j in range(0,len(entries)):
                if entries[j].a: 
                    links.append(entries[j].a['href'])
            a = a.find_next()
        elif a.name == 'h2':
            advance = 1
        else:
            a = a.find_next()
            
######### Now we have a list of links. ###########
#### Our job is to loop over that list and extract everything from those pages. ##
for j in range(0, len(links)):
    page_name = "https://en.wikipedia.org" + links[j]
    
    page = requests.get(page_name)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Get headlines
    header_tags = soup.find_all("h2")
    head_tag = soup.h2 # This is always contents
    
    page_title = soup.h1.get_text().encode('utf-8', errors='ignore')
    page_title= page_title.translate(None, string.punctuation).lower()
    page_title_formatted = page_title.replace(" ", "_")
    
    # Remove that it says wikipedia
    
    
    
    for i in range(0, len(header_tags)):
        head_tag = head_tag.find_next('h2')
        head_text = head_tag.get_text().encode('utf-8', errors='ignore').replace('[edit]', '')
        head_text_formatted = head_text.replace(" ", "_").lower()
        
        # If this isn't references, navigation, see also...
        nonolist = ['navigation_menu','references','see_also','notes','further_reading','citations','footnotes','external_links']
        
        
        if not (head_text_formatted in nonolist):
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
                file_base = "./Results/Beheading/" + page_title_formatted +  '__' + head_text_formatted + ".txt"
                f = open(file_base,"w")
                for item in text:
                  f.write("%s\n" % item)  
                f.close()
        
