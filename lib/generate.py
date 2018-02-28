from sys import stderr
from .ntheory import factors

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
		exps = kwargs['print_exp']
		exps = list(map(int, exps.rstrip(',').split(',')))
		assert all(exp > 1 for exp in exps)
	except:
		stderr.write(
			'Error: Cannot parse %r as a comma-separated list of integers larger than 1.\n'
			 % kwargs['print_exp']
		)

		exit(1)

	tabs = '\t' * indent
	sep = ''

	for exp in exps:
		set_quot = tabs + 'quot = %s;\n'
		file.write(set_quot % 'UINT64_MAX')
		exp_factors = factors(exp)

		for prime, exponent in exp_factors.items():
			if prime not in primes:
				file.write(set_quot % '__UINT64_C(0)')
			else:
				file.write(
					set_quot % 's%u / %u < quot ? s%u / %u : quot'
					% (prime, exponent, prime, exponent)
				)

		file.write('%sprintf("%s%%" PRIu64, quot);\n' % (tabs, sep))
		sep = ' '

	file.write(tabs + 'printf("\\n");\n')

def gen_print_pow(primes, file, indent, **kwargs):
	try:
		base = kwargs['print_pow']
		base = int(base)
		assert base > 0
		base = factors(base)
	except:
		stderr.write('Error: Cannot parse %r as a positive integer.\n' % kwargs['print_pow'])
		exit(1)

	tabs = '\t' * indent

	if not base:
		file.write(tabs + 'if(1)\n')
		return

	for prime in base:
		if prime not in primes:
			file.write(tabs + 'if(0)\n')
			return

	file.write(tabs + 'quot = s%u / %u;\n\n' % next(iter(base.items())))
	file.write('%sif\n%s(\n%s\t' % (tabs, tabs, tabs))
	and_ = '\n%s&&\n%s\t' % (tabs, tabs)
	file.write(and_.join('%u * quot == s%u' % (base[prime], prime) for prime in primes))
	file.write('\n%s)\n' % tabs)

def gen_print_whole(primes, file, indent, **kwargs):
	file.write('\t' * indent)
	file.write('printf("%s\\n"' % ' * '.join('%u^%%" PRIu64 "' % prime for prime in primes))

	for prime in primes:
		file.write(', s%u' % prime)

	file.write(');\n')
