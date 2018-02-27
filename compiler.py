from ctypes import cdll
from generate import generate
from parser import parse_code, parse_integer
from subprocess import call
from tempfile import NamedTemporaryFile

def print_when_state(primes, file, indentation):
	file.write('\t' * indentation)
	file.write('printf("%s\\n"' % ' * '.join('%s^%%" PRIu64 "' % prime for prime in primes))

	for prime in primes:
		file.write(', s%u' % prime)

	file.write(');\n')

def run(code, input, print_when, print_what, **kwargs):
	fractions = list(parse_code(code))
	input = parse_integer(input)
	primes= sorted(set.union(*map(set, fractions)) | set(input))
	numargs = len(primes)

	c_file = NamedTemporaryFile(mode = 'w+', suffix = '.c')
	c_file.write('#include <%s.h>\n' * 4 % ('inttypes', 'signal', 'stdlib', 'stdio') + '\n')
	c_file.write('void quit(int signal)\n{\n')
	c_file.write('\tif (signal == 2) fputs("\\n", stderr);\n\texit(128 | signal);')
	c_file.write('\n}\n\nvoid run()\n{\n')

	for prime in primes:
		c_file.write('\tuint64_t s%u = %u;\n' % (prime, input[prime]))

	c_file.write('\n\tuint64_t one, quot;\n\n')
	c_file.write('\tsignal(SIGINT, quit);\n')
	c_file.write('\tsignal(SIGPIPE, quit);\n')
	c_file.write('\n\twhile (1)\n\t{\n')

	if print_when == 'print_all':
		generate(print_what, primes, c_file, 2, **kwargs)

	if print_when == 'print_pow':
		generate(print_when, primes, c_file, 2, **kwargs)
		c_file.write('\t\t{\n')
		generate(print_what, primes, c_file, 3, **kwargs)
		c_file.write('\t\t}\n\n')

	c_file.write('\t\tfflush(stdout);\n\n')

	for fraction in fractions:
		conditions = (
			's%u >= %u' % (prime, -exponent)
			for prime, exponent in fraction.items()
			if exponent < 0
		)

		c_file.write('\t\tif (%s)\n\t\t{\n' % (' && '.join(conditions) or '1'))

		for prime, exponent in fraction.items():
			c_file.write('\t\t\ts%u += %d;\n' % (prime, exponent))

		c_file.write('\t\t\tcontinue;\n\t\t}\n\n')

	c_file.write('\t\tbreak;\n\t}\n\n')

	if print_when == 'print_final':
		generate(print_what, primes, c_file, 1, **kwargs)

	c_file.write('}\n')
	c_file.flush()
	so_file = NamedTemporaryFile(mode = 'rb', suffix = '.so')

	if call([
		'cc', '-ansi', '-pedantic', '-Wall', '-Wextra', '-Wno-unused-variable', '-Werror',
		 '-O2', '-shared', '-fPIC',	'-o', so_file.name, c_file.name
	]):
		exit(1)

	c_file.close()
	program = cdll.LoadLibrary(so_file.name)
	so_file.close()
	program.run()
