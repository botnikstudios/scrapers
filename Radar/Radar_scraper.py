# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 16:22:30 2017

@author: Elle
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file. It scrapes people.com
"""
from bs4 import BeautifulSoup
import requests
import string
from datetime import datetime, timedelta
import re
import time
from dateutil import parser

search_term = "Ryan Reynolds"
days_ago = 15
# Take out any punctuation marks from name and convert to lowercase
search_term = search_term.translate(None, string.punctuation)
search_term = search_term.lower()

# 
# Format search term for the URL formula
search_term_formatted = search_term.replace(" ", "+")

# For TMZ, update the search formula
#page_link = 'http://eonline.com/search?query=' + search_term_formatted 

page_link = "http://radaronline.com/search/?search=" + search_term_formatted
#page_link = "https://cnn.com"
page = requests.get(page_link)
soup = BeautifulSoup(page.content, 'html.parser')

timestamp = []
article_link_list = []
stories = []
headlines = []
fetched_stories = []
fetched_headlines = []

articles = soup.find_all('article')

# For every article on the page, get the link and the time it was posted at.
for i in range(0,len(articles)):
    this_article = articles[i]
    
    headline_tag = this_article.find_all(class_="promo-title")
    date_tag = this_article.find_all(class_="posted-date")
    link_tag = this_article.find_all("a")
    
    # Update headline list 
    headline = headline_tag[0].get_text()
    headlines.append(headline.encode('utf-8'))
    
    # Get the link
    link = link_tag[0]['href']
    article_link_list.append(link.encode('utf-8'))
    
    # Get the date stamp in the correct format
    date_full = date_tag[0].get_text()
    date_full = date_full.encode('utf-8')  #encode into utf-8 string
    date_short = re.findall('(?<=Posted )(.*)(?= @)', date_full)
    timestamp.append(parser.parse(date_short[0]))
    
   
# NEXT PART: Figure out which dates are within a window    
# Which articles were posted within N days?    
is_recent = [datetime.today() - timedelta(days=days_ago) < x for x in timestamp]
link_indices = [i for i, x in enumerate(is_recent) if x]

for i in range(0,len(link_indices)):
    page_result_link = article_link_list[link_indices[i]]
    page_result = requests.get(page_result_link)
    res_soup = BeautifulSoup(page_result.content, 'html.parser')
    story_tag = res_soup.find_all(class_="entry")
    if story_tag: # Gracefully handle in case nothing comes up
        story = story_tag[0].get_text()
        fetched_stories.append(story.encode('utf-8', errors='ignore'))
    
        title = headlines[link_indices[i]]
        fetched_headlines.append(title)

# Write results to a CSV.
file_base = "Radar_" + search_term.lower().replace(" ", "_") + "_" + time.strftime("%d_%m_%y")
f = open(file_base + "_headlines.txt","w")
for item in fetched_headlines:
  f.write("%s\n" % item)  
f.close()

f = open(file_base + "_articles.txt","w")
for item in fetched_stories:
  f.write("%s\n" % item)  
f.close()
