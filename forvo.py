import base64
import urllib.request
from bs4 import BeautifulSoup
url = 'http://forvo.com/word/{0}'
words = [line.rstrip('\n') for line in open('import.txt', encoding="utf-8")]
_AUDIO_HTTP_HOST = "audio.forvo.com:80"

is_mandarin = False
is_korean = False
for query in words:
	try:
		page = urllib.request.urlopen(url.format(urllib.parse.quote(query)))
		soup = BeautifulSoup(page.read(), "lxml")
		##check for chinese
		if is_mandarin and soup.find_all('em', {'id': 'zh'}):
			soup = soup.find('em', {'id': 'zh'}).parent.parent
		if is_korean and soup.find_all('em', {'id': 'ko'}):
			soup = soup.find('em', {'id': 'ko'}).parent.parent
		for audio in soup.find_all('a', {'class': 'play'}):
			key = audio['onclick'].split(',')[1]
			decoded_key =base64.b64decode(key).decode("utf-8")
			mp3_path = 'http://{0}/mp3/{1}'.format(_AUDIO_HTTP_HOST, decoded_key)
			dest = query + '_' + decoded_key.split('/')[-1]
			try:
				urllib.request.urlretrieve(mp3_path, dest)
			except (urllib.error.HTTPError, urllib.error.ContentTooShortError) as e:
				print("no {0}".format(query))
	except (urllib.error.HTTPError, urllib.error.ContentTooShortError) as e:
			print("no {0}".format(query))