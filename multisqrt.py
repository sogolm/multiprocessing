import math
from multiprocessing import Pool


# Take square root of numbers within a list using a pool of 4 processes
def pool_sqrt(lst):
	pool = Pool(processes=4)
	sqrt_lst = pool.map(math.sqrt, lst)
	return sqrt_lst

if __name__ == '__main__':
	lst = [4, 9, 16, 25]
	sqrt_lst = pool_sqrt(lst)
	print sqrt_lst
	print sum(sqrt_lst)

