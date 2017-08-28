# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:04:28 2017

@author: Elle
"""

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

page_link = "http://eonline.com/search?query=" + search_term_formatted 
domain = "http://www.eonline.com"

#page_link = "https://cnn.com"
#page = requests.get(page_link)
#soup = BeautifulSoup(page.content, 'html.parser')

browser = webdriver.Chrome()
browser.get(page_link)
html = browser.page_source
browser.close()
browser.quit()

soup = BeautifulSoup(html, 'html.parser')
articles = soup.find_all(class_ = "result") # This will get some junk, too. 


#### Initialize the vectors for storing results
timestamp= []
article_link_list = []
headlines_list = []
fetched_stories = []
fetched_headlines=[]

for i in range(0, len(articles)):
    this_article = articles[i]
    
    
    headline_tag = this_article.find_all(class_="result-body")
    date_tag = this_article.find_all(class_="News")
    link_tag = this_article.find_all("a")
    
    # Update headline list 
    headline = headline_tag[0].get_text()
    headlines_list.append(headline.encode('utf-8'))
    
    # Get the link
    link = link_tag[0]['href']
    article_link_list.append(link.encode('utf-8'))
    
    # Get the date stamp in the correct format
    date_full = date_tag[1].get_text()
    date_full = date_full.encode('utf-8')  #encode into utf-8 string
    date_short = re.findall(' .*$', date_full)
    timestamp.append(parser.parse(date_short[0]))
    
##### Of the results we got, how many are recent enough?
is_recent = [datetime.today() - timedelta(days=days_ago) < x for x in timestamp]
link_indices = [i for i, x in enumerate(is_recent) if x]    
    
    
# Loop over the recent results
for i in range(0,len(link_indices)):
    page_result_link = article_link_list[link_indices[i]]
    page_result = requests.get(page_result_link)
    res_soup = BeautifulSoup(page_result.content, 'html.parser')
    story_tag = res_soup.find_all(class_="post-content text-block clearfix post-content--groupedn-txt ")
    story = ""
    for j in range(0,len(story_tag)):
        story_tmp = story_tag[j].get_text()
        story_tmp = story_tmp.encode('utf-8')
        story += story_tmp


    # append to lists!
    fetched_stories.append(story)
    fetched_headlines.append(headlines_list[link_indices[i]])
    
    
    
##################### Write to file ##########################


file_base = "Eonline_" + search_term.lower().replace(" ", "_") + "_" + time.strftime("%d_%m_%y")
f = open(file_base + "_headlines.txt","w")
for item in fetched_headlines:
  f.write("%s\n" % item)  
f.close()

f = open(file_base + "_articles.txt","w")
for item in fetched_stories:
  f.write("%s\n" % item)  
f.close()


