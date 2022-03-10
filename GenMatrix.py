#%%
import numpy as np
from typing import Tuple, List, Union
from itertools import product
from numba import jit

Coord = Tuple[int, int]
Matrix = np.matrix

class DataGenerator():
	def __init__(self, size:int):
		""" 
		param1: int size: an integer to determine the size of the board
		"""
		self.__size = size

	def get_b(self, coords: List[Coord])->np.ndarray:
		"""  
		param 1: coords: the layout of initial state of lights
		return: a 1-dim array representing b vector
		"""
		b = np.zeros(self.__size**2)
		for coord in coords:
			x, y = coord[0], coord[1]
			index = self.__size*(x - 1) + y
			b[index - 1] = 1
		return b.reshape(-1,1)


	def get_A(self)->Matrix:
		""" 
		return: matrix A
		"""
	# size2 = SIZE**2 # size of the matrix
		A = []
		size = self.__size
		for x in range(size): 
			for y in range(size):# iteration of board girds
				for xx in range(size):
					for yy in range(size): # iteration of prefix
						middle = (xx+1, yy+1)
						left = (middle[0], middle[1]-1)
						right = (middle[0], middle[1]+1)
						top = (middle[0]-1, middle[1])
						bottom = (middle[0]+1, middle[1]) # 5 affected areas
						if (x + 1, y + 1) in [middle, left, right, top, bottom]:
							A.append(1)
						else:
							A.append(0)
		A = np.array(A).reshape(size**2, -1)
		return A
#%%
class Solver():
	def __gcd(self, a: int, b: int)->int:
		""" 
		Solve the greatest common divisior, called in a recursive way. 
		"""
		return self.__gcd(b, a % b) if a % b else b
	
	def __lcm(self, a: int, b: int)->int:
		""" 
		Solve the least common multiplier 
		"""
		return int(a / self.__gcd(a, b) * b)
	
	def gauss_xor(self, Ab: Matrix)->Union[int, Tuple[np.ndarray, np.ndarray]]:
		""" 
		Solve augmented matrix with Guassian Elimination method, but 
		use xor(logic) arithmetic instead of numeral arithmetic to coupe with
		"Lights Out" Puzzle
		"""
		# store the shape of the matrix
		r, c = Ab.shape
		for i, j in zip(range(r), range(c)):
			# first row holding element 1
			rOne = i
			# if initial one is not rOne, swap the first one row with the initial one
			if Ab[rOne, j] != 1:
				for ii in range(rOne + 1, r):
					if Ab[ii, j] == 1:
						Ab[[ii,rOne],:] = Ab[[rOne, ii],:]
						break
			# else if the whole column are 0, go to next column
			elif (Ab[:, j] == 0).all():
				continue
			
			# then do elimination
			for ii in range(rOne + 1, r):
				if Ab[ii, j] == 1:
				# elementwise xor for the whole row
					Ab[ii, :] = np.bitwise_xor(Ab[ii, :],Ab[rOne, :])
			
		return Ab[:,:c], Ab[:,-1]

	# @jit(nopython=True)		
	# def solve_brutal(self, A: np.ndarray, b: np.ndarray)->Union[None, List[np.ndarray]]:
	# 	""" 
	# 	Solve the equations in brutal force way
	# 	param1 ndarray A: coefficient matrix
	# 	param2 ndarray b: constance vector
	# 	return: a matrix holding corresponding actions
	# 	"""
	# 	# all possible combinations of actions
	# 	size = A.shape[1]
	# 	actions = []
	# 	ps = product(range(2), repeat=size)
	# 	for p in ps:
	# 		p = np.array(p)
	# 		p = p.astype(int)
	# 		# flag notating a feasible solution
	# 		match = 1
	# 		for i in range(size):
	# 			if np.sum(p^A[i,:]) != b[i]: 
	# 				match = 0
	# 				break
	# 		if match: 
	# 			actions.append(p)
		
	# 	if len(actions) == 0: 
	# 		# print("No feasible solution!!!")
	# 		return 
	# 	# print(f'There are {len(actions):2d} solutions altogether.')
	# 	return actions
			
# @jit(nopython=True)		
	def solve_brutal(self, A: np.ndarray, b: np.ndarray)->Union[None, List[np.ndarray]]:
		""" 
		Solve the equations in brutal force way
		param1 ndarray A: coefficient matrix
		param2 ndarray b: constance vector
		return: a matrix holding corresponding actions
		"""
		# all possible combinations of actions
		size = A.shape[1]
		actions = []
		ps = product(range(2), repeat=size)
		for p in ps:
			p = np.array(p)
			p = p.astype(int)
			# flag notating a feasible solution
			match = 1
			for i in range(size):
				if np.sum(p*A[i,:])%2 != b[i]: 
					match = 0

			if match: 
				actions.append(p)
		# print(f'There are {len(actions):2d} solutions altogether.')
		return actions
#%%

if __name__ == '__main__':
	g = DataGenerator(5)
	A = g.get_A()
	b = g.get_b([(2,2)])
	# Ab = np.hstack((A,b)).astype(int)
	# print(f'Ab : \n{Ab}\n shape:{Ab.shape}')

	s = Solver()
	# tri = s.gauss_xor(Ab)
	# actions = s.solve_brutal(A,b)
	s.solve_brutal(A,b)
	pass
	# print(f'triangular matrix of Ab: {Ab}')

			