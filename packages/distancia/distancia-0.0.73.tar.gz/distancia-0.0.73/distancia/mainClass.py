from abc import ABC   # permet de définir des classes de base
from .tools     import *

class Distance(ABC):

	type1=list
	type2=list
	
	def __call__(self,*args):
		if len(args)==2:
			return self.compute(args[0], args[1])
		if len(args)==3:
			return self.compute(args[0], args[1], args[2])
		if len(args)==4:
			return self.compute(args[0], args[1], args[2], args[3])
		
	def calculate(self,*args):
	#def distance(self, obj1, obj2):
		"""
		Calculate the distance between two objects.
		:param obj1: First object
		:param obj2: Second object
		....
		:return: Distance between obj1, obj2, ...
		"""
		return self.compute(*args)
		
	def distance(self,*args):
		"""
		Calculate the distance between two objects.
		:param obj1: First object
		:param obj2: Second object
		....
		:return: Distance between obj1, obj2, ...
		"""
		return self.compute(*args)
		
	'''
	def compute(self,*args):
		self.distance_function(*args)
	'''
	def get_metric_name(self):
		return self.name

	def set_metric(metric_name):
		self.name=metric_name
		
	def checkDimensionData(self,data1,data2):
		
		self.__class__.__name__=c_name
		str_raise=f'In {c_name} class, '
		if c_name=='Euclidean'or c_name=='L2'or c_name=='Manhattan'or  c_name=='L1'or  c_name=='Minkowski'or  c_name=='RussellRao' or  c_name=='Chebyshev'or  c_name=='KendallTau'or  c_name=='Canberra' or  c_name=='BrayCurtis'or  c_name=='Matching'or  c_name=='Kulsinski'or  c_name=='Yule' or  c_name=='Bhattacharyya'or  c_name=='Gower'or  c_name=='Hellinger' or  c_name=='CzekanowskiDice' or  c_name=='Wasserstein' :
			if len(data1) != len(data2):
				raise ValueError(str_raise+'points must have the same dimensions')
		if c_name=='Mahalanobis':
			if len(data1[0]) != len(data2):
				raise ValueError(str_raise+"points dimensions must match dataset dimensions")
		if c_name=='Levenshtein'or  c_name=='Jaro'or  c_name=='SorensenDice'or  c_name=='JaroWinkler':
			pass
		if c_name=='Hamming':
			if len(data2) != len(data2):
				raise ValueError(str_raise+'strings must be of the same length')
		if c_name=='InverseTanimoto':
			if not isinstance(data1, set) or not isinstance(data2, set):
				raise ValueError(str_raise+'inputs must be of type set.')

	def is_metric_symmetric(self, point1, point2):
		"""
		Checks if the metric is symmetric, i.e., if d(point1, point2) == d(point2, point1).
        
		:param point1: First point.
		:param point2: Second point.
		:return: True if the metric is symmetric, False otherwise.
        """
		distance_1 = self.metric_function(point1, point2)
		distance_2 = self.metric_function(point2, point1)
        
		return distance_1 == distance_2
		
	def is_metric_positive_definite(self, point1, point2):
		"""
		Checks if the metric is positive definite.
		A metric is positive definite if:
		1. d(point1, point1) == 0 (self-distance is zero).
		2. d(point1, point2) > 0 for all point1 != point2 (distance between distinct points is positive).
        
		:param point1: First point.
		:param point2: Second point.
		:return: True if the metric is positive definite, False otherwise.
		"""
		# Check self-distance
		if self.compute(point1, point1) != 0:
			return False
		if self.compute(point2, point2) != 0:
			return False
        
		# Check positive distance for distinct points
		if point1 != point2 and self.compute(point1, point2) <= 0:
			return False
        
		return True

	def is_metric_subadditive(self, point1, point2, point3):
		"""
		Checks if the metric satisfies the triangle inequality (subadditivity).
		The triangle inequality states:
		d(point1, point3) <= d(point1, point2) + d(point2, point3)
        
		:param point1: First point (A).
		:param point2: Second point (B).
		:param point3: Third point (C).
		:return: True if the metric satisfies the triangle inequality, False otherwise.
		"""
		# Compute the distances
		d_12 = self.compute(point1, point2)
		d_23 = self.compute(point2, point3)
		d_13 = self.compute(point1, point3)
        
		# Check the triangle inequality
		return d_13 <= d_12 + d_23
		
