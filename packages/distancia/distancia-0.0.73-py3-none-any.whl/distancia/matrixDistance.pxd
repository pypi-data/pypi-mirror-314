

cdef class CosineSimilarity:
	cpdef double compute(self, list[float] point1, list[float] point2)
	cpdef double dot_product(self, list[float] vec1, list[float] vec2)
	cpdef double norm(self, list[float] vec)
	cpdef void exemple(self)


cdef class CosineInverse:
	cpdef double compute(self, list[float] point1, list[float] point2)
	cpdef void exemple(self)
	
cdef class Jaccard:
	cpdef double compute(self, set set1, set set2)
	cpdef void exemple(self)
	
cdef class Tanimoto:
	cpdef double compute(self, set set1, set set2)

cdef class GeneralizedJaccard:
	cpdef double compute(self, list[float] point1, list[float] point2)
	cpdef void exemple(self)
	
cdef class Dice:
	cpdef double compute(self,  set set1, set set2)
	cpdef void exemple(self)
	
cdef class Tversky:
	cpdef double compute(self, set set1, set set2)
	cpdef void exemple(self)
	
cdef class Pearson:
	cpdef double compute(self, list[float] x, list[float] y)
	cpdef void exemple(self)
	
cdef class Spearman:
	cpdef double compute(self, list[float] x, list[float] y)
	cpdef void exemple(self)
	
cdef class Ochiai:
	cpdef double compute(self, list[bool] point1, list[bool] point2)
	cpdef void exemple(self)
cdef class MotzkinStraus:
	cpdef double compute(self, list[float] x, list[float] y)
	cpdef void exemple(self)
cdef class EnhancedRogersTanimoto:
	cpdef double compute(self, list[float] vector_a, list[float] vector_b)
	cpdef void exemple(self)
cdef class ContextualDynamicDistance:
	cpdef double compute(self, list[float] x, list[float] y, list[float] context_x, list[float] context_y)
	cpdef double convolution_context_weight_func(self,list[float]context_x, list[float]context_y,int index, int kernel_size):
	cpdef void exemple(self)
	
cdef class MahalanobisTaguchi:
	cpdef double array calculate_mean_vector(self)
	cpdef double array array calculate_covariance_matrix(self)
	cpdef invert_matrix(self, list[list[float]] matrix)
	cpdef double compute(self, list[float] data_point)
	cpdef void exemple(self)
	
cdef class Otsuka:
	cpdef double compute(self, list[float] vector1, list[float] vector2)
	cpdef void exemple(self)
	
cdef class RogersTanimoto:
	cpdef double compute(self, list[float] vector1, list[float] vector1)
	cpdef void exemple(self)
	
cdef class SokalMichener:
	cpdef double compute(self, list[float] vector1, list[float] vector2)
	cpdef void exemple(self)
	
cdef class SokalSneath:
	cpdef double compute(self, list[float] vector1, list[float] vector2)
	cpdef void exemple(self)
	
cdef class RatcliffObershelp:
	cpdef double compute(self, str str1 ,str str2)
	cpdef void exemple(self)
	
cdef class :
	cpdef double compute(self, list[float] point1, list[float] point2)
	cpdef void exemple(self)

cdef class Gestalt

cdef class FagerMcGowan:
	
	cpdef double compute(self, set set_a, set set_b, int N)
	
	cpdef void exemple(self)
