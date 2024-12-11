
cdef class Distance(ABC):
	list obj1_exemple
	list obj2_exemple
	list type1=list
	list type2=list
	
	cpdef double def __call__(self,*args):

	cpdef double def calculate(self,*args):

	cpdef void def get_metric_name(self):

	cpdef void def set_metric(metric_name):
		
	cpdef void def checkData(self,data1,data2):

	cpdef bool def is_metric_symmetric(self, point1, point2):
		
	cpdef bool def is_metric_positive_definite(self, point1, point2):

	cpdef bool def is_metric_subadditive(self, point1, point2, point3):
		
	cpdef void def check_properties(self, obj1, obj2, obj3):

	cpdef void def exemple(self):
