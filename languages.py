from flask import Flask, jsonify, make_response, render_template, send_from_directory, url_for
from urllib.request import urlopen
import urllib
import json
from bs4 import BeautifulSoup
from bson.objectid import ObjectId

app = Flask(__name__, static_folder="static")

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

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
@app.route('/hanja/articles', methods=['GET'])
@app.route('/hanja#/articles', methods=['GET'])
def get_hanja():
    return app.send_static_file('hanja.html')

@app.route('/api/v1.0/korean/hanja/list/<string:list_name>', methods=['GET'])
def get_hanja_list(list_name):
    hanja_json_dict = {
      '8':   'hanja_8.json',
        '7':   'hanja_7.json',
        '6-1': 'hanja_6-1.json',
        '6-2': 'hanja_6-2.json',
        '5-1': 'hanja_5-1.json',
        '5-2': 'hanja_5-2.json',
        '4-1': 'hanja_4-1.json',
        '4-2': 'hanja_4-2.json',
        '3-1': 'hanja_3-1.json',
        '3-2': 'hanja_3-2.json',
        '2-2': 'hanja_2-2.json',
        '2-1': 'hanja_2-1.json',
        '1': 'hanja_1.json'
    }
    import json, os
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    APP_STATIC = os.path.join(APP_ROOT, 'hanja')
    filename = hanja_json_dict[list_name]
    with open(os.path.join(APP_STATIC, filename)) as outfile:
        data = json.load(outfile)
    return jsonify({'result': data})

@app.route('/api/v1.0/korean/hanja/article/<string:id>', methods=['GET'])
def get_article_route(id):
    from hanja.hanja_to_mongo import get_article
    return JSONEncoder().encode(get_article(id))

@app.route('/api/v1.0/korean/hanja/article/all/', methods=['GET'])
def get_all_articles_route():
    from hanja.hanja_to_mongo import get_all_articles
    return JSONEncoder().encode(get_all_articles())

@app.route('/api/v1.0/korean/hanja/article/articleID/<string:id>', methods=['GET'])
def get_article_by_article_id_route(id):
    from hanja.hanja_to_mongo import get_article_by_article_id
    return JSONEncoder().encode(get_article_by_article_id(id))

@app.route('/api/v1.0/korean/naver/def/eng/<string:word>', methods=['GET'])
def get_definition_english(word):
    root = get_definition(word)
    return str({'word': root[0], 'definition': root[1], 'hanja': root[2]})

def get_definition(word):
    u2 = urllib.parse.quote(word)
    url = 'http://endic.naver.com/search.nhn?sLn=en&isOnlyViewEE=N&query=%s' %(u2)
    print(url)
    page=urlopen(url)

    soup = BeautifulSoup(page.read(), "html.parser")
    #check if this is a 1 pager
    div = soup.find(class_='fnt_k18')
    if div:
        term = div.strong.contents[0]
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
    if not div or not div.strong:
        return None
    #else get the one that has stuff eg http://endic.naver.com/krenEntry.nhn?sLn=en&entryId=ee70e407172a440daef84629e6e8df8a&query=%EA%B7%B8
    term = div.strong.contents[0]
    hanja = str(div.next_sibling).strip()
    definition = div.find_next(class_='fnt_k05').get_text()
    return (term, definition, hanja)


def get_definition_krdict(word, download_audio = False, audio_destination = None):
    u2 = urllib.parse.quote(word)
    url = 'https://krdict.korean.go.kr/eng/dicSearch/search?nation=eng&nationCode=6&ParaWordNo=&mainSearchWord={0}'\
          .format(u2)
    print(url)
    page = urlopen(url)

    soup = BeautifulSoup(page.read(), "html.parser")
    results = soup.find(id='article0')
    if results:
        term = results.a.strong.text
        if term != word:
            print("WARNING: FIRST WORD IS DIFFERENT")
        definition_results = results.ol.li.find_all('p')
        eng_def = definition_results[0].text.replace('\n',' ').strip()
        krn_def = definition_results[1].text.strip()
        eng_translate_def = definition_results[2].text.strip()
        if download_audio is True and audio_destination is not None:
            import re, os
            audio_file = results.img
            audio_link = audio_file['onclick'].split('\'')[1]
            if not os.path.exists(audio_destination):
                os.makedirs(audio_destination)
            dest = '{0}/{1}.mp3'.format(audio_destination, term)
            try:
                urllib.request.urlretrieve(audio_link, dest)
            except (urllib.error.HTTPError, urllib.error.ContentTooShortError) as e:
                print("no mp3 for {0}".format(dest))
        return eng_def, krn_def, eng_translate_def, term
    else:
        print("WORD NOT FOUND")
        return None, None, None, None


