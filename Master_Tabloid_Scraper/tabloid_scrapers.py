# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 20:23:50 2017

This defines the functions to be used in a module so that *all* the tabloid scrapers
we're currently using can be called at once. 

@author: Elle
"""


#### Scrape E! Online #####

def EScraper(search_term, days_ago):
    from bs4 import BeautifulSoup
    import requests
    import string
    import re
    from selenium import webdriver
    from dateutil import parser
    from datetime import datetime, timedelta
    import time
    import os
    from sys import platform
  
    # Take out any punctuation marks from name and convert to lowercase
    search_term = search_term.translate(None, string.punctuation)
    search_term = search_term.lower()
    
    # 
    # Format search term for the URL formula
    search_term_formatted = search_term.replace(" ", "+")
    
    # Pull the HTML for the page using Selenium--->bs4 pipeline
    page_link = "http://eonline.com/search?query=" + search_term_formatted 
    
    if platform == "linux" or platform == "linux2":
        cwd = os.getcwd()
        browser = webdriver.Chrome(cwd + '/chromedriver')
    elif platform == "win32" or platform == "win64":
        browser = webdriver.Chrome()
    
    browser.get(page_link)
    html = browser.page_source
    browser.close()
    browser.quit()
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all(class_ = "result") 
    
    #### Initialize the vectors for storing results
    timestamp= []
    article_link_list = []
    headlines_list = []
    fetched_stories = []
    fetched_headlines=[]
    
    # Loop over every search result the query pulls
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



######## Define our scraper for Radar Online
def RadarScraper(search_term, days_ago):
    from bs4 import BeautifulSoup
    import requests
    import string
    from datetime import datetime, timedelta
    import re
    import time
    from dateutil import parser
    
    # Take out any punctuation marks from name and convert to lowercase
    search_term = search_term.translate(None, string.punctuation)
    search_term = search_term.lower()
    
    # Format search term for the URL formula
    search_term_formatted = search_term.replace(" ", "+")

    page_link = "http://radaronline.com/search/?search=" + search_term_formatted
    page = requests.get(page_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    timestamp = []
    article_link_list = []
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
            fetched_stories.append(story.encode('utf-8',errors='ignore'))
        
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




#################### Perez scraper ###########################################
def PerezScraper(search_term, days_ago):
    from bs4 import BeautifulSoup
    import requests
    import string
    from selenium import webdriver
    from dateutil import parser
    from datetime import datetime, timedelta
    import time
    import re
    from sys import platform
    import os
    
    # Take out any punctuation marks from name and convert to lowercase
    search_term = search_term.translate(None, string.punctuation)
    search_term = search_term.lower()

    # Format search term for the URL formula
    search_term_formatted = search_term.replace(" ", "+")

    page_link = "http://perezhilton.com/search/" + search_term_formatted 
    
    if platform == "linux" or platform == "linux2":
        cwd = os.getcwd()
        browser = webdriver.Chrome(cwd + '/chromedriver')
    elif platform == "win32" or platform == "win64":
        browser = webdriver.Chrome()

    browser.get(page_link)
    html = browser.page_source
    browser.close()
    browser.quit()
    
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all(class_ = "post") # This will get some junk, too. 

    #### Initialize the vectors for storing results
    timestamp= []
    article_link_list = []
    headlines_list = []
    fetched_stories = []
    fetched_headlines=[]
    
    for i in range(1, len(articles)):
        child = articles[i].find_all("a")
        
        # If it really is a search result- as in, child isn't empty-
        if child:
            headline = child[0].get_text()
            headlines_list.append(headline.encode('utf-8', errors = 'ignore'))
            link = child[0]['href']
            article_link_list.append(link.encode('utf-8', errors='ignore'))
            date = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', link)
            timestamp.append(parser.parse(date[0].encode('utf-8', errors = 'ignore')))

    ##### Of the results we got, how many are recent enough?
    is_recent = [datetime.today() - timedelta(days=days_ago) < x for x in timestamp]
    link_indices = [i for i, x in enumerate(is_recent) if x]
    
    # Loop over the recent results. May have to introduce pagination if the last date
    # presented is too recent, since Perez only shows six articles at a time.
    for i in range(0,len(link_indices)):
        page_result_link =  article_link_list[link_indices[i]]
        page_result = requests.get(page_result_link)
        res_soup = BeautifulSoup(page_result.content, 'html.parser')
        story_tag = res_soup.find_all(class_="entry ")
        story_tmp = story_tag[0].get_text()
        story = story_tmp.split("\nTags:")[0]
        fetched_stories.append(story.encode('utf-8'))
        fetched_headlines.append(headlines_list[link_indices[i]])

    ########### Write to file ################
    
    file_base = "Perez_" + search_term.lower().replace(" ", "_") + "_" + time.strftime("%d_%m_%y")
    f = open(file_base + "_headlines.txt","w")
    for item in fetched_headlines:
      f.write("%s\n" % item)  
    f.close()
    
    f = open(file_base + "_articles.txt","w")
    for item in fetched_stories:
      f.write("%s\n" % item)  
    f.close()
    
    
###################### Scrape People #########################################
def PeopleScraper(search_term, days_ago):
    from bs4 import BeautifulSoup
    import requests
    import string
    from datetime import datetime, timedelta
    import re
    import time

    # Take out any punctuation marks from name and convert to lowercase
    search_term = search_term.translate(None, string.punctuation)
    search_term = search_term.lower()
    
    # 
    # Format search term for the URL formula
    search_term_formatted = search_term.replace(" ", "+")
    
    # For TMZ, update the search formula
    #page_link = 'http://eonline.com/search?query=' + search_term_formatted 
    
    page_link = "http://people.com/?s=" + search_term_formatted
    page = requests.get(page_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    timestamp = []
    article_link = []
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
    file_base = "People_" + search_term.lower().replace(" ", "_") + "_" + time.strftime("%d_%m_%y")
    f = open(file_base + "_headlines.txt","w")
    for item in fetched_headlines:
      f.write("%s\n" % item)  
    f.close()
    
    f = open(file_base + "_articles.txt","w")
    for item in fetched_stories:
      f.write("%s\n" % item)  
    f.close()
    
################## Celebuzz scraper ############################################
def CelebuzzScraper(search_term, days_ago):
    
    from bs4 import BeautifulSoup
    import requests
    import string
    from datetime import datetime, timedelta
    import time
    from dateutil import parser
    
    # Take out any punctuation marks from name and convert to lowercase
    search_term = search_term.translate(None, string.punctuation)
    search_term = search_term.lower()
        # 
    # Format search term for the URL formula
    search_term_formatted = search_term.replace(" ", "+")    
    page_link = "http://www.celebuzz.com/?s=" + search_term_formatted
    page = requests.get(page_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    timestamp = []
    article_link_list = []
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

    