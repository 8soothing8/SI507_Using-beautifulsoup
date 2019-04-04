
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
import csv


# -*- coding: utf-8 -*-

import requests, json
from bs4 import BeautifulSoup
from advanced_expiry_caching import Cache

START_URL = "https://www.nps.gov"
FILENAME = "nps_cache.json"

# So I can use 1 (one) instance of the Cache tool -- just one for my whole program, even though I'll get data from multiple places
PROGRAM_CACHE = Cache(FILENAME)

def access_page_data(url):
    data = PROGRAM_CACHE.get(url)
    if not data:
        data = requests.get(url).text
        PROGRAM_CACHE.set(url, data) # default here with the Cache.set tool is that it will expire in 7 days, which is probs fine, but something to explore
    return data

#######

main_page = access_page_data(START_URL)

main_soup = BeautifulSoup(main_page, features="html.parser")
list_of_topics = main_soup.find('ul',{'class':"dropdown-menu SearchBar-keywordSearch"})

all_links = list_of_topics.find_all('a')

topics_pages = [] # gotta get all the data in BeautifulSoup objects to work with...
for link in all_links:
#    print(link)
    page_data = access_page_data(START_URL+link['href'])
#    print(page_data)
    soup_of_page = BeautifulSoup(page_data, features="html.parser")
#    print(soup_of_page)
    topics_pages.append(soup_of_page)
#
# print(topics_pages[1].prettify())


def csv_header_lst():
	return ["","Text","Number of hashtags","Number of favorites","Most common letter"]

header = ["Name", "Type", "Description", "Location"]

with open('national_parks.csv', 'w', newline ='') as csv_file:
    park_csv = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    park_csv.writerow(header)

    with open('nps_cache.json', 'r', encoding = 'utf8') as nps_data:
        read_data = nps_data.read()
    data = json.loads(read_data)


    for elem in data:
        state_soup = BeautifulSoup(data[elem]["values"], features="html.parser").find_all('div',{'id':'parkListResults'})

        for park in state_soup:
            park_names = park.find("h3").get_text()
            park_types = park.find("h2").get_text()
            park_states = park.find("h4").get_text()
            park_descriptions = park.find("p").get_text().strip('\n')

            # print(park_descriptions)

            row = [park_names, park_types, park_descriptions, park_states]

            for i in range(len(row)):
                if row[i] == '':
                    row[i] ='NA'
                    
            park_csv.writerow(row)
