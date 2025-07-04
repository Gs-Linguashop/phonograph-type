import sys

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
				d[key] = parse_string_to_radicals_multiple_choices(cols[1])
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
					d[key] = [[value]]
	return d

def substitute_and_write(input_file, output_file, subs_dict, ignore = None, single_only = False):
	if ignore is None: ignore = set()
	result_lines = set()
	with open(input_file, 'r', encoding='utf8') as infile:
		for line in infile:
			line = line.rstrip('\n')
			decomp_raw = parse_string_to_radicals(line.split('\t')[1])
			if single_only and len(decomp_raw) != 1: result_lines.add(line); continue
			decomp_subs = sub_decomps(decomp_raw, subs_dict, ignore)
			result_lines.update([line.split('\t')[0] + '\t' + ''.join(decomp) for decomp in decomp_subs])
	sorted_lines = sorted(result_lines)
	with open(output_file, 'w', encoding='utf8') as outfile:
		for l in sorted_lines:
			outfile.write(l + '\n')

def sub_decomps(decomp, subs_dict, ignore, cursor = 0):
	for i in range(cursor, len(decomp)):
		char = decomp[i]
		if char in ignore or char not in subs_dict: continue
		if len(subs_dict[char]) == 1 and ''.join(subs_dict[char][0]) == char: continue
		return_list = []
		for sub in subs_dict[char]:
			return_list.extend(sub_decomps(decomp[:i] + sub + decomp[i + 1:], subs_dict, ignore, cursor = i))
		# Remove duplicate decompositions by converting lists to tuples for hashing
		unique_return_list = []
		seen = set()
		for item in return_list:
			t = tuple(item)
			if t not in seen: seen.add(t); unique_return_list.append(item)
		return unique_return_list
	return [decomp]  # If no substitutions were made, return the original decomposition

def add_radicals(input_file, output_file, radical_map, ignore = None):
	if ignore is None: ignore = set()
	result_lines = set()
	with open(input_file, 'r', encoding='utf8') as infile:
		for line in infile:
			line = line.rstrip('\n')
			char = line.split('\t')[0]
			if radical_map(char) is None: continue
			if char in ignore: result_lines.add(line); continue
			decomp = parse_string_to_radicals(line.split('\t')[1])
			if len(decomp) == 1: decomp.append(radical_map(char))
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