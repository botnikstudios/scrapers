# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 20:51:23 2018
Scrape Epicurious
@author: andro
"""

import requests
import re
from bs4 import BeautifulSoup
import csv
import os
import string





https://www.epicurious.com/search/chocolate%20chip%20cookies?content=recipe
search_term = "chocolate chip cookies"

# Take out any punctuation marks from name and convert to lowercase
translator = str.maketrans('', '', string.punctuation)

search_term = search_term.translate(translator)
search_term = search_term.lower()

# Format search term for the URL formula
search_term_formatted = search_term.replace(" ", "+")


# Get the page links to every recipe
save_link = []
for i in range(1,30):
	# Go to every page and get the list of links
	page_link = 'http://www.epicurious.com/search/' + search_term_formatted + "?content=recipe&page=" + str(i)
	page = requests.get(page_link)
	soup = BeautifulSoup(page.content, 'html.parser')
	all_links = soup.find_all('a')
	for link in all_links:
		if 'view-complete-item' in str(link):
			save_link.append(link["href"])
            
save_link = list(set(save_link))


# Loop over each recipe and grab all the data!
counter = 1
title_list = []

for link in save_link:
    page_name = "https://www.epicurious.com/" + link 
    page = requests.get(page_name)
    soup = BeautifulSoup(page.content,'html.parser')
    
    
    # Get the  recipe name
    title_tag = soup.find_all('title')
    title = title_tag[0].get_text()
    title_list.append(title)
    
    # Get the serving size
    yield_tag = soup.find_all(class_ = "yield")
    if yield_tag:
        servings = yield_tag[1].get_text()
    else:
        servings = ""
    
    # Get the ingredients list
    ingredients_list = []
    ing_tags = soup.find_all(class_ = "ingredient")
    for tags in ing_tags:
        ingredients_list.append(tags.get_text())
    
    # Get the recipe
    dir_list = []
    dir_tags = soup.find_all(class_ = "preparation-step")
    for tags in dir_tags:
        dir_list.append(tags.get_text().strip())
    
    # Get the rating
    rating_tag = soup.find_all(class_ = "rating")
    rating = rating_tag[0].get_text()
    
     # Now save this to its own file
    directory = './Results/' + search_term_formatted
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename_servings = './Results/' + search_term_formatted + '/servings_' + str(counter) + '.txt'
    filename_ingredients = './Results/' + search_term_formatted + '/ingredients_' + str(counter) + '.txt'
    filename_recipes = './Results/' + search_term_formatted + '/recipe_' + str(counter) + '.txt'
    filename_rating = './Results/' + search_term_formatted + '/rating_' + str(counter) + '.txt'
        
    # Write the ingredients list
    f = open(filename_ingredients,'wb')
    for item in ingredients_list:
        f.write(item.encode('utf-8') + b'\n')
    f.close()
        
    # Write the recipe instructions to their own file
    g = open(filename_recipes,'wb')
    for item in dir_list:
        g.write(item.encode('utf-8') + b'\n')
    g.close()
        
    # Write the serving size to its own file
    e = open(filename_servings,'wb')
    e.write(servings.encode('utf-8') + b'\n')
    e.close()
    
    # Write the ratings to its own file
    d = open(filename_rating,'wb')
    d.write(rating.encode('utf-8') + b'\n')
    d.close()

    # Increment the counter
    counter = counter +1
    time.sleep(1.25)

# Write the title list to its own file
h = open('recipe_directory.txt','wb')
for index in range(0,len(title_list)):
    h.write(str(index).encode('utf-8') + b',' + str(title_list[index]).encode('utf-8','ignore') + b'\n' )
h.close()
		