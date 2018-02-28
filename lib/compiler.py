from os import chdir
from shutil import rmtree
from subprocess import call
from sys import stderr
from tempfile import mkdtemp
from .generate import generate
from .parser import parse_code, parse_integer

def run(code, input, print_when, print_what, **kwargs):
	fractions = list(parse_code(code))
	input = parse_integer(input)
	primes= sorted(set.union(*map(set, fractions)) | set(input))
	numargs = len(primes)
	use_gmp = print_what == 'print_numeric'

	c_code = []
	c_code.append('#include <gmp.h>\n' * use_gmp)
	c_code.append('#include <stdio.h>\n')
	c_code.append('\nint main()\n{\n')

	for prime in primes:
		c_code.append('\tunsigned long s%u = %u;\n' % (prime, input[prime]))

	c_code.append('\tunsigned long one, quot;\n\n')
	c_code.append('\tmpz_t pow, out;\n\tmpz_init(pow);\n\tmpz_init(out);\n\n' * use_gmp)
	c_code.append('\twhile (1)\n\t{\n')

	if print_when == 'print_all':
		generate(print_what, primes, c_code.append, 2, **kwargs)
		c_code.append('\t\tfflush(stdout);\n\n')

	if print_when == 'print_pow':
		generate(print_when, primes, c_code.append, 2, **kwargs)
		c_code.append('\t\t{\n')
		generate(print_what, primes, c_code.append, 3, **kwargs)
		c_code.append('\t\t\tfflush(stdout);\n\t\t}\n\n')

	for fraction in fractions:
		conditions = (
			's%u >= %u' % (prime, -exponent)
			for prime, exponent in fraction.items()
			if exponent < 0
		)

		c_code.append('\t\tif\n\t\t(\n\t\t\t')
		c_code.append('\n\t\t&&\n\t\t\t'.join(conditions) or '1')
		c_code.append('\n\t\t)\n\t\t{\n')

		for prime, exponent in fraction.items():
			c_code.append('\t\t\ts%u += %d;\n' % (prime, exponent))

		c_code.append('\t\t\tcontinue;\n\t\t}\n\n')

	c_code.append('\t\tbreak;\n\t}\n\n')

	if print_when == 'print_final':
		generate(print_what, primes, c_code.append, 1, **kwargs)

	c_code.append('\treturn 0;\n}\n')
	tempdir = mkdtemp()
	chdir(tempdir)
	src = open('program.c', mode = 'w')
	src.write(''.join(c_code))
	src.close()

	try:
		assert not call(['cc', '-O2', '-oprogram', 'program.c'] + ['-lgmp'] * use_gmp)
		call(['./program'])
	except AssertionError:
		exit(1)
	except KeyboardInterrupt:
		stderr.write('\n')
		exit(130)
	finally:
		rmtree(tempdir)
