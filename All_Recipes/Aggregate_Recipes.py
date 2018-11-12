#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:52:48 2017

@author: eobrien
"""
import glob
import os

folders = ["chocolate+chip+cookies"]


mass_text = []

for folder in folders:
    path  = os.getcwd() + './Results/' + folder
    files = glob.glob(path + '/*.txt')
    # iterate over the list getting each file 
    for fle in files:
       # open the file and then call .read() to get the text 
      
       with open(fle) as f:
          text = f.read()
          mass_text.append(text)
          

# Print mass text
#mass_text = [item.replace("No Closed Caption","") for item in mass_text]

#mass_text = ''.join(mass_text)
f = open('mashed_potatoes.txt', 'wb')
for item in mass_text:
    f.write(item + '\n')
f.close()