from src_py.parse_encode import *
from collections import defaultdict, Counter
from src_radical.get_kangxi_radical import *

class Char:
    def __init__(self, name, type = None, parent_name = None, parent_type = None):
        self.name = name
        if len(name) == 1: self.ord = ord(name)
        else: self.ord = None # char is dummy, unicode unavailable 
        if type is None:
            if len(name) == 1: self.type = 'reg' 
            else: self.type = 'dummy'
        else: self.type = type # 'reg' 'dummy' 'reduced'
        self.parent_name = parent_name
        self.parent_type = parent_type # 'phonetic' 'dummy' 'reduced' 'alternative'

    def set_parent(self, parent_name, parent_type):
        if self.name == parent_name: self.parent_name = None
        else: self.parent_name = parent_name
        self.parent_type = parent_type
    
    def find_decomposition(self, forest, decomp_dict):
        l = []
        if self.name in decomp_dict: l.extend(decomp_dict[self.name])
        parent_l = []
        if self.parent_name is not None: 
            parent_l.extend(forest.dict[self.parent_name].find_decomposition(forest, decomp_dict))
        parent_l, parent_all_len_one = remove_len_one_if_more_exist(parent_l)
        l, _ = remove_len_one_if_more_exist(l)
        if parent_all_len_one and len(l) >= 1: return l
        return l + parent_l

def remove_len_one_if_more_exist(ls):
    new_ls = []
    for l in ls:
        if len(l) > 1: new_ls.append(l)
    if len(new_ls) == 0: return ls, True # True for all len = 1
    return new_ls, False

class Forest:
    def __init__(self):
        self.dict = {None:None}
    
    def add(self, char, dup_chars): 
        if char.name in self.dict: 
            if dup_chars is not None: dup_chars.add(char.name)
        else: self.dict[char.name] = char

def parse(parent_name, children_string, forest, dup_chars, parent_type = 'phonetic', mode = None): # parent must be in forest, only children are added to the forest in this method 
    if parent_name not in forest.dict: raise Exception("Parent Missing: " + parent_name)
    if (children_string.count('(') != children_string.count(')') 
        or children_string.count('[') != children_string.count(']') 
        or children_string.count('{') != children_string.count('}')): 
        raise Exception("Format Error: " + children_string)
    if '\t' in children_string: parse(parent_name, children_string.replace('\t', '(', 1) + ')', forest, dup_chars, parent_type = parent_type, mode = mode); return
    nested_string = ''
    nesting = 0
    previous_char = parent_name
    for cursor in children_string:
        current_char = cursor
        if cursor in '([{': nesting += 1
        elif cursor in '}])': nesting -= 1
        if nesting == 0:
            if cursor == ']': current_char = nested_string + ']'
            if cursor == '}': parse(previous_char, nested_string[1:], forest, dup_chars, parent_type = 'alternative', mode = mode)
            elif cursor == ')': parse(previous_char, nested_string[1:], forest, dup_chars, parent_type = 'phonetic', mode = mode)
            elif current_char != parent_name: 
                if mode == 'init': forest.add(Char(current_char, parent_name = parent_name, parent_type = parent_type), dup_chars = dup_chars)
                if mode == 'mod' and parent_name is not None: forest.dict[current_char].set_parent(parent_name, parent_type)
                previous_char = current_char
            if cursor in '}])': nested_string = ''
        if nesting > 0: nested_string += cursor

def read_dict(file_name, forest, dup_chars, mode): # mode can be 'init' or 'mod'
    with open(file_name,'r',encoding='utf8') as file: lines = file.read().splitlines()
    for line in lines:
        if line[0] == '#': continue
        parse(None, line.split('\t#')[0], forest, dup_chars, mode = mode)

def read_subs(file_name):
    subs = dict()
    with open(file_name,'r',encoding='utf8') as file: lines = file.read().splitlines()
    for line in lines:
        if line[0] == '#': continue
        l = line.split('\t#')[0].split('\t')
        subs[l[0]] = l[1:]
    return subs

def count_char_occurrences(file_name):

    key_counts = defaultdict(int)
    key_items = defaultdict(list)

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f:
            if line.strip() == '' or line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            key, item = parts[0], parse_string_to_radicals(parts[1])
            key_counts[key] += 1
            key_items[key].append(item)

    char_totals = Counter()
    for key, items in key_items.items():
        count = key_counts[key]
        for item in items:
            for c in item:
                char_totals[c] += 1 / count
    
    count_sum = sum(char_totals.values())
    for c in char_totals:
        char_totals[c] = round(char_totals[c]/count_sum*26, 3)  # Round to 3 decimal places

    return dict(sorted(char_totals.items(), key=lambda item: item[1], reverse=True))



# Main
src_dir = 'src/'; log_dir = 'log/'; src_encode_dir = 'src_encode/'

forest =  Forest()
dup_chars = set()
read_dict(src_dir + 'phonograph_char_dict.txt', forest, dup_chars, mode = 'init')
read_dict(src_dir + 'phonograph_rare.txt', forest, dup_chars, mode = 'init')
read_dict(src_dir + 'phonograph_hierarchy.txt', forest, dup_chars, mode = 'mod')

decomp_dict = parse_decomposition_dict(src_encode_dir + "phonograph_dict.txt",src_encode_dir + "extra.txt")
basic_dict = parse_decomposition_dict(src_encode_dir + "keys.txt")
key_dict = parse_key_dict(src_encode_dir + "basic.txt")
 
with open(log_dir + 'dict_raw.txt',"w",encoding="utf8") as f:
    for char in forest.dict:
        if char is None or forest.dict[char].type != 'reg': continue
        for decomp in forest.dict[char].find_decomposition(forest, decomp_dict):
            f.writelines(char + '\t' + ''.join(decomp) + '\n')

with open(log_dir + 'occurrence_raw.txt',"w",encoding="utf8") as f:
    occurrence = count_char_occurrences(log_dir + 'dict_raw.txt')
    for char, count in occurrence.items():
        f.writelines(char + '\t' + str(count) + '\n')

print("decomposing...")
substitute_and_write(log_dir + 'dict_raw.txt', log_dir + 'dict.txt', decomp_dict, ignore = key_dict)
print("processing singlets...")
with open('src_radical/kangxi_radical_chars.txt', 'r', encoding='utf8') as f:
    kangxi_radicals = list(f.read().replace('\n', ''))
from functools import partial
radical_map = partial(get_kangxi_radical, kangxi_radicals)
add_radicals(log_dir + 'dict.txt', log_dir + 'dict.txt', radical_map, ignore = decomp_dict)
substitute_and_write(log_dir + 'dict.txt', log_dir + 'dict.txt', basic_dict, single_only = True)
# repeat_singlets(log_dir + 'dict.txt', log_dir + 'dict.txt')
print("collecting keys...")
substitute_and_write(log_dir + 'dict.txt', log_dir + 'dict.txt', key_dict)
print("done")

with open(log_dir + 'occurrence.txt',"w",encoding="utf8") as f:
    occurrence = count_char_occurrences(log_dir + 'dict.txt')
    for char, count in occurrence.items():
        f.writelines(char + '\t' + str(count) + '\n')

# Concatenate two text files and save the result
def concatenate_files(file1, file2, output_file):
    with open(file1, 'r', encoding='utf8') as f1, open(file2, 'r', encoding='utf8') as f2, open(output_file, 'w', encoding='utf8') as out:
        out.writelines(f1.readlines())
        out.writelines(f2.readlines())

concatenate_files('src_py/header.yaml', log_dir + 'dict.txt', 'phonograph.dict.yaml')