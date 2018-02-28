from collections import defaultdict
from re import compile, finditer, match, sub
from sys import stderr
from .ntheory import factors

_str_power = r'(?:[1-9][0-9]*(?: *\^ *[1-9][0-9]*)?)'
_str_product = r'(?:(?:%s *\* *)*%s)' % (_str_power, _str_power)
_str_integer = r'(%s|%s)' % (_str_product, _str_power)
_str_term = r'(\(%s\)|%s)' % (_str_product, _str_power)
_str_fraction = r'(?:%s */ *%s)' % (_str_term, _str_term)
_str_ws = r'[\t\n ]'
_str_sep = r'(?:%s*[,.;]%s*|%s+)' % (_str_ws, _str_ws, _str_ws)
_str_code = r'(?:%s*(?:%s%s)*%s?)' % (_str_ws, _str_fraction, _str_sep, _str_fraction)
_str_comment = r'(?:#[^\n]*)'
_re_code = compile(_str_code)
_re_comment = compile(_str_comment)
_re_fraction = compile(_str_fraction)
_re_integer = compile(_str_integer)

def match_or_error(regex, string, error_name, print_caret):
	the_match = match(regex, string)
	parsed = 0 if the_match == None else the_match.span()[1]

	if parsed < len(string):
		print_from = max(parsed - 20, 0)
		stderr.write('Error: Unable to parse as a positive %s:\n\n' % error_name)
		stderr.write(string[print_from:][:80].split('\n')[0] + '\n')
		if print_caret: stderr.write('~' * (parsed - print_from) + '^\n')
		exit(1)

def parse_code(code):
	code = sub(_re_comment, '', code).strip('\t\n ')
	match_or_error(_re_code, code, 'fraction', True)

	for fraction_match in finditer(_re_fraction, code):
		the_factors = defaultdict(int)
		numerator, denominator = fraction_match.groups()

		for prime, exponent in parse_integer(numerator.strip('()')).items():
			the_factors[prime] += exponent

		for prime, exponent in parse_integer(denominator.strip('()')).items():
			the_factors[prime] -= exponent
			if the_factors[prime] == 0: del the_factors[prime]

		yield dict(the_factors)

def parse_integer(integer):
	match_or_error(_re_integer, integer, 'integer', False)
	the_factors = defaultdict(int)

	for power in integer.split('*'):
		power = power.split('^') + ['1']
		base = int(power[0])
		outer_exponent = int(power[1])

		for prime, inner_exponent in factors(base).items():
			the_factors[prime] += inner_exponent * outer_exponent

	return the_factors
