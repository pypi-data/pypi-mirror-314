
cpdef class CustomDistanceFunction(Distance):

    cpdef def compute(self, data1, data2):

cpdef class IntegratedDistance:

    cpdef def compute(self, point1, point2):

    cpdef def apply_to_dataframe(self, df, col1, col2, result_col='distance'):

    cpdef def apply_to_sklearn(self, X, Y=None):

cpdef class DistanceMatrix:

    cpdef def _compute_distance_matrix(self):

    cpdef def get_matrix(self):

cpdef class ParallelandDistributedComputation:

    cpdef def compute_distances_parallel(self, reference_point=None, max_workers=None, use_multiprocessing=False):

cpdef class OutlierDetection:

    cpdef def _calculate_centroid(self):

    cpdef def _calculate_distances(self):

    cpdef def detect_outliers(self):

cpdef class BatchDistance:

    cpdef def compute_batch(self):

cpdef class ComprehensiveBenchmarking:

    cpdef def run_benchmark(self):

    cpdef def print_results(self):

cpdef class LMNN:

    cpdef def fit(self, X, y):

    cpdef def find_target_neighbors(self, X, y):

    cpdef def find_impostors(self, i, X, y, L):

    cpdef def triplet_loss(self, xi, xj, xl, L):

    cpdef def transform(self, X):

    cpdef def transform_point(self, x, L):

    cpdef def vector_subtract(self, v1, v2):

    cpdef def outer_product(self, v):

    cpdef def scalar_matrix_mult(self, scalar, matrix):

    cpdef def matrix_add(self, m1, m2):

    cpdef def matrix_subtract(self, m1, m2):

    cpdef def predict(self, X_train, y_train, X_test):
	
cpdef class DistanceMetricLearning:

    cpdef def fit(self):

    cpdef def transform(self, X):

    cpdef def _learn_lmnn(self):

    cpdef def _learn_itml(self):
 
    cpdef def _learn_nca(self):

    cpdef def get_metric(self):

cpdef class MetricFinder:

	cpdef def find_metric(self, point1, point2):

	cpdef def find_string_metric(self, str1, str2):

	cpdef def find_similarity_metric(self, point1, point2):

cpdef class APICompatibility:
    
    cpdef def rest_endpoint(self, host="0.0.0.0", port=5000):

cpdef class AutomatedDistanceMetricSelection:
    
    cpdef def select_metric(self, data):

    cpdef def is_high_dimensional(self, data):

    cpdef def is_binary_data(self, data):

    cpdef def has_outliers(self, data):

    cpdef def is_time_series(self, data):

cpdef class StatisticalAnalysis:

    cpdef def mean_distance(self, dataset):

    cpdef def variance_distance(self, dataset):

    cpdef def distance_distribution(self, dataset, bins=10):

    cpdef def correlation_with_other_metric(self, dataset, other_metric):

cpdef class Visualization:

    cpdef def plot_distance_matrix(self, dataset):

    cpdef def plot_distance_histogram(self, dataset, bins=10):

    cpdef def plot_similarity_matrix(self, dataset):

    cpdef def compute_distance_matrix(self, dataset):

    cpdef def find_clusters(self, distance_matrix):

    cpdef def plot_dendrogram(self, dataset):

    cpdef def plot_pca(self, dataset, n_components=2):

    cpdef def eigen_decomposition(self, matrix):
	
cpdef class PlotDendrogram:

    cpdef def fit(self, X):

    cpdef def plot(self):

cpdef class ComparisonAndValidation:

    cpdef def compare_with_other_metric(self, dataset, other_metric):

    cpdef def cross_validation_score(self, dataset, labels,metric, k_folds=5):

    cpdef def evaluate_metric_on_benchmark(self, dataset, labels, benchmark_metric):

cpdef class DimensionalityReductionAndScaling:

    cpdef def metric_scaling(self, distance, multiplier):

    cpdef def compute_distance_matrix(self, dataset):

    cpdef def dimensionality_reduction_embedding(self, dataset, method='MDS', dimensions=2, max_iter=300, epsilon=1e-9):

    cpdef def _mds_embedding(self, dataset, dimensions, max_iter, epsilon):

cpdef class AdvancedAnalysis:

    cpdef def sensitivity_analysis(self, dataset, perturbation):

    cpdef def robustness_analysis(self, dataset, noise_level):

    cpdef def entropy_of_distances(self, dataset):

    cpdef def consistency_check_over_subsets(self, dataset, num_subsets=5):

    cpdef def _compute_average_distance(self, dataset):

    cpdef def _compute_all_distances(self, dataset):

    cpdef def _compute_frequency_distribution(self, distances):

    cpdef def _perturb_dataset(self, dataset, perturbation):

    cpdef def _add_noise_to_dataset(self, dataset, noise_level):

cpdef class ReportingAndDocumentation:

    cpdef def generate_metric_report(self, dataset):

    cpdef def export_distance_matrix(self, dataset, file_format='csv', filename='distance_matrix.csv'):

    cpdef def document_metric_properties(self):

    cpdef def _format_distance_matrix(self, dataset):

    cpdef def _compute_mean_distance(self, dataset):

    cpdef def _compute_variance_distance(self, dataset):
 
