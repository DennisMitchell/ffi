from os import remove
from subprocess import call
from sys import stderr
from tempfile import NamedTemporaryFile
from .generate import generate
from .parser import parse_code, parse_integer

def run(code, input, print_when, print_what, **kwargs):
	fractions = list(parse_code(code))
	input = parse_integer(input)
	primes= sorted(set.union(*map(set, fractions)) | set(input))
	numargs = len(primes)

	c_code = []
	c_code.append('#include <%s.h>\n' * 2 % ('inttypes', 'stdio'))
	c_code.append('\nint main()\n{\n')

	for prime in primes:
		c_code.append('\tuint64_t s%u = %u;\n' % (prime, input[prime]))

	c_code.append('\n\tuint64_t one, quot;\n\n')
	c_code.append('\twhile (!ferror(stdout))\n\t{\n')

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
	c_file = NamedTemporaryFile(mode = 'w+', suffix = '.c', delete = False)
	c_file.write(''.join(c_code))
	c_file.close()
	bin_file = NamedTemporaryFile(mode = 'rb', delete = False, suffix = '.exe')
	bin_file.close()

	if call([
		'cc', '-Wall', '-Wextra', '-Wno-unused-variable', '-Werror',
		'-O2', '-o', bin_file.name, c_file.name
	]):
		remove(c_file.name)
		exit(1)

	remove(c_file.name)

	try:
		call([bin_file.name])
		remove(bin_file.name)
	except KeyboardInterrupt:
		stderr.write('\n')
		remove(bin_file.name)
		exit(130)
