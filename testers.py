from languages import get_hanja

with open('import_hanja.txt', 'r', encoding="utf-8") as f:
	all_lines = f.readlines()
defs = []
for word in all_lines:
	this_word = []
	this_def = get_hanja(word.strip())
	if this_def:
		this_word = [word.strip(), this_def['sound'], this_def['definition']]
	else:
		this_word.append(word.strip())
		this_word.append("MANUALLY DO")
	defs.append('\t'.join(list(this_word)))
print('\n'.join(defs))
with open('export_hanja.csv', 'w', encoding='utf-8') as f:
	f.write('\n'.join(defs))