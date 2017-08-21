from bs4 import BeautifulSoup
import urllib2
import re
import os
import string


def scrape_category(home_url, num_pages):

	wishtype = home_url.split('/')[-1].split('-')[-1]
	path = "wish_" + wishtype
	print path
	outfile = open(path, 'w')

	for i in range(1, num_pages+1):
		url = 'http://wish.org/wishes/wish-stories/i-wish-to-give?page=%s#sm.0001wp95zguk7f62po51id9xxuod4' % home_url

		page = demand_page(url)
		soup = BeautifulSoup(page, "html.parser")
		fragment = '/i-wish-to-%s/' % wishtype
		items = soup.findAll(href=re.compile(fragment))
		print len(items), "items"

		

		for i in range(1,len(items)):
			url = items[i]['href']
			if True:	
				page = demand_page(url)

				if page:
					soup = BeautifulSoup(page, "html.parser")
					body = soup.findAll(class_='rich-text')
					for x in [body[0]]:
						text = " " + x.get_text().encode('utf8')
						print text[-100:]
						outfile.write(text)


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

