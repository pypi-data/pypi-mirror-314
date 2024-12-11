from .mainClass import Distance
from .vectorDistance  import Euclidean
#from .tools     import *

class DynamicTimeWarping(Distance):
	def __init__(self)-> None:
		"""
		Compute the Dynamic Time Warping (DTW) distance between two time series.
    
		DTW is a measure of similarity between two temporal sequences that may vary in speed.
		This class allows the computation of the DTW distance and the optimal alignment path between the sequences.
    
		Attributes:
		series_a (list or array): First time series.
		series_b (list or array): Second time series.
		distance_matrix (2D list): The accumulated cost matrix used to compute the DTW distance.
		dtw_distance (float): The computed DTW distance between series_a and series_b.
		"""
		super().__init__()
		self.type='vec_float'

	def compute(self, series_a, series_b):
		"""
		Compute the DTW distance between the two time series.
        
		Returns:
			float: The DTW distance.
		"""
		self.series_a = series_a
		self.series_b = series_b
		self.distance_matrix = None
		self.dtw_distance = None
        
		n = len(self.series_a)
		m = len(self.series_b)
		self.distance_matrix = [[float('inf')] * m for _ in range(n)]
		self.distance_matrix[0][0] = 0
        
		for i in range(1, n):
			for j in range(1, m):
				cost = abs(self.series_a[i] - self.series_b[j])
				self.distance_matrix[i][j] = cost + min(self.distance_matrix[i-1][j],    # Insertion
						self.distance_matrix[i][j-1],    # Deletion
						self.distance_matrix[i-1][j-1])  # Match

		self.dtw_distance = self.distance_matrix[-1][-1]
		return self.dtw_distance

	def get_optimal_path(self):
		"""
		Retrieve the optimal path that aligns the two time series with the minimum cost.
        
		Returns:
			list of tuples: The optimal path as a list of index pairs (i, j).
		"""
		i, j = len(self.series_a) - 1, len(self.series_b) - 1
		path = [(i, j)]
        
		while i > 0 and j > 0:
			if i == 0:
				j -= 1
			elif j == 0:
				i -= 1
			else:
				step = min(self.distance_matrix[i-1][j], self.distance_matrix[i][j-1], self.distance_matrix[i-1][j-1])
                
				if step == self.distance_matrix[i-1][j-1]:
					i -= 1
					j -= 1
				elif step == self.distance_matrix[i-1][j]:
					i -= 1
				else:
					j -= 1
            
				path.append((i, j))
        
		path.reverse()
		return path

from typing import List

#class dev pour les textes !!!!
class LongestCommonSubsequence(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='vec_str'

		"""
		A class to compute the Longest Common Subsequence (LCS) between two text files.
		"""

	def _lcs_matrix(self, text1: str, text2: str) -> List[List[int]]:
		"""
		Constructs the LCS matrix for two input texts.
        
		:param text1: The first text as a string.
		:param text2: The second text as a string.
		:return: A 2D list (matrix) containing the lengths of LCS for substrings of text1 and text2.
		"""
		len1: int = len(text1)
		len2: int = len(text2)
        
		# Create a 2D matrix initialized with 0
		lcs_matrix: List[List[int]] = [[0] * (len2 + 1) for _ in range(len1 + 1)]

		for i in range(1, len1 + 1):
			for j in range(1, len2 + 1):
				if text1[i - 1] == text2[j - 1]:
					lcs_matrix[i][j] = lcs_matrix[i - 1][j - 1] + 1
				else:
					lcs_matrix[i][j] = max(lcs_matrix[i - 1][j], lcs_matrix[i][j - 1])

		return lcs_matrix

	def _backtrack_lcs(self, lcs_matrix: List[List[int]], text1: str, text2: str) -> str:
		"""
		Backtracks through the LCS matrix to reconstruct the longest common subsequence.
        
		:param lcs_matrix: A 2D list (matrix) containing the lengths of LCS for substrings of text1 and text2.
		:param text1: The first text as a string.
		:param text2: The second text as a string.
		:return: The longest common subsequence as a string.
		"""
		i: int = len(text1)
		j: int = len(text2)
		lcs: List[str] = []

		while i > 0 and j > 0:
			if text1[i - 1] == text2[j - 1]:
				lcs.append(text1[i - 1])
				i -= 1
				j -= 1
			elif lcs_matrix[i - 1][j] >= lcs_matrix[i][j - 1]:
				i -= 1
			else:
				j -= 1

		return ''.join(reversed(lcs))

	def compute(self, text1: str, text2: str) -> str:
		"""
		Computes the Longest Common Subsequence (LCS) between two texts.
        
		:param text1: The first text as a string.
		:param text2: The second text as a string.
		:return: The longest common subsequence as a string.
		"""
		# Compute the LCS matrix
		lcs_matrix: List[List[int]] = self._lcs_matrix(text1, text2)

		# Backtrack to find the actual LCS
		lcs: str = self._backtrack_lcs(lcs_matrix, text1, text2)

		return lcs
		
	def example(self):
		self.obj1_exemple = "AGGTAB"
		self.obj2_exemple = "GXTXAYB"
		sequence=self.compute(self.obj1_exemple,self.obj2_exemple)
		
		print(f"{self.__class__.__name__} distance between {self.obj1_exemple} and {self.obj2_exemple} is {sequence}")

class Frechet(Distance):

	def __init__(self)-> None:
		"""
		Initialize the FrechetDistance with two curves.

		:param curve_a: First curve, a list of tuples representing points (e.g., [(x1, y1), (x2, y2), ...])
		:param curve_b: Second curve, a list of tuples representing points (e.g., [(x1, y1), (x2, y2), ...])
		"""
		super().__init__()
		self.type='vec_tuple_float'


	def _c(self, i, j):
		"""
		Internal method to compute the discrete Fréchet distance using dynamic programming.

		:param i: Index in curve_a
		:param j: Index in curve_b
		:return: Fréchet distance between curve_a[0..i] and curve_b[0..j]
		"""
		if self.ca[i][j] > -1:
			return self.ca[i][j]
		elif i == 0 and j == 0:
			self.ca[i][j] = Euclidean().calculate(self.curve_a[0], self.curve_b[0])
		elif i > 0 and j == 0:
			self.ca[i][j] = max(self._c(i - 1, 0), Euclidean().calculate(self.curve_a[i], self.curve_b[0]))
		elif i == 0 and j > 0:
			self.ca[i][j] = max(self._c(0, j - 1), Euclidean().calculate(self.curve_a[0], self.curve_b[j]))
		elif i > 0 and j > 0:
			self.ca[i][j] = max(
				min(self._c(i - 1, j), self._c(i - 1, j - 1), self._c(i, j - 1)),
				Euclidean().calculate(self.curve_a[i], self.curve_b[j])
				)
		else:
			self.ca[i][j] = float('inf')
		return self.ca[i][j]

	def compute(self, curve_a, curve_b):
		"""
		Compute the Fréchet distance between the two curves.

		:return: The Fréchet distance between curve_a and curve_b
		"""
		self.curve_a = curve_a
		self.curve_b = curve_b
		self.ca = [[-1 for _ in range(len(curve_b))] for _ in range(len(curve_a))]
        
		return self._c(len(self.curve_a) - 1, len(self.curve_b) - 1)
	
	def example(self):
		self.obj1_example = [(0, 0), (1, 1), (2, 2)]
		self.obj2_example = [(0, 0), (1, 2), (2, 3)]
		distance=self.compute(self.obj1_example,self.obj2_example)
		print(f"{self.__class__.__name__} distance between {self.obj1_example} and {self.obj2_example} is {distance:.2f}")




