from assembler_exceptions import AssemblerException
import re

class LexicalAnalyzer():
	__pattern_token_name_mapping = [
		('^MOV$|^ADD$|^SUB$|^PRT$|^JMP$|^JFZ$|^JNZ$|^PRTM$' , 'OPRTR'),
		('^AX$|^BX$|^CX$|^DX$' , 'REG'),
		('\-?[0-9]+' , 'INT'),
		(';.*' , 'CMNT')
	]
	
	__errors = []
	
	def tokenize(self, file_addr):
		tokens = []
		
		with open(file_addr, 'r') as asm:
			line_num = 1
			for exp in asm:
				attr_values = re.split('[ ,]+', exp)
				
				for attr_value in attr_values:
					attr_value = attr_value.rstrip()
					
					if not attr_value:
						continue
					
					token = self.__identify_token(attr_value)
					
					if None == token:
						self.__errors.append((line_num, 'Undefined string \'' + attr_value + '\'.'))
						break
					if 'CMNT' != token[0]:
						tokens.append((token[0], token[1], line_num))
					else:
						break
				
				tokens.append(('END', '', line_num))
				line_num += 1
		
		asm.close()
		
		if self.__errors:
			raise AssemblerException(self.__errors)
		
		return tokens
	
	def __identify_token(self, attr_value):
		for pattern, token_name in self.__pattern_token_name_mapping:
			if None != re.match(pattern, attr_value):
				return (token_name, attr_value)
		
		return None