#############################
	'''
	def check_data(self, obj1, obj2):
		"""
		Verify the data of a distance measure: type, dimension.
		"""
		
		print(type(obj1))
		print(self.type1)
		properties = {
				f'collection1_type {self.type1}': type(obj1) is self.type1,
				f'collection2_type {self.type2}': type(obj2) is self.type2,
				f'data_type': True and True,
				f'association_rules': True and True,
		}
		print(f"Data verification: {properties}")
	'''
	def check_properties(self, obj1, obj2, obj3):
		"""
		Verify the properties of a distance measure: non-negativity, identity of indiscernibles, symmetry, and triangle inequality.
		:param obj1: First object
		:param obj2: Second object
		:param obj3: Third object
		:return: Dictionary indicating whether each property holds
		"""
		d12 = self.compute(obj1, obj2)
		d13 = self.compute(obj1, obj3)
		d23 = self.compute(obj2, obj3)

		properties = {
				'non_negativity': d12 >= 0 and d13 >= 0 and d23 >= 0,
				'identity_of_indiscernibles': (d12 == 0) == (obj1 == obj2) and (d13 == 0) == (obj1 == obj3) and (d23 == 0) == (obj2 == obj3),
				'symmetry': d12 == self.compute(obj2, obj1) and d13 == self.compute(obj3, obj1) and d23 == self.compute(obj3, obj2),
				'triangle_inequality': d12 <= d13 + d23 and d13 <= d12 + d23 and d23 <= d12 + d13,
		}
		print(f"Properties verification: {properties}")

	def example(self):
		if self.type=='text':
			self.obj1_example=Text().generate()
			self.obj2_example=Text().generate()
		if self.type=='vec_float':
			self.obj1_example=Vector().generate(4)
			print(Vector().generate(4))
			self.obj2_example=Vector().generate(4)
		if self.type=='vec_proba':
			self.obj1_example=Vector().generate(4,form='proba')
			self.obj2_example=Vector().generate(4,form='proba')
		if self.type=='vec_nn':
			self.obj1_example=Vector().generate(4,form='bin')
			self.obj2_example=Vector().generate(4,form='proba')
		if self.type=='str':
			self.obj1_example = "martha"
			self.obj2_example = "mbarht"
		if self.type=='vec_str':
			self.obj1_example = Vector().generate(4,form='letter')
			self.obj2_example = Vector().generate(4,form='letter')
		if self.type=='vec_word':
			self.obj1_example = ["red", "blue", "green"]
			self.obj2_example = ["yellow", "blue", "green", "purple"]
		if self.type=='text':
			self.obj1_example = "the quick brown fox jumps over the lazy dog"
			self.obj2_example = "the fast brown fox leaps over the sleepy cat"
		if self.type=='vec_int':
			self.obj1_example=Vector().generate(4,form='int')
			self.obj2_example=Vector().generate(4,form='int')
		if self.type=='vec_bin':
			self.obj1_example=Vector().generate(4,form='bin')
			self.obj2_example=Vector().generate(4,form='bin')
		if self.type=='vec_bool':
			self.obj1_example=Vector().generate(4,form='bool')
			self.obj2_example=Vector().generate(4,form='bool')
		if self.type=='matrix_float':
			self.obj1_example=Matrix().generate(3)
			self.obj2_example=Matrix().generate(3)
		if self.type=='file':
			self.obj1_example='./sample/file1.txt'
			self.obj2_example='./sample/file2.txt'
			
		if self.type=='graph':
			self.obj1_example=Graph(Graph.nodes_1,Graph.edges_1)
			self.obj2_example=Graph(Graph.nodes_2,Graph.edges_2)
			
		if self.type=='Markov_chain':
			self.obj1_example=MarkovChain.mc_1
			self.obj2_example=MarkovChain.mc_2
			
		if self.type=='sound':
			self.obj1_example,self.obj2_example=Sound.example()

		if hasattr(self, 'obj4_example'):
			distance=self.compute(self.obj1_example, self.obj2_example,self.obj3_example,self.obj4_example)
		elif hasattr(self, 'obj3_example'):
			distance=self.compute(self.obj1_example, self.obj2_example,self.obj3_example)
		else:
			distance=self.compute(self.obj1_example, self.obj2_example)
		print(f"{self.__class__.__name__} distance between {self.obj1_example} and {self.obj2_example} is {distance:.2f}")
		'''
		if not hasattr(self, 'obj3_example')and not hasattr(self, 'obj4_example'):
			print(f"{self.__class__.__name__} distance between {self.obj1_example} and {self.obj2_example} is {self.compute(self.obj1_example, self.obj2_example):.2f}")
		elif not hasattr(self, 'obj4_example'):
			print(f"{self.__class__.__name__} distance {self.obj3_example} between {self.obj1_example} and {self.obj2_example} is {self.compute(self.obj1_example, self.obj2_example, self.obj3_example):.2f}")
		else:
			print(f"{self.__class__.__name__} distance {self.obj3_example}, {self.obj4_example} between {self.obj1_example} and {self.obj2_example} is {self.compute(self.obj1_example, self.obj2_example, self.obj3_example, self.obj4_example):.2f}")
		'''
