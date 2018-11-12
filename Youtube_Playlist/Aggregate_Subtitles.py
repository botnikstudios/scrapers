#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:52:48 2017

@author: eobrien
"""
import glob
import os
from collections import OrderedDict

#folders = ["Barefoot","Duff","Emeril","Food_Goals","Giada","Martha","Recipe_of_the_Day","RR","Sweet_Eats","Sweet_Side"]
#eywords = ["potato","cranberry","turkey","Thanksgiving","thanksgiving","pumpkin","pie"]
#keywords = ["Thanksgiving","thanksgiving","pumpkin pie","cranberry","mashed potatoes"]
mass_text = []

folders = ["Arbys"]

for folder in folders:
    path  = os.getcwd() + '/' + folder
    files = glob.glob(path + '/*.txt')
    # iterate over the list getting each file 
    for fle in files:
       # open the file and then call .read() to get the text 
       with open(fle) as f:
          text = f.read()
          mass_text.append(text)
          
         # if any(term in text for term in keywords):
         

# Print mass text
mass_text = [item.replace("No Closed Caption","") for item in mass_text]

# Remove any duplicates
mass_text = list(OrderedDict.fromkeys(mass_text))
#mass_text = ''.join(mass_text)
f = open('Arbys_Corpus.txt', 'w')
for item in mass_text:
    f.write(item + '\n')
f.close()