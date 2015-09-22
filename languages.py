from flask import Flask, jsonify, make_response, render_template, send_from_directory, url_for
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder="static")


@app.route('/api/v1.0/korean/naver/root/eng/<string:word>', methods=['GET'])
def get_root_english(word):
	root = get_root(word)
	return str({'word': root[0], 'definition': root[1]})

@app.route('/api/v1.0/korean/naver/root/kor/<string:word>', methods=['GET'])
def get_root_korean(word):
	root = get_root_korean(word)
	return str({'word': root[0], 'definition': root[1]})

@app.route('/flashcards', methods=['GET'])
def get_flashcards():
	return app.send_static_file('flashcards.html')

@app.route('/audio', methods=['GET'])
def get_audio():
	return app.send_static_file('audio.html')

@app.route('/hanja', methods=['GET'])
def get_hanja():
	return app.send_static_file('hanja.html')

@app.route('/api/v1.0/korean/naver/def/eng/<string:word>', methods=['GET'])
def get_definition_english(word):
	root = get_definition(word)
	return str({'word': root[0], 'definition': root[1], 'hanja': root[2]})

def get_definition(word):
	u2 = urllib.parse.quote(word)
	url = 'http://endic.naver.com/search.nhn?sLn=en&isOnlyViewEE=N&query=%s' %(u2)
	print(url)
	page=urlopen(url)

	soup = BeautifulSoup(page.read())
	#check if this is a 1 pager
	div = soup.find(class_='fnt_k18')
	if div:
		term = div.strong.contents
		defs = div.find_next(class_='align_line')
		if(defs.a):
			defs.a.decompose()
		definition = str(defs.get_text(' ',strip=True))
		print("FSA")
		return (term, definition)
	#look for words/idioms section
	section = 'Words/Idioms'
	images = soup.find_all('img', alt=True)
	words = None
	for i in images:
		if(i['alt'] == section):
			words = i.find_previous(class_='word_num')
	if not words:
		return None
	possibleWords = words.find_all(class_='fnt_e30')
	if not possibleWords:
		return None
	found = False
	for w in possibleWords:
		if found:
			break
		for link in w.find_all('a'):
			l = link.get('href')
			if(l.find('/krenEntry.nhn?entryId')!= -1):
				div = link
				found = True
				break
	if not div:
		return None
	#else get the one that has stuff eg http://endic.naver.com/krenEntry.nhn?sLn=en&entryId=ee70e407172a440daef84629e6e8df8a&query=%EA%B7%B8
	term = div.strong.contents
	hanja = str(div.next_sibling).strip()
	definition = div.find_next(class_='fnt_k05').get_text()
	return (term, definition, hanja)

def get_root(word):
	if word == None: return None
	print(word)
	u2 = urllib.parse.quote(word)
	url = 'http://endic.naver.com/search.nhn?sLn=en&isOnlyViewEE=N&query=%s' %(u2)
	print(url)
	page=urlopen(url)

	soup = BeautifulSoup(page.read())
	#check if this is a 1 pager
	div = soup.find(class_='fnt_k18')
	if div:
		term = div.strong.contents
		defs = div.find_next(class_='align_line')
		if(defs.a):
			defs.a.decompose()
		definition = str(defs.get_text(' ',strip=True))
		return (term, definition)
	#look for words/idioms section
	section = 'Words/Idioms'
	images = soup.find_all('img', alt=True)
	words = None
	for i in images:
		if(i['alt'] == section):
			words = i.find_previous(class_='word_num')
	if not words:
		return None
	possibleWords = words.find_all(class_='fnt_e30')
	if not possibleWords:
		return None
	found = False
	for w in possibleWords:
		if found:
			break
		for link in w.find_all('a'):
			l = link.get('href')
			if(l.find('/krenEntry.nhn?entryId')!= -1):
				div = link
				found = True
				break
	if not div or not div.strong:
		return None
	#else get the one that has stuff eg http://endic.naver.com/krenEntry.nhn?sLn=en&entryId=ee70e407172a440daef84629e6e8df8a&query=%EA%B7%B8
	term = div.strong.contents
	definition = div.find_next(class_='fnt_k05').get_text()
	return (term, definition)

def get_root_korean(word):
	from bs4 import NavigableString
	print(word)
	u2 = urllib.parse.quote(word)
	url = 'http://krdic.naver.com/search.nhn?sLn=en&isOnlyViewEE=N&query=%s' %(u2)
	print(url)
	page=urlopen(url)

	soup = BeautifulSoup(page.read())
	#check if this is a 1 pager
	div = soup.find(class_='fnt_k18')
	if div:
		term = div.strong.contents
		defs = div.find_next(class_='align_line')
		if(defs.a):
			defs.a.decompose()
		definition = str(defs.get_text(' ',strip=True))
		return (term, definition)
	#look for words/idioms section
	section = '??'
	spans = soup.find_all('span', class_= 'head_word')
	if not spans:
		return None
	words = spans[0].find_previous(class_='section')
	if not words or not words.find('strong'):
		return None
	term = words.find('strong').contents[0]
	possibleWords = words.find_all(class_='fnt15')

	if not possibleWords:
		return None
	thisw = None
	for w in possibleWords:

		link = w.get('href')
		if(link.find('/detail')!= -1):
			thisw =w
			break
	if not thisw:
		return None
	list =  thisw.find_previous('li')
	if list.find("ul"):
		#print(list.find('ul').find_next("span"))
		definition = list.find('ul').find_next("span").get_text()
		#print(list.find('ul').find_next("span").get_text())
	else:
		allDescendants = []
		for child in list.find('p').descendants:
			if isinstance(child, NavigableString):
				allDescendants.append(child.string)
		if allDescendants:
			definition =''.join(allDescendants)
		else: return None
	return (term, definition)


if __name__ == '__main__':
	app.run(debug=True)
