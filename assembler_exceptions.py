class AssemblerException(Exception):
	_errors = []
	
	def __init__(self, errors=[]):
		self._errors = errors
	
	def __str__(self):
		errors = ''
		for error in self._errors:
			errors += 'Line %d: %s\n' % error
		
		return errors