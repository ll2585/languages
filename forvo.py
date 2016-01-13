import base64
import urllib.request
from bs4 import BeautifulSoup
url = 'http://forvo.com/word/{0}'
words = [line.rstrip('\n') for line in open('forvo_words.txt', encoding="utf-8")]
_AUDIO_HTTP_HOST = "audio.forvo.com:80"

for query in words:
	page = urllib.request.urlopen(url.format(urllib.parse.quote(query)))
	soup = BeautifulSoup(page.read())
	for audio in soup.find_all('a', {'class': 'play'}):
		key = audio['onclick'].split(',')[1]
		decoded_key =base64.b64decode(key).decode("utf-8") 
		mp3_path = 'http://{0}/mp3/{1}'.format(_AUDIO_HTTP_HOST, decoded_key)
		dest = 'forvo/'+ query + '_' + decoded_key.split('/')[-1]
		urllib.request.urlretrieve(mp3_path, dest)