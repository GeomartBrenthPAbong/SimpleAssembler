from assembler_exceptions import AssemblerException

class SemanticsAnalyzer():
	__operator_operands = {
		'MOV' : 'REG_OPERAND',
		'ADD' : 'REG_OPERAND',
		'SUB' : 'REG_OPERAND',
		'PRT' : 'OPERAND',
		'JMP' : 'OPERAND',
		'JFZ' : 'OPERAND',
		'JNZ' : 'OPERAND',
		'PRTM' : 'NONE'
	}
	__errors = []
	
	def analyze(self, exprs):
		if not exprs:
			return
		
		for line_num, operator, operands in exprs:
			self.__redirect(line_num, operator, operands)
		
		
		if self.__errors:
			raise AssemblerException(self.__errors)
		
		
	def __redirect(self, line_num, operator, operands):
		func_code = self.__operator_operands[operator]
		
		if 'REG_OPERAND' == func_code:
			self.__reg_operand(line_num, operator, operands)
		elif 'OPERAND' == func_code:
			self.__operand(line_num, operator, operands)
		elif 'NONE' == func_code:
			self.__none(line_num, operator, operands)
	
	def __reg_operand(self, line_num, operator, operands):
		if 2 != len(operands):
			self.__errors.append((line_num, 'Invalid number of operands for operation \'' + operator + '\'.'))
		
		if 'REG' != operands[0][0]:
			self.__errors.append((line_num, 'The first operand of operation \'' + operator + '\' must be a register.'))
	
	def __operand(self, line_num, operator, operands):
		if 1 != len(operands):
			self.__errors.append((line_num, 'Invalid number of operands for operation \'' + operator + '\'.'))
		
	def __none(self, line_num, operator, operands):
		if operands:
			self.__errors.append((line_num, 'Operation \'' + operator + '\' must have no operands.'))