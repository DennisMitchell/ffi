from argparse import ArgumentParser
from lib.compiler import run

def ffi(*args):
	argparser = ArgumentParser(description = 'Frabjous FRACTRAN Interpreter', prog = 'ffi')

	try:
		argparser._actions[0].help = 'Show this help message and exit.'
	except:
		pass

	argparser.add_argument(
		'file', metavar = 'FILE',
		help = 'Read source code from FILE.'
	)

	argparser.add_argument(
		'input', metavar = 'INPUT', nargs='?', default = '2',
		help = 'Pass INPUT to the program. (defaults to 2)'
	)

	print_when = argparser.add_argument_group('when to print')
	print_when = print_when.add_mutually_exclusive_group()

	print_when.add_argument(
		'-f', '--final', dest = 'print_when', default = 'print_final',
		action = 'store_const', const = 'print_final',
		help = 'Print only the final state. (default)'
	)

	print_when.add_argument(
		'-a', '--all', dest = 'print_when',
		action = 'store_const', const = 'print_all',
		help = 'Print all intermediate states.'
	)

	print_when.add_argument(
		'-p', '--pow', dest = 'print_pow', metavar = 'BASE',
		help = 'Print only states that are perfect powers of BASE.'
	)

	print_what = argparser.add_argument_group('what to print')
	print_what = print_what.add_mutually_exclusive_group()

	print_what.add_argument(
		'-c', '--compact', dest = 'print_what', default = 'print_compact',
		action = 'store_const', const = 'print_compact',
		help = 'Print a compact representation of the state. (default)'
	)

	print_what.add_argument(
		'-w', '--whole', dest = 'print_what',
		action = 'store_const', const = 'print_whole',
		help = 'Print the whole state, including 0 and 1 exponents.'
	)

	print_what.add_argument(
		'-n', '--numeric', dest = 'print_what',
		action = 'store_const', const = 'print_numeric',
		help = 'Print the state as a numeric literal. (requires GMP)'
	)

	print_what.add_argument(
		'-e', '--exp', dest = 'print_exp', metavar = 'LIST',
		help = 'For each integer in LIST (comma-separated), print its exponent '
			'in the state.'
	)

	args = argparser.parse_args(list(args) or None)
	if args.print_pow: args.print_when = 'print_pow'
	if args.print_exp: args.print_what = 'print_exp'

	run(
		open(args.file).read(), args.input, args.print_when, args.print_what,
		print_pow = args.print_pow,
		print_exp = args.print_exp,
	)

if __name__ == '__main__':
	ffi()
