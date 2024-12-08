# import math library
import math

# defining rounding upwards

def round_up(number, decimals = 0):
	multiplier = 10 ** decimals
	return math.floor(number * multiplier + 0.5) / multiplier