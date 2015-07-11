import random
import string

def random_num_string(length):
	return ''.join(random.choice(string.digits) for _ in range(length))