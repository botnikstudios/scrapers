from bs4 import BeautifulSoup
import urllib2
import re
import random


artist_name = raw_input('Enter artist name:\n')
artist_url_fragment = '-'.join(artist_name.split(' '))

url = "http://www.metrolyrics.com/%s-lyrics.html" % artist_url_fragment

page = urllib2.urlopen(url).read()
	
soup = BeautifulSoup(page, "html.parser")


suffix = 'lyrics-' + artist_url_fragment
print suffix

# finds all elements with the 'a' tag (i.e. all the links)
foo = soup.findAll(href=re.compile(suffix))

print len(foo)


outfilename = "/Users/jbrew/Desktop/library/lyrics/%s.txt" % '-'.join(artist_name.split())
outfile = open(outfilename, 'w')

for link in foo:
	print link['href']
	url = link['href']
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page, "html.parser")
	subfoo = soup.findAll(class_ = 'verse')
	for x in subfoo:
		outfile.write(x.get_text().encode('utf8') + " ")
