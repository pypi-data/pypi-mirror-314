###################################################

#################################
#Loss function
#################################
from .mainClass import *
from .tools     import log,exp

import math
#claude ai
class CrossEntropy(Distance):
	def __init__(self, epsilon: float = 1e-15):
		super().__init__()
		self.type='vec_nn'

		self.epsilon = epsilon  # Pour éviter le log(0)
		
	def compute(self, y_true, y_pred):
		return self.__call__(y_true, y_pred)
		
	def __call__(self, y_true: list[list[float]], y_pred: list[list[float]]) -> float:
		"""
		Calcule la cross-entropie entre les étiquettes vraies et les prédictions.

		:param y_true: Étiquettes vraies (one-hot encoded)
		:param y_pred: Probabilités prédites
		:return: Valeur de la cross-entropie
		"""
		total_ce = 0.0
		for true_row, pred_row in zip(y_true, y_pred):
			for true_val, pred_val in zip(true_row, pred_row):
				# Clip les valeurs prédites pour éviter log(0)
				pred_val = max(min(pred_val, 1 - self.epsilon), self.epsilon)
				total_ce -= true_val * log(pred_val)
        
		return total_ce / len(y_true)

	def gradient(self, y_true: list[list[float]], y_pred: list[list[float]]) -> list[list[float]]:
		"""
		Calcule le gradient de la cross-entropie.

		:param y_true: Étiquettes vraies (one-hot encoded)
		:param y_pred: Probabilités prédites
		:return: Gradient de la cross-entropie
		"""
		grad = []
		for true_row, pred_row in zip(y_true, y_pred):
			grad_row = []
			for true_val, pred_val in zip(true_row, pred_row):
				# Clip les valeurs prédites pour éviter division par zéro
				pred_val = max(min(pred_val, 1 - self.epsilon), self.epsilon)
				grad_row.append(-true_val / pred_val / len(y_true))
			grad.append(grad_row)
        
		return grad

	def example(self):
		# Exemple d'utilisation
		y_true = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
		y_pred = [[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.2, 0.2, 0.6]]

		loss = self.compute(y_true, y_pred)
		grad = self.gradient(y_true, y_pred)

		print(f"Cross-Entropie: {loss}")
		print(f"Gradient: ")
		for row in grad:
			print(row)

		return loss, grad
