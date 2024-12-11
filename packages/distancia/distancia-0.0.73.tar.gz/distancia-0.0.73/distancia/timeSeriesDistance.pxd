

cdef class DynamicTimeWarping:
	cpdef double compute(self, list series_a,list series_b):
	cpdef list get_optimal_path(self):

cdef class LongestCommonSubsequence:
	cpdef double LCS(self,list sequence_a,list sequence_b):
	cpdef list get_lcs(self):
	cpdef double compute(self,list sequence_a,list sequence_b):

cdef class Frechet:
	cpdef _c(self,int i,int j):
	cpdef double compute(self,list curve_a,list curve_b):


