from bs4 import BeautifulSoup
import urllib2
import re

url = "http://www.cnn.com/TRANSCRIPTS/sm.html"
base = "http://transcripts.cnn.com/"

page = urllib2.urlopen(url).read()
	
soup = BeautifulSoup(page, "html.parser")

links = soup.findAll(href=re.compile('TRANSCRIPTS'))


# list stores first few letters of the subhead tag to keep track of which episodes are done already
speakers = {}



outfilename = "CNN/SM.txt"
outfile = open(outfilename, 'w')

for link in links[3:]:
	print link['href']
	url = base + link['href']
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page, "html.parser")

	bodytext = soup.findAll(class_="cnnBodyText")
	body = bodytext[2].get_text()

	outfile.write(body + " ")
