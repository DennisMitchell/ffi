from ntheory import factors
from sys import stderr

def generate(name, *args, **kwargs):
	try:
		globals()['gen_%s' % name](*args, **kwargs)
	except KeyError:
		stderr.write('Error: %r is not a valid output method.\n' % name)
		exit(1)

def gen_print_compact(primes, file, indent, **kwargs):
	tabs = '\t' * indent
	file.write(tabs + 'one = 1;\n')

	for prime in primes:
		file.write('%sif (s%u == 1) one = ' % (tabs, prime))
		file.write('!printf("%%s%u", one ? "" : " * ");\n' %  prime)
		file.write('%selse if (s%u) one = ' % (tabs, prime))
		file.write('!printf("%%s%u^%%" PRIu64, one ? "" : " * ", s%u);\n' % (prime, prime))

	file.write(tabs + 'printf("%s\\n", one ? "1" : "");\n')

def gen_print_exp(primes, file, indent, **kwargs):
	try:
		exps_of = kwargs['print_exp']
		exps_of = list(map(int, exps_of.rstrip(',').split(',')))
	except:
		stderr.write(
			'Error: Cannot parse %r as a comma-separated list of integers.\n' % exps_of
		)

		exit(1)

	file.write('\t' * indent)
	file.write('printf("%s\\n"' % ' '.join('%" PRIu64 "' for prime in exps_of))

	for prime in exps_of:
		file.write(', s%u' % prime if prime in primes else ', (uint64_t) 0')

	file.write(');\n')

def gen_print_pow(primes, file, indent, **kwargs):
	try:
		base = kwargs['print_pow']
		base = int(base)
		assert base > 0
		base = factors(base)
	except:
		stderr.write('Error: Cannot parse %r as a positive integer.\n' % base)
		exit(1)

	tabs = '\t' * indent

	if not base:
		file.write(tabs + 'if(1)\n')
		return

	for prime in base:
		if prime not in primes:
			file.write(tabs + 'if(0)\n')
			return

	file.write(tabs + 'quot = s%u / %u;' % next(iter(base.items())))
	file.write(tabs + 'if(%s)\n' % ' && '.join(
		's%u %% %u == 0 && s%u / %u == quot' % (prime, base[prime], prime, base[prime])
		if prime in base
		else 's%u == 0' % prime
		for prime in primes
	))

def gen_print_whole(primes, file, indent, **kwargs):
	file.write('\t' * indent)
	file.write('printf("%s\\n"' % ' * '.join('%u^%%" PRIu64 "' % prime for prime in primes))

	for prime in primes:
		file.write(', s%u' % prime)

	file.write(');\n')
