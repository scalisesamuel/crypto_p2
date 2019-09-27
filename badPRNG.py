#!/usr/bin/python

# badPRNG.py

from header import *
import random

prime_count = 0.0	# Holds the count of coprime pairs generated
pair_count = 1		# Holds the count of number pairs generated

# Settings for LCG
x_0 = 1
a = 13
c = 0
m = 31

# Function to serve as the Linear Congruential Generator using the above settings
def lcg(a_val, x_val, c_val, m_val):
	x_n = ( a_val * x_val + c_val ) % m_val
	return x_n

# Loop to calculate pairs of random integers. Checks if pairs are coprimes based on the gcd func.
# Calculates the estimate of PI based on teh probability that a coprime pair was generated.
for index in range(1, 1000):
	x = x_0 = lcg ( a, x_0, c, m )
	y = x_0 = lcg ( a, x_0, c, m )
	z = gcd(x,y)

	if z == 1:
		prime_count += 1
	
	pair_count += 1

probability = prime_count / 1000
estimation = piEstimator(probability)

print ("Pairs of random numbers generated:", pair_count)
print ("Coprimes found:", prime_count)
print ("Chance of coprime:", probability)
print ("Estimation of PI:", estimation)
