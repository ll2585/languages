'''
This method loads a txt of hanja, and saves a json with the relevant info from https://ko.wiktionary.org/wiki/[hanja]
'''
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import json

def load_hanja(hanja):
	hanja_in_unicode = urllib.parse.quote(hanja)
	url = 'https://ko.wiktionary.org/wiki/{0}'.format(hanja_in_unicode)
	page=urlopen(url)

	soup = BeautifulSoup(page.read())
	meaning = soup.find(title='훈').find_next("td").text
	sound = soup.find(title='분류:한자 음').find_next("td").text
	return {'字': hanja, '訓': meaning, '音': sound}

def save_hanja_to_json(hanja_file, output_name):
	data = []
	count = 1
	with open(hanja_file, 'r', encoding="utf-8") as f:
		hanjas = f.read().splitlines()
	for hanja in hanjas:
		this_hanja = load_hanja(hanja)
		this_hanja['id'] = count
		count += 1
		data.append(this_hanja)
	with open(output_name, 'w') as outfile:
		json.dump(data, outfile)

save_hanja_to_json('hanja_8.txt', 'hanja_8.json')