from sys import stderr

def generate(name, *args, **kwargs):
	try:
		globals()['gen_%s' % name](*args, **kwargs)
	except KeyError:
		stderr.write('Error: %r is not a valid output method.\n' % name)
		exit(1)

def gen_print_compact(primes, file, indent, **kwargs):
	indent = '\t' * indent
	file.write(indent + 'int one = 1;\n')

	for prime in primes:
		file.write('%sif (s%u == 1) one = ' % (indent, prime))
		file.write('!printf("%%s%u", one ? "" : " * ");\n' %  prime)
		file.write('%selse if (s%u) one = ' % (indent, prime))
		file.write('!printf("%%s%u^%%" PRIu64, one ? "" : " * ", s%u);\n' % (prime, prime))

	file.write(indent + 'printf("%s\\n", one ? "1" : "");\n')

def gen_print_exp(primes, file, indent, **kwargs):
	exps_of = kwargs['print_exp']

	try:
		exps_of = list(map(int, exps_of.rstrip(',').split(',')))
	except:
		stderr.write(
			'Error: Cannot parse %r as a comma-separated list of primes.\n' % exps_of
		)

		exit(1)

	file.write('\t' * indent)
	file.write('printf("%s\\n"' % ' '.join('%" PRIu64 "' for prime in exps_of))

	for prime in exps_of:
		if prime not in primes:
			stderr.write(
				'Error: %u is not a prime or does not occur in the program.\n' % prime
			)

			exit(1)

		file.write(', s%u' % prime)

	file.write(');\n')

def gen_print_state(primes, file, indent, **kwargs):
	file.write('\t' * indent)
	file.write('printf("%s\\n"' % ' * '.join('%s^%%" PRIu64 "' % prime for prime in primes))

	for prime in primes:
		file.write(', s%u' % prime)

	file.write(');\n')
