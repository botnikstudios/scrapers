# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 21:13:57 2017

@author: Elle
"""

import tabloid_scrapers

search_term = "bachelor engaged"
days_ago = 2
results_loc = './Results/bachelor_engaged'

try:
    tabloid_scrapers.RadarScraper(search_term, days_ago,results_loc)
except:
    print('An error scraping Radar occurred.')

try:
    tabloid_scrapers.PerezScraper(search_term, days_ago,results_loc)
except:
    print('An error scraping Perez Hilton occurred.')


try:
    tabloid_scrapers.CelebuzzScraper(search_term, days_ago,results_loc)
except:
    print('An error scraping Celebuzz occurred.')


try:
    tabloid_scrapers.PeopleScraper(search_term, days_ago,results_loc)
except:
    print('An error scraping People occurred.')


try:
    tabloid_scrapers.EScraper(search_term, days_ago,results_loc)
except:
    print('An error scraping E online occurred.')


try:
    tabloid_scrapers.OKScraper(search_term, days_ago,results_loc)
except:
    print('An error scraping OK Magazine occurred.')
    

try:
    tabloid_scrapers.TMZScraper(search_term, days_ago,results_loc)
except:
    print('An error scraping TMZ occurred.')
    
    

try:
    tabloid_scrapers.NatlEnquirerScraper(search_term, days_ago,results_loc)
except:
    print('An error scraping The National Enquirer occurred.')
    
