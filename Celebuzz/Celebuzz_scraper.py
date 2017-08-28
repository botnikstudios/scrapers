# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 18:08:28 2017

@author: Elle
"""

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

search_term = "Katy Perry"
days_ago = 2
# Take out any punctuation marks from name and convert to lowercase
search_term = search_term.translate(None, string.punctuation)
search_term = search_term.lower()

# 
# Format search term for the URL formula
search_term_formatted = search_term.replace(" ", "+")

# For TMZ, update the search formula
#page_link = 'http://eonline.com/search?query=' + search_term_formatted 

page_link = "http://www.celebuzz.com/?s=" + search_term_formatted
#page_link = "https://cnn.com"
page = requests.get(page_link)
soup = BeautifulSoup(page.content, 'html.parser')

timestamp = []
article_link_list = []
stories = []
headlines = []
fetched_stories = []
fetched_headlines = []


articles = soup.find_all(class_="post")

# OK magazine doesn't give dates- it just lists in chronological order a lot of results.
# So, grab maybe 4, and we'll check if each one is within the date range. 

for i in range(0, len(articles)):
    this_article = articles[i]
    
    result_tag = this_article.find_all('a')
    if result_tag:
        
        # Update headline list 
        headline = result_tag[0].get_text()
        headlines.append(headline.encode('utf-8').strip())
        
        # Get the link
        link = result_tag[0]['href']
        link = link.encode('utf-8')
        article_link_list.append(link)
        
        # Get the date stamp in the correct format
        date_str= link[24:34]
        timestamp.append(parser.parse(date_str))

   

 # Which articles were posted within N days?    
is_recent = [datetime.today() - timedelta(days=days_ago) < x for x in timestamp]
link_indices = [i for i, x in enumerate(is_recent) if x]
    

# Loop over the recent results
for i in range(0,len(link_indices)):
    page_result_link = article_link_list[link_indices[i]]
    page_result = requests.get(page_result_link)
    res_soup = BeautifulSoup(page_result.content, 'html.parser')
    story_tag = res_soup.find_all(class_="article-content clearfix")
    story = story_tag[0].get_text()
    story = story.encode('utf-8')


    # append to lists!
    fetched_stories.append(story)
    fetched_headlines.append(headlines[link_indices[i]])
    



# Write results to a CSV.
file_base = "Celebuzz_" + search_term.lower().replace(" ", "_") + "_" + time.strftime("%d_%m_%y")
f = open(file_base + "_headlines.txt","w")
for item in fetched_headlines:
  f.write("%s\n" % item)  
f.close()

f = open(file_base + "_articles.txt","w")
for item in fetched_stories:
  f.write("%s\n" % item)  
f.close()
