import requests, csv

from bs4 import BeautifulSoup

BASE_REST_URL = 'http://gm.gnavi.co.jp{}'

# List of cities you can choose from
TOKYO_URL = 'http://gm.gnavi.co.jp/restaurant/list/tokyo/all_area/all_small_area/all_food/all_star/p{}'
OSAKA_URL = 'http://gm.gnavi.co.jp/restaurant/list/osaka/all_area/all_small_area/all_food/all_star/p{}'
KYOTO_URL = 'http://gm.gnavi.co.jp/restaurant/list/kyoto/all_area/all_small_area/all_food/all_star/p{}'

# Select one city from the list above
BASE_URL = OSAKA_URL

# Manually select the number of pages to parse
# eg. '1-10 of 206' => 206/10 => round up to 21
NUM_PAGES = 21

# Choose a file name to write to. Remember to include '.csv' at the end.
FILE_NAME = 'japan_mich_rest_OSAKA.csv'

FIELD = ['address', 'hours', 'holiday', 'price', 'url', 'tel']

def _get_index(page=1):
	res = requests.get(BASE_URL.format(page))
	soup = BeautifulSoup(res.text, 'html.parser')
	restaurants = soup.find_all('ul', {'id':'restaurantList'})[0]
	return [rest.get('href') for rest in restaurants.findAll('a', href=True)]

def _get_rest_info(uri):
	BASE_REST_URL.format(uri)
	res = requests.get(BASE_REST_URL.format(uri))
	soup = BeautifulSoup(res.text, 'html.parser')
	rest_info = soup.find_all('div', {'id':'rInfo'})[0]

	name_set = soup.find_all('div', {'id': 'restaurantName'})[0]
	rest_name = name_set.find_all('em', {'class': 'px26'})[0].text

	parsed_info = {}
	parsed_info['rating'] = soup.find_all('li', {'class': 'rating'})[0].text.strip()
	parsed_info['name'] = rest_name
	for field in FIELD:
		info_pane = rest_info.findAll('dl', {'class': field})
		if len(info_pane) > 0:
			# Structure changed, now the dl has dt and dd. We want the dd only.
			parsed_info[field] = info_pane[0].find('dd').get_text()
		else:
			parsed_info[field] = 'n/a'
	return parsed_info

def scrape():
	with open(FILE_NAME, 'w') as f:
		w = csv.writer(f)
		header_written = False

		for page in range(1, NUM_PAGES+1):
			for place in _get_index(page=page):
				rest_data = _get_rest_info(place)
				
				if not header_written:
					w.writerow(rest_data.keys())
					header_written = True

				vals = rest_data.values()
				w.writerow(vals)

			print("Done with page {}".format(page))


if __name__ == '__main__':
	scrape()
