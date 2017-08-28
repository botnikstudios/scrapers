#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:01:01 2017

@author: eobrien
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


search_term = "Taylor Swift"
days_ago = 4
# Take out any punctuation marks from name and convert to lowercase
search_term = search_term.translate(None, string.punctuation)
search_term = search_term.lower()

# 
# Format search term for the URL formula
search_term_formatted = search_term.replace(" ", "+")

# For TMZ, update the search formula
#page_link = 'http://eonline.com/search?query=' + search_term_formatted 

#page_link = "http://people.com/?s=" + search_term_formatted
page_link = "http://www.nationalenquirer.com/search/?search=" + search_term
#page_link = "https://cnn.com"
page = requests.get(page_link)
soup = BeautifulSoup(page.content, 'html.parser')


articles = soup.find_all(class_="post-detail")
timestamp = []
article_link = []
fetched_stories = []
fetched_headlines = []
fetched_subheads = []



# For every article on the page, get the link and the time it was posted at.
for i in range(0,len(articles)):
    article_tags = articles[i]

    
    time_children = article_tags.find_all(class_="posted-date")
    if not time_children:
        timestamp.append(datetime.strptime('January 1 1900', "%B %d %Y"))
    else:
        timestamp_tmp = time_children[0].get_text()
        timestamp_stripped = re.findall('Posted (.*?) @', timestamp_tmp)
        timestamp_stripped = timestamp_stripped[0]

        timestamp_stripped = timestamp_stripped.encode('utf-8', errors='ignore')
        timestamp_stripped = timestamp_stripped.translate(None, string.punctuation)
        timestamp.append(datetime.strptime(timestamp_stripped, "%b %d %Y"))
    
    article_link_children = article_tags.find_all('a')
    article_link_tmp = article_link_children[0]
    article_link.append(article_link_tmp['href'].encode('utf-8',errors='ignore'))

# Which results are recent?
is_recent = [datetime.today() - timedelta(days=days_ago) < x for x in timestamp]
link_indices = [i for i, x in enumerate(is_recent) if x]

# Loop over the recent results- DUMB. The national enquirer actually only has 
# headlines, no articles. All the articles are in the form of galleries. Sigh.
for i in range(0,len(link_indices)):
    page_result_link = article_link[i]
    page_result = requests.get(page_result_link)
    res_soup = BeautifulSoup(page_result.content, 'html.parser')
    story_tag = res_soup.find_all(type="application/ld+json")
    if len(story_tag) > 1:
        story_tmp = story_tag[1].get_text()
        story = re.findall('caption":"(.*?)","url"', story_tmp)
        story = ' '.join(story)
        story = story.decode('unicode_escape')
        fetched_stories.append(story.encode('utf-8',errors='ignore'))
        title_tag = res_soup.find_all("title")
        title = title_tag[0].get_text()
        subtitle_tag = res_soup.find_all(class_="entry-subtitle")
        subtitle = subtitle_tag[0].get_text()
        fetched_headlines.append(title.encode('utf-8', errors = 'ignore'))
        fetched_subheads.append(subtitle.encode('utf-8', errors = 'ignore'))
    
    
# Write results to a txt file
out_file = open("Natl_Enquirer_Scraper_Output.txt","w")
for j in range(0,len(fetched_stories)):
    out_file.write("%s\n" % fetched_headlines[j])
    out_file.write("%s\n" % fetched_subheads[j])
    out_file.write("%s\n" % fetched_stories[j])
out_file.close()
