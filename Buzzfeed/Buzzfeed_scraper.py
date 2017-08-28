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

search_term = "Taylor Swift"
days_ago = 1
# Take out any punctuation marks from name and convert to lowercase
search_term = search_term.translate(None, string.punctuation)
search_term = search_term.lower()

# 
# Format search term for the URL formula
search_term_formatted = search_term.replace(" ", "+")

# For TMZ, update the search formula
#page_link = 'http://eonline.com/search?query=' + search_term_formatted 

page_link = "https://www.buzzfeed.com/search?q=" + search_term_formatted
domain = "https://www.buzzfeed.com"

within_days = 8
#page_link = "https://cnn.com"
#page = requests.get(page_link)
#soup = BeautifulSoup(page.content, 'html.parser')

#cwd = os.getcwd()
#browser = webdriver.Chrome(cwd+'/chromedriver')
browser = webdriver.Chrome()
browser.get(page_link)
html = browser.page_source
browser.close()

soup = BeautifulSoup(html, 'html.parser')

articles = soup.find_all(class_="lede")

days_ago_list = []
article_link_list = []
stories = []
headlines_list = []
fetched_stories = []
fetched_headlines=[]


# For every article on the page, get the link and the time it was posted at.
for i in range(0,len(articles)):
    article_tags = articles[i]
    child = article_tags.find_all('h2')
    header = child[0].find_all('a')
    
    # URL
    if len(header) > 1:
        url = domain + header[1]['href']
        url = url.encode('UTF8')
        article_link_list.append(url)
        
        headline = header[1].get_text()
        headline = headline.strip()
        headline = headline.encode('UTF8')
        headlines_list.append(headline)
        
        date_tag = article_tags.find_all(class_="small-meta__item__time-ago")
        date = date_tag[0].get_text()
        date = date.encode('UTF8')
        # Convert buzzfeed date notation to days
        is_min = re.findall('minutes', date)
        is_hours = re.findall('hours', date)
        is_days = re.findall('days', date)
        is_weeks = re.findall('weeks', date)
        is_months = re.findall('months',date)
        is_years = re.findall('years',date)
        # Buzzfeed says "a day ago" instead of 1 day ago, so need to be careful.
        # Would be even better to get a true system timestamp somehow.
        # Not a big deal because buzzfeed sorts results by date, so if something is 
        # timely, we could always just get the top 5
        num = [int(s) for s in date.split() if s.isdigit()]
        if is_min or is_hours:
            days_ago = 0
        elif is_days:
            days_ago = num[0]
        elif is_weeks:
            days_ago = num[0] * 7
        elif is_months:
            days_ago = num[0] * 30
        elif is_years:
            days_ago = num[0] * 365
        days_ago_list.append(days_ago)
    else:
        article_link_list.append('NA')
        headlines_list.append('NA')
        days_ago_list.append('100000')
    
    
# Get the articles that are within the given time frame    
is_recent = [x < within_days for x in days_ago_list]
link_indices = [i for i, x in enumerate(is_recent) if x]

for i in range(0, len(link_indices)):
    page_result_link = article_link_list[link_indices[i]]
    page_result = requests.get(page_result_link)
    res_soup = BeautifulSoup(page_result.content, 'html.parser')   
  
    story_tag1 = res_soup.find_all(class_="subbuzz__description subbuzz__description--standard ")
    story_tag2 = res_soup.find_all(class_="subbuzz subbuzz-text xs-mb4 xs-relative ")
    photo_caption_tag = res_soup.find_all(class_="js-subbuzz__title-text")
    story_list2 = [pt.get_text() for pt in story_tag2]
    story_list1 = [pt.get_text() for pt in story_tag1]
    caption_list = [pt.get_text() for pt in photo_caption_tag]
    story1 = ' '.join(story_list1)
    story2 = ' '.join(story_list2)
    captions = ' '.join(caption_list)
    this_headline = headlines_list[link_indices[i]]
    
    whole_story= story1 + story2 + captions

    fetched_stories.append(whole_story.encode('utf-8',errors='ignore'))
    fetched_headlines.append(this_headline[link_indices[i]])

# Write results to a txt file
out_file = open("Buzzfeed_Scraper_Output.txt","w")
for j in range(0,len(fetched_stories)):
    out_file.write("%s\n" % fetched_headlines[j])
    out_file.write("%s\n" % fetched_stories[j])
out_file.close()
