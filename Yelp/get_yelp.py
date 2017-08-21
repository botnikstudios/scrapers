from bs4 import BeautifulSoup
import urllib2
import os

"""
get_yelp() prompts the user to choose a city and a search term. The program uses Yelp's search function
and pulls up the page for the top non-sponsored result and collects the text from however many pages of reviews the
user asks for.
"""

# this variable maps city names (as they will be displayed to the user) to Yelp's city codes as they appear in urls
# used later on for constructing the urls to visit
cities = {'chicago': 'Chicago,+IL','new york': 'New+York,+NY','london': 'London,+United+Kingdom','seattle': 'Seattle,+WA', 'los angeles': 'Los+Angeles', 'san francisco': 'San+Francisco,+CA', 'richmond': 'Richmond,+VA'}

# main user loop
def get_yelp():

	# get the city part to put in the search url
	city_list = list(cities.keys())
	for i in range(len(city_list)):
		print "%s %s" % (i + 1,city_list[i])

	choice = raw_input('Choose a city by number:\n')
	city = city_list[int(choice) - 1]
	city_string = cities[city]

	search_term = raw_input('Enter search term:\n')
	search_term_string = search_term.replace(' ', '+')

	num_businesses = raw_input('How many pages of businesses?\n')

	num_pages = raw_input('How many pages of reviews per business?\n')

	outfilename = '/Users/jbrew/Desktop/library/reviews/yelp/texts/%s/%s' % (city, search_term.replace(' ', '_'))
	outfile = open(outfilename, 'w')



	for start_result_num in range(0,int(num_businesses)):
		start_string = int(start_result_num * 15)
		url = 'https://www.yelp.com/search?find_desc=%s&find_loc=%s&start=%s' % (search_term_string, city_string, start_string)
		print '\n' + url
		scrape_search_url(url, start_result_num, search_term, num_pages, outfile)



def scrape_search_url(search_url, start_result_num, search_term, num_pages, outfile):

	page = urllib2.urlopen(search_url).read()
	soup = BeautifulSoup(page, "html.parser")
	businesses = soup.findAll(class_='indexed-biz-name')

	links = []

	for b in businesses:
		for n in range(1,16):
			result_num = 15*start_result_num + n
			num_string = str(result_num) + '.'
		
			if b.get_text().encode('utf8').split()[0] == num_string:
				links.append(b.contents[1]['href'])

	for link in links:

		url_list = []
		for n in range(0, int(num_pages) * 20, 20):
			url = "https://www.yelp.com%s?start=%s" % (link, n)
			url_list.append(url)

		for url in url_list:
			print url
			page = urllib2.urlopen(url).read()
			soup = BeautifulSoup(page, "html.parser")

			foo = soup.findAll(itemprop="review")
			for review in foo:
				rating = review.findAll(itemprop="ratingValue")[0]['content']
				#print rating
				reviewtext = review.findAll(itemprop="description")[0].get_text().encode('utf8')
				#print reviewtext
				try:
					header = '#####\nrating: %s\n' % rating
					outfile.write(header + reviewtext)
				except:
					pass

					#outfile.write(x.get_text().encode('utf8')+ '\n\n')






get_yelp()





