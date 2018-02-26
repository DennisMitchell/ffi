from ctypes import cdll
from parser import parse_code, parse_integer
from subprocess import call
from tempfile import NamedTemporaryFile

def gen_print_state(primes, file, indentation):
	file.write('\t' * indentation)
	file.write('printf("%s\\n"' % ' * '.join('%s^%%" PRIu64 "' % prime for prime in primes))

	for prime in primes:
		file.write(', s%u' % prime)

	file.write(');\n')

def run(code, input, print_all):
	fractions = list(parse_code(code))
	input = parse_integer(input)
	primes= sorted(set.union(*map(set, fractions)) | set(input))
	numargs = len(primes)

	c_file = NamedTemporaryFile(mode = 'w+', suffix = '.c')
	c_file.write('#include <%s.h>\n' * 4 % ('inttypes', 'signal', 'stdlib', 'stdio') + '\n')
	c_file.write('void quit(int signal)\n{\n')
	c_file.write('\tfputs("\\nKeyboardInterrupt\\n", stderr);\n\texit(130);\n}\n\n')
	c_file.write('void run()\n{\n\tsignal(SIGINT, quit);')

	for prime in primes:
		c_file.write('\tuint64_t s%u = %u;\n' % (prime, input[prime]))

	c_file.write('\n\twhile (1)\n\t{\n')

	if print_all:
		gen_print_state(primes, c_file, 2)

	for fraction in fractions:
		conditions = (
			's%u >= %u' % (prime, -exponent)
			for prime, exponent in fraction.items()
			if exponent < 0
		)

		c_file.write('\t\tif (%s)\n\t\t{\n' % (' && '.join(conditions) or 1))

		for prime, exponent in fraction.items():
			if exponent:
				c_file.write('\t\t\ts%u += %d;\n' % (prime, exponent))

		c_file.write('\t\t\tcontinue;\n\t\t}\n\n')

	c_file.write('\t\tbreak;\n\t}\n\n')

	if not print_all:
		gen_print_state(primes, c_file, 1)

	c_file.write('}\n')
	c_file.flush()
	so_file = NamedTemporaryFile(mode = 'rb', suffix = '.so')
	call(['cc', '-O2', '-shared', '-fPIC', '-o', so_file.name, c_file.name])
	c_file.close()
	program = cdll.LoadLibrary(so_file.name)
	so_file.close()
	program.run()