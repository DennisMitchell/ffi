from collections import defaultdict

prime_cache = \
	[  2,   3,   5,   7,  11,  13,  17,  19,  23,  29,  31,  37,  41,  43,  47,  53,
	  59,  61,  67,  71,  73,  79,  83,  89,  97, 101, 103, 107, 109, 113, 127, 131,
	 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
	 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311]

last_prime = 821641 # 65536th prime number
sieve = []
sieve_max = int(last_prime ** 0.5)

def factors(integer):
	the_factors = defaultdict(int)

	for prime in primes():
		if integer <= 1: break

		while integer % prime == 0:
			the_factors[prime] += 1
			integer //= prime

	if integer > 1:
		raise SystemExit('Error: %s is not %u-smooth.' % (integer, last_prime))

	return the_factors

def primes():
	for number in prime_cache:
		yield number

	if not sieve:
		sieve[:] = (last_prime + 1) // 2 * [False, True]

	for number in range(prime_cache[-1] + 1, last_prime + 1):
		if sieve[number]:
			if number <= sieve_max:
				sieve[::number] = [False] * len(sieve[::number])

			prime_cache.append(number)
			yield number
