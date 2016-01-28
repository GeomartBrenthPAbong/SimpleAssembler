def twos_complement(x):
	i = len(x) - 1
	invert = False
	
	new_str = range(len(x))
	
	while i >= 0 and '0' == x[i]: 
		new_str[i] = '0'
		i-= 1
	
	if i >= 0: new_str[i] = '1'
	i -= 1
	
	while i >=0: 
		new_str[i] = '1' if '0' == x[i] else '0'
		i -= 1
	
	return ''.join(new_str)

def print_dashes(num_dashes):
	dashes = ''
	for num_dash in num_dashes:
		dashes += ' '
		while num_dash >= 0:
			dashes += '-'
			num_dash -= 1
	print dashes

def print_list(contents, num_dashes):
	data = '|'
	counter = 0
	for content in contents:
		data += " %s" % content
		num_spaces = num_dashes[counter] - len(content)
		
		while num_spaces > 0:
			data += " "
			num_spaces -= 1
		
		data += '|'
		counter += 1
	print data

def print_mem(mem):
	labels = ['AX', 'BX', 'CX', 'DX']
	
	dash_nums = []
	for datum in mem:
		dash_nums.append(len(str(datum)) + 2)
		
	print_dashes(dash_nums)
	print_list(labels, dash_nums)
	print_dashes(dash_nums)
	print_list(map(str, mem), dash_nums)
	print_dashes(dash_nums)

def signed_bin_add(x, y):
	maxlen = max(len(x), len(y))
	
	x_s = x[0]
	y_s = y[0]
	
	x = x[1:]
	y = y[1:]
	
	x = x.zfill(maxlen)
	y = y.zfill(maxlen)
	
	if '1' == x_s and '0' == y_s: x = twos_complement(x)
	if '1' == y_s and '0' == x_s: y = twos_complement(y)
	
	result = ''
	carry = 0
	
	for i in range(maxlen-1, -1, -1):
		r = carry
		r += 1 if x[i] == '1' else 0
		r += 1 if y[i] == '1' else 0
	
		result = ('1' if r % 2 == 1 else '0') + result
		carry = 0 if r < 2 else 1
	
	if ('1' == x_s and '1' == y_s) or \
		('0' == x_s and '0' == y_s):
			if carry !=0 : result = '1' + result
			result = '1' + result if '1' == x_s else '0' + result
	elif '1' == result[0]:
		result = '1' + twos_complement(result)
	
	return result

def int_to_bin(integer):
	sign = '1' if integer < 0 else '0'
	return sign + '{0:07b}'.format(abs(integer))


def bin_to_int(binary):
	import math
	power = len(binary) - 2
	
	counter = 1
	r = 0
	while counter < len(binary):
		if '1' == binary[counter]:
			r += math.pow(2, power)
		power -= 1
		counter += 1
	
	r = int(r)
	return r if '0' == binary[0] else -1 * r