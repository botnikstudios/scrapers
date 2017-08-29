#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 16:34:34 2017

This is a brute force approach to building up a big-ass database of tabloids. 

@author: eobrien
"""

# -*- coding: utf-8 -*-


import TabDBmod
import csv


with open('Search_names.csv', 'rb') as f:
     reader = csv.reader(f)
     search_list = list(reader)
     
     
for i in range(6, len(search_list)):
    use_term = search_list[i]
    search_term = use_term[0]
    days_ago = 10000

    try:
        TabDBmod.RadarScraperDB(search_term, days_ago)
    except:
        print('An error scraping Radar occurred.')
    
    try:
        TabDBmod.PerezScraperDB(search_term, days_ago)
    except:
        print('An error scraping Perez Hilton occurred.')
    
    
    try:
        TabDBmod.CelebuzzScraperDB(search_term, days_ago)
    except:
        print('An error scraping Celebuzz occurred.')
    
    
    try:
        TabDBmod.PeopleScraperDB(search_term, days_ago)
    except:
        print('An error scraping People occurred.')
    
    
    try:
        TabDBmod.EScraperDB(search_term, days_ago)
    except:
        print('An error scraping E online occurred.')
    
    
    try:
       TabDBmod.OKScraperDB(search_term, days_ago)
    except:
        print('An error scraping OK Magazine occurred.')
        
    
    try:
        TabDBmod.TMZScraperDB(search_term, days_ago)
    except:
        print('An error scraping TMZ occurred.')
        
        
    
    try:
        TabDBmod.NatlEnquirerScraperDB(search_term, days_ago)
    except:
        print('An error scraping The National Enquirer occurred.')
        
