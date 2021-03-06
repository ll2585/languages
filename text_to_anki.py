import re, os
from languages import get_definition, get_root_korean, get_definition_krdict
from jamo import get_jamo
from datetime import datetime


filename = 'HP_01_CH_03.txt'
export_file = 'HP_01_CH_03_words.csv'
# HAS TO BE A FILE WITH ALL THE CLOZE BLOCKS DELIMITED WITH '|' AND ALL TERMS DELIMITED WITH '[TERM]'
pat = r'(?<=\[).+?(?=\])'
cloze_before_label = '문장 (cloze)'
cloze_after_label = '문장'
term_label = '단어'
eng_def_label = '영어'
krn_def_label = '정의'
char_hint_label = '자 힌트'
audio_label = '녹음'

with open(filename, 'r', encoding="utf-8") as f:
    all_lines = f.read()

splitted = all_lines.split('|')

cloze_blocks = []
all_terms = []
term_dict = {}
all_clozes = []

for line in splitted:
    cloze_blocks.append(line.replace('\n\n', '\n').strip().replace('\n','<br />'))

for block in cloze_blocks:
    raw_text = block.replace('[', '').replace(']', '')
    terms = (re.findall(pat, block))
    for t in terms:
        print(t)
        if t in term_dict:
            print("ALREADY DID THIS")
            continue
        all_terms.append(t)
        cloze_before = raw_text.replace(t, '<font color="#0000ff"><b>[...]</b></font>')
        cloze_after = raw_text.replace(t, '<font color="#0000ff"><b>{0}</b></font>'.format(t))
        term_dict[t] = {}
        term_dict[t][cloze_before_label] = cloze_before
        term_dict[t][cloze_after_label] = cloze_after

        stripped_word = t.strip()
        this_def = get_definition(stripped_word)
        if this_def:
            term = this_def[0]
            audio_destination_folder = datetime.today().strftime('%Y%m%d')
            krdict_defs = get_definition_krdict(term, download_audio=True, audio_destination=audio_destination_folder)
            if krdict_defs[3] and os.path.isfile('{0}/{1}.mp3'.format(audio_destination_folder, krdict_defs[3])):
                term_dict[t][audio_label] = '[sound:{0}.mp3]'.format(krdict_defs[3])
            else:
                term_dict[t][audio_label] = ''
            if krdict_defs[0]:
                eng_def = '{0} [{1}]'.format(krdict_defs[0], krdict_defs[2])
                krn_def = krdict_defs[1]
                term_dict[t][term_label] = term
                term_dict[t][eng_def_label] = eng_def
                term_dict[t][krn_def_label] = krn_def
            else:
                term_dict[t][term_label] = term
                term_dict[t][eng_def_label] = this_def[1]
                korean_def = get_root_korean(term.strip())
                if korean_def:
                    term_dict[t][krn_def_label] = korean_def[1]
                else:
                    term_dict[t][krn_def_label] = 'NO KOREAN DEF'
        else:
            term_dict[t][term_label] = stripped_word
            term_dict[t][eng_def_label] = "MANUALLY DO"
            term_dict[t][krn_def_label] = "MANUALLY DO"
            term_dict[t][audio_label] = ''
        char_hint = get_jamo(t[0])[0]
        if char_hint == 'ᄀ': char_hint = 'ㄱ'
        term_dict[t][char_hint_label] = char_hint
        # print(cloze_after)
    # print(raw_text)
    print('-----------------')

to_file = []
for t in all_terms:
    this_word = [term_dict[t][term_label],
                 term_dict[t][eng_def_label],
                 term_dict[t][krn_def_label],
                 term_dict[t][char_hint_label],
                 term_dict[t][cloze_before_label],
                 term_dict[t][cloze_after_label],
                 term_dict[t][audio_label]]
    to_file.append('\t'.join(list(this_word)))

print('\n'.join(to_file))
with open(export_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(to_file))
