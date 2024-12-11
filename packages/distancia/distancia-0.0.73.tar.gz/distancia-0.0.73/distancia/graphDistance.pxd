
cpdef class Graph:

    cpdef def create_adjacency_matrix(self):

    cpdef list def create_adjacency_list(self):

    cpdef def count_motifs(self, motif_size):

    cpdef def _find_sub_motifs(self, node, neighbors, remaining):
        
    cpdef def get_nodes(self):
			
cpdef class ShortestPath:

    cpdef def dijkstra(self, start_node, end_node):
			
    cpdef double def compute(self,graph, start_node, end_node):

cpdef class GraphEditDistance:
        
    cpdef double def compute(self, graph1, graph2):

    cpdef def _node_diff(self, g1, g2):

    cpdef def _edge_diff(self, g1, g2):

    cpdef def _get_edges(self, graph):

cpdef class SpectralDistance:

    cpdef def laplacian_matrix(self, G):

    cpdef list def eigenvalues(self,list[list float] matrix):

    cpdef double def compute(self, G1, G2):

cpdef class WeisfeilerLehmanSimilarity:

    cpdef def wl_labeling(self, G):

    cpdef double def compute(self, G1, G2):

    cpdef def is_isomorphic(self, G1, G2, threshold=0.99):

cpdef class ComparingRandomWalkStationaryDistributions:

    cpdef def compute_stationary_distribution(self, graph):

    cpdef def compare_distributions(self, str metric):

    cpdef def random_walk(self, graph,int  steps, start_node):

    cpdef def compare_random_walks(self, int num_walks,int walk_length):

cpdef class DiffusionDistance:

    cpdef def compute(self, graph, source_node, steps):

    cpdef def compare_diffusion(self, source_node, steps, str metric):
        
cpdef class GraphKernelDistance:
    
    cpdef def random_walk_kernel(self, depth=3):
    
    cpdef def random_walk(self, node1, node2, depth):

    cpdef def get_neighbors(self, graph, node):
    
    cpdef double def compute(self, method="random_walk", **kwargs):

cpdef class FrobeniusDistance:

    cpdef double def compute(self):

cpdef class PatternBasedDistance:

    cpdef double def compute(self):

    cpdef double def _calculate_distance(self, motifs1, motifs2):
        
cpdef class GraphCompressionDistance:

    cpdef int def compress(self, data):

    cpdef str def adjacency_to_string(self, matrix):

    cpdef def combined_compression(self):

    cpdef double def compute(self):
        
cpdef class DegreeDistributionDistance:

    cpdef double def compare_distributions(self, dist1, dist2):

    cpdef double def compute(self):

cpdef class CommunityStructureDistance:
    
    cpdef def __init__(self, community_detection_algorithm):

    cpdef double def jaccard_index(self, set1, set2):

    cpdef double def compare_communities(self, communities1, communities2):

    cpdef double def compute(self, graph1, graph2):

