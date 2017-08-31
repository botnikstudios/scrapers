#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 10:06:22 2017

@author: eobrien
"""

import os
import re

os.chdir("/home/eobrien/botnik/Tabloid_Scrapers/Master_Tabloid_Scraper/ResultsDB")
headlines = []

for filename in os.listdir(os.getcwd()):
    with open(filename, 'r') as f:
        first_line = f.readline()
    first_line_title = re.findall('^(.*?)/n', first_line)
    if len(str(first_line_title)) < 175:
        headlines.append(first_line_title)
    
# Write to file
os.chdir("/home/eobrien/botnik/Tabloid_Scrapers/Master_Tabloid_Scraper")
thefile = open("headlines.txt", "w")
for item in headlines:
    thefile.write("%s\n" % item)

thefile.close()