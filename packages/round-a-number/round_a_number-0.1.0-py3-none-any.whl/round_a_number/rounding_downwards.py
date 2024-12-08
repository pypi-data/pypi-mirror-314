# import math library
import math

# defining rounding downwards 

def round_down(number, decimals = 0):
	multiplier = 10 ** decimals
	return math.ceil(number * multiplier - 0.5) / multiplier
