# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 16:59:23 2018

@author: andro
"""

from bs4 import BeautifulSoup
import requests
import string
import os
import time
import re



search_term = "fitness"

# Take out any punctuation marks from name and convert to lowercase
translator = str.maketrans('', '', string.punctuation)

search_term = search_term.translate(translator)
search_term = search_term.lower()

# Format search term for the URL formula
search_term_formatted = search_term.replace(" ", "+")


save_link = []


page_link = 'https://www.womenshealthmag.com/search/?q=' + search_term_formatted
page = requests.get(page_link)
soup = BeautifulSoup(page.content, 'html.parser')
all_links = soup.find_all('a')

for i in range(1,15):
	# Go to every page and get the list of links
	page_link = 'http://allrecipes.com/search/results/?wt=' + search_term_formatted + '&page=' + str(i)
	page = requests.get(page_link)
	soup = BeautifulSoup(page.content, 'html.parser')
	all_links = soup.find_all('a')
	for link in all_links:
		if link.find_all(class_="simple-item-image item-image"):
			save_link.append(link["href"])
            
save_link = [ x for x in save_link if "http://allrecipes.com" in x ]