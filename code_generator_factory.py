from python_code_generator import PythonCodeGenerator

class CodeGeneratorFactory():
	@staticmethod
	def create(code_type):
		if 'python' == code_type:
			return PythonCodeGenerator()
		else:
			raise Exception('Invalid Code Generator.')