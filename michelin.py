import requests, csv

from bs4 import BeautifulSoup


BASE_URL = 'http://gm.gnavi.co.jp/restaurant/list/tokyo/all_area/all_small_area/all_food/all_star/p{}'
BASE_REST_URL = 'http://gm.gnavi.co.jp{}'

FIELD = ['address', 'hours', 'holiday', 'price', 'url', 'tel']

def _get_index(page=1):
	res = requests.get(BASE_URL.format(page))
	soup = BeautifulSoup(res.text)
	restaurants = soup.find_all('ul', {'id':'restaurantList'})[0]
	return [rest.get('href') for rest in restaurants.findAll('a', href=True)]
		

def _get_rest_info(uri):
	BASE_REST_URL.format(uri)
	res = requests.get(BASE_REST_URL.format(uri))
	soup = BeautifulSoup(res.text)
	rest_info = soup.find_all('div', {'id':'rInfo'})[0]

	name_set = soup.find_all('div', {'id': 'restaurantName'})[0]
	rest_name = name_set.find_all('em', {'class': 'px26'})[0].text

	parsed_info = {}
	parsed_info['rating'] = soup.find_all('li', {'class': 'rating'})[0].text.strip()
	parsed_info['name'] = rest_name
	for field in FIELD:
		info_pane = rest_info.findAll('dl', {'class': field})
		if len(info_pane) > 0:
			parsed_info[field] = info_pane[0].text
		else:
			parsed_info[field] = 'n/a'
	return parsed_info

def scrape():
	with open('japan_mich_rest.csv', 'wb') as f:
		w = csv.writer(f)
		header_written = False
		for i in range(1, 52):
			for place in _get_index(page=i):
				rest_data = _get_rest_info(place)
				
				if not header_written:
					w.writerow(rest_data.keys())
					header_written = True
				vals = rest_data.values()
				w.writerow([v.encode('utf-8') for v in vals])
			print 'Done with page {}'.format(i)


if __name__ == '__main__':
	scrape()
