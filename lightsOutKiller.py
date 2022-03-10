#%%
import numpy as np
import re
from itertools import product
from typing import List, Tuple

Coord = Tuple[int, int]

class LightsOutKiller():
	def __init__(self, size: int):
		"""
		Suitable for Square Boards Only
		int 		self.__size	: size of the board
		np.ndarray 	self.__board: 2-d array representing the board
		"""
		self.__size = 5
		self.__board = np.zeros((size,size))
		self.__coords = set()
	
	def get_light(self):
		"""
		Get the positions of initial lights from input
		"""
		_coords = set()
		goOn = True
		while goOn:
			copy = True
			userInput = input("Please type in positions for initial lights, e.g. (x, y): ").split(' ')
			for usipt in userInput:
				if usipt == '': continue
				if re.match('\s*\d+,\d+', usipt):
					# input is valid
					coord = tuple(map(int,usipt.strip().strip(')').strip('(').split(',')))
					if (coord[0] <= self.__size) and (coord[1] <= self.__size):
						_coords.add(coord)
					else:
						print('Input location exceeds the board...')
						copy = False
						break
				else:
					print("Invalid input...")
					copy = False
					break
			if copy: 
				self.__coords = _coords
			# check user input valification
			valid = False
			while valid == False:
				checkGoOn = input("Is there anymore lights on?(Y/N)")
				if checkGoOn in ['Y', 'y']:
					goOn = True
					valid = True
				elif checkGoOn in ['N', 'n']:
					goOn = False
					valid = True
				else: 
					print("Come on! it's not even an option...")
					continue# invalid terminator
		print(f'The final layout initialization is: {self.__coords}')
		return

	
	def set_light(self)->None:
		""" 
		Set the initial lights layout of a board game
		param1 coords: coordinates of initial lights, in form of (x, y), original point(1,1) located at left-up corner
		"""
		for coord in self.__coords:
			x, y = coord[0], coord[1]
			self.__board[x-1, y-1] = 1
		return

	# board[3,1] = 1
	def get_solution(self):
		size = self.__size
		ps = product(range(2), repeat=size)
		result = []
		for p in ps:
			B = self.__board.copy()
			for j in range(size):
				if j == 0:
					upper = p
				else:
					upper = list((B[j-1,:]==1).astype(int))
					B[j-1,:] = 0
				for i, e in enumerate(upper):
					if e:
						mask = np.ones(size)
						mask2 = np.ones(size)
						ones = np.ones(size)
						# middle
						if i in range(1,size-1):
							mask[[i-1, i, i+1]] = 0
							# B[j,[i-1, i, i+1]] ^= np.ones((1,3))
						elif i == 0:
							mask[[i,i+1]] = 0
							# B[j,[i,i+1]] ^= np.ones((1,2))
							# B[j,i] = B[j,i] ^ 1
							# B[j,i+1] = B[j,i+1] ^ 1
						elif i == size-1:
							mask[[i-1,i]] = 0 
						B[j,:] = np.logical_xor(np.logical_xor(mask,  B[j,:]), ones).astype(int)
						#TODO: Fix this bitwise operation
						if j < size - 1:
							# B[j + 1, i] ^= np.ones((1,1))
							mask2[i] = 0
							B[j + 1, :] = np.logical_xor(np.logical_xor(B[j + 1, :], mask2), ones).astype(int)
			if np.sum(B) == 0:
				result.append(p)
		return result



# %%
# def get_
if __name__ == '__main__':
	lok = LightsOutKiller(5)	
	lok.get_light()
	lok.set_light()
	result = lok.get_solution()

	print(result)

# %%
