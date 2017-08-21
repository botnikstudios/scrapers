from bs4 import BeautifulSoup
import urllib2
import re
import string


def scrape_TED_category(category_name):
	path = 'transcripts/%s' % category_name
	outfile = open(path, 'w')
	url = 'https://www.ted.com/talks?topics%%5B%%5D=%s' % category_name
	page = demand_page(url)
	soup = BeautifulSoup(page, "html.parser")
	items = soup.findAll(class_ = 'h9 m5')

	for item in items:
		link = item.find('a')
		composite_url = 'https://www.ted.com%s/transcript?language=en' % link['href']
		try:
			page = demand_page(composite_url)
		except:
			page = None
		if page:
			soup = BeautifulSoup(page, "html.parser")
			paragraphs = soup.findAll(class_ = 'talk-transcript__para__text')
			for p in paragraphs:
				outfile.write(p.get_text().encode('utf8').replace('Laughter','').replace('Applause','') + " ")

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

topics = get_topics()



approved_categories = []

"""
for category in sorted(topics.keys()):
	print '\n' + category
	go = raw_input('Yes?\n')
	if go == 'y':
		approved_categories.append(category)

		
path = 'approvedlist'
with open(path, 'w') as f:
	f.write("\n".join(approved_categories))
"""

approved_categories = [line for line in open('approvedlist', 'r').readlines()]

for category in approved_categories[-15:]:
	scrape_TED_category(category.replace(' ','+'))
		
#scrape_TED_category('ai')