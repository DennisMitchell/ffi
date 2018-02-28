from .ntheory import factors

def generate(name, *args, **kwargs):
	try:
		globals()['gen_%s' % name](*args, **kwargs)
	except KeyError:
		raise SystemExit('Error: %r is not a valid output method.' % name)

def gen_print_compact(primes, emit, indent, **kwargs):
	tabs = '\t' * indent
	emit(tabs + 'one = 1;\n')

	for prime in primes:
		emit('%sif (s%u == 1) one = ' % (tabs, prime))
		emit('!printf("%%s%u", one ? "" : " * ");\n' %  prime)
		emit('%selse if (s%u) one = ' % (tabs, prime))
		emit('!printf("%%s%u^%%lu", one ? "" : " * ", s%u);\n' % (prime, prime))

	emit(tabs + 'printf("%s\\n", one ? "1" : "");\n')

def gen_print_exp(primes, emit, indent, **kwargs):
	try:
		exps = kwargs['print_exp']
		exps = list(map(int, exps.rstrip(',').split(',')))
		assert all(exp > 1 for exp in exps)
	except:
		raise SystemExit(
			'Error: Cannot parse %r as a comma-separated list of integers larger than 1.'
			 % kwargs['print_exp']
		)

	tabs = '\t' * indent
	sep = ''

	for exp in exps:
		set_quot = tabs + 'quot = %s;\n'
		emit(set_quot % '~0UL')
		exp_factors = factors(exp)

		for prime, exponent in exp_factors.items():
			if prime not in primes:
				emit(set_quot % '0UL')
			else:
				emit(
					set_quot % 's%u / %u < quot ? s%u / %u : quot'
					% (prime, exponent, prime, exponent)
				)

		emit('%sprintf("%s%%lu", quot);\n' % (tabs, sep))
		sep = ' '

	emit(tabs + 'printf("\\n");\n')

def gen_print_numeric(primes, emit, indent, **kwargs):
	tabs = '\t' * indent
	emit(tabs + 'mpz_set_ui(out, 1);\n')

	for prime in primes:
		emit(tabs + 'mpz_ui_pow_ui(pow, %uUL, s%u);\n' % (prime, prime))
		emit(tabs + 'mpz_mul(out, out, pow);\n')

	emit(tabs + 'gmp_printf("%Zu\\n", out);\n')

def gen_print_pow(primes, emit, indent, **kwargs):
	try:
		base = kwargs['print_pow']
		base = int(base)
		assert base > 0
		base = factors(base)
	except:
		raise SystemExit(
			'Error: Cannot parse %r as a positive integer.' % kwargs['print_pow']
		)

	tabs = '\t' * indent

	if not base:
		emit(tabs + 'if(1)\n')
		return

	for prime in base:
		if prime not in primes:
			emit(tabs + 'if(0)\n')
			return

	emit(tabs + 'quot = s%u / %u;\n\n' % next(iter(base.items())))
	emit('%sif\n%s(\n%s\t' % (tabs, tabs, tabs))
	and_ = '\n%s&&\n%s\t' % (tabs, tabs)
	emit(and_.join('%u * quot == s%u' % (base[prime], prime) for prime in primes))
	emit('\n%s)\n' % tabs)

def gen_print_whole(primes, emit, indent, **kwargs):
	emit('\t' * indent)
	emit('printf("%s\\n"' % ' * '.join('%u^%%lu"' % prime for prime in primes))

	for prime in primes:
		emit(', s%u' % prime)

	emit(');\n')
