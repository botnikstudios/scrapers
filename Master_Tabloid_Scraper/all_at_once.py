# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 21:13:57 2017

@author: Elle
"""

import tabloid_scrapers

search_term = "Ryan Reynolds"
days_ago = 15

tabloid_scrapers.RadarScraper(search_term, days_ago)
tabloid_scrapers.PerezScraper(search_term, days_ago)
tabloid_scrapers.CelebuzzScraper(search_term, days_ago)
tabloid_scrapers.PeopleScraper(search_term, days_ago)
tabloid_scrapers.EScraper(search_term, days_ago)