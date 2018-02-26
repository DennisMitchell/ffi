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

	print_when = argparser.add_argument_group('when to print')
	print_when = print_when.add_mutually_exclusive_group()

	print_when.add_argument(
		'-f', '--final', dest = 'print_all', action = 'store_false', default = False,
		help = 'Print only the final state. (default)'
	)

	print_when.add_argument(
		'-a', '--all', dest = 'print_all', action = 'store_true',
		help = 'Print all intermediate states.'
	)

	print_how = argparser.add_argument_group('what to print')
	print_how = print_how.add_mutually_exclusive_group()

	print_how.add_argument(
		'-c', '--compact', dest = 'print_how', default = 'print_compact',
		action = 'store_const', const = 'print_compact',
		help = 'Print a compact representation of the state. (default)'
	)

	print_how.add_argument(
		'-w', '--whole', dest = 'print_how',
		action = 'store_const', const = 'print_state', default = 'print_state',
		help = 'Print the whole state, including 0 and 1 exponents.'
	)

	print_how.add_argument(
		'-e', '--exp', dest = 'print_exp', metavar = 'PRIMES',
		help = 'Print the exponent of PRIMES. (comma-separated list)'
	)

	args = argparser.parse_args(list(args) or None)
	if args.print_exp: args.print_how = 'print_exp'

	run(
		open(args.file).read(), args.input, args.print_all, args.print_how,
		print_exp = args.print_exp
	)

if __name__ == '__main__':
	ffi()
