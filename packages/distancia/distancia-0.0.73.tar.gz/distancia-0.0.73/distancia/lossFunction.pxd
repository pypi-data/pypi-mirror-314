

cdef class CrossEntropy:
		
	cpdef def compute(self,list[float] y_true,list[float] y_pred):
		
	cpdef def __call__(self,list[float] y_true,list[float] y_pred):
    
	cpdef def softmax(self,list[float]  logits):

cdef class KullbackLeibler:
		   
	cpdef def compute(self,list[float] y_true,list[float] y_pred):
		
	cpdef def __call__(self,float p,float q):

cdef class MeanAbsoluteError:

	cpdef def compute(self,list[float] y_true,list[float] y_pred):
		
	cpdef def __call__(self,list[float] y_true,list[float] y_pred):

cdef class MAE:

cdef class MeanAbsolutePercentageError:

	cpdef def compute(self,list[float] y_true,list[float] y_pred):
		
	cpdef def __call__(self,list[float] y_true,list[float] y_pred):

cdef class MAPE:
		
cdef class MeanSquaredError:
	cpdef def compute(self,list[float] y_true,list[float] y_pred):
		
	cpdef def __call__(self,list[float] y_true,list[float] y_pred):

cdef class MSE:		

cdef class SquaredLogarithmicError:

	cpdef def compute(self,list[float] y_true,list[float] y_pred):
		
	cpdef def __call__(self,list[float] y_true,list[float] y_pred):

cdef class SLE:

cdef class GaloisWassersteinLoss:
	cpdef def __init__(self,float alpha,float beta,float gamma):

	cpdef def build_galois_trellis(self):
    
	cpdef def compute_cdf(self,float probabilities):
    
	cpdef def compute(self,list[float] y_true,list[float] y_pred):
    
	cpdef def __call__(self,list[float] y_true,list[float] y_pred):

	
