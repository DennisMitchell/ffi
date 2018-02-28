from collections import defaultdict

last_prime = 821641 # 65536th prime number
prime_cache = [2]
sieve = (last_prime + 1) // 2 * [False, True]
sieve_max = int(last_prime ** 0.5)

def factors(integer):
	the_factors = defaultdict(int)

	for prime in primes():
		if integer <= 1: break

		while integer % prime == 0:
			the_factors[prime] += 1
			integer //= prime

	if integer > 1:
		raise SystemExit('Error: %s is not %u-smooth.\n' % (integer, last_prime))

	return the_factors

def primes():
	for number in prime_cache:
		yield number

	start = prime_cache[-1] + 1

	for number in range(start, last_prime + 1):
		if sieve[number]:
			if number <= sieve_max:
				sieve[::number] = [False] * len(sieve[::number])

			prime_cache.append(number)
			yield number
