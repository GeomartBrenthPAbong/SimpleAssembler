from code_generator import CodeGenerator

class PythonCodeGenerator(CodeGenerator):
	def generate(self, exps, filename='a'):
		file_obj = open(filename + '.py', 'w')
		
		file_obj.write('memory = [0, 0, 0, 0]\n')
		file_obj.write('ip = ' + str(exps[0][0]) + '\n\n')
		
		self.__append_static_file(file_obj)
		file_obj.write('\n\n')
		
		max_line_num = 0
		for line_num, operator, operands in exps:
			line_expr = self.__create_line_expr(operator, operands)
			function = self.__create_func('f' + str(line_num), [], line_expr)
			
			max_line_num = line_num
			file_obj.write(function)
		
		file_obj.write('\n\n')
		file_obj.write('try:\n')
		while_loop_exprs = ["func = 'f' + str(ip) + '()'", \
							"eval(func)", \
							"ip += 1"]
		
		ip_roller = self.__create_while('ip <= ' + str(max_line_num), while_loop_exprs, 1)
		file_obj.write(ip_roller)
		
		file_obj.write('except NameError:\n\tpass')
		file_obj.close()
	
	def __append_static_file(self, file_obj):
		with open('static.py', 'r') as statics:
			for line in statics:
				file_obj.write(line)
		
		statics.close()
	
	def __corresponding_term(self, operand):
		if 'REG' == operand[0]:
			return 'memory[' + self._mem_loc[operand[1]] + ']'
		return operand[1]
	
	def __create_func(self, function_name, params, line_exprs, num_tabs=0):
		tabs = self.__create_tabs(num_tabs)
		
		params = "(" + ", ".join(params) + ")"
		return tabs + 'def ' + function_name + params + ':\n' + self.__block_body(tabs, line_exprs)
		
	
	def __create_while(self, while_cond, line_exprs, num_tabs=0):
		tabs = self.__create_tabs(num_tabs)
		
		return tabs + 'while ' + while_cond + ':\n' + self.__block_body(tabs, line_exprs)
	
	def __create_if(self, if_cond_block_map, num_tabs=0):
		tabs = self.__create_tabs(num_tabs)
		
		counter = 0
		if_block = ''
		if_tab = self.__create_tabs(1)
		for if_cond, line_exprs in if_cond_block_map:
			if counter == 0:
				keyword = 'if'
			elif if_cond:
				keyword = 'elif'
			else:
				keyword = 'else'
			
			if_block += tabs + keyword + ' ' + if_cond + ':\n' + \
						 self.__block_body(tabs + if_tab, line_exprs)
			
			counter += 1
		
		return if_block
	
	def __create_tabs(self, num_tabs):
		tabs = ''
		while num_tabs > 0:
			tabs += '\t'
			num_tabs -= 1
		
		return tabs
	
	def __block_body(self, tabs, line_exprs):
		block = ''
		for line_expr in line_exprs:
			block += tabs + '\t' + line_expr + '\n'
		
		return block
	
	def __create_line_expr(self, operator, operands):
		if 'MOV' == operator:
			return [self.__corresponding_term(operands[0]) + \
					' = ' + \
					self.__corresponding_term(operands[1]) + \
					'\n']
		elif 'ADD' == operator:
			return [self.__corresponding_term(operands[0]) + \
					' = bin_to_int(signed_bin_add(int_to_bin(' + \
					self.__corresponding_term(operands[0]) + \
					'), int_to_bin(' + \
					self.__corresponding_term(operands[1]) + \
					')))\n']
		elif 'SUB' == operator:
			return [self.__corresponding_term(operands[0]) + \
					' = bin_to_int(signed_bin_add(int_to_bin(' + \
					self.__corresponding_term(operands[0]) + \
					'), int_to_bin(-1 * ' + \
					self.__corresponding_term(operands[1]) + \
					')))\n']
		elif 'PRT' == operator:
			return ['print ' + \
					self.__corresponding_term(operands[0]) + \
					'\n']
		elif 'JMP' == operator:
			return ['global ip', 'ip = ' + self.__corresponding_term(operands[0]) + ' - 1\n']
		elif 'JFZ' == operator:
			if_block = [('0 == memory[0]', \
						['global ip', \
						'ip = ' + self.__corresponding_term(operands[0])  + ' - 1'])]
			return [self.__create_if(if_block)]
		elif 'JNZ' == operator:
			if_block = [('0 != memory[0]', \
						['global ip', \
						'ip = ' + self.__corresponding_term(operands[0])  + ' - 1'])]
			return [self.__create_if(if_block)]
		elif 'PRTM' == operator:
			return ['print_mem(memory)\n']
		else:
			return ''