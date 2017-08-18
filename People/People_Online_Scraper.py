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

search_term = "Chester Bennington"
days_ago = 30
# Take out any punctuation marks from name and convert to lowercase
search_term = search_term.translate(None, string.punctuation)
search_term = search_term.lower()

# 
# Format search term for the URL formula
search_term_formatted = search_term.replace(" ", "+")

# For TMZ, update the search formula
#page_link = 'http://eonline.com/search?query=' + search_term_formatted 

page_link = "http://people.com/?s=" + search_term_formatted
#page_link = "https://cnn.com"
page = requests.get(page_link)
soup = BeautifulSoup(page.content, 'html.parser')

timestamp = []
article_link = []
stories = []
headlines = []
fetched_stories = []
fetched_headlines = []

articles = soup.find_all('article')

# For every article on the page, get the link and the time it was posted at.
for i in range(0,len(articles)):
    this_article = articles[i]
    article_tags = this_article.contents[1]
    
    time_children = article_tags.find_all(class_="article-header__timestamp")
    if not time_children:
        timestamp.append(datetime.strptime('January 1 1900', "%B %d %Y"))
    else:
        timestamp_tmp = time_children[0].get_text()
        timestamp_stripped = re.findall(' on (.*?) at', timestamp_tmp)
        timestamp_stripped = timestamp_stripped[0]

        timestamp_stripped = timestamp_stripped.encode('utf-8', errors='ignore')
        timestamp_stripped = timestamp_stripped.translate(None, string.punctuation)
        timestamp.append(datetime.strptime(timestamp_stripped, "%B %d %Y"))
    
    article_link_children = article_tags.find_all('a')
    article_link_tmp = article_link_children[0]
    article_link.append(article_link_tmp['href'].encode('utf-8',errors='ignore'))
    
# NEXT PART: Figure out which dates are within a window    
# Which articles were posted within N days?    
is_recent = [datetime.today() - timedelta(days=days_ago) < x for x in timestamp]
link_indices = [i for i, x in enumerate(is_recent) if x]

for i in range(0,len(link_indices)):
    page_result_link = article_link[i]
    page_result = requests.get(page_result_link)
    res_soup = BeautifulSoup(page_result.content, 'html.parser')
    story_tag = res_soup.find_all(class_="article-body__inner")
    if story_tag: # Gracefully handle in case nothing comes up
        story = story_tag[0].get_text()
        fetched_stories.append(story.encode('utf-8',errors='ignore'))
    
        title_tag = res_soup.find_all(class_="article-header__title")
        title_tag = title_tag[0].get_text()
        fetched_headlines.append(title_tag.encode('utf-8', errors = 'ignore'))

# Write results to a CSV.
out_file = open("People_Scraper_Output.txt","w")
for j in range(0,len(stories)):
    out_file.write("%s\n" % fetched_headlines[j])
    out_file.write("%s\n" % fetched_stories[j])
out_file.close()
