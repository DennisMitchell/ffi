from argparse import ArgumentParser
from compiler import run

def ffi(*args):

	argparser = ArgumentParser(description = 'Frabjous FRACTRAN Interpreter')

	try:
		argparser._actions[0].help = 'Show this help message and exit.'
	except:
		pass

	argparser.add_argument(
		'file', metavar = 'FILE',
		help = 'Read source code from FILE.'
	)

	argparser.add_argument(
		'input', metavar = 'INPUT',
		help = 'Pass INPUT to the program.'
	)

	print_when = argparser.add_mutually_exclusive_group()

	print_when.add_argument(
		'-f', '--final', dest='print_all', action='store_false', default = False,
		help = 'Print only the final state. This is the default.'
	)

	print_when.add_argument(
		'-a', '--all', dest='print_all', action='store_true',
		help = 'Print all states, including the initial and the final state.'
	)

	args = argparser.parse_args(list(args) or None)
	run(open(args.file).read(), args.input, args.print_all)

if __name__ == '__main__':
	ffi()
