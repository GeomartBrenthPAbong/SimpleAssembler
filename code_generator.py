from abc import ABCMeta, abstractmethod

class CodeGenerator():
	__metaclass__ = ABCMeta
	
	_mem_loc = {
		'AX' : '0',
		'BX' : '1',
		'CX' : '2',
		'DX' : '3'
	}
	
	#abstractmethod
	def generate(self, exps, filename='a'):
		pass