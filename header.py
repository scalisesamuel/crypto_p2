# Header file used for badPRNG and goodPRNG files

import math

# Function to calculate the greatest common divisor


def gcd( a, b):
	if(b == 0):
		return a
	else:
		return gcd( b, a % b )


# Function to estimate PI based on the idea that given two random integers
#  x and y, the probability that the gcd(x,y) = 1 is 6/(PI ** 2).
def piEstimator ( prob ):
	return math.sqrt ( 6 / prob )

