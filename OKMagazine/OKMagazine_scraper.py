# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 17:02:49 2017

@author: Elle
"""

# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests
import string
from datetime import datetime, timedelta
import time
from dateutil import parser

search_term = "Taylor Swift"
days_ago = 10
# Take out any punctuation marks from name and convert to lowercase
search_term = search_term.translate(None, string.punctuation)
search_term = search_term.lower()

# 
# Format search term for the URL formula
search_term_formatted = search_term.replace(" ", "+")

# For TMZ, update the search formula
#page_link = 'http://eonline.com/search?query=' + search_term_formatted 

page_link = "http://okmagazine.com/search/?search=" + search_term_formatted
#page_link = "https://cnn.com"
page = requests.get(page_link)
soup = BeautifulSoup(page.content, 'html.parser')

timestamp = []
article_link_list = []
stories = []
headlines = []
fetched_stories = []
fetched_headlines = []


articles = soup.find_all("article")

# OK magazine doesn't give dates- it just lists in chronological order a lot of results.
# So, grab maybe 4, and we'll check if each one is within the date range. 

for i in range(0, min(len(articles),4)):
    this_article = articles[i]
    
    headline_tag = this_article.find_all(class_="promo-title")
    link_tag = this_article.find_all("a")
    
    # Update headline list 
    headline = headline_tag[0].get_text()
    headlines.append(headline.encode('utf-8'))
    
    # Get the link
    link = link_tag[0]['href']
    article_link_list.append(link.encode('utf-8'))
 

   
# NEXT PART: Figure out which dates are within a window    


for i in range(0,len(headlines)):
    page_result_link = article_link_list[i]
    page_result = requests.get(page_result_link)
    res_soup = BeautifulSoup(page_result.content, 'html.parser')
    story_tag = res_soup.find_all(class_="gallery-item-caption")
    story = ""
    for j in range(0,len(story_tag)):
        story_tmp = story_tag[j].get_text()
        story_tmp = story_tmp.encode('utf-8')
        story += story_tmp

    # Also get the date it occurred on
    date_tag = res_soup.find_all(class_="posted-date")
    date_str = date_tag[0].get_text()
    date_str = date_str.encode('utf-8').strip()
    
    # Append to master lists
    fetched_stories.append(story)
    fetched_headlines.append(headlines[i])
    timestamp.append(parser.parse(date_str[0:15]))
    
    
  # Which articles were posted within N days?    
is_recent = [datetime.today() - timedelta(days=days_ago) < x for x in timestamp]
link_indices = [i for i, x in enumerate(is_recent) if x]
    

# Write results to a CSV.
file_base = "OKMagazine_" + search_term.lower().replace(" ", "_") + "_" + time.strftime("%d_%m_%y")
f = open(file_base + "_headlines.txt","w")
for item in link_indices:
  f.write("%s\n" % fetched_headlines[item])  
f.close()

f = open(file_base + "_articles.txt","w")
for item in link_indices:
  f.write("%s\n" % fetched_stories[item])  
f.close()
