IGNORE_CHAR = set("⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻1234")

def parse_string_to_radicals(string):
	result = []
	i = 0
	while i < len(string):
		if string[i] == '[':
			end = string.find(']', i)
			if end == -1:
				result.append(string[i:])
				break
			result.append(string[i:end+1])
			i = end + 1
		else:
			if string[i] not in IGNORE_CHAR: result.append(string[i])
			i += 1
	return result

def parse_string_to_radicals_multiple_choices(string):
	l = []
	for s in string.split('/'):
		result = []
		i = 0
		while i < len(s):
			if s[i] == '[':
				end = s.find(']', i)
				if end == -1:
					result.append(s[i:])
					break
				result.append(s[i:end+1])
				i = end + 1
			else:
				if s[i] not in IGNORE_CHAR: result.append(s[i])
				i += 1
		l.append(result)
	return l

def parse_decomposition_dict(*filenames):
	d = dict()
	for filename in filenames:
		with open(filename, 'r', encoding='utf-8') as f:
			for line in f:
				line = line.strip()
				if not line or line.startswith('#'):
					continue
				cols = line.split('\t')
				if len(cols) < 2:
					continue
				key = cols[0]
				values = parse_string_to_radicals_multiple_choices(cols[1])
				d[key] = [''.join(value) for value in values]
	return d

def parse_key_dict(*filenames):
	d = dict()
	for filename in filenames:
		with open(filename, 'r', encoding='utf-8') as f:
			for line in f:
				line = line.strip()
				if not line or line.startswith('#'):
					continue
				cols = line.split('\t')
				if len(cols) < 2:
					continue
				value = cols[0]
				keys = parse_string_to_radicals(cols[1])
				for key in keys:
					d[key] = [value]
	return d

def substitute_and_write(input_file, output_file, subs_dict, ignore = None, single_only = False):
	if ignore is None: ignore = set()
	result_lines = set()
	with open(input_file, 'r', encoding='utf8') as infile:
		for line in infile:
			line = line.rstrip('\n')
			substituted = [parse_string_to_radicals(line.split('\t')[1])]
			for key, values in subs_dict.items():
				if key in ignore: continue
				new_substituted = []
				for l in substituted:
					if key in l and (not single_only or len(l) == 1):
						for v in values:
							new_substituted.append([v if item == key else item for item in l])
					else:
						new_substituted.append(l)
				substituted = new_substituted
			result_lines.update([line.split('\t')[0] + '\t' + ''.join(decomp) for decomp in substituted])
	sorted_lines = sorted(result_lines)
	with open(output_file, 'w', encoding='utf8') as outfile:
		for l in sorted_lines:
			outfile.write(l + '\n')

def add_radicals(input_file, output_file, radical_map, ignore = None):
	if ignore is None: ignore = set()
	result_lines = set()
	with open(input_file, 'r', encoding='utf8') as infile:
		for line in infile:
			line = line.rstrip('\n')
			char = line.split('\t')[0]
			if char in ignore: continue
			if char not in radical_map: continue
			decomp = parse_string_to_radicals(line.split('\t')[1])
			if len(decomp) == 1 and decomp[0] != char: decomp.append(radical_map[char])
			result_lines.add(char + '\t' + ''.join(decomp))
	sorted_lines = sorted(result_lines)
	with open(output_file, 'w', encoding='utf8') as outfile:
		for l in sorted_lines:
			outfile.write(l + '\n')

def repeat_singlets(input_file, output_file):
	result_lines = set()
	with open(input_file, 'r', encoding='utf8') as infile:
		for line in infile:
			line = line.rstrip('\n')
			char = line.split('\t')[0]
			decomp = parse_string_to_radicals(line.split('\t')[1])
			if len(decomp) == 1: decomp.append(decomp[0])
			result_lines.add(char + '\t' + ''.join(decomp))
	sorted_lines = sorted(result_lines)
	with open(output_file, 'w', encoding='utf8') as outfile:
		for l in sorted_lines:
			outfile.write(l + '\n')