def get_root(word):
    if word == None: return None
    print("looking up {0} on english dict".format(word))
    u2 = urllib.parse.quote(word)
    url = 'http://endic.naver.com/search.nhn?sLn=en&isOnlyViewEE=N&query=%s' %(u2)
    print(url)
    page=urlopen(url)

    soup = BeautifulSoup(page.read(), "html.parser")
    #check if this is a 1 pager
    div = soup.find(class_='fnt_k18')
    if div:
        term = div.strong.contents[0]
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
    term = div.strong.contents[0]
    definition = div.find_next(class_='fnt_k05').get_text()
    return (term, definition)

def get_root_korean(word):
    from bs4 import NavigableString
    print("looking up {0} on korean dict".format(word))
    u2 = urllib.parse.quote(word)
    url = 'http://krdic.naver.com/search.nhn?sLn=en&isOnlyViewEE=N&query=%s' % (u2)
    print(url)
    page = urlopen(url)

    soup = BeautifulSoup(page.read(), "html.parser")
    # check if this is a 1 pager
    div = soup.find(class_='fnt_k18')
    if div:
        term = div.strong.contents
        defs = div.find_next(class_='align_line')
        if (defs.a):
            defs.a.decompose()
        definition = str(defs.get_text(' ', strip=True))
        return (term, definition)
    # look for words/idioms section
    section = '단어'
    spans = soup.find_all('span', class_='head_word')
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
        if (link.find('/detail') != -1):
            thisw = w
            break
    if not thisw:
        return None
    list = thisw.find_previous('li')
    if list.find("ul"):
        # print(list.find('ul').find_next("span"))
        definition = list.find('ul').find_next("span").get_text()
    # print(list.find('ul').find_next("span").get_text())
    else:
        allDescendants = []
        for child in list.find('p').descendants:
            if isinstance(child, NavigableString):
                allDescendants.append(child.string)
        if allDescendants:
            definition = ''.join(allDescendants)
        else:
            return None
    return (term, definition)

def get_hanja(word):
    u2 = urllib.parse.quote(word)
    url = 'http://hanja.naver.com/word?q=%s' %(u2)
    print(url)
    page=urlopen(url)

    soup = BeautifulSoup(page.read(), "lxml")
    #check if this is a 1 pager
    div = soup.find(class_='t_w')

    if div:
        sound = div.strong.contents[0]
        defs = soup.find(class_='entry_txt').p.get_text().strip().replace('\u3000', ' ')
        return {'sound': sound, 'definition': defs}
    else:
        return get_hanja_daum(word)


def get_hanja_daum(word):
    u2 = urllib.parse.quote(word)
    url = 'http://alldic.daum.net/search.do?q=%s&dic=hanja' %(u2)
    print(url)
    page=urlopen(url)

    soup = BeautifulSoup(page.read(), "lxml")
    #check if this is a 1 pager
    div = soup.find_all(class_='han_sch')

    if len(div)>0:
        for d in div:
            possible_div = d.find(class_='link_txt')
            if possible_div.find(class_="num_word"):
                for tag in possible_div.find(class_="num_word"):
                    tag.extract()
                print(possible_div)
            if d.find(class_='link_txt').text == word:
                sound = d.find(class_='trans_kor').text.replace('[','').replace(']','')
                defs = d.find_all(class_='trans_words')
                defs_joined = [the_text.text for the_text in defs]
                defs =' '.join(defs_joined)
                return {'sound': sound, 'definition': defs}
        #sound = div.strong.contents[0]
        #defs = soup.find(class_='entry_txt').p.get_text().strip().replace('\u3000', ' ')
        #return {'sound': sound, 'definition': defs}
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9090)
    #print(get_hanja_daum('合金'))
