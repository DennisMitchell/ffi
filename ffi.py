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
		'-f', '--final', dest = 'print_all', action = 'store_false', default = False,
		help = 'Print only the final state. (default)'
	)

	print_when.add_argument(
		'-a', '--all', dest = 'print_all', action = 'store_true',
		help = 'Print all states, including the initial and the final state.'
	)

	print_how = argparser.add_mutually_exclusive_group()

	print_how.add_argument(
		'-c', '--compact', dest = 'print_how', default = 'print_compact',
		action = 'store_const', const = 'print_compact',
		help = 'Print a compact representation of the state. (default)'
	)

	print_how.add_argument(
		'-w', '--whole', dest = 'print_how',
		action = 'store_const', const = 'print_state', default = 'print_state',
		help = 'Print the whole state, including exponents less than 2.'
	)

	args = argparser.parse_args(list(args) or None)
	run(open(args.file).read(), args.input, args.print_all, args.print_how)

if __name__ == '__main__':
	ffi()
