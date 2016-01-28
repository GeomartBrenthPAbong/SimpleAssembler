from assembler_exceptions import AssemblerException
from collections import deque

class SyntaxAnalyzer():
	__tokens = None
	__errors = []

	def analyze(self, list_tokens):
		if not list_tokens:
			return []
		
		self.__tokens = deque(list_tokens)
		exps = []
		
		while len(self.__tokens) > 0:
			token = self.__tokens.popleft()
			token_name, _, line_num = token
			
			if 'END' == token_name:
				continue
			elif 'OPRTR' != token_name:
				self.__errors.append((line_num, 'No operator.'))
			else:
				exp = self.__create_exp(token)
				exps.append(exp)
		
		if self.__errors:
			raise AssemblerException(self.__errors)
		
		return exps
	
	def __is_operand(self, token):
		return 'REG' == token[0] or 'INT' == token[0]
	
	def __create_exp(self, token):
		_, attr_value, line_num = token
		
		next_token = self.__tokens.popleft()
		operands = []
		
		while 'END' != next_token[0]:
			if not self.__is_operand(next_token):
				self.__errors.append((line_num, 'Operands must be a register or a constant.'))
			else:
				operands.append(next_token)
			
			next_token = self.__tokens.popleft()
		
		if 2 < len(operands):
			self.__errors.append((line_num, 'Maximum number of operands is 2.'))
		
		return (line_num, attr_value, operands)