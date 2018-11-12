# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import string
import os
import time
import re



search_term = "chocolate chip cookies"

# Take out any punctuation marks from name and convert to lowercase
translator = str.maketrans('', '', string.punctuation)

search_term = search_term.translate(translator)
search_term = search_term.lower()

# Format search term for the URL formula
search_term_formatted = search_term.replace(" ", "+")


save_link = []

for i in range(1,15):
	# Go to every page and get the list of links
	page_link = 'http://allrecipes.com/search/results/?wt=' + search_term_formatted + '&page=' + str(i)
	page = requests.get(page_link)
	soup = BeautifulSoup(page.content, 'html.parser')
	all_links = soup.find_all('a')
	for link in all_links:
		if link.find_all(class_="grid-col__rec-image"):
			save_link.append(link["href"])
            
save_link = [ x for x in save_link if "http://allrecipes.com" in x ]


# Now go to each collected recipe
counter = 1
title_list = []
for link in save_link:
    #page_link = 'http://allrecipes.com' + link
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    
    ingredients_list = []
    directions = []
    
	# Get title
    title_tag = soup.find_all('title')
    title = title_tag[0].get_text()
    title_list.append(title)
    
    # Get the number of servings
    serv_tag = soup.find_all(class_="subtext")
    if serv_tag:
        serv_text = serv_tag[0].get_text()
    else: 
        serv_text = ''
    # Get the ratings
    rating_tag = soup.find_all(class_="rating-stars")
    rating = re.findall('ratingstars="([^"]*)"', str(rating_tag[0]))
    
	# Get ingredients
    ing_tags = soup.find_all(class_="checkList__line")
    for tags in ing_tags:
        itemtags = tags.find_all(itemprop = 'ingredients')
        if itemtags:
            ingredients_list.append(itemtags[0].get_text().strip())
        
	# Get directions
    print(len(ingredients_list))
    dir_tags = soup.find_all(class_="recipe-directions__list--item")
    for tags in dir_tags:
         dir_text = tags.get_text()
         directions.append(dir_text)

    # Now save this to its own file
    directory = './Results/' + search_term_formatted
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename_servings = './Results/' + search_term_formatted + '/servings_' + str(counter) + '.txt'
    filename_ingredients = './Results/' + search_term_formatted + '/ingredients_' + str(counter) + '.txt'
    filename_rating= './Results/' + search_term_formatted + '/rating_' + str(counter) + '.txt'

    filename_recipes = './Results/' + search_term_formatted + '/recipe_' + str(counter) + '.txt'
    f = open(filename_ingredients,'wb')
    for item in ingredients_list:
        f.write(item.encode('utf-8') + b'\n')
            
    f.close()
    
    # Write the recipe instructions to their own file
    g = open(filename_recipes,'wb')
    for item in directions:
       g.write(item.encode('utf-8') + b'\n')
    g.close()
    
    # Write the serving size to its own file
    e = open(filename_servings,'wb')
    e.write(serv_text.encode('utf-8') + b'\n')
    
    # Write the rating to its own file
    d= open(filename_rating,'wb')
    d.write(rating[0].encode('utf-8') + b'/5\n')

    
    # Increment the counter
    counter = counter +1
    time.sleep(1.25)

# Write the title list to its own file
h = open('./Results/' + search_term_formatted + '/recipe_directory2.txt','wb')
for index in range(0,len(title_list)):
    h.write(str(index) + ',' + title_list[index].encode('utf-8') + b'\n')
h.close()
		
	
