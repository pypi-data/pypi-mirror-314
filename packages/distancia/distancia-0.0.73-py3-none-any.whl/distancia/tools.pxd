

cpdef bool def check_bin(str_):

    
cpdef bool def check_probability(number):

    
cpdef int def factorial(n):
	
cpdef double def exp(x, terms=20):

cpdef double def sin(x, terms=10):

cpdef double def cos(x, terms=10):

cpdef double def degrees_to_radians(degrees):

cpdef double def atan(x, terms=10):

cpdef double def atan2(y, x, terms=10):

cpdef double def log(x, iterations=1000):
    
cpdef list[int]def rank(data):


cpdef double def spearman_correlation(x, y):

cpdef class Scalar:
	
cpdef class Matrix:
    
	cpdef list[list[float]] def invert_matrix(matrix):
		
	cpdef list[list[float]] def covariance_matrix(data):
		
	cpdef list def eigenvalues_2x2(self, matrix):

	cpdef list[list[float]] def matrix_subtraction(self, A, B):

	cpdef double def matrix_trace(self, matrix):

	cpdef list[float]def characteristic_polynomial(self, matrix):
            
cpdef class Graph:

	cpdef list[list[float]] def create_adjacency_matrix(self):

	cpdef list[float]def create_adjacency_list(self):

	cpdef dict def count_motifs(self, motif_size):

	cpdef list def _find_sub_motifs(self, node, neighbors, remaining):
        
	cpdef list def get_nodes(self):
        
	cpdef list def get_edges(self, graph):
        
	cpdef dict def dijkstra(self, start_node, end_node):
        
cpdef class MarkovChain:

    cpdef void def add_text(self, text: str) -> None:

    cpdef str def generate_text(self, length: int = 100) -> str:

    cpdef dict def _weighted_choice(self, choices: Dict[str, int]) -> str:

    cpdef double def get_probability(self, state: Tuple[str, ...], next_word: str) -> float:

    cpdef str def get_most_likely_next(self, state: Tuple[str, ...]) -> str:

    cpdef void def exemple(self) -> None:
        
cpdef class MarkovChain:

	cpdef def stationary_distribution(self, matrix, tolerance=1e-10, max_iterations=1000):