#claude ai 
class Softmax(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='vec_nn'
        
    def compute(self, x):
      return self.__call__(x)

    def __call__(self, x: list[float]) -> list[float]:
        """
        Calcule la fonction softmax pour un vecteur d'entrée.

        :param x: Liste de valeurs d'entrée
        :return: Liste de probabilités softmax
        """
        # Soustrayons le maximum pour la stabilité numérique
        exp_x = [exp(xi - max(x)) for xi in x]
        sum_exp_x = sum(exp_x)
        return [xi / sum_exp_x for xi in exp_x]

    def gradient(self, softmax_output: list[float]) -> list[list[float]]:
        """
        Calcule le gradient de la fonction softmax.

        :param softmax_output: Sortie de la fonction softmax
        :return: Matrice jacobienne du gradient
        """
        n = len(softmax_output)
        gradient = []
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(softmax_output[i] * (1 - softmax_output[i]))
                else:
                    row.append(-softmax_output[i] * softmax_output[j])
            gradient.append(row)
        return gradient

    def example(self):
        # Exemple d'utilisation
        x = [1.0, 2.0, 3.0]
        
        softmax_output = self.compute(x)
        print("Sortie Softmax:")
        print(softmax_output)
        
        gradient = self.gradient(softmax_output)
        print("\nGradient Softmax:")
        for row in gradient:
            print(row)

        return softmax_output, gradient

class KullbackLeibler(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='vec_nn'
 
	def compute(self, y_true, y_pred):
		return self.__call__(y_true, y_pred)
		
	def __call__(self, p, q):
		"""
		Calculate the Kullback-Leibler divergence between two probability distributions.
        
		:param p: The true probability distribution (list of probabilities).
		:param q: The predicted probability distribution (list of probabilities).
		:return: The KL divergence value.
		"""
		kl_divergence = 0.0
        
		for pi, qi in zip(p, q):
			if pi > 0 and qi > 0:  # To avoid log(0), we only calculate for positive values.
				kl_divergence += pi * log(pi / qi)
        
		return kl_divergence


class MeanAbsoluteError(Distance):

	def __init__(self) -> None:
		super().__init__()  
		self.type='vec_nn'

	def compute(self, y_true, y_pred):
		return self.__call__(y_true, y_pred)
		
	def __call__(self, y_true, y_pred):
		"""
		Calculate the Mean Absolute Error between two lists of values.
        
		:param y_true: List of true values.
		:param y_pred: List of predicted values.
		:return: The MAE value.
		"""
		if len(y_true) != len(y_pred):
			raise ValueError("The length of y_true and y_pred must be the same.")
        
		total_error = 0.0
		n = len(y_true)
        
		for i in range(n):
			total_error += abs(y_true[i] - y_pred[i])
        
		mae = total_error / n
		return mae

class MAE(MeanAbsoluteError):
	def __init__(self) -> None:
		super().__init__()


class MeanAbsolutePercentageError(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='vec_float'

	def compute(self, y_true, y_pred):
		return self.__call__(y_true, y_pred)
		
	def __call__(self, y_true, y_pred):
		"""
		Calculate the Mean Absolute Percentage Error (MAPE) between two lists of values.
        
		:param y_true: List of true values.
		:param y_pred: List of predicted values.
		:return: The MAPE value as a percentage.
		"""
		if len(y_true) != len(y_pred):
			raise ValueError("The length of y_true and y_pred must be the same.")
        
		total_percentage_error = 0.0
		n = len(y_true)
        
		for i in range(n):
			if y_true[i] != 0:
				percentage_error = abs((y_true[i] - y_pred[i]) / y_true[i])
				total_percentage_error += percentage_error
			else:
				raise ValueError("y_true contains a zero value, which would cause a division by zero error in MAPE calculation.")
        
		mape = (total_percentage_error / n) * 100
		return mape

class MAPE(MeanAbsolutePercentageError):
	def __init__(self) -> None:
		super().__init__()
		
class MeanSquaredError(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='vec_nn'

	def compute(self, y_true, y_pred):
		return self.__call__(y_true, y_pred)
		
	def __call__(self, y_true, y_pred):
		"""
		Calculate the Mean Squared Error (MSE) between two lists of values.
        
		:param y_true: List of true values.
		:param y_pred: List of predicted values.
		:return: The MSE value.
		"""
		if len(y_true) != len(y_pred):
			raise ValueError("The length of y_true and y_pred must be the same.")
        
		total_squared_error = 0.0
		n = len(y_true)
        
		for i in range(n):
			squared_error = (y_true[i] - y_pred[i]) ** 2
			total_squared_error += squared_error
        
		mse = total_squared_error / n
		return mse

class MSE(MeanSquaredError):
	def __init__(self) -> None:
		super().__init__()
		

class SquaredLogarithmicError(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='vec_float'

	def compute(self, y_true, y_pred):
		return self.__call__(y_true, y_pred)
		
	def __call__(self, y_true, y_pred):
		"""
		Calculate the Squared Logarithmic Error (SLE) between two lists of values.
        
		:param y_true: List of true values. Must be positive.
		:param y_pred: List of predicted values. Must be positive.
		:return: The SLE value.
		"""
		if len(y_true) != len(y_pred):
			raise ValueError("The length of y_true and y_pred must be the same.")
        
		if any(v <= 0 for v in y_true) or any(v <= 0 for v in y_pred):
			raise ValueError("All values in y_true and y_pred must be positive for SLE calculation.")
        
		total_squared_log_error = 0.0
		n = len(y_true)
        
		for i in range(n):
			# Apply log transformation
			log_y_true = log(y_true[i] + 1)
			log_y_pred = log(y_pred[i] + 1)
			# Compute squared log error
			squared_log_error = (log_y_true - log_y_pred) ** 2
			total_squared_log_error += squared_log_error
        
		sle = total_squared_log_error / n
		return sle

class SLE(SquaredLogarithmicError):
	def __init__(self) -> None:
		super().__init__()


class GaloisWassersteinLoss(Distance):

    def __init__(self, alpha=1.0, beta=1.0, gamma=1.0) -> None:
        super().__init__()
        self.type='vec_nn'

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.trellis = self.build_galois_trellis()

    def build_galois_trellis(self):
        """
        Construct a Galois trellis representing the hierarchical relationships between classes.
        
        :return: A dictionary representing the trellis where the keys are pairs of classes,
                 and the values are the distances between those classes.
        """
        # Example structure for the trellis
        # Replace this with a more complex or domain-specific trellis if necessary
        trellis = {
            (0, 0): 0, (0, 1): 1, (0, 2): 2,
            (1, 0): 1, (1, 1): 0, (1, 2): 1,
            (2, 0): 2, (2, 1): 1, (2, 2): 0
        }
        return trellis
    
    def compute_cdf(self, probabilities):
        """
        Compute the cumulative distribution function (CDF) from a list of probabilities.
        
        :param probabilities: List of probabilities for each class.
        :return: CDF as a list.
        """
        cdf = []
        cumulative_sum = 0.0
        for p in probabilities:
            cumulative_sum += p
            cdf.append(cumulative_sum)
        return cdf
    
    def compute(self, y_true, y_pred):
        """
        Compute the Galois distance between true and predicted distributions using the internal Galois trellis.
        
        :param y_true: List of true class probabilities.
        :param y_pred: List of predicted class probabilities.
        :return: The Galois distance value.
        """
        distance = 0.0
        for i in range(len(y_true)):
            for j in range(len(y_pred)):
                if y_true[i] > 0 and y_pred[j] > 0:
                    distance += self.trellis.get((i, j), 1) * abs(y_true[i] - y_pred[j])
        return distance
    
    def __call__(self, y_true, y_pred):
        """
        Calculate the Galois-Wasserstein Loss between the true and predicted distributions.
        
        :param y_true: List of true class probabilities.
        :param y_pred: List of predicted class probabilities.
        :return: The Galois-Wasserstein Loss value.
        """
        if len(y_true) != len(y_pred):
            raise ValueError("The length of y_true and y_pred must be the same.")
        
        # Compute CDF for true and predicted distributions
        cdf_true = self.compute_cdf(y_true)
        cdf_pred = self.compute_cdf(y_pred)
        
        # Compute Wasserstein distance
        wasserstein_distance = sum(abs(cdf_true[i] - cdf_pred[i]) for i in range(len(cdf_true)))
        
        # Compute Cross Entropy
        cross_entropy = CrossEntropy()(y_true, y_pred)
        
        # Compute Galois distance
        galois_distance = self.galois_distance(y_true, y_pred)
        
        # Compute combined loss
        loss = self.alpha * wasserstein_distance + self.beta * cross_entropy + self.gamma * galois_distance
        return loss
	
