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
		print("loading {0}".format(hanja))
		try:
			this_hanja = load_hanja(hanja)
			this_hanja['id'] = count
			count += 1
			data.append(this_hanja)
		except (AttributeError, urllib.error.HTTPError):
			this_hanja = {'字': hanja, '訓': 'ERROR', '音': 'ERROR'}
			this_hanja['id'] = count
			count += 1
			data.append(this_hanja)
	with open(output_name, 'w') as outfile:
		json.dump(data, outfile)

'''
hanja_list = [
              'hanja_3-2',
              'hanja_2-1',
              'hanja_2-2',
              'hanja_1',
              ]
for h in hanja_list:
	print('on file {0}'.format(h))
	save_hanja_to_json('{0}.txt'.format(h), '{0}.json'.format(h))
	'''