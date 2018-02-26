from sys import stderr

def generate(name, *args):
	try:
		globals()['gen_%s' % name](*args)
	except KeyError:
		stderr.write('"%s" is not a valid output method.' % name)

def gen_print_compact(primes, file, indent):
	indent = '\t' * indent
	file.write(indent + 'int one = 1;\n')

	for prime in primes:
		file.write('%sif (s%u == 1) one = ' % (indent, prime))
		file.write('!printf("%%s%u", one ? "" : " * ");\n' %  prime)
		file.write('%selse if (s%u) one = ' % (indent, prime))
		file.write('!printf("%%s%u^%%" PRIu64, one ? "" : " * ", s%u);\n' % (prime, prime))

	file.write(indent + 'printf("%s\\n", one ? "1" : "");\n')

def gen_print_state(primes, file, indentation):
	file.write('\t' * indentation)
	file.write('printf("%s\\n"' % ' * '.join('%s^%%" PRIu64 "' % prime for prime in primes))

	for prime in primes:
		file.write(', s%u' % prime)

	file.write(');\n')
