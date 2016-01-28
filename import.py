"""
how to use:
1) make a list of korean vocab words
2) put it into import.txt
3) make sure that export.csv is clear
4) run this
5) manually check export.csv and save it as something else
6) copy export.csv to anki or whatever
"""
from languages import get_definition, get_root_korean
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
	if get_root_korean:
		this_word.append(korean_def[1])
	defs.append('\t'.join(list(this_word)))
print('\n'.join(defs))
with open('export.csv', 'w', encoding='utf-8') as f:
	f.write('\n'.join(defs))