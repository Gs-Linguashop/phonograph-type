# radical list obtained at https://github.com/pwxcoo/chinese-xinhua

import json

def read_radicals(input_file):
	radical_map = dict()

	with open(input_file, 'r', encoding='utf-8') as f:
		data = json.load(f)
	
	for obj in data:
		for char in [obj["word"], obj["oldword"]]:
			if radical_map.get(char, "") == "":
				radical_map[char] = obj["radicals"]

	return radical_map