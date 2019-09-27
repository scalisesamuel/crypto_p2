#!/usr/bin/python

# goodPRNG.py

from header import *
import random

prime_count = 0.0		# Holds the count of coprime pairs generated
pairs_generated_count = 1	# Holds the count of number pairs generated

# Loop to calculate pairs of random integers. Checks if the pairs are coprimes based on the gcd func. 
# Calculates the estimate of PI based on the probability that a coprime pair was generated.
for index in range(1,1000000):
	x = random.SystemRandom().randint(1,1000000)
	y = random.SystemRandom().randint(1,1000000)
	z = gcd(x,y)

	if z == 1:
		prime_count += 1
	
	pairs_generated_count += 1

probability = prime_count / 1000000
estimation = piEstimator(probability)

print ("Pairs of random numbers generated:", pairs_generated_count)
print ("Coprimes found:", prime_count)
print ("Chance of coprime:", probability)
print ("Estimation of PI:", estimation)
