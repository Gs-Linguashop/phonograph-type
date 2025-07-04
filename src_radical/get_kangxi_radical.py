def get_kangxi_radical(char_list, input_char):
	"""
	Given a sorted list of Unicode characters (by codepoint), find the latest character in the list
	whose codepoint is smaller than the input character.
	Return None if input_char is before the first character in the list or not in BMP (U+0000 to U+9FA5).
	"""
	if not char_list:
		return None

	input_cp = ord(input_char)
	if input_cp < 0x0000 or input_cp > 0x9FA5:
		return None

	# Binary search for efficiency
	left, right = 0, len(char_list) - 1
	result = None
	while left <= right:
		mid = (left + right) // 2
		mid_cp = ord(char_list[mid])
		if mid_cp <= input_cp:
			result = char_list[mid]
			left = mid + 1
		else:
			right = mid - 1

	return result