from bs4 import BeautifulSoup
import urllib2
import re
import os
import string


def scrape_category(category_name='history'):

	url = 'http://www.pbs.org/wgbh/nova/transcripts/int_hist.html'

	page = demand_page(url)
	soup = BeautifulSoup(page, "html.parser")
	items = soup.findAll(href=True)



	for i in range(21,86):
#	for i in range(21,22):
		
		link = items[i]['href']
		print link
		path = 'PBS/%s/%s' % (category_name, link.split('/')[-1].split('.')[0])
		outfile = open(path, 'w')

		composite_url = 'http://www.pbs.org/%s' % link
		try:
			page = demand_page(composite_url)
		except:
			page = None
		if page:
			soup = BeautifulSoup(page, "html.parser")
			paragraphs = soup.findAll('p')
			for p in paragraphs:
				outfile.write("###LINE###" + p.get_text().encode('utf8'))

"""
def get_topics():
	url = 'https://www.ted.com/topics'
	page = demand_page(url)
	soup = BeautifulSoup(page, "html.parser")
	items = soup.findAll(class_ = "sa d:b f-w:700")
	topics = {}
	for item in items:
		link = item['href']
		title = link.split('/')[-1].replace('+',' ')
		topics[title] = link
	return topics
"""

def demand_page(url):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
				   'Accept-Encoding': 'none',
				   'Accept-Language': 'pl-PL,pl;q=0.8',
				   'Connection': 'keep-alive'}

	req = urllib2.Request(url, headers=hdr)

	try:
		page = urllib2.urlopen(req)
		return page
	except urllib2.HTTPError, e:
		print e.fp.read()


scrape_category()
		
#scrape_TED_category('ai')