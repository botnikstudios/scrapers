# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 16:59:23 2018

@author: andro
"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import unicodedata

# You need to have a copy of chromedriver on your local machine. If you are using windows,
# it should be an .exe if you are on Windows, I think no executable extension if you are Mac/Linux
# The path to the driver goes here.
driver = webdriver.Chrome(executable_path='.\chromedriver.exe')
driver.implicitly_wait(30) # Good scraping practice

# Put in the link for the infinite scroll page where you will be scraping from
base_url = "https://www.womenshealthmag.com/workouts/" 
verificationErrors = []
accept_next_alert = True

driver.get(base_url)
# Set the upper limit on how many pages you will scroll through
max_scroll = 15
for i in range(1,max_scroll):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4) # Sleep 4 seconds between scrolls so you don't get booted
html_source = driver.page_source # Grab the HTML on the page currently
data = html_source.encode('utf-8') 
        

####### Now that you've collected the HTML from the infinite scroll page, you can 
# collect links from it and scrape from those links. In this example, I am scraping fitness
# articles from womens health magazine. The links to these articles are displayed as 
# cards on an infinite scroll page. Now, I want to collect all the links, go to
# the articles, and scrape the body of the text.
soup = BeautifulSoup(data, 'html.parser')

# This is the tag that accompanies fitness article links. You will likely need to change it
# if you are scraping a different site.
all_links = soup.find_all(class_="full-item-title item-title")
all_articles = []

for link in all_links:
    goto = link['href']
    page_result = requests.get('https://www.womenshealthmag.com' + goto)
    res_soup = BeautifulSoup(page_result.content.decode('utf-8','ignore'), 'html.parser')

    # Get the body of the text
    all_text = res_soup.find_all(class_='body-text')
    txt = ""
    for block in all_text:
        tmp_txt = block.get_text()
        new_str = unicodedata.normalize("NFKD", tmp_txt)
        txt = txt + new_str
    all_articles.append(txt)

# Save all the articles you collected in a .txt file 
f = open("womenshealth_fitness_articles.txt","w")
for item in all_articles:
  f.write(str(item.encode('latin1', errors='ignore')))  
f.close()