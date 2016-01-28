from lexical_analyzer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer
from semantics_analyzer import SemanticsAnalyzer
from code_generator_factory import CodeGeneratorFactory
from assembler_exceptions import AssemblerException

import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required = True, help = "Path to file")
ap.add_argument("-n", "--name", required = False, help = "Name of the generated python file")
args = vars(ap.parse_args())

if not args:
	exit()

f = args['file'].split('.')
if 'asm' != f[-1]:
	print 'Invalid file.'
	exit()

try:
	la = LexicalAnalyzer()
	tokens = la.tokenize(args["file"])
	
	sxa = SyntaxAnalyzer()
	exprs = sxa.analyze(tokens)
	
	ssa = SemanticsAnalyzer()
	ssa.analyze(exprs)
	
	cg = CodeGeneratorFactory.create('python')
	
	filename = 'a' if not args['name'] else args['name']
	
	cg.generate(exprs, filename)
except Exception as e:
	print e
