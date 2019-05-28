"""
how to use:
1) make a list of korean vocab words
2) put it into import.txt
3) make sure that export.csv is clear
4) run this
5) manually check export.csv and save it as something else
6) copy export.csv to anki or whatever
"""
from languages import get_definition, get_root_korean, get_definition_krdict

def write_original(): #korean/english/hanja/korean def
    with open('import.txt', 'r', encoding="utf-8") as f:
        all_lines = f.readlines()
    defs = []
    for word in all_lines:
        this_word = []
        this_def = get_definition(word.strip())
        korean_def = get_root_korean(word.strip())
        if this_def:
            this_word.append(this_def[0][0])
            this_word.append(this_def[1])
            this_word.append(this_def[2])
        else:
            this_word.append(word.strip())
            this_word.append("MANUALLY DO")
        if korean_def:
            this_word.append(korean_def[1])
        defs.append('\t'.join(list(this_word)))
    print('\n'.join(defs))
    with open('export.csv', 'w', encoding='utf-8') as f:
        f.write('\n'.join(defs))

def write_with_hint(): #korean/english/korean def/hangul hint
    from jamo import get_jamo
    with open('import.txt', 'r', encoding="utf-8") as f:
        all_lines = f.readlines()
    defs = []
    for word in all_lines:
        this_word = []
        stripped_word = word.strip()
        this_def = get_definition(stripped_word)
        if this_def:
            term = this_def[0]
            krdict_defs = get_definition_krdict(term)
            if krdict_defs[0]:
                eng_def = '{0} [{1}]'.format(krdict_defs[0], krdict_defs[2])
                krn_def = krdict_defs[1]
                this_word.append(term)
                this_word.append(eng_def)
                this_word.append(krn_def)
            else:
                this_word.append(term)
                this_word.append(this_def[1])
                korean_def = get_root_korean(word.strip())
                if korean_def:
                    this_word.append(korean_def[1])
        else:
            this_word.append(word.strip())
            this_word.append("MANUALLY DO")
        this_word.append(get_jamo(word[0])[0])
        defs.append('\t'.join(list(this_word)))
    print('\n'.join(defs))
    with open('export.csv', 'w', encoding='utf-8') as f:
        f.write('\n'.join(defs))

debug = False

if debug:
    word = '헝클어뜨리다'
    print("-------------EXPECTED FOUND------------")
    print(get_definition_krdict(word))

    word = '유쾌하지'
    print("-------------EXPECTED NOT FOUND------------")
    print(get_definition_krdict(word))
else:
    write_with_hint()
#korean_def = get_root_korean(word.strip())
#print(korean_def)