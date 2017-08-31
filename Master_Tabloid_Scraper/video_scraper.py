#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 12:15:50 2017

@author: eobrien
"""

import time
from bs4 import BeautifulSoup
from urllib2 import urlopen
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import sys
import os

# Clicks on "Load More" button to display all users videos. 
def display_all_videos(driver):
    while(True):
        try:
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "yt-uix-load-more")))
            element.click()
        except:
            break

# Creates a list of tuples (video_title, video_link) of all 
# videos displayed on page 
def video_list(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    videos = soup.find_all("ytd-playlist-panel-video-renderer")
    video_links = []
    for vid in range(0, len(videos)):
        a = videos[vid]
        b = a.find_all('a')
        video_links.append(b[0]["href"])
    return video_links

# Clicks on CC(Closed Caption) button in YouTube video
def enable_subtitles(driver):
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ytp-subtitles-button")))
    elem.click()

def subtitles_link(driver):
    time.sleep(1)
    timings = driver.execute_script("return window.performance.getEntries();")

    # Find string in timings that contains the substring 'srv3'
    # which is the subtitles link.
    link = ""
    for t in timings:
         for v in t.values():
             if "srv3" in str(v):
                 link = v
    return link

def create_file(filename, link,subtitles):
    # remove illegal chars for file name
    title = "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()

    try:
        file = open(title + '.txt', 'w')    
        file.write('LINK: ' + link + '\n')
        file.write(subtitles)
        file.close()
    except:
        print("Can't create file for: " + title + " : " + link)

def scrape_subtitles(subtitle_link):
    r = urlopen(subtitle_link).read()
    soup = BeautifulSoup(r)

    # Remove tags (<*>), \n, and unecessary whitespace 
    s = re.sub(r'<.+?>', '', soup.prettify())   
    s = re.sub(r'\n', '', s)                    
    s = re.sub( '\s+', ' ', s ).strip()         
    return s

def main(argv):
    cwd = os.getcwd()
    driver = webdriver.Chrome(cwd + '/chromedriver')

    # Visit page and load all videos to create a list of
    # tuples(video_name,video_link) of the videos 
    driver.get(argv)
    #enable_subtitles(driver)
    #link = subtitles_link(driver)
    #subtitles = scrape_subtitles(link)
    
    
    display_all_videos(driver)
    video_links = video_list(driver)

    # Visit video's page and enable 'CC' to scrape the subtitles and 
    # save subtitles to '.txt' file. 
    for v in video_links:

        print(str(v))
        driver.get("https://youtube.com" + v)
        try:
            enable_subtitles(driver)
            link = subtitles_link(driver)
            subtitles = scrape_subtitles(link)
        except:
            subtitles = "No Closed Caption"
        create_file(v[0],v[1],subtitles)

if __name__ == "__main__":
    main(sys.argv)