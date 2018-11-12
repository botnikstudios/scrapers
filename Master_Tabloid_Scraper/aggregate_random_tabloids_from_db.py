#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 15:47:53 2017

@author: eobrien
"""


import os
from collections import OrderedDict
import random
import string

#folders = ["Results_DB"]

num_articles = 10000
indices = random.sample(range(1,31000),num_articles)


mass_text = []


for ind in indices:
    path = os.getcwd() + '/ResultsDB'
    filename = path + '/article_' + str(ind) + '.txt'
    f = open(filename)
    text = f.read()
    if not "function" in text:
        mass_text.append(text)          

# Print mass text
#mass_text = [item.replace("Photos","") for item in mass_text]
#mass_text = [item.replace("Images","") for item in mass_text]
##mass_text = [item.replace("PHOTOS","") for item in mass_text]
#mass_text = [item.replace("radaronline.com","") for item in mass_text]
#mass_text = [item.replace("RadarOnline.com","") for item in mass_text]
#mass_text = [item.replace("Radar","") for item in mass_text]
#mass_text = [item.translate(None, string.punctuation) for item in mass_text]
#mass_text = [item.translate(None, string.digits) for item in mass_text]


# Remove any duplicates
mass_text = list(OrderedDict.fromkeys(mass_text))
#mass_text = ''.join(mass_text)
f = open('Random_Tabloid_Corpus.txt', 'wb')
for item in mass_text:
    f.write(item + '\n')
f.close()