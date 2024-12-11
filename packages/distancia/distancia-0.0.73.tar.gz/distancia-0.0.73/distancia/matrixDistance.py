from .mainClass import *
from .tools     import Vector,Matrix
from .vectorDistance     import Euclidean

class Mahalanobis(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='list_list'

	def compute(self,point :list, data :list[list]) -> float:
		"""
		Calculate the Mahalanobis distance between a point and a dataset.
    
		:param point: A point as a list of coordinates
		:param data: A dataset as a list of points (list of lists)
		:return: Mahalanobis distance between the point and the dataset
		:raises ValueError: If the point dimensions do not match the dataset dimensions
		! lever une execption si la matrice est singulière
		"""
    
		cov_matrix = Matrix.covariance(data)
		cov_matrix_inv = Matrix.inverse_Gauss_Jordan(cov_matrix)
    
		diff = [point[i] - mean_data[i] for i in range(len(point))]
    
		# Matrix multiplication: diff^T * cov_matrix_inv * diff
		result = 0
		for i in range(len(diff)):
			for j in range(len(diff)):
				result += diff[i] * cov_matrix_inv[i][j] * diff[j]
    
		return result**0.5
		
	def example(self):
		self.obj1_example=Vector().generate_vector(4)
		self.obj2_example = Vector().generate_vector(4)
		#super().example()
		




class MahalanobisTaguchi(Distance):
	
    def __init__(self, reference_group :list[list])-> None:
        """
        Initialize the MahalanobisTaguchi class with a reference group.
        
        :param reference_group: A list of lists where each inner list is a data point in the reference group.
        """
        super().__init__()
        self.type='vec_float'


        self.reference_group = reference_group
        self.mean_vector = self.calculate_mean_vector()
        self.covariance_matrix = Matrix.covariance(reference_group)
        self.inverse_covariance_matrix = Matrix.invert(self.covariance_matrix)

    def calculate_mean_vector(self):
        """
        Calculate the mean vector of the reference group.

        :return: A list representing the mean vector.
        """
        num_points = len(self.reference_group)
        num_dimensions = len(self.reference_group[0])

        mean_vector = [0] * num_dimensions

        for point in self.reference_group:
            for i in range(num_dimensions):
                mean_vector[i] += point[i]

        mean_vector = [x / num_points for x in mean_vector]
        return mean_vector

    def compute(self, data_point)-> float:
        """
        Calculate the Mahalanobis-Taguchi distance for a given data point.

        :param data_point: A list representing the data point to be evaluated.
        :return: The Mahalanobis-Taguchi distance as a float.
        """
        diff_vector = [data_point[i] - self.mean_vector[i] for i in range(len(self.mean_vector))]
        
        # Matrix multiplication with the inverse covariance matrix
        temp_vector = [0] * len(diff_vector)
        for i in range(len(diff_vector)):
            for j in range(len(diff_vector)):
                temp_vector[i] += diff_vector[j] * self.inverse_covariance_matrix[j][i]

        # Final dot product to get the Mahalanobis-Taguchi distance
        distance_squared = sum(temp_vector[i] * diff_vector[i] for i in range(len(diff_vector)))
        return distance_squared ** 0.5
        
    def example(self):
        # Example reference group data (2D array where each row is a data point)

        # Example test data (data point to be evaluated against the reference group)
        test_data = [1.3, 2.3, 3.3]

        # Calculate the Mahalanobis-Taguchi distance for the test data
        distance = self.compute(test_data)

        # Print the result
        print(f"Mahalanobis-Taguchi distance for the test data {test_data} is: {distance}")

from typing import List, Tuple
import math

class MatrixSpectral(Distance):
	
    def __init__(self)-> None:
        """
        Initialize the MahalanobisTaguchi class with a reference group.
        
        :param reference_group: A list of lists where each inner list is a data point in the reference group.
        """
        super().__init__()
        self.type='matrix_float'

        self.reset()

    def reset(self) -> None:
        """
        Reset all computed values
        """
        self.spectrum1: List[float] = []
        self.spectrum2: List[float] = []
        self.distance: float = 0.0

    def compute_spectrum(self, matrix: List[List[float]], max_iter: int = 100, tol: float = 1e-6) -> List[float]:
        """
        Compute eigenvalues using power iteration with deflation
        
        Args:
            matrix: Input matrix
            max_iter: Maximum iterations for convergence
            tol: Convergence tolerance
            
        Returns:
            List[float]: Sorted eigenvalues
        """
        n = len(matrix)
        spectrum = []
        working_matrix = [row[:] for row in matrix]  # Copy matrix

        for _ in range(n):
            # Initialize random vector
            vector = [1.0] * n
            vector, _ = Vector.normalize(vector)
            
            # Power iteration
            eigenvalue = 0.0
            for _ in range(max_iter):
                # Compute new vector
                new_vector = Matrix.multiply_vector(working_matrix, vector)
                new_vector, new_norm = Vector.normalize(new_vector)
                
                # Update eigenvalue estimate
                new_eigenvalue = sum(v1 * v2 for v1, v2 in zip(vector, Matrix.multiply_vector(working_matrix, vector)))
                
                # Check convergence
                if abs(new_eigenvalue - eigenvalue) < tol:
                    eigenvalue = new_eigenvalue
                    break
                    
                vector = new_vector
                eigenvalue = new_eigenvalue
            
            spectrum.append(eigenvalue)
            
            # Deflation
            for i in range(n):
                for j in range(n):
                    working_matrix[i][j] -= eigenvalue * vector[i] * vector[j]

        return sorted(spectrum, reverse=True)

    def compute(self, matrix1: List[List[float]], matrix2: List[List[float]]) -> float:
        """
        Compute spectral distance between two matrices
        
        Args:
            matrix1: First matrix
            matrix2: Second matrix
            
        Returns:
            float: Spectral distance between matrices
            
        Raises:
            ValueError: If matrices have different dimensions
        """
        # Validate matrices
        n1, n2 = len(matrix1), len(matrix2)
        if n1 != n2 or any(len(row) != n1 for row in matrix1) or any(len(row) != n2 for row in matrix2):
            raise ValueError("Matrices must be square and have the same dimensions")

        # Reset previous computations
        self.reset()

        # Compute spectra
        self.spectrum1 = self.compute_spectrum(matrix1)
        self.spectrum2 = self.compute_spectrum(matrix2)

        # Compute Euclidean distance between spectra
        #self.distance = math.sqrt(sum((s1 - s2) ** 2 for s1, s2 in zip(self.spectrum1, self.spectrum2)))
        self.distance = Euclidean().compute(self.spectrum1, self.spectrum2)
        
        return self.distance

    def get_spectra(self) -> Tuple[List[float], List[float]]:
        """
        Get computed spectra of both matrices
        
        Returns:
            Tuple[List[float], List[float]]: Spectra of both matrices
        """
        return self.spectrum1, self.spectrum2

from typing import List, Tuple
import math

class NormalizedSpectral(Distance):
	
    def __init__(self)-> None:
        """
        Initialize the MahalanobisTaguchi class with a reference group.
        
        :param reference_group: A list of lists where each inner list is a data point in the reference group.
        """
        super().__init__()
        self.type='matrix_float'

        self.reset()

    def reset(self) -> None:
        """
        Reset all computed values
        """
        self.spectrum1: List[float] = []
        self.spectrum2: List[float] = []
        self.normalized_spectrum1: List[float] = []
        self.normalized_spectrum2: List[float] = []
        self.distance: float = 0.0

    def _frobenius_norm(self, matrix: List[List[float]]) -> float:
        """
        Compute the Frobenius norm of a matrix
        
        Args:
            matrix: Input matrix
            
        Returns:
            float: Frobenius norm
        """
        return math.sqrt(sum(sum(x*x for x in row) for row in matrix))

    def compute_spectrum(self, matrix: List[List[float]], max_iter: int = 100, tol: float = 1e-6) -> List[float]:
        """
        Compute eigenvalues using power iteration with deflation
        
        Args:
            matrix: Input matrix
            max_iter: Maximum iterations for convergence
            tol: Convergence tolerance
            
        Returns:
            List[float]: Sorted eigenvalues
        """
        n = len(matrix)
        spectrum = []
        working_matrix = [row[:] for row in matrix]

        for _ in range(n):
            # Initialize random vector
            vector = [1.0] * n
            vector, _ = Vector.normalize(vector)
            
            # Power iteration
            eigenvalue = 0.0
            for _ in range(max_iter):
                new_vector = Matrix.multiply_vector(working_matrix, vector)
                new_vector, new_norm = Vector.normalize(new_vector)
                
                # Rayleigh quotient for eigenvalue estimation
                new_eigenvalue = sum(v1 * v2 for v1, v2 in zip(vector, Matrix.multiply_vector(working_matrix, vector)))
                
                if abs(new_eigenvalue - eigenvalue) < tol:
                    eigenvalue = new_eigenvalue
                    break
                    
                vector = new_vector
                eigenvalue = new_eigenvalue
            
            spectrum.append(eigenvalue)
            
            # Deflation
            for i in range(n):
                for j in range(n):
                    working_matrix[i][j] -= eigenvalue * vector[i] * vector[j]

        return sorted(spectrum, reverse=True)

    def normalize_spectrum(self, spectrum: List[float], norm_factor: float) -> List[float]:
        """
        Normalize spectrum by dividing by norm factor
        
        Args:
            spectrum: List of eigenvalues
            norm_factor: Normalization factor
            
        Returns:
            List[float]: Normalized spectrum
        """
        if norm_factor < 1e-10:  # Avoid division by zero
            return spectrum
        return [val/norm_factor for val in spectrum]

    def compute(self, matrix1: List[List[float]], matrix2: List[List[float]], 
                        normalization: str = 'frobenius') -> float:
        """
        Compute normalized spectral distance between two matrices
        
        Args:
            matrix1: First matrix
            matrix2: Second matrix
            normalization: Normalization method ('frobenius' or 'spectral')
            
        Returns:
            float: Normalized spectral distance
            
        Raises:
            ValueError: If matrices have different dimensions or invalid normalization method
        """
        # Validate matrices
        n1, n2 = len(matrix1), len(matrix2)
        if n1 != n2 or any(len(row) != n1 for row in matrix1) or any(len(row) != n2 for row in matrix2):
            raise ValueError("Matrices must be square and have the same dimensions")
            
        if normalization not in ['frobenius', 'spectral']:
            raise ValueError("Normalization must be either 'frobenius' or 'spectral'")

        # Reset previous computations
        self.reset()

        # Compute spectra
        self.spectrum1 = self.compute_spectrum(matrix1)
        self.spectrum2 = self.compute_spectrum(matrix2)

        # Compute normalization factors
        if normalization == 'frobenius':
            norm1 = self._frobenius_norm(matrix1)
            norm2 = self._frobenius_norm(matrix2)
        else:  # spectral normalization
            norm1 = max(abs(val) for val in self.spectrum1)
            norm2 = max(abs(val) for val in self.spectrum2)

        # Normalize spectra
        self.normalized_spectrum1 = self.normalize_spectrum(self.spectrum1, norm1)
        self.normalized_spectrum2 = self.normalize_spectrum(self.spectrum2, norm2)

        # Compute normalized distance
        self.distance = math.sqrt(sum((s1 - s2) ** 2 
                                for s1, s2 in zip(self.normalized_spectrum1, 
                                                 self.normalized_spectrum2)))
        
        return self.distance

    def get_spectra(self) -> Tuple[List[float], List[float]]:
        """
        Get original computed spectra
        
        Returns:
            Tuple[List[float], List[float]]: Original spectra of both matrices
        """
        return self.spectrum1, self.spectrum2

    def get_normalized_spectra(self) -> Tuple[List[float], List[float]]:
        """
        Get normalized spectra
        
        Returns:
            Tuple[List[float], List[float]]: Normalized spectra of both matrices
        """
        return self.normalized_spectrum1, self.normalized_spectrum2

'''SpectralResistance supprime pour ne pas importer numpy
from typing import List, Union, Optional
import numpy as np
from numpy.linalg import pinv
import numpy.typing as npt

class SpectralResistance(Distance):
    """
    A class to compute the spectral resistance distance between two matrices.
    
    The spectral resistance distance is defined as the Euclidean norm of the
    difference between the pseudo-inverses of the Laplacian matrices.
    
    Attributes:
        epsilon (float): Small value to avoid numerical instability in computations
    """
    
        
    def __init__(self, epsilon: float = 1e-10) -> None:
        """
        Initialize the SpectralResistanceDistance calculator.
        
        Args:
            epsilon (float): Numerical stability parameter
        """
        super().__init__()
        self.type='matrix_float'
        self.epsilon = epsilon
    
    def compute_laplacian(self, matrix: Union[List[List[float]], npt.NDArray]) -> npt.NDArray:
        """
        Compute the Laplacian matrix from an adjacency matrix.
        
        Args:
            matrix: Input adjacency matrix
            
        Returns:
            NDArray: The Laplacian matrix
        
        Raises:
            ValueError: If the input matrix is not square
        """
        matrix = np.array(matrix, dtype=float)
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Input matrix must be square")
            
        # Compute degree matrix (diagonal matrix of row sums)
        degree = np.diag(np.sum(matrix, axis=1))
        
        # Laplacian = Degree - Adjacency
        return degree - matrix
    
    def compute(self, 
                        matrix1: Union[List[List[float]], npt.NDArray], 
                        matrix2: Union[List[List[float]], npt.NDArray],
                        normalized: bool = False) -> float:
        """
        Compute the spectral resistance distance between two matrices.
        
        Args:
            matrix1: First input matrix
            matrix2: Second input matrix
            normalized: Whether to normalize the distance (default: False)
            
        Returns:
            float: The spectral resistance distance
            
        Raises:
            ValueError: If matrices have different dimensions
        """
        # Convert to numpy arrays
        m1 = np.array(matrix1, dtype=float)
        m2 = np.array(matrix2, dtype=float)
        
        # Check dimensions
        if m1.shape != m2.shape:
            raise ValueError("Matrices must have the same dimensions")
        
        # Compute Laplacians
        L1 = self.compute_laplacian(m1)
        L2 = self.compute_laplacian(m2)
        
        # Compute pseudoinverses
        L1_pinv = pinv(L1 + self.epsilon * np.eye(L1.shape[0]))
        L2_pinv = pinv(L2 + self.epsilon * np.eye(L2.shape[0]))
        
        # Compute Frobenius norm of difference
        distance = np.linalg.norm(L1_pinv - L2_pinv, ord='fro')
        
        if normalized:
            # Normalize by the sum of the norms
            norm1 = np.linalg.norm(L1_pinv, ord='fro')
            norm2 = np.linalg.norm(L2_pinv, ord='fro')
            distance = distance / (norm1 + norm2 + self.epsilon)
            
        return distance
    
    def get_resistance_matrix(self, matrix: Union[List[List[float]], npt.NDArray]) -> npt.NDArray:
        """
        Compute the resistance matrix for a given adjacency matrix.
        The resistance matrix contains the resistance distances between all pairs of nodes.
        
        Args:
            matrix: Input adjacency matrix
            
        Returns:
            NDArray: The resistance matrix
        """
        L = self.compute_laplacian(matrix)
        L_pinv = pinv(L + self.epsilon * np.eye(L.shape[0]))
        n = L.shape[0]
        
        # Initialize resistance matrix
        R = np.zeros((n, n))
        
        # Compute resistance distances between all pairs of nodes
        for i in range(n):
            for j in range(n):
                R[i,j] = L_pinv[i,i] + L_pinv[j,j] - 2 * L_pinv[i,j]
                
        return R
'''        
from typing import List, Tuple, Optional
import math
from copy import deepcopy

class PureDiffusion(Distance):
    """
    A class to compute the diffusion distance between two matrices using pure Python.
    Implements matrix operations and eigenvalue decomposition without external libraries.
    
    Attributes:
        time_param (float): Time parameter for the diffusion process
        n_eigenvalues (int): Number of eigenvalues to use in computation
        epsilon (float): Small value for numerical stability
        max_iterations (int): Maximum iterations for power method
        tolerance (float): Convergence tolerance for eigenvalue computation
    """
    
    def __init__(self, 
                 time_param: float = 1.0, 
                 n_eigenvalues: Optional[int] = None,
                 epsilon: float = 1e-10,
                 max_iterations: int = 1000,
                 tolerance: float = 1e-6) -> None:
        """
        Initialize the DiffusionDistance calculator.
        
        Args:
            time_param: Time parameter for diffusion process
            n_eigenvalues: Number of eigenvalues to use
            epsilon: Numerical stability parameter
            max_iterations: Maximum iterations for eigenvalue computation
            tolerance: Convergence tolerance
        """
        super().__init__()
        self.type='matrix_float'
        
        self.time_param = time_param
        self.n_eigenvalues = n_eigenvalues
        self.epsilon = epsilon
        self.max_iterations = max_iterations
        self.tolerance = tolerance
    
   
    

    

    
    def _power_iteration(self, 
                        matrix: List[List[float]], 
                        num_vectors: int) -> Tuple[List[float], List[List[float]]]:
        """
        Compute eigenvalues and eigenvectors using power iteration method.
        
        Args:
            matrix: Input matrix
            num_vectors: Number of eigenvectors to compute
            
        Returns:
            Tuple[List[float], List[List[float]]]: Eigenvalues and eigenvectors
        """
        n = len(matrix)
        eigenvalues = []
        eigenvectors = []
        
        # Deep copy of matrix for deflation
        working_matrix = deepcopy(matrix)
        
        for _ in range(min(num_vectors, n)):
            # Initialize random vector
            vector = [1.0 / math.sqrt(n) for _ in range(n)]
            
            # Power iteration
            for _ in range(self.max_iterations):
                new_vector = [0.0 for _ in range(n)]
                
                # Matrix-vector multiplication
                for i in range(n):
                    for j in range(n):
                        new_vector[i] += working_matrix[i][j] * vector[j]
                
                # Normalize
                norm = math.sqrt(sum(x * x for x in new_vector))
                if norm < self.epsilon:
                    break
                
                vector = [x / norm for x in new_vector]
                
                # Compute Rayleigh quotient (eigenvalue estimate)
                eigenvalue = sum(working_matrix[i][j] * vector[i] * vector[j] 
                               for i in range(n) for j in range(n))
                
            eigenvalues.append(eigenvalue)
            eigenvectors.append(vector)
            
            # Matrix deflation
            for i in range(n):
                for j in range(n):
                    working_matrix[i][j] -= eigenvalue * vector[i] * vector[j]
        
        return eigenvalues, Matrix.transpose(eigenvectors)
    
    def compute(self, 
                        matrix1: List[List[float]], 
                        matrix2: List[List[float]],
                        normalized: bool = False) -> float:
        """
        Compute diffusion distance between two matrices.
        
        Args:
            matrix1: First input matrix
            matrix2: Second input matrix
            normalized: Whether to normalize the distance
            
        Returns:
            float: Diffusion distance between matrices
            
        Raises:
            ValueError: If matrices have different dimensions
        """
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same dimensions")
            
        n = len(matrix1)
        n_eigvals = self.n_eigenvalues if self.n_eigenvalues else n
        
        # Compute eigendecompositions
        evals1, evecs1 = self._power_iteration(Matrix.normalize(matrix1), n_eigvals)
        evals2, evecs2 = self._power_iteration(Matrix.normalize(matrix2), n_eigvals)
        
        # Compute diffusion matrices
        diff1 = [[0.0 for _ in range(n)] for _ in range(n)]
        diff2 = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for k in range(len(evals1)):
            scale1 = math.exp(-self.time_param * (1 - evals1[k]))
            scale2 = math.exp(-self.time_param * (1 - evals2[k]))
            
            for i in range(n):
                for j in range(n):
                    diff1[i][j] += scale1 * evecs1[i][k] * evecs1[j][k]
                    diff2[i][j] += scale2 * evecs2[i][k] * evecs2[j][k]
        
        # Compute Frobenius norm of difference
        distance = 0.0
        for i in range(n):
            for j in range(n):
                diff = diff1[i][j] - diff2[i][j]
                distance += diff * diff
        distance = math.sqrt(distance)
        
        if normalized:
            # Compute norms of individual matrices
            norm1 = math.sqrt(sum(diff1[i][j] * diff1[i][j] 
                                for i in range(n) for j in range(n)))
            norm2 = math.sqrt(sum(diff2[i][j] * diff2[i][j] 
                                for i in range(n) for j in range(n)))
            distance = distance / (norm1 + norm2 + self.epsilon)
            
        return distance
    
    def get_diffusion_coordinates(self, 
                                matrix: List[List[float]], 
                                dim: int = 2) -> List[List[float]]:
        """
        Compute diffusion coordinates for dimensionality reduction.
        
        Args:
            matrix: Input matrix
            dim: Number of dimensions for the embedding
            
        Returns:
            List[List[float]]: Diffusion coordinates
            
        Raises:
            ValueError: If dim is larger than matrix dimension
        """
        if dim > len(matrix):
            raise ValueError(f"Requested dimensions {dim} larger than matrix dimension {len(matrix)}")
            
        eigenvalues, eigenvectors = self._power_iteration(Matrix.normalize(matrix), dim)
        n = len(matrix)
        coordinates = [[0.0 for _ in range(dim)] for _ in range(n)]
        
        for i in range(n):
            for j in range(dim):
                coordinates[i][j] = eigenvectors[i][j] * math.exp(
                    -self.time_param * (1 - eigenvalues[j]))
                
        return coordinates
from typing import List, Tuple, Optional
import math
from copy import deepcopy

class RandomWalk(Distance):
    """
    A class to compute the random walk distance between two matrices.
    The random walk distance measures the difference between transition probabilities
    of random walks on the graphs represented by the matrices.
    
    Attributes:
        alpha (float): Damping factor for random walk (between 0 and 1)
        max_iter (int): Maximum number of iterations for convergence
        tolerance (float): Convergence tolerance for matrix operations
        epsilon (float): Small value for numerical stability
    """
    
    def __init__(self, 
                 alpha: float = 0.85,
                 max_iter: int = 100,
                 tolerance: float = 1e-6,
                 epsilon: float = 1e-10) -> None:
        """
        Initialize the RandomWalkDistance calculator.
        
        Args:
            alpha: Damping factor (default: 0.85)
            max_iter: Maximum iterations for convergence (default: 100)
            tolerance: Convergence tolerance (default: 1e-6)
            epsilon: Numerical stability parameter (default: 1e-10)
            
        Raises:
            ValueError: If alpha is not between 0 and 1
        """
        super().__init__()
        self.type='matrix_float'
        
        if not 0 <= alpha <= 1:
            raise ValueError("Alpha must be between 0 and 1")
            
        self.alpha = alpha
        self.max_iter = max_iter
        self.tolerance = tolerance
        self.epsilon = epsilon
    
    
    def _normalize_matrix(self, matrix: List[List[float]]) -> List[List[float]]:
        """
        Normalize matrix to create transition probability matrix.
        
        Args:
            matrix: Input adjacency matrix
            
        Returns:
            List[List[float]]: Normalized transition matrix
        """
        n = len(matrix)
        normalized = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Compute out-degrees
        for i in range(n):
            out_degree = sum(max(0.0, matrix[i][j]) for j in range(n))
            # Handle isolated nodes
            if out_degree > self.epsilon:
                for j in range(n):
                    normalized[i][j] = max(0.0, matrix[i][j]) / out_degree
            else:
                # Uniform distribution for isolated nodes
                for j in range(n):
                    normalized[i][j] = 1.0 / n
                    
        return normalized
    
    def _compute_stationary_distribution(self, 
                                       transition_matrix: List[List[float]]
                                       ) -> List[float]:
        """
        Compute the stationary distribution of a Markov chain.
        
        Args:
            transition_matrix: Normalized transition matrix
            
        Returns:
            List[float]: Stationary distribution vector
        """
        n = len(transition_matrix)
        
        # Initialize uniform distribution
        distribution = [1.0 / n for _ in range(n)]
        
        for _ in range(self.max_iter):
            new_distribution = [0.0 for _ in range(n)]
            
            # Power iteration
            for i in range(n):
                for j in range(n):
                    new_distribution[i] += distribution[j] * transition_matrix[j][i]
                    
            # Check convergence
            max_diff = max(abs(new_distribution[i] - distribution[i]) 
                         for i in range(n))
            
            distribution = new_distribution
            
            if max_diff < self.tolerance:
                break
                
        return distribution
    
    def compute(self, 
                        matrix1: List[List[float]], 
                        matrix2: List[List[float]],
                        normalized: bool = False) -> float:
        """
        Compute random walk distance between two matrices.
        
        Args:
            matrix1: First input matrix
            matrix2: Second input matrix
            normalized: Whether to normalize the distance
            
        Returns:
            float: Random walk distance between matrices
            
        Raises:
            ValueError: If matrices have different dimensions
        """
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same dimensions")
        
        n = len(matrix1)
        
        # Normalize matrices to get transition probabilities
        P1 = self._normalize_matrix(matrix1)
        P2 = self._normalize_matrix(matrix2)
        
        # Compute stationary distributions
        pi1 = self._compute_stationary_distribution(P1)
        pi2 = self._compute_stationary_distribution(P2)
        
        # Compute fundamental matrices
        # Z = (I - αP)^(-1)
        Z1 = [[0.0 for _ in range(n)] for _ in range(n)]
        Z2 = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Initialize with identity matrix
        for i in range(n):
            for j in range(n):
                Z1[i][j] = 1.0 if i == j else 0.0
                Z2[i][j] = 1.0 if i == j else 0.0
        
        # Compute fundamental matrices using power series
        for _ in range(self.max_iter):
            Z1_new = Matrix.multiply(P1, Z1)
            Z2_new = Matrix.multiply(P2, Z2)
            
            # Scale by alpha
            for i in range(n):
                for j in range(n):
                    Z1[i][j] = (1 - self.alpha) * (1.0 if i == j else 0.0) + self.alpha * Z1_new[i][j]
                    Z2[i][j] = (1 - self.alpha) * (1.0 if i == j else 0.0) + self.alpha * Z2_new[i][j]
        
        # Compute distance
        distance = 0.0
        for i in range(n):
            for j in range(n):
                diff = Z1[i][j] - Z2[i][j]
                # Weight by stationary distributions
                distance += abs(diff) * pi1[i] * pi2[j]
        
        if normalized:
            # Compute individual norms
            norm1 = sum(abs(Z1[i][j]) * pi1[i] * pi1[j] 
                       for i in range(n) for j in range(n))
            norm2 = sum(abs(Z2[i][j]) * pi2[i] * pi2[j] 
                       for i in range(n) for j in range(n))
            distance = distance / (math.sqrt(norm1 * norm2) + self.epsilon)
        
        return distance
    
    def get_node_distances(self, 
                          matrix: List[List[float]]
                          ) -> List[List[float]]:
        """
        Compute pairwise random walk distances between nodes.
        
        Args:
            matrix: Input adjacency matrix
            
        Returns:
            List[List[float]]: Matrix of pairwise node distances
        """
        n = len(matrix)
        P = self._normalize_matrix(matrix)
        pi = self._compute_stationary_distribution(P)
        
        # Initialize distance matrix
        distances = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Compute fundamental matrix
        Z = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            Z[i][i] = 1.0
            
        for _ in range(self.max_iter):
            Z_new = Matrix.multiply(P, Z)
            for i in range(n):
                for j in range(n):
                    Z[i][j] = (1 - self.alpha) * (1.0 if i == j else 0.0) + self.alpha * Z_new[i][j]
        
        # Compute pairwise distances
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    distances[i][j] += abs(Z[i][k] - Z[j][k]) * pi[k]
                    
        return distances
        
from typing import List, Union
from math import exp

class HeatKernel(Distance):
    """
    A class to compute the Heat Kernel distance between two matrices.
    The Heat Kernel distance is a measure that captures both the direct and indirect
    relationships between matrices by considering paths of all lengths.
    
    The distance is calculated as: d(A,B) = ||exp(-t*A) - exp(-t*B)||
    where:
    - t is the time parameter (controls the scale of the diffusion)
    - exp is the matrix exponential
    - ||.|| is the Frobenius norm
    """

    def __init__(self, time_parameter: float = 1.0):
        """
        Initialize the HeatKernelDistance calculator.
        
        Args:
            time_parameter (float): The time parameter t for the heat kernel.
                                  Controls how far the heat diffusion spreads.
                                  Larger values give more weight to indirect connections.
        """
        super().__init__()
        self.type='matrix_float'
        
        self.time_parameter = time_parameter

    def compute(self, A: List[List[float]], B: List[List[float]]) -> float:
        """
        Compute the Heat Kernel distance between two matrices.
        
        Args:
            A (List[List[float]]): First matrix
            B (List[List[float]]): Second matrix
            
        Returns:
            float: Heat Kernel distance between A and B
        """
        exp_A = Matrix().exp(A,self.time_parameter)
        exp_B = Matrix().exp(B,self.time_parameter)
        diff = Matrix.subtraction(exp_A, exp_B)
        return Matrix.frobenius_norm(diff)

from typing import List, Tuple, Optional
from math import sqrt

class GraphEditMatrix(Distance):
    """
    Implements Graph Edit Distance (GED) calculation between two matrices.
    Graph Edit Distance measures the minimum cost of transforming one graph into another
    through edit operations like node/edge insertion, deletion, and substitution.
    """
    
    def __init__(self, node_cost: float = 1.0, edge_cost: float = 1.0):
        """
        Initialize the Graph Edit Distance calculator with configurable costs.
        
        Args:
            node_cost (float): Cost of node-level edit operations. Default is 1.0.
            edge_cost (float): Cost of edge-level edit operations. Default is 1.0.
        """
        super().__init__()
        self.type='matrix_float'
        
        self.node_cost = node_cost
        self.edge_cost = edge_cost
    
    def compute(self, matrix1: List[List[float]], matrix2: List[List[float]]) -> float:
        """
        Calculate the Graph Edit Distance between two adjacency matrices.
        
        Args:
            matrix1 (List[List[float]]): First graph's adjacency matrix
            matrix2 (List[List[float]]): Second graph's adjacency matrix
        
        Returns:
            float: Computed edit distance between the two graphs
        
        Raises:
            ValueError: If input matrices are invalid (non-square or different sizes)
        """
        # Validate input matrices
        if not self._validate_matrices(matrix1, matrix2):
            raise ValueError("Input matrices must be square and of equal dimensions")
        
        n1, n2 = len(matrix1), len(matrix2)
        total_cost: float = 0.0
        
        # Node edit operations cost
        total_cost += abs(n1 - n2) * self.node_cost
        
        # Edge edit operations cost
        min_size = min(n1, n2)
        for i in range(min_size):
            for j in range(i + 1, min_size):  # Upper triangular matrix
                # Compute edge difference
                edge_diff = abs(matrix1[i][j] - matrix2[i][j])
                total_cost += edge_diff * self.edge_cost
        
        return total_cost
    
    def similarity_score(self, matrix1: List[List[float]], matrix2: List[List[float]]) -> float:
        """
        Compute a normalized similarity score between two graph matrices.
        
        Args:
            matrix1 (List[List[float]]): First graph's adjacency matrix
            matrix2 (List[List[float]]): Second graph's adjacency matrix
        
        Returns:
            float: Similarity score between 0 and 1 (1 = identical, 0 = maximally different)
        """
        distance = self.compute(matrix1, matrix2)
        max_distance = self._calculate_max_possible_distance(matrix1, matrix2)
        
        # Normalize the distance
        return 1.0 - (distance / max_distance) if max_distance > 0 else 1.0
    
    def _validate_matrices(self, matrix1: List[List[float]], matrix2: List[List[float]]) -> bool:
        """
        Validate that input matrices are square and have consistent dimensions.
        
        Args:
            matrix1 (List[List[float]]): First matrix to validate
            matrix2 (List[List[float]]): Second matrix to validate
        
        Returns:
            bool: True if matrices are valid, False otherwise
        """
        return (
            all(len(row) == len(matrix1) for row in matrix1) and
            all(len(row) == len(matrix2) for row in matrix2) and
            len(matrix1) == len(matrix2)
        )
    
    def _calculate_max_possible_distance(self, matrix1: List[List[float]], matrix2: List[List[float]]) -> float:
        """
        Calculate the maximum possible edit distance between two matrices.
        
        Args:
            matrix1 (List[List[float]]): First matrix
            matrix2 (List[List[float]]): Second matrix
        
        Returns:
            float: Maximum possible edit distance
        """
        n1, n2 = len(matrix1), len(matrix2)
        
        # Maximum node edit cost
        max_node_cost = abs(n1 - n2) * self.node_cost
        
        # Maximum edge edit cost (complete graph)
        max_edge_count = (max(n1, n2) * (max(n1, n2) - 1)) // 2
        max_edge_cost = max_edge_count * self.edge_cost
        
        return max_node_cost + max_edge_cost


    
from typing import List, Dict, Set, Tuple, Union
from collections import defaultdict
from hashlib import sha256

class WeisfeilerLehman(Distance):
    """
    A class to compute the Weisfeiler-Lehman distance between two matrices.
    This implementation treats matrices as adjacency matrices of graphs and compares their
    structural similarities using the Weisfeiler-Lehman graph kernel algorithm.
    
    The WL algorithm works by iteratively:
    1. Aggregating neighborhood information for each node
    2. Hashing the aggregated information to create new labels
    3. Comparing the resulting label distributions
    """

    def __init__(self, num_iterations: int = 3):
        """
        Initialize the Weisfeiler-Lehman Distance calculator.
        
        Args:
            num_iterations (int): Number of WL iterations to perform.
                                Higher values capture more global structure.
        """
        super().__init__()
        self.type='matrix_float'
        
        self.num_iterations = num_iterations

    def _matrix_to_adjacency_list(self, matrix: List[List[float]]) -> Dict[int, Set[int]]:
        """
        Convert a matrix to an adjacency list representation.
        
        Args:
            matrix (List[List[float]]): Input matrix
            
        Returns:
            Dict[int, Set[int]]: Adjacency list representation
        """
        adj_list = defaultdict(set)
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != 0:
                    adj_list[i].add(j)
        return adj_list

    def _hash_label(self, label: str) -> str:
        """
        Create a compressed hash of a label string.
        
        Args:
            label (str): Input label
            
        Returns:
            str: Hashed label
        """
        return sha256(label.encode()).hexdigest()[:8]

    def _get_neighborhood_label(self, 
                              node: int, 
                              adj_list: Dict[int, Set[int]], 
                              labels: Dict[int, str]) -> str:
        """
        Compute the neighborhood label for a node.
        
        Args:
            node (int): Target node
            adj_list (Dict[int, Set[int]]): Adjacency list of the graph
            labels (Dict[int, str]): Current node labels
            
        Returns:
            str: Combined neighborhood label
        """
        neighbor_labels = sorted([labels[neighbor] for neighbor in adj_list[node]])
        return f"{labels[node]}_{'_'.join(neighbor_labels)}"

    def _wl_iteration(self, 
                     adj_list: Dict[int, Set[int]], 
                     labels: Dict[int, str]) -> Dict[int, str]:
        """
        Perform one iteration of the WL algorithm.
        
        Args:
            adj_list (Dict[int, Set[int]]): Adjacency list of the graph
            labels (Dict[int, str]): Current node labels
            
        Returns:
            Dict[int, str]: Updated node labels
        """
        new_labels = {}
        for node in adj_list:
            neighborhood_label = self._get_neighborhood_label(node, adj_list, labels)
            new_labels[node] = self._hash_label(neighborhood_label)
        return new_labels

    def _get_label_distribution(self, labels: Dict[int, str]) -> Dict[str, int]:
        """
        Compute the distribution of labels in the graph.
        
        Args:
            labels (Dict[int, str]): Node labels
            
        Returns:
            Dict[str, int]: Frequency of each label
        """
        distribution = defaultdict(int)
        for label in labels.values():
            distribution[label] += 1
        return distribution

    def _compare_distributions(self, 
                             dist1: Dict[str, int], 
                             dist2: Dict[str, int]) -> float:
        """
        Compare two label distributions using L1 distance.
        
        Args:
            dist1 (Dict[str, int]): First label distribution
            dist2 (Dict[str, int]): Second label distribution
            
        Returns:
            float: Distance between distributions
        """
        all_labels = set(dist1.keys()) | set(dist2.keys())
        return sum(abs(dist1.get(label, 0) - dist2.get(label, 0)) for label in all_labels)

    def compute(self, A: List[List[float]], B: List[List[float]]) -> float:
        """
        Compute the Weisfeiler-Lehman distance between two matrices.
        
        Args:
            A (List[List[float]]): First matrix
            B (List[List[float]]): Second matrix
            
        Returns:
            float: Weisfeiler-Lehman distance between A and B
        """
        # Convert matrices to adjacency lists
        adj_list_A = self._matrix_to_adjacency_list(A)
        adj_list_B = self._matrix_to_adjacency_list(B)
        
        # Initialize labels with degree information
        labels_A = {node: str(len(neighbors)) for node, neighbors in adj_list_A.items()}
        labels_B = {node: str(len(neighbors)) for node, neighbors in adj_list_B.items()}
        
        total_distance = 0.0
        
        # Perform WL iterations
        for _ in range(self.num_iterations):
            # Update labels
            labels_A = self._wl_iteration(adj_list_A, labels_A)
            labels_B = self._wl_iteration(adj_list_B, labels_B)
            
            # Compare label distributions
            dist_A = self._get_label_distribution(labels_A)
            dist_B = self._get_label_distribution(labels_B)
            
            # Accumulate distances
            iteration_distance = self._compare_distributions(dist_A, dist_B)
            total_distance += iteration_distance
        
        # Normalize by number of iterations
        return total_distance / self.num_iterations


from typing import List, Dict, Set, Tuple
from collections import defaultdict
from statistics import mean, median
from math import sqrt

class NetSimile(Distance):
    """
    Implementation of NetSimile distance measure for graphs/networks represented as matrices.
    NetSimile computes the similarity between networks based on local structural features:
    - Node degree
    - Clustering coefficient
    - Average neighbor degree
    - Number of edges in ego network
    - Average clustering of neighbors
    
    For each feature, it computes 7 aggregated values:
    - Median
    - Mean
    - Standard deviation
    - Skewness
    - Kurtosis
    - 90th percentile
    - Number of non-zero values
    """

    def __init__(self):
        """Initialize the NetSimile distance calculator."""
        super().__init__()
        self.type='matrix_float'

    def _matrix_to_adjacency_list(self, matrix: List[List[float]]) -> Dict[int, Set[int]]:
        """
        Convert an adjacency matrix to an adjacency list.
        
        Args:
            matrix (List[List[float]]): Input adjacency matrix
            
        Returns:
            Dict[int, Set[int]]: Adjacency list representation
        """
        adj_list = defaultdict(set)
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != 0:
                    adj_list[i].add(j)
        return adj_list

    def _get_node_degree(self, node: int, adj_list: Dict[int, Set[int]]) -> int:
        """
        Calculate the degree of a node.
        
        Args:
            node (int): Target node
            adj_list (Dict[int, Set[int]]): Adjacency list
            
        Returns:
            int: Node degree
        """
        return len(adj_list[node])

    def _get_clustering_coefficient(self, node: int, adj_list: Dict[int, Set[int]]) -> float:
        """
        Calculate the clustering coefficient of a node.
        
        Args:
            node (int): Target node
            adj_list (Dict[int, Set[int]]): Adjacency list
            
        Returns:
            float: Clustering coefficient
        """
        neighbors = adj_list[node]
        if len(neighbors) < 2:
            return 0.0
        
        possible_edges = len(neighbors) * (len(neighbors) - 1) / 2
        actual_edges = 0
        
        for neighbor1 in neighbors:
            for neighbor2 in neighbors:
                if neighbor1 < neighbor2 and neighbor2 in adj_list[neighbor1]:
                    actual_edges += 1
        
        return actual_edges / possible_edges if possible_edges > 0 else 0.0

    def _get_average_neighbor_degree(self, node: int, adj_list: Dict[int, Set[int]]) -> float:
        """
        Calculate the average degree of node's neighbors.
        
        Args:
            node (int): Target node
            adj_list (Dict[int, Set[int]]): Adjacency list
            
        Returns:
            float: Average neighbor degree
        """
        neighbors = adj_list[node]
        if not neighbors:
            return 0.0
        
        neighbor_degrees = [len(adj_list[neighbor]) for neighbor in neighbors]
        return sum(neighbor_degrees) / len(neighbor_degrees)

    def _get_ego_net_edges(self, node: int, adj_list: Dict[int, Set[int]]) -> int:
        """
        Calculate the number of edges in node's ego network.
        
        Args:
            node (int): Target node
            adj_list (Dict[int, Set[int]]): Adjacency list
            
        Returns:
            int: Number of edges in ego network
        """
        ego_net = {node} | adj_list[node]
        edge_count = 0
        
        for v in ego_net:
            for u in adj_list[v]:
                if u in ego_net and v < u:  # Count each edge only once
                    edge_count += 1
        
        return edge_count

    def _compute_statistics(self, values: List[float]) -> List[float]:
        """
        Compute the seven statistical measures for a feature.
        
        Args:
            values (List[float]): List of feature values
            
        Returns:
            List[float]: Seven statistical measures
        """
        if not values:
            return [0.0] * 7
        
        n = len(values)
        mean_val = mean(values)
        
        # Standard deviation
        variance = sum((x - mean_val) ** 2 for x in values) / n
        std_dev = sqrt(variance)
        
        # Skewness
        if std_dev == 0:
            skewness = 0
        else:
            skewness = sum((x - mean_val) ** 3 for x in values) / (n * std_dev ** 3)
        
        # Kurtosis
        if std_dev == 0:
            kurtosis = 0
        else:
            kurtosis = sum((x - mean_val) ** 4 for x in values) / (n * std_dev ** 4)
        
        # 90th percentile
        sorted_values = sorted(values)
        idx_90 = int(0.9 * (n - 1))
        percentile_90 = sorted_values[idx_90]
        
        # Number of non-zero values
        non_zero = sum(1 for x in values if x != 0)
        
        return [
            median(values),
            mean_val,
            std_dev,
            skewness,
            kurtosis,
            percentile_90,
            non_zero
        ]

    def _extract_features(self, adj_list: Dict[int, Set[int]]) -> List[List[float]]:
        """
        Extract all features for all nodes.
        
        Args:
            adj_list (Dict[int, Set[int]]): Adjacency list
            
        Returns:
            List[List[float]]: Feature matrix
        """
        features = []
        for node in adj_list:
            node_features = []
            
            # Degree
            degree = self._get_node_degree(node, adj_list)
            node_features.append(degree)
            
            # Clustering coefficient
            clustering = self._get_clustering_coefficient(node, adj_list)
            node_features.append(clustering)
            
            # Average neighbor degree
            avg_neighbor_degree = self._get_average_neighbor_degree(node, adj_list)
            node_features.append(avg_neighbor_degree)
            
            # Ego network edges
            ego_edges = self._get_ego_net_edges(node, adj_list)
            node_features.append(ego_edges)
            
            features.append(node_features)
        
        return features

    def _compute_signature(self, features: List[List[float]]) -> List[float]:
        """
        Compute the NetSimile signature from features.
        
        Args:
            features (List[List[float]]): Feature matrix
            
        Returns:
            List[float]: Network signature
        """
        signature = []
        n_features = len(features[0])
        
        # For each feature
        for i in range(n_features):
            feature_values = [node[i] for node in features]
            # Compute statistics and extend signature
            signature.extend(self._compute_statistics(feature_values))
        
        return signature

    def _canberra_distance(self, signature1: List[float], signature2: List[float]) -> float:
        """
        Compute Canberra distance between two signatures.
        
        Args:
            signature1 (List[float]): First signature
            signature2 (List[float]): Second signature
            
        Returns:
            float: Canberra distance
        """
        distance = 0.0
        for x, y in zip(signature1, signature2):
            if x == 0 and y == 0:
                continue
            distance += abs(x - y) / (abs(x) + abs(y))
        return distance

    def compute(self, A: List[List[float]], B: List[List[float]]) -> float:
        """
        Compute the NetSimile distance between two networks represented as matrices.
        
        Args:
            A (List[List[float]]): First adjacency matrix
            B (List[List[float]]): Second adjacency matrix
            
        Returns:
            float: NetSimile distance between the networks
        """
        # Convert matrices to adjacency lists
        adj_list_A = self._matrix_to_adjacency_list(A)
        adj_list_B = self._matrix_to_adjacency_list(B)
        
        # Extract features
        features_A = self._extract_features(adj_list_A)
        features_B = self._extract_features(adj_list_B)
        
        # Compute signatures
        signature_A = self._compute_signature(features_A)
        signature_B = self._compute_signature(features_B)
        
        # Calculate distance between signatures
        return self._canberra_distance(signature_A, signature_B)


from typing import List, Set, Dict, Tuple
from collections import defaultdict

class PatternBased(Distance):
    """
    Implementation of Pattern-based distance measure for matrices.
    This measure identifies and compares local structural patterns between matrices.
    It focuses on:
    - Structural motifs (repeating patterns)
    - Local connectivity patterns
    - Submatrix patterns
    - Pattern frequency distributions
    
    The algorithm works by:
    1. Extracting local patterns of specified size
    2. Computing pattern frequencies
    3. Comparing pattern distributions
    """

    def __init__(self, pattern_size: int = 2):
        """
        Initialize the Pattern-based distance calculator.
        
        Args:
            pattern_size (int): Size of local patterns to extract (default: 2)
        """
        super().__init__()
        self.type='matrix_float'
        
        self.pattern_size = pattern_size

    def _extract_pattern(self, 
                        matrix: List[List[float]], 
                        row: int, 
                        col: int) -> Tuple[Tuple[float, ...], ...]:
        """
        Extract a local pattern from the matrix starting at given position.
        
        Args:
            matrix (List[List[float]]): Input matrix
            row (int): Starting row
            col (int): Starting column
            
        Returns:
            Tuple[Tuple[float, ...]]: Pattern as a tuple of tuples for hashability
        """
        pattern = []
        n = len(matrix)
        m = len(matrix[0])
        
        for i in range(self.pattern_size):
            if row + i >= n:
                return tuple()
            
            row_pattern = []
            for j in range(self.pattern_size):
                if col + j >= m:
                    return tuple()
                row_pattern.append(matrix[row + i][col + j])
            pattern.append(tuple(row_pattern))
            
        return tuple(pattern)

    def _get_pattern_signature(self, pattern: Tuple[Tuple[float, ...], ...]) -> str:
        """
        Convert a pattern to a canonical string representation.
        This helps identify equivalent patterns regardless of exact values.
        
        Args:
            pattern (Tuple[Tuple[float, ...]]): Input pattern
            
        Returns:
            str: Pattern signature
        """
        if not pattern:
            return ""
            
        # Create value mapping for normalization
        value_map = {}
        next_value = 0
        signature_parts = []
        
        for row in pattern:
            row_sig = []
            for val in row:
                if val not in value_map:
                    value_map[val] = str(next_value)
                    next_value += 1
                row_sig.append(value_map[val])
            signature_parts.append('_'.join(row_sig))
        
        return '|'.join(signature_parts)

    def _extract_all_patterns(self, matrix: List[List[float]]) -> Dict[str, int]:
        """
        Extract all patterns from the matrix and count their frequencies.
        
        Args:
            matrix (List[List[float]]): Input matrix
            
        Returns:
            Dict[str, int]: Pattern frequency distribution
        """
        pattern_counts = defaultdict(int)
        n = len(matrix)
        m = len(matrix[0])
        
        for i in range(n - self.pattern_size + 1):
            for j in range(m - self.pattern_size + 1):
                pattern = self._extract_pattern(matrix, i, j)
                if pattern:
                    signature = self._get_pattern_signature(pattern)
                    pattern_counts[signature] += 1
                    
        return pattern_counts

    def _normalize_distribution(self, distribution: Dict[str, int]) -> Dict[str, float]:
        """
        Normalize pattern frequency distribution.
        
        Args:
            distribution (Dict[str, int]): Pattern frequency counts
            
        Returns:
            Dict[str, float]: Normalized distribution
        """
        total = sum(distribution.values())
        if total == 0:
            return {}
        
        return {k: v / total for k, v in distribution.items()}

    def _compute_correlation_distance(self, 
                                   dist1: Dict[str, float], 
                                   dist2: Dict[str, float]) -> float:
        """
        Compute correlation-based distance between pattern distributions.
        
        Args:
            dist1 (Dict[str, float]): First distribution
            dist2 (Dict[str, float]): Second distribution
            
        Returns:
            float: Distance between distributions
        """
        # Get all patterns
        all_patterns = set(dist1.keys()) | set(dist2.keys())
        
        # Convert to vectors
        vec1 = [dist1.get(p, 0.0) for p in all_patterns]
        vec2 = [dist2.get(p, 0.0) for p in all_patterns]
        
        # Compute correlation coefficient
        n = len(vec1)
        if n == 0:
            return 1.0
            
        mean1 = sum(vec1) / n
        mean2 = sum(vec2) / n
        
        numerator = sum((x - mean1) * (y - mean2) for x, y in zip(vec1, vec2))
        denom1 = sum((x - mean1) ** 2 for x in vec1)
        denom2 = sum((y - mean2) ** 2 for y in vec2)
        
        if denom1 == 0 or denom2 == 0:
            return 1.0
            
        correlation = numerator / ((denom1 * denom2) ** 0.5)
        
        # Convert correlation to distance (1 - correlation) / 2
        # This ensures distance is between 0 and 1
        return (1 - correlation) / 2

    def _compute_jaccard_distance(self, 
                                dist1: Dict[str, float], 
                                dist2: Dict[str, float]) -> float:
        """
        Compute Jaccard distance between pattern sets.
        
        Args:
            dist1 (Dict[str, float]): First distribution
            dist2 (Dict[str, float]): Second distribution
            
        Returns:
            float: Jaccard distance
        """
        patterns1 = set(dist1.keys())
        patterns2 = set(dist2.keys())
        
        intersection = len(patterns1 & patterns2)
        union = len(patterns1 | patterns2)
        
        if union == 0:
            return 0.0
            
        return 1 - (intersection / union)

    def compute(self, 
                        A: List[List[float]], 
                        B: List[List[float]], 
                        method: str = "correlation") -> float:
        """
        Compute the Pattern-based distance between two matrices.
        
        Args:
            A (List[List[float]]): First matrix
            B (List[List[float]]): Second matrix
            method (str): Distance method - "correlation" or "jaccard"
            
        Returns:
            float: Pattern-based distance between matrices
        """
        # Extract patterns and their frequencies
        patterns_A = self._extract_all_patterns(A)
        patterns_B = self._extract_all_patterns(B)
        
        # Normalize distributions
        norm_dist_A = self._normalize_distribution(patterns_A)
        norm_dist_B = self._normalize_distribution(patterns_B)
        
        # Compute distance based on selected method
        if method == "jaccard":
            return self._compute_jaccard_distance(norm_dist_A, norm_dist_B)
        else:  # correlation
            return self._compute_correlation_distance(norm_dist_A, norm_dist_B)
from typing import List, Set, Dict, Tuple
from itertools import combinations

class CliqueBasedGraph(Distance):
    """
    Calculates graph distance using clique-based structural comparison.
    
    Focuses on analyzing maximal cliques and their overlap between graphs.
    """
    
    def __init__(self, node_weight: float = 1.0, clique_weight: float = 2.0):
        """
        Initialize the Clique-Based Graph Distance calculator.
        
        Args:
            node_weight (float): Weight for node differences. Defaults to 1.0
            clique_weight (float): Weight for clique structure differences. Defaults to 2.0
        """
        super().__init__()
        self.type='matrix_float'
        
        self.node_weight = node_weight
        self.clique_weight = clique_weight
    
    def compute(self, graph1: List[List[float]], graph2: List[List[float]]) -> float:
        """
        Compute graph distance based on clique structure.
        
        Args:
            graph1 (List[List[float]]): First graph adjacency matrix
            graph2 (List[List[float]]): Second graph adjacency matrix
        
        Returns:
            float: Calculated graph distance
        """
        self._validate_matrices(graph1, graph2)
        
        # Find maximal cliques in both graphs
        cliques1 = self._find_maximal_cliques(graph1)
        cliques2 = self._find_maximal_cliques(graph2)
        
        # Calculate distance components
        node_distance = self._compute_node_distance(graph1, graph2)
        clique_distance = self._compute_clique_distance(cliques1, cliques2)
        
        return node_distance + clique_distance
    
    def _validate_matrices(self, graph1: List[List[float]], graph2: List[List[float]]) -> None:
        """
        Validate input graph matrices.
        
        Args:
            graph1 (List[List[float]]): First graph matrix
            graph2 (List[List[float]]): Second graph matrix
        
        Raises:
            ValueError: If matrices are invalid
        """
        if not (
            all(len(row) == len(graph1) for row in graph1) and
            all(len(row) == len(graph2) for row in graph2)
        ):
            raise ValueError("Input matrices must be square")
    
    def _find_maximal_cliques(self, graph: List[List[float]]) -> List[Set[int]]:
        """
        Find all maximal cliques in the graph using Bron-Kerbosch algorithm.
        
        Args:
            graph (List[List[float]]): Graph adjacency matrix
        
        Returns:
            List[Set[int]]: List of maximal cliques
        """
        def is_clique(nodes: Set[int]) -> bool:
            """Check if given nodes form a complete subgraph."""
            return all(
                graph[u][v] > 0 
                for u, v in combinations(nodes, 2)
                if u != v
            )
        
        def bron_kerbosch(r: Set[int], p: Set[int], x: Set[int]) -> None:
            """
            Recursive Bron-Kerbosch algorithm for finding maximal cliques.
            
            Args:
                r (Set[int]): Current clique being built
                p (Set[int]): Potential nodes to add
                x (Set[int]): Excluded nodes
            """
            if not p and not x:
                if is_clique(r):
                    maximal_cliques.append(r)
                return
            
            for v in list(p):
                new_r = r.union({v})
                new_p = p.intersection(set(
                    u for u in range(len(graph)) 
                    if graph[v][u] > 0 and u in p
                ))
                new_x = x.intersection(set(
                    u for u in range(len(graph)) 
                    if graph[v][u] > 0 and u in x
                ))
                
                bron_kerbosch(new_r, new_p, new_x)
                p.remove(v)
                x.add(v)
        
        # Initialize variables
        maximal_cliques: List[Set[int]] = []
        nodes = set(range(len(graph)))
        
        # Run Bron-Kerbosch algorithm
        bron_kerbosch(set(), nodes, set())
        
        return maximal_cliques
    
    def _compute_node_distance(self, 
                                graph1: List[List[float]], 
                                graph2: List[List[float]]) -> float:
        """
        Calculate distance based on node differences.
        
        Args:
            graph1 (List[List[float]]): First graph matrix
            graph2 (List[List[float]]): Second graph matrix
        
        Returns:
            float: Node-based distance
        """
        n1, n2 = len(graph1), len(graph2)
        return abs(n1 - n2) * self.node_weight
    
    def _compute_clique_distance(self, 
                                  cliques1: List[Set[int]], 
                                  cliques2: List[Set[int]]) -> float:
        """
        Calculate distance based on clique structure differences.
        
        Args:
            cliques1 (List[Set[int]]): Maximal cliques of first graph
            cliques2 (List[Set[int]]): Maximal cliques of second graph
        
        Returns:
            float: Clique structure distance
        """
        # Compute clique matching and differences
        matched_cliques = 0
        total_cliques = len(cliques1) + len(cliques2)
        
        for c1 in cliques1:
            for c2 in cliques2:
                # Compute clique similarity
                overlap = len(c1.intersection(c2)) / max(len(c1), len(c2))
                if overlap > 0.5:  # Threshold for matching
                    matched_cliques += 1
                    break
        
        # Calculate clique distance
        unmatched_cliques = total_cliques - (2 * matched_cliques)
        return unmatched_cliques * self.clique_weight
    
    def similarity_score(self, graph1: List[List[float]], graph2: List[List[float]]) -> float:
        """
        Compute a similarity score between 0 and 1.
        
        Args:
            graph1 (List[List[float]]): First graph adjacency matrix
            graph2 (List[List[float]]): Second graph adjacency matrix
        
        Returns:
            float: Similarity score (1 = identical, 0 = completely different)
        """
        distance = self.compute(graph1, graph2)
        max_distance = self._compute_max_distance(graph1, graph2)
        
        return 1.0 - (distance / max_distance) if max_distance > 0 else 1.0
    
    def _compute_max_distance(self, 
                               graph1: List[List[float]], 
                               graph2: List[List[float]]) -> float:
        """
        Calculate maximum possible distance between graphs.
        
        Args:
            graph1 (List[List[float]]): First graph matrix
            graph2 (List[List[float]]): Second graph matrix
        
        Returns:
            float: Maximum possible distance
        """
        n1, n2 = len(graph1), len(graph2)
        max_node_diff = abs(n1 - n2)
        max_clique_count = max(len(self._find_maximal_cliques(graph1)), 
                               len(self._find_maximal_cliques(graph2)))
        
        return (max_node_diff * self.node_weight + 
                max_clique_count * self.clique_weight)

from typing import List, TypeVar, Union
from math import sqrt

T = TypeVar('T', int, float)

class CycleMatrixDistance(Distance):
    """
    A class to calculate distance between matrices based on cycle detection.
    
    The distance is computed by analyzing the cyclic patterns in matrix transformations.
    Supports integer and float matrix elements.
    """
    
    def __init__(self, matrix1: List[List[T]], matrix2: List[List[T]]):
        """
        Initialize the distance calculator with two matrices.
        
        Args:
            matrix1 (List[List[T]]): First input matrix 
            matrix2 (List[List[T]]): Second input matrix
        
        Raises:
            ValueError: If matrices have different dimensions
        """
        super().__init__()
        self.type='matrix_float'
        
        self._validate_matrices(matrix1, matrix2)
        self.matrix1 = matrix1
        self.matrix2 = matrix2
        self.rows = len(matrix1)
        self.cols = len(matrix1[0])
    
    def _validate_matrices(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> None:
        """
        Validate that both matrices have the same dimensions.
        
        Args:
            matrix1 (List[List[T]]): First matrix to validate
            matrix2 (List[List[T]]): Second matrix to validate
        
        Raises:
            ValueError: If matrices have different dimensions
        """
        if len(matrix1) != len(matrix2):
            raise ValueError("Matrices must have the same number of rows")
        
        if len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same number of columns")
    
    def _detect_local_cycles(self, tolerance: float = 1e-6) -> List[List[int]]:
        """
        Detect local cyclic patterns between corresponding matrix elements.
        
        Args:
            tolerance (float): Precision threshold for cycle detection
        
        Returns:
            List[List[int]]: Cycle lengths for each matrix element
        """
        cycle_map: List[List[int]] = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        for i in range(self.rows):
            for j in range(self.cols):
                # Compare elements and detect cycle length
                current = self.matrix1[i][j]
                target = self.matrix2[i][j]
                
                if abs(current - target) <= tolerance:
                    cycle_map[i][j] = 0
                else:
                    # Estimate cycle length based on element differences
                    cycle_length = int(abs(target - current) * 100)
                    cycle_map[i][j] = max(1, cycle_length)
        
        return cycle_map
    
    def compute(self, tolerance: float = 1e-6) -> float:
        """
        Compute the distance between matrices based on cycle detection.
        
        Args:
            tolerance (float): Precision threshold for cycle detection
        
        Returns:
            float: Calculated distance representing cyclic transformation complexity
        """
        cycle_map = self._detect_local_cycles(tolerance)
        
        # Compute total cycle complexity
        total_cycle_complexity = sum(
            sum(row) for row in cycle_map
        )
        
        # Normalize distance using root mean square
        matrix_size = self.rows * self.cols
        normalized_distance = sqrt(total_cycle_complexity / matrix_size)
        
        return normalized_distance
    
    def __str__(self) -> str:
        """
        Provide a string representation of the distance calculation.
        
        Returns:
            str: Descriptive string of cycle matrix distance
        """
        distance = self.compute()
        return f"Cycle Matrix Distance: {distance:.4f}"
from typing import List, TypeVar, Union
from math import sqrt, acos, pi

T = TypeVar('T', int, float)

class TriangleMatrixDistance(Distance):
    """
    A class to calculate distance between matrices based on triangular transformations.
    
    The distance is computed by analyzing triangular patterns and angle variations
    between corresponding matrix elements.
    """
    
    def __init__(self, matrix1: List[List[T]], matrix2: List[List[T]]):
        """
        Initialize the distance calculator with two matrices.
        
        Args:
            matrix1 (List[List[T]]): First input matrix 
            matrix2 (List[List[T]]): Second input matrix
        
        Raises:
            ValueError: If matrices have different dimensions
        """
        super().__init__()
        self.type='matrix_float'
        
        self._validate_matrices(matrix1, matrix2)
        self.matrix1 = matrix1
        self.matrix2 = matrix2
        self.rows = len(matrix1)
        self.cols = len(matrix1[0])
    
    def _validate_matrices(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> None:
        """
        Validate that both matrices have the same dimensions.
        
        Args:
            matrix1 (List[List[T]]): First matrix to validate
            matrix2 (List[List[T]]): Second matrix to validate
        
        Raises:
            ValueError: If matrices have different dimensions
        """
        if len(matrix1) != len(matrix2):
            raise ValueError("Matrices must have the same number of rows")
        
        if len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same number of columns")
    
    def _compute_triangle_angle(self, a: T, b: T, c: T) -> float:
        """
        Compute the angle of a triangle formed by three matrix elements.
        
        Args:
            a (T): First element
            b (T): Second element
            c (T): Third element
        
        Returns:
            float: Angle in radians between the triangle's sides
        """
        # Prevent division by zero and handle very small values
        a, b, c = abs(float(a)), abs(float(b)), abs(float(c))
        
        # Avoid invalid triangle configurations
        if a + b <= c or a + c <= b or b + c <= a:
            return 0.0
        
        # Compute the cosine of the angle using the law of cosines
        cos_angle = (a**2 + b**2 - c**2) / (2 * a * b)
        
        # Ensure cos_angle is within valid range [-1, 1]
        cos_angle = max(min(cos_angle, 1), -1)
        
        return acos(cos_angle)
    
    def compute(self, window_size: int = 3, tolerance: float = 1e-6) -> float:
        """
        Compute the distance between matrices based on triangular patterns.
        
        Args:
            window_size (int): Size of the sliding window for triangle computation
            tolerance (float): Precision threshold for comparisons
        
        Returns:
            float: Calculated distance representing triangular transformation complexity
        """
        if window_size < 3:
            raise ValueError("Window size must be at least 3")
        
        total_triangle_angles = 0.0
        total_windows = 0
        
        # Slide the window across the matrix
        for i in range(self.rows - window_size + 1):
            for j in range(self.cols - window_size + 1):
                # Compute triangle angles for corresponding windows
                window1_angles = self._compute_window_angles(
                    self.matrix1, i, j, window_size
                )
                window2_angles = self._compute_window_angles(
                    self.matrix2, i, j, window_size
                )
                
                # Compare window angles
                window_distance = self._compare_window_angles(
                    window1_angles, window2_angles, tolerance
                )
                
                total_triangle_angles += window_distance
                total_windows += 1
        
        # Normalize the distance
        return sqrt(total_triangle_angles / total_windows) if total_windows > 0 else 0.0
    
    def _compute_window_angles(self, matrix: List[List[T]], row: int, col: int, 
                                window_size: int) -> List[float]:
        """
        Compute triangle angles for a specific matrix window.
        
        Args:
            matrix (List[List[T]]): Source matrix
            row (int): Starting row of the window
            col (int): Starting column of the window
            window_size (int): Size of the sliding window
        
        Returns:
            List[float]: Angles of triangles within the window
        """
        angles = []
        
        # Compute all possible triangle angles within the window
        for i in range(window_size):
            for j in range(i + 1, window_size):
                for k in range(j + 1, window_size):
                    a = matrix[row + i][col + j]
                    b = matrix[row + i][col + k]
                    c = matrix[row + j][col + k]
                    
                    angle = self._compute_triangle_angle(a, b, c)
                    angles.append(angle)
        
        return angles
    
    def _compare_window_angles(self, angles1: List[float], 
                                angles2: List[float], 
                                tolerance: float) -> float:
        """
        Compare triangle angles between two matrix windows.
        
        Args:
            angles1 (List[float]): Angles from first matrix window
            angles2 (List[float]): Angles from second matrix window
            tolerance (float): Precision threshold for comparisons
        
        Returns:
            float: Distance between window angle configurations
        """
        if len(angles1) != len(angles2):
            return float('inf')
        
        # Compute angle differences
        angle_differences = [
            abs(a1 - a2) for a1, a2 in zip(sorted(angles1), sorted(angles2))
        ]
        
        # Compute root mean square of angle differences
        return sqrt(
            sum(diff**2 for diff in angle_differences) / len(angle_differences)
        )
    
    def __str__(self) -> str:
        """
        Provide a string representation of the distance calculation.
        
        Returns:
            str: Descriptive string of triangle matrix distance
        """
        distance = self.compute()
        return f"Triangle Matrix Distance: {distance:.4f}"

from typing import List, TypeVar, Dict, Set, Tuple
from math import sqrt, log

T = TypeVar('T', int, float)

class GraphletMatrixDistance(Distance):
    """
    A class to calculate distance between matrices based on graphlet distribution.
    
    Computes matrix similarity by analyzing the distribution of local graph structures
    (graphlets) within the matrix as an adjacency representation.
    """
    
    def __init__(self, matrix1: List[List[T]], matrix2: List[List[T]]):
        """
        Initialize the distance calculator with two matrices.
        
        Args:
            matrix1 (List[List[T]]): First input matrix as adjacency matrix
            matrix2 (List[List[T]]): Second input matrix as adjacency matrix
        
        Raises:
            ValueError: If matrices are not square or have different dimensions
        """
        super().__init__()
        self.type='matrix_float'
        
        self._validate_matrices(matrix1, matrix2)
        self.matrix1 = matrix1
        self.matrix2 = matrix2
        self.size = len(matrix1)
    
    def _validate_matrices(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> None:
        """
        Validate matrix properties: square matrices of same size.
        
        Args:
            matrix1 (List[List[T]]): First matrix to validate
            matrix2 (List[List[T]]): Second matrix to validate
        
        Raises:
            ValueError: If matrices are invalid
        """
        if not all(len(row) == len(matrix1) for row in matrix1):
            raise ValueError("Matrix 1 must be square")
        
        if not all(len(row) == len(matrix2) for row in matrix2):
            raise ValueError("Matrix 2 must be square")
        
        if len(matrix1) != len(matrix2):
            raise ValueError("Matrices must have the same dimensions")
    
    def _count_graphlets(self, matrix: List[List[T]]) -> Dict[str, int]:
        """
        Count different types of local graph structures (graphlets).
        
        Args:
            matrix (List[List[T]]): Adjacency matrix to analyze
        
        Returns:
            Dict[str, int]: Counts of different graphlet types
        """
        graphlets: Dict[str, int] = {
            'isolated_node': 0,   # 0-node
            'single_edge': 0,     # 1-edge 
            'triangle': 0,         # 3-node complete
            'star': 0,             # Star-like structure
            'path': 0              # Linear path
        }
        
        # Find total graph structures
        for i in range(self.size):
            # Isolated node check
            if sum(1 for j in range(self.size) if matrix[i][j] != 0) == 0:
                graphlets['isolated_node'] += 1
            
            for j in range(i+1, self.size):
                # Check for edges
                if matrix[i][j] != 0:
                    graphlets['single_edge'] += 1
                    
                    # Path and star detection
                    for k in range(j+1, self.size):
                        if matrix[j][k] != 0:
                            graphlets['path'] += 1
                        
                        # Triangle detection
                        if matrix[i][k] != 0:
                            graphlets['triangle'] += 1
                            
                        # Star detection
                        if matrix[i][k] != 0 and matrix[j][k] != 0:
                            graphlets['star'] += 1
        
        return graphlets
    
    def compute(self, normalize: bool = True) -> float:
        """
        Compute the distance between matrices based on graphlet distribution.
        
        Args:
            normalize (bool): Whether to normalize the distance
        
        Returns:
            float: Calculated distance representing graphlet distribution difference
        """
        # Count graphlets for both matrices
        graphlets1 = self._count_graphlets(self.matrix1)
        graphlets2 = self._count_graphlets(self.matrix2)
        
        # Compute Jensen-Shannon divergence between graphlet distributions
        js_divergence = self._jensen_shannon_divergence(graphlets1, graphlets2)
        
        return sqrt(js_divergence) if normalize else js_divergence
    
    def _jensen_shannon_divergence(self, 
                                    dist1: Dict[str, int], 
                                    dist2: Dict[str, int]) -> float:
        """
        Compute Jensen-Shannon divergence between two graphlet distributions.
        
        Args:
            dist1 (Dict[str, int]): First graphlet distribution
            dist2 (Dict[str, int]): Second graphlet distribution
        
        Returns:
            float: Jensen-Shannon divergence value
        """
        # Total counts for normalization
        total1 = sum(dist1.values())
        total2 = sum(dist2.values())
        
        # Compute probability distributions
        prob1 = {k: v/total1 for k, v in dist1.items()}
        prob2 = {k: v/total2 for k, v in dist2.items()}
        
        # Merge keys from both distributions
        all_keys = set(prob1.keys()) | set(prob2.keys())
        
        # Compute divergence
        js_div = 0.0
        for key in all_keys:
            p1 = prob1.get(key, 0.0)
            p2 = prob2.get(key, 0.0)
            
            # Average probability
            avg_prob = 0.5 * (p1 + p2)
            
            # Compute KL divergence components
            if p1 > 0:
                js_div += p1 * log(p1 / avg_prob)
            if p2 > 0:
                js_div += p2 * log(p2 / avg_prob)
        
        return js_div
    
    def __str__(self) -> str:
        """
        Provide a string representation of the distance calculation.
        
        Returns:
            str: Descriptive string of graphlet matrix distance
        """
        distance = self.compute()
        return f"Graphlet Matrix Distance: {distance:.4f}"
    
    def detailed_graphlet_analysis(self) -> Dict[str, Tuple[int, int]]:
        """
        Provide detailed graphlet distribution comparison.
        
        Returns:
            Dict[str, Tuple[int, int]]: Graphlet counts for both matrices
        """
        graphlets1 = self._count_graphlets(self.matrix1)
        graphlets2 = self._count_graphlets(self.matrix2)
        
        return {
            graphlet: (count1, graphlets2.get(graphlet, 0))
            for graphlet, count1 in graphlets1.items()
        }
from typing import List, TypeVar, Optional
from math import sqrt

T = TypeVar('T', int, float)

class OptimizedMaxFlowMatrixDistance(Distance):
    """
    Optimized matrix distance calculation using maximum flow analysis.
    """
    
    def __init__(self, matrix1: List[List[T]], matrix2: List[List[T]]):
        """
        Initialize distance calculator with improved performance.
        """
        super().__init__()
        self.type='matrix_float'
        
        self._validate_matrices(matrix1, matrix2)
        self.matrix1 = matrix1
        self.matrix2 = matrix2
        self.rows = len(matrix1)
        self.cols = len(matrix1[0])
    
    def _validate_matrices(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> None:
        """
        Quickly validate matrix dimensions.
        """
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have identical dimensions")
    
    def _dinic_max_flow(self, graph: List[List[float]]) -> float:
        """
        Dinic's algorithm for maximum flow - significantly faster
        """
        def bfs() -> bool:
            # Reset levels and queue
            level[:] = [-1] * len(graph)
            level[source] = 0
            queue = [source]
            
            while queue:
                v = queue.pop(0)
                for u in range(len(graph)):
                    if level[u] == -1 and graph[v][u] > 0:
                        level[u] = level[v] + 1
                        queue.append(u)
            
            return level[sink] != -1
        
        def dfs(v: int, flow: float) -> float:
            if v == sink:
                return flow
            
            for u in range(len(graph)):
                residual = graph[v][u]
                if level[u] == level[v] + 1 and residual > 0:
                    curr_flow = dfs(u, min(flow, residual))
                    if curr_flow > 0:
                        graph[v][u] -= curr_flow
                        graph[u][v] += curr_flow
                        return curr_flow
            
            return 0.0
        
        # Graph size and source/sink
        n = self.rows * self.cols + 2
        source, sink = 0, n - 1
        
        # Maximum flow
        max_flow = 0.0
        
        # Level tracking for Dinic's algorithm
        level = [0] * n
        
        while bfs():
            while True:
                path_flow = dfs(source, float('inf'))
                if path_flow == 0:
                    break
                max_flow += path_flow
        
        return max_flow
    
    def _build_fast_flow_network(self, matrix: List[List[T]]) -> List[List[float]]:
        """
        Optimized flow network construction with fixed-size matrix
        """
        n = self.rows * self.cols + 2
        graph = [[0.0] * n for _ in range(n)]
        source, sink = 0, n - 1
        
        # Optimized network construction
        for i in range(self.rows):
            for j in range(self.cols):
                node = i * self.cols + j + 1
                flow_value = abs(float(matrix[i][j]))
                
                # Simplified source and sink connections
                if i == 0:
                    graph[source][node] = flow_value
                if i == self.rows - 1:
                    graph[node][sink] = flow_value
                
                # Layer connections
                if i < self.rows - 1:
                    next_layer_node = (i + 1) * self.cols + j + 1
                    graph[node][next_layer_node] = flow_value
        
        return graph
    
    def compute(self, normalize: bool = True) -> float:
        """
        Compute matrix distance using optimized max flow calculation
        """
        network1 = self._build_fast_flow_network(self.matrix1)
        network2 = self._build_fast_flow_network(self.matrix2)
        
        max_flow1 = self._dinic_max_flow(network1)
        max_flow2 = self._dinic_max_flow(network2.copy())
        
        flow_distance = abs(max_flow1 - max_flow2)
        return sqrt(flow_distance) if normalize else flow_distance

from typing import List, Optional, Tuple

class MinimumCutDistanceCalculator(Distance):
    """
    A class to calculate the minimum cut distance between two matrices.
    
    This implementation provides a method to compute the minimum number of 
    elements that need to be removed to disconnect two matrices.
    """
    
    def __init__(self, matrix1: List[List[int]], matrix2: List[List[int]]):
        """
        Initialize the calculator with two input matrices.
        
        Args:
            matrix1 (List[List[int]]): First input matrix
            matrix2 (List[List[int]]): Second input matrix
        """
        super().__init__()
        self.type='matrix_float'
        
        self._validate_matrices(matrix1, matrix2)
        self.matrix1 = matrix1
        self.matrix2 = matrix2
        self.rows = len(matrix1)
        self.cols = len(matrix1[0])
    
    def _validate_matrices(self, matrix1: List[List[int]], matrix2: List[List[int]]) -> None:
        """
        Validate that the input matrices have the same dimensions.
        
        Raises:
            ValueError: If matrices have different dimensions or are empty
        """
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
        
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same dimensions")
    
    def compute(self) -> int:
        """
        Calculate the minimum cut distance between two matrices.
        
        The minimum cut distance is the minimum number of elements 
        that must be changed to transform matrix1 into matrix2.
        
        Returns:
            int: The minimum number of elements that need to be changed
        """
        cut_distance = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix1[i][j] != self.matrix2[i][j]:
                    cut_distance += 1
        
        return cut_distance
    
    def get_cut_positions(self) -> List[Tuple[int, int]]:
        """
        Get the positions of elements that need to be changed.
        
        Returns:
            List[Tuple[int, int]]: List of (row, col) positions where 
            matrices differ
        """
        cut_positions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix1[i][j] != self.matrix2[i][j]:
                    cut_positions.append((i, j))
        
        return cut_positions
    
    def get_detailed_difference(self) -> Optional[dict]:
        """
        Provide a detailed breakdown of the differences between matrices.
        
        Returns:
            Optional[dict]: A dictionary with detailed difference information
        """
        if self.compute() == 0:
            return None
        
        return {
            "total_cut_distance": self.compute(),
            "cut_positions": self.get_cut_positions(),
            "matrix1_values": [self.matrix1[pos[0]][pos[1]] for pos in self.get_cut_positions()],
            "matrix2_values": [self.matrix2[pos[0]][pos[1]] for pos in self.get_cut_positions()]
        }
from typing import List, Tuple, Set
from enum import Enum
from collections import deque

class PercolationType(Enum):
    """
    Enum to represent different types of percolation connectivity.
    """
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 3

class Percolation(Distance):
    """
    A class to calculate the percolation distance between two matrices.
    
    Percolation distance measures the minimum number of changes required 
    to create a connected path through the matrix.
    """
    
    def __init__(self, matrix1: List[List[int]], matrix2: List[List[int]], 
                 percolation_type: PercolationType = PercolationType.HORIZONTAL):
        """
        Initialize the percolation distance calculator.
        
        Args:
            matrix1 (List[List[int]]): First input matrix
            matrix2 (List[List[int]]): Second input matrix
            percolation_type (PercolationType): Type of percolation connectivity
        """
        super().__init__()
        self.type='matrix_float'
        
        self._validate_matrices(matrix1, matrix2)
        self.matrix1 = matrix1
        self.matrix2 = matrix2
        self.rows = len(matrix1)
        self.cols = len(matrix1[0])
        self.percolation_type = percolation_type
    
    def _validate_matrices(self, matrix1: List[List[int]], matrix2: List[List[int]]) -> None:
        """
        Validate input matrices dimensions.
        
        Raises:
            ValueError: If matrices have different dimensions or are empty
        """
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
        
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same dimensions")
    
    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get neighboring cells based on percolation type.
        
        Args:
            x (int): Row index
            y (int): Column index
        
        Returns:
            List[Tuple[int, int]]: List of neighboring cell coordinates
        """
        neighbors = []
        directions = []
        
        if self.percolation_type == PercolationType.HORIZONTAL:
            directions = [(0, 1), (0, -1)]
        elif self.percolation_type == PercolationType.VERTICAL:
            directions = [(1, 0), (-1, 0)]
        elif self.percolation_type == PercolationType.DIAGONAL:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), 
                          (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                neighbors.append((nx, ny))
        
        return neighbors
    
    def compute(self) -> int:
        """
        Calculate the percolation distance between two matrices.
        
        Returns:
            int: Minimum number of changes to create a percolation path
        """
        changes = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix1[i][j] != self.matrix2[i][j]:
                    changes.append((i, j))
        
        return self._find_minimum_percolation_path(changes)
    
    def _find_minimum_percolation_path(self, changes: List[Tuple[int, int]]) -> int:
        """
        Find the minimum number of changes to create a percolation path.
        
        Args:
            changes (List[Tuple[int, int]]): Positions of different cells
        
        Returns:
            int: Minimum number of changes for percolation
        """
        if not changes:
            return 0
        
        # Try all possible minimal subsets of changes
        min_changes = len(changes)
        
        for k in range(1, len(changes) + 1):
            for subset in self._generate_combinations(changes, k):
                if self._check_percolation_path(subset):
                    min_changes = min(min_changes, k)
                    break
        
        return min_changes
    
    def _check_percolation_path(self, changes: List[Tuple[int, int]]) -> bool:
        """
        Check if a given set of changes creates a percolation path.
        
        Args:
            changes (List[Tuple[int, int]]): Positions to change
        
        Returns:
            bool: True if a percolation path exists, False otherwise
        """
        # Create a modified matrix
        modified_matrix = [row.copy() for row in self.matrix1]
        for x, y in changes:
            modified_matrix[x][y] = self.matrix2[x][y]
        
        # Check for percolation path
        if self.percolation_type == PercolationType.HORIZONTAL:
            return self._check_horizontal_percolation(modified_matrix)
        elif self.percolation_type == PercolationType.VERTICAL:
            return self._check_vertical_percolation(modified_matrix)
        elif self.percolation_type == PercolationType.DIAGONAL:
            return self._check_diagonal_percolation(modified_matrix)
    
    def _check_horizontal_percolation(self, matrix: List[List[int]]) -> bool:
        """
        Check if a horizontal percolation path exists.
        
        Args:
            matrix (List[List[int]]): Modified matrix
        
        Returns:
            bool: True if a horizontal path exists
        """
        for row in matrix:
            if len(set(row)) == 1:
                return True
        return False
    
    def _check_vertical_percolation(self, matrix: List[List[int]]) -> bool:
        """
        Check if a vertical percolation path exists.
        
        Args:
            matrix (List[List[int]]): Modified matrix
        
        Returns:
            bool: True if a vertical path exists
        """
        for j in range(self.cols):
            column = [matrix[i][j] for i in range(self.rows)]
            if len(set(column)) == 1:
                return True
        return False
    
    def _check_diagonal_percolation(self, matrix: List[List[int]]) -> bool:
        """
        Check if a diagonal percolation path exists.
        
        Args:
            matrix (List[List[int]]): Modified matrix
        
        Returns:
            bool: True if a diagonal path exists
        """
        # Check diagonals and anti-diagonals
        for start_row in range(self.rows):
            diagonal1 = [matrix[start_row + i][i] for i in range(min(self.rows - start_row, self.cols))]
            if len(set(diagonal1)) == 1:
                return True
        
        for start_col in range(self.cols):
            diagonal2 = [matrix[i][start_col + i] for i in range(min(self.rows, self.cols - start_col))]
            if len(set(diagonal2)) == 1:
                return True
        
        return False
    
    def _generate_combinations(self, items: List[Tuple[int, int]], k: int) -> List[List[Tuple[int, int]]]:
        """
        Generate all combinations of k items from the list.
        
        Args:
            items (List[Tuple[int, int]]): List of items
            k (int): Number of items to select
        
        Returns:
            List[List[Tuple[int, int]]]: All possible combinations
        """
        def backtrack(start: int, current: List[Tuple[int, int]]):
            if len(current) == k:
                result.append(current.copy())
                return
            
            for i in range(start, len(items)):
                current.append(items[i])
                backtrack(i + 1, current)
                current.pop()
        
        result: List[List[Tuple[int, int]]] = []
        backtrack(0, [])
        return result


from typing import List, Union
from numbers import Number

class VonNeumann(Distance):
    """
    Calculate the Von Neumann distance (Manhattan/L1 distance) between two matrices
    using pure Python lists.
    
    Args:
        matrix1 (List[List[Number]]): First input matrix as list of lists
        matrix2 (List[List[Number]]): Second input matrix as list of lists
    
    Returns:
        float: The Von Neumann distance between the matrices
        
    Raises:
        ValueError: If matrices have different dimensions or are empty
        TypeError: If matrices contain non-numeric values
        
    Examples:
        >>> m1 = [[1, 2], [3, 4]]
        >>> m2 = [[2, 3], [4, 5]]
        >>> von_neumann_distance(m1, m2)
        4.0  # |1-2| + |2-3| + |3-4| + |4-5| = 1 + 1 + 1 + 1 = 4
    """
    
    def __init__(self):
        """
        Initialize the percolation distance calculator.
        
        Args:
            matrix1 (List[List[int]]): First input matrix
            matrix2 (List[List[int]]): Second input matrix
            percolation_type (PercolationType): Type of percolation connectivity
        """
        super().__init__()
        self.type='matrix_float'
    @staticmethod
    def validate(matrix1: List[List[float]], matrix2: List[List[float]]) -> None:
      # Validate matrices dimensions
      if not matrix1 or not matrix2:
        raise ValueError("Matrices cannot be empty")
    
      if len(matrix1) != len(matrix2):
        raise ValueError("Matrices must have the same number of rows")
    
      if len(matrix1[0]) != len(matrix2[0]):
        raise ValueError("Matrices must have the same number of columns")
      # Validate that all rows have the same length
      
      for row1, row2 in zip(matrix1, matrix2):
        if len(row1) != len(matrix1[0]) or len(row2) != len(matrix2[0]):
            raise ValueError("All rows must have the same length")
        
        # Validate that all elements are numeric
        if not all(isinstance(x, float) for x in row1 + row2):
            raise TypeError("All matrix elements must be numeric")

    def compute(self,matrix1: List[List[float]],matrix2: List[List[float]]) -> float:
      # Calculate Von Neumann distance
      distance: float = 0.0
      for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            distance += abs(matrix1[i][j] - matrix2[i][j])
      return distance


from typing import List, Union, Tuple
from numbers import Number
import math

class GraphEntropyDistance:
    """
    A class to compute the entropy distance between two graphs represented as adjacency matrices.
    The entropy is calculated using graph spectra and Von Neumann entropy.
    """
    
    def __init__(self, epsilon: float = 1e-10, max_iterations: int = 50):
        """
        Initialize the GraphEntropyDistance calculator.
        
        Args:
            epsilon (float): Small value to avoid log(0) in calculations
            max_iterations (int): Maximum iterations for eigenvalue calculations
        """
        self._epsilon = epsilon
        self._max_iterations = max_iterations
    
    @staticmethod
    def validate_matrices(matrix1: List[List[Number]], 
                         matrix2: List[List[Number]]) -> None:
        """Validate input matrices format and values."""
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
        
        if len(matrix1) != len(matrix2):
            raise ValueError("Matrices must have the same dimensions")
        
        for row1, row2 in zip(matrix1, matrix2):
            if len(row1) != len(matrix1) or len(row2) != len(matrix2):
                raise ValueError("Matrices must be square")
            if not all(isinstance(x, Number) for x in row1 + row2):
                raise TypeError("All matrix elements must be numeric")
    
    def _get_degree_matrix(self, matrix: List[List[Number]]) -> List[List[float]]:
        """
        Calculate the degree matrix of a graph.
        
        Args:
            matrix: Input adjacency matrix
            
        Returns:
            Degree matrix
        """
        n = len(matrix)
        degree_matrix = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            degree = sum(float(matrix[i][j]) for j in range(n))
            degree_matrix[i][i] = degree if degree > self._epsilon else self._epsilon
            
        return degree_matrix
    
    def _get_laplacian(self, matrix: List[List[Number]]) -> List[List[float]]:
        """
        Calculate the normalized Laplacian matrix.
        L = D^(-1/2) (D - A) D^(-1/2)
        where D is degree matrix and A is adjacency matrix.
        """
        n = len(matrix)
        degree_matrix = self._get_degree_matrix(matrix)
        
        # Calculate D^(-1/2)
        d_inv_sqrt = [[0.0] * n for _ in range(n)]
        for i in range(n):
            d_inv_sqrt[i][i] = 1.0 / math.sqrt(degree_matrix[i][i])
        
        # Calculate normalized Laplacian
        laplacian = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    laplacian[i][j] = 1.0
                elif matrix[i][j] != 0:
                    laplacian[i][j] = -matrix[i][j] / math.sqrt(
                        degree_matrix[i][i] * degree_matrix[j][j]
                    )
        
        return laplacian
    
    def _matrix_vector_multiply(self, matrix: List[List[float]], 
                              vector: List[float]) -> List[float]:
        """Matrix-vector multiplication."""
        n = len(matrix)
        result = [0.0] * n
        for i in range(n):
            for j in range(n):
                result[i] += matrix[i][j] * vector[j]
        return result
    
    def _normalize_vector(self, vector: List[float]) -> List[float]:
        """Normalize a vector to unit length."""
        magnitude = math.sqrt(sum(x*x for x in vector))
        if magnitude < self._epsilon:
            return [0.0] * len(vector)
        return [x/magnitude for x in vector]
    
    def _calculate_eigenvalues(self, matrix: List[List[float]]) -> List[float]:
        """
        Calculate eigenvalues using power iteration and deflation.
        Returns approximate eigenvalues sorted in descending order.
        """
        n = len(matrix)
        eigenvalues: List[float] = []
        current_matrix = [row[:] for row in matrix]
        
        for _ in range(n):
            # Find current largest eigenvalue
            vector = self._normalize_vector([1.0] * n)
            for _ in range(self._max_iterations):
                new_vector = self._matrix_vector_multiply(current_matrix, vector)
                vector = self._normalize_vector(new_vector)
            
            # Calculate Rayleigh quotient
            Av = self._matrix_vector_multiply(current_matrix, vector)
            lambda_value = sum(v * av for v, av in zip(vector, Av))
            eigenvalues.append(lambda_value)
            
            # Deflate matrix
            for i in range(n):
                for j in range(n):
                    current_matrix[i][j] -= lambda_value * vector[i] * vector[j]
        
        return sorted(eigenvalues, reverse=True)
    
    def _calculate_entropy(self, matrix: List[List[Number]]) -> float:
        """
        Calculate the von Neumann entropy using the normalized Laplacian spectrum.
        """
        laplacian = self._get_laplacian(matrix)
        eigenvalues = self._calculate_eigenvalues(laplacian)
        
        entropy = 0.0
        n = len(matrix)
        for eigenvalue in eigenvalues:
            if self._epsilon < eigenvalue < 1.0 - self._epsilon:
                p = eigenvalue / n
                entropy -= p * math.log2(p)
        
        return entropy
    
    def calculate_distance(self, matrix1: List[List[Number]], 
                         matrix2: List[List[Number]]) -> float:
        """
        Calculate the graph entropy distance between two matrices.
        
        Args:
            matrix1: First input matrix
            matrix2: Second input matrix
            
        Returns:
            Graph entropy distance between the matrices
        """
        self.validate_matrices(matrix1, matrix2)
        entropy1 = self._calculate_entropy(matrix1)
        entropy2 = self._calculate_entropy(matrix2)
        return abs(entropy1 - entropy2)
    
    @staticmethod
    def display_matrix(matrix: List[List[Number]]) -> None:
        """Display a matrix in a readable format."""
        for row in matrix:
            print([f"{x:>5.2f}" for x in row])



