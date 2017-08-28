# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 15:44:32 2017

@author: Elle
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:32:34 2017

@author: Elle
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file. It scrapes buzzfeed.com
"""
from bs4 import BeautifulSoup
import requests
import string
import re
from selenium import webdriver
from dateutil import parser
from datetime import datetime, timedelta
import time
from HTMLParser import HTMLParser 

h = HTMLParser()

search_term = "Taylor Swift"
days_ago = 2
# Take out any punctuation marks from name and convert to lowercase
search_term = search_term.translate(None, string.punctuation)
search_term = search_term.lower()

# 
# Format search term for the URL formula
search_term_formatted = search_term.replace(" ", "+")

# For TMZ, update the search formula
#page_link = 'http://eonline.com/search?query=' + search_term_formatted 

page_link = "http://tmz.com/search/news/" + search_term_formatted +"?adid=TMZ_Web_Nav_Search"
domain = "http://www.tmz.com"

#page_link = "https://cnn.com"
#page = requests.get(page_link)
#soup = BeautifulSoup(page.content, 'html.parser')

browser = webdriver.Chrome()
browser.get(page_link)
html = browser.page_source
browser.close()
browser.quit()

soup = BeautifulSoup(html, 'html.parser')
articles = soup.find_all(class_ = "title") # This will get some junk, too. 


#### Initialize the vectors for storing results
timestamp= []
article_link_list = []
headlines_list = []
fetched_stories = []
fetched_headlines=[]

for i in range(1, len(articles)):
    this_article = articles[i]
    child = articles[i].find_all(class_="has-adid")
    
    # If it really is a search result- as in, child isn't empty-
    if child:
        headline = child[0].get_text()
        link = child[0]['href']
        article_link_list.append(link.encode('utf-8', errors='ignore'))
        date = link[1:12].encode('utf-8', errors='ignore') # TMZ encodes date strings in first 12 char of URL
        timestamp.append(parser.parse(date))

##### Of the results we got, how many are recent enough?
is_recent = [datetime.today() - timedelta(days=days_ago) < x for x in timestamp]
link_indices = [i for i, x in enumerate(is_recent) if x]

# Loop over the recent results
for i in range(0,len(link_indices)):
    page_result_link = domain + article_link_list[link_indices[i]]
    page_result = requests.get(page_result_link)
    res_soup = BeautifulSoup(page_result.content, 'html.parser')
    story_tag = res_soup.find_all(type="application/ld+json")
    story_tmp = story_tag[0].get_text()
    story = re.findall('articleBody": "(.*?)"\n}', story_tmp)
    
    # Clean up the text- TMZ litters with HTML string
    story = story[0].encode('utf-8').replace('\\n', ' ')
    story = h.unescape(story)
    story = story.encode('utf-8').replace('\\', ' ')
    
    
    headline = re.findall('headline": "(.*?)",', story_tmp)
    headline = h.unescape(headline[0])
    headline = headline.encode('utf-8')

    
    fetched_stories.append(story)
    fetched_headlines.append(headline)
    
    
    
##################### Write to file ##########################


file_base = "TMZ_" + search_term.lower().replace(" ", "_") + "_" + time.strftime("%d_%m_%y")
f = open(file_base + "_headlines.txt","w")
for item in fetched_headlines:
  f.write("%s\n" % item)  
f.close()

f = open(file_base + "_articles.txt","w")
for item in fetched_stories:
  f.write("%s\n" % item)  
f.close()


