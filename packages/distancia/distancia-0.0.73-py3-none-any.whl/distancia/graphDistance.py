from .mainClass import Distance
from .vectorDistance import Euclidean,L1
from .tools     import Graph
        
        
class ShortestPath(Distance):
	
    def __init__(self)-> None:
        """
        Initialise la classe avec un graphe représenté sous forme de dictionnaire.
        :param graph: Un dictionnaire représentant le graphe, où les clés sont les nœuds et les valeurs sont des dictionnaires
                      de voisins avec les poids des arêtes.
        """
        super().__init__()
        self.type='graph'


    def compute(self,graph, start_node, end_node):
        """
        Obtient la distance du plus court chemin entre deux nœuds dans le graphe.
        :param start_node: Le nœud de départ.
        :param end_node: Le nœud d'arrivée.
        :return: La distance du plus court chemin.
        """

        return graph.dijkstra(start_node, end_node)
        
    def example(self):
        # Create a weighted, undirected graph
        g = Graph(directed=False, weighted=True)
    
        # Add some edges
        g.add_edge("A", "B", 4)
        g.add_edge("B", "C", 3)
        g.add_edge("C", "D", 2)
        g.add_edge("D", "A", 5)
    
        # Perform Dijkstra
        distance, path = self.compute(g,"A", "C")
        print(f"Shortest path from A to C: {path}")
        print(f"Distance: {distance}")
        print(f"{self.__class__.__name__} distance between A and C in {g} is {distance:.2f}")



class GraphEditDistance(Distance):
    def __init__(self)-> None:
        """
        Initializes the GraphEditDistance class with two graphs.
        
        :param graph1: The first graph as a dictionary where keys are nodes and values are sets of connected nodes.
        :param graph2: The second graph as a dictionary where keys are nodes and values are sets of connected nodes.
        """
        super().__init__()
        self.type='graph'

        

    def compute(self, graph1, graph2):
        """
        Computes the Graph Edit Distance (GED) between the two graphs.

        :return: The Graph Edit Distance between the two graphs.
        """
        
        # Compute node differences
        node_diff = self.node_diff(graph1,graph2)

        # Compute edge differences
        edge_diff = self.edge_diff(graph1,graph2)

        # Total cost is the sum of node and edge differences
        return node_diff + edge_diff

    def node_diff(self,g1,g2):
        """
        Computes the difference in nodes between two graphs.
        
        :param g1: The first graph.
        :param g2: The second graph.
        :return: The node difference.
        """

        # Nodes to delete from g1 or add to g2
        node_intersection = g1.nodes & g2.nodes
        node_union = g2.nodes | g1.nodes

        # Node difference is the sum of deletions and additions
        return len(node_union) - len(node_intersection)

    def edge_diff(self, g1, g2):
        """
        Computes the difference in edges between two graphs.
        
        :param g1: The first graph.
        :param g2: The second graph.
        :return: The edge difference.
        """
        g1_edges = set(g1.get_edges())
        g2_edges = set(g2.get_edges())

        # Edges to delete from g1 or add to g2
        edge_intersection = g1_edges & g2_edges
        edge_union = g2_edges | g1_edges

        # Edge difference is the sum of deletions and additions
        return len(edge_union) + len(edge_intersection)
        
    def example(self):
        g1 = Graph(directed=False, weighted=True)
    
        # Add some edges
        g1.add_edge("A", "B", 4)
        g1.add_edge("B", "C", 3)
        g1.add_edge("C", "D", 2)
        g1.add_edge("D", "A", 5)
        
        g2 = Graph(directed=False, weighted=True)
    
        # Add some edges
        g2.add_edge("A", "B", 4)
        g2.add_edge("C", "D", 2)
        g2.add_edge("D", "A", 5)
        
        #graph=Graph(Graph.nodes_1,Graph.edges_1)
        distance=self.compute(g1,g2)
        print(f"{self.__class__.__name__} distance between {g2} in {g1} is {distance:.2f}")
        
        
#claude A I
try:
  import networkx as nx
except ImportError:
    nx = None  # networkx n'est pas disponible
    
class SpectralDistance(Distance):
    """
    A class to compute the spectral distance between two graphs.

    The spectral distance is based on the difference between the eigenvalues
    of the Laplacian matrices of the graphs.

    Attributes:
        k (int): Number of eigenvalues to consider (default is None, which uses all eigenvalues)
        normalized (bool): Whether to use normalized Laplacian (default is False)
    """

    def __init__(self, k=None, normalized=False)-> None:
        """
        Initialize the SpectralDistance object.

        Args:
            k (int, optional): Number of eigenvalues to consider. If None, all eigenvalues are used.
            normalized (bool, optional): Whether to use the normalized Laplacian. Defaults to False.
        """
        super().__init__()
        self.type='graph'

        self.k = k
        self.normalized = normalized

    def laplacian_matrix(self, G):
        """
        Compute the Laplacian matrix of the graph.

        Args:
            G (networkx.Graph): Input graph

        Returns:
            list of list: Laplacian matrix
        """
        n = G.number_of_nodes()
        L = [[0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    L[i][j] = G.degree(i)
                elif G.has_edge(i, j):
                    L[i][j] = -1
        
        if self.normalized:
            for i in range(n):
                for j in range(n):
                    if G.degree(i) > 0 and G.degree(j) > 0:
                        L[i][j] /= (G.degree(i) * G.degree(j))**0.5
        
        return L

    def eigenvalues(self, matrix):
        """
        Compute eigenvalues using the power iteration method.

        Args:
            matrix (list of list): Input matrix

        Returns:
            list: Approximate eigenvalues
        """
        n = len(matrix)
        eigenvalues = []
        for _ in range(n):
            # Initialize random vector
            v = [1/(n)**0.5 for _ in range(n)]
            for _ in range(100):  # Number of iterations
                # Matrix-vector multiplication
                u = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
                # Normalize
                norm = (sum(x*x for x in u))**0.5
                if norm==0:norm=1
                v = [x/norm for x in u]
            # Compute Rayleigh quotient
            lambda_ = sum(v[i] * sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n))
            eigenvalues.append(lambda_)
            # Deflate the matrix
            for i in range(n):
                for j in range(n):
                    matrix[i][j] -= lambda_ * v[i] * v[j]
        return sorted(eigenvalues)

    def compute(self, G1, G2):
        """
        Calculate the spectral distance between two graphs.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph

        Returns:
            float: Spectral distance between G1 and G2

        Raises:
            ValueError: If the graphs have different numbers of nodes and k is None
        """
        L1 = self.laplacian_matrix(G1)
        L2 = self.laplacian_matrix(G2)
        
        eig1 = self.eigenvalues(L1)
        eig2 = self.eigenvalues(L2)

        if self.k is None:
            if len(eig1) != len(eig2):
                raise ValueError("Graphs must have the same number of nodes when k is None")
            k = len(eig1)
        else:
            k = min(self.k, len(eig1), len(eig2))

        # Pad or truncate eigenvalues to length k
        eig1 = eig1[:k] + [0] * max(0, k - len(eig1))
        eig2 = eig2[:k] + [0] * max(0, k - len(eig2))

        # Compute Euclidean distance between eigenvalues
        #distance = (sum((e1 - e2)**2 for e1, e2 in zip(eig1, eig2)))**0.5
        distance = Euclidean().calculate(eig1, eig2)

        return distance
    def example(self):
        def create_sample_graphs():
         # Create a path graph
         P10 = nx.path_graph(10)
         # Create a cycle graph
         C10 = nx.cycle_graph(10)
         # Create a complete graph
         K10 = nx.complete_graph(10)
         # Create two random graphs
         G1 = nx.gnm_random_graph(10, 20)
         G2 = nx.gnm_random_graph(10, 20)
         return P10, C10, K10, G1, G2
        def compare_graphs(graphs, names):
         # Initialize SpectralDistance object
         sd = SpectralDistance(k=5, normalized=True)
         print("Spectral distances between graphs:")
         for i, (G1, name1) in enumerate(zip(graphs, names)):
          for j, (G2, name2) in enumerate(zip(graphs[i+1:], names[i+1:])):
            distance = sd.calculate(G1, G2)
            print(f"{name1} vs {name2}: {distance:.4f}")
        # Create sample graphs
        P10, C10, K10, G1, G2 = create_sample_graphs()
        graph_names = ["Path", "Cycle", "Complete", "Random1", "Random2"]
        # Compare the graphs
        compare_graphs([P10, C10, K10, G1, G2], graph_names)
#claude
from collections import Counter

class WeisfeilerLehmanSimilarity(Distance):
    """
    A class to compute the Weisfeiler-Lehman similarity between two graphs.

    The Weisfeiler-Lehman algorithm is used to create a multi-set of labels
    for each graph, which are then compared to compute a similarity score.

    Attributes:
        num_iterations (int): Number of iterations for the WL algorithm
        node_label_attr (str): Attribute name for initial node labels
    """

    def __init__(self, num_iterations=3, node_label_attr=None)-> None:
        """
        Initialize the WeisfeilerLehmanSimilarity object.

        Args:
            num_iterations (int): Number of iterations for the WL algorithm. Default is 3.
            node_label_attr (str, optional): Attribute name for initial node labels.
                If None, all nodes are initially labeled with the same value.
        """
        super().__init__()
        self.type='graph'

        self.num_iterations = num_iterations
        self.node_label_attr = node_label_attr

    def wl_labeling(self, G):
        """
        Perform Weisfeiler-Lehman labeling on the graph.

        Args:
            G (networkx.Graph): Input graph

        Returns:
            list: List of label multi-sets for each iteration
        """
        if self.node_label_attr:
            labels = nx.get_node_attributes(G, self.node_label_attr)
        else:
            labels = {node: '1' for node in G.nodes()}

        label_lists = [Counter(labels.values())]

        for _ in range(self.num_iterations):
            new_labels = {}
            for node in G.nodes():
                # Collect labels of neighbors
                neighbor_labels = sorted(labels[nbr] for nbr in G.neighbors(node))
                # Create a new label by combining current label and sorted neighbor labels
                new_labels[node] = f"{labels[node]}({''.join(neighbor_labels)})"
            
            # Update labels and add to label_lists
            labels = new_labels
            label_lists.append(Counter(labels.values()))

        return label_lists

    def compute(self, G1, G2):
        """
        Calculate the Weisfeiler-Lehman similarity between two graphs.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph

        Returns:
            float: Weisfeiler-Lehman similarity between G1 and G2
        """
        # Get label multi-sets for both graphs
        label_lists1 = self.wl_labeling(G1)
        label_lists2 = self.wl_labeling(G2)

        # Compute similarity for each iteration
        similarities = []
        for labels1, labels2 in zip(label_lists1, label_lists2):
            intersection = sum((labels1 & labels2).values())
            union = sum((labels1 | labels2).values())
            similarities.append(intersection / union if union > 0 else 0)

        # Return the average similarity across all iterations
        return sum(similarities) / len(similarities)

    def is_isomorphic(self, G1, G2, threshold=0.99):
        """
        Check if two graphs are potentially isomorphic using WL similarity.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph
            threshold (float): Similarity threshold for isomorphism. Default is 0.99.

        Returns:
            bool: True if the graphs are potentially isomorphic, False otherwise
        """
        if G1.number_of_nodes() != G2.number_of_nodes() or G1.number_of_edges() != G2.number_of_edges():
            return False
        
        similarity = self.calculate(G1, G2)
        return similarity > threshold
    def example(self):
     pass
'''
import numpy as np
import networkx as nx

class ComparingRandomWalkStationaryDistributions(Distance):
    """
    A class to compare stationary distributions of random walks on graphs.
    """

    def __init__(self,metric=L1())-> None:
        """
        Initialize the Distance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        super().__init__()
        self.type='graph'

        self.metric = metric

    def compute_stationary_distribution(self, graph):
        """
        Compute the stationary distribution of a random walk on the given graph.

        Parameters:
        graph (networkx.Graph): The graph to compute the stationary distribution for

        Returns:
        numpy.ndarray: The stationary distribution vector
        """
        # Get the adjacency matrix
        adj_matrix = nx.adjacency_matrix(graph).toarray()

        # Compute the transition matrix
        degree = np.sum(adj_matrix, axis=1)
        transition_matrix = adj_matrix / degree[:, np.newaxis]

        # Compute the eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(transition_matrix.T)

        # Find the eigenvector corresponding to eigenvalue 1
        stationary_index = np.argmin(np.abs(eigenvalues - 1))
        stationary_distribution = np.real(eigenvectors[:, stationary_index])

        # Normalize the distribution
        return stationary_distribution / np.sum(stationary_distribution)

    def compute(self, graph1, graph2):
        """
        Compare the stationary distributions of the two graphs.

        Parameters:
        metric (str): The distance metric to use. Options: 'l1', 'l2', 'kl'. Default is 'l1'.

        Returns:
        float: The distance between the two stationary distributions
        """
        dist1 = self.compute_stationary_distribution(graph1)
        dist2 = self.compute_stationary_distribution(graph2)

        if len(dist1) != len(dist2):
            raise ValueError("The graphs must have the same number of nodes")

        return self.metric.compute(dist1,dist2)
        
    def compare_random_walks(self, num_walks, walk_length):
        """
        Compare random walks on both graphs.

        Parameters:
        num_walks (int): The number of random walks to perform on each graph
        walk_length (int): The length of each random walk

        Returns:
        dict: A dictionary containing the average walk length and node visit frequencies for both graphs
        """
        results = {}

        for i, graph in enumerate([self.graph1, self.graph2]):
            total_length = 0
            node_visits = {node: 0 for node in graph.nodes()}

            for _ in range(num_walks):
                walk = self.random_walk(graph, walk_length)
                total_length += len(walk)
                for node in walk:
                    node_visits[node] += 1

            avg_length = total_length / num_walks
            visit_freq = {node: visits / (num_walks * walk_length) for node, visits in node_visits.items()}

            results[f'graph{i+1}'] = {
                'avg_walk_length': avg_length,
                'node_visit_frequencies': visit_freq
            }

        return results
    def example(self):
      """
      Test the distance calculation between graphs
      """
      # Test 1: Identical graphs
      g1 = Graph(weighted=True)
      g1.add_edge('A', 'B', 1.0)
      g1.add_edge('B', 'C', 2.0)
    
      # Test 3: Different structure
      print("Test : Different structure of graph")
      g4 = Graph(weighted=True)
      g4.add_edge('A', 'B', 1.0)
      g4.add_edge('B', 'C', 2.0)
      g4.add_edge('A', 'C', 1.5)  # Additional edge
    
      g1.add_node('C')  # Ensure both graphs have same nodes
      distance = self.compute(g1,g4)
      print(f"Distance between graphs with different structure: {distance}")
'''
from typing import Dict, Set
from collections import defaultdict
class ComparingRandomWalkStationaryDistributions(Distance):
  """
  A class to compare stationary distributions of random walks on graphs.
  """

  def __init__(self)-> None:
        """
        Initialize the Distance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        super().__init__()
        self.type='graph'
        


  def power_iteration(self,matrix: Dict[str, Dict[str, float]], nodes: Set[str], 
                   num_iterations: int = 100, tolerance: float = 1e-10) -> Dict[str, float]:
    """
    Calcule le vecteur propre principal par la méthode des puissances.
    """
    # Distribution initiale uniforme
    n = len(nodes)
    vector = {node: 1.0/n for node in nodes}
    
    for _ in range(num_iterations):
        new_vector = Graph.multiply_matrix_vector(matrix, vector)
        new_vector = Graph.normalize_vector(new_vector)
        
        # Vérification de la convergence
        diff = sum(abs(new_vector[node] - vector[node]) for node in nodes)
        if diff < tolerance:
            return new_vector
            
        vector = new_vector
    
    return vector

  def compute(self,graph1, graph2):
    """
    Compare les distributions stationnaires de deux graphes.
    graph1, graph2: objets graphe avec la structure spécifiée
    Retourne: (différence L1, distribution1, distribution2)
    """
    # Calcul des matrices de transition
    trans_matrix1 = Graph.get_transition_matrix(graph1)
    trans_matrix2 = Graph.get_transition_matrix(graph2)
    
    # Calcul des distributions stationnaires
    stat_dist1 = self.power_iteration(trans_matrix1, graph1.nodes)
    stat_dist2 = self.power_iteration(trans_matrix2, graph2.nodes)
    
    # Pour assurer que nous comparons les mêmes nœuds
    all_nodes = set(graph1.nodes).union(set(graph2.nodes))
    
    # Compléter les distributions avec des zéros pour les nœuds manquants
    for node in all_nodes:
        if node not in stat_dist1:
            stat_dist1[node] = 0.0
        if node not in stat_dist2:
            stat_dist2[node] = 0.0
    
    # Calcul de la distance L1
    l1_distance = sum(abs(stat_dist1[node] - stat_dist2[node]) 
                     for node in all_nodes)
    
    return l1_distance, stat_dist1, stat_dist2
    
  def example(self):
    # Création de deux graphes d'exemple
    graph1 = Graph(directed=False, weighted=True)
    graph1.add_edge("A", "B", 1.0)
    graph1.add_edge("B", "C", 2.0)
    graph1.add_edge("C", "A", 1.5)
    
    graph2 = Graph(directed=False, weighted=True)
    graph2.add_edge("A", "B", 2.0)
    graph2.add_edge("B", "C", 1.0)
    graph2.add_edge("C", "D", 1.0)
    graph2.add_edge("D", "E", 1.0)
    
    distance, dist1, dist2 = ComparingRandomWalkStationaryDistributions().compute(graph1, graph2)
    print(f"Distance L1: {distance}")
    print(f"Distribution stationnaire graphe 1: {dist1}")
    print(f"Distribution stationnaire graphe 2: {dist2}")

    
''' fonctionne tres bien mais avec networkx
#claude
import networkx as nx
from collections import deque

class DiffusionDistance(Distance):
    """
    A class to compare diffusion processes on two graphs.
    """

    def __init__(self, steps =  5, metric='l1')-> None:
        """
        Initialize the DiffusionDistance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        super().__init__()
        self.type='graph'

        self.steps = steps
        self.metric = metric


    def computeDiffusion(self, graph, source_node=None, steps=None):
        """
        Compute the diffusion process on the given graph starting from the source node.

        Parameters:
        graph (networkx.Graph): The graph to compute the diffusion process on
        source_node (int): The starting node for the diffusion process
        steps (int): The number of steps to run the diffusion process

        Returns:
        dict: A dictionary where the keys are the nodes and the values are the diffusion values
        """
        if source_node is None:
           source_node = np.random.choice(list(graph.nodes()))
           
        diffusion_values = {node: 0 for node in graph.nodes()}
        diffusion_values[source_node] = 1

        queue = deque([(source_node, 0)])

        while queue and queue[0][1] < steps:
            node, step = queue.popleft()
            neighbors = list(graph.neighbors(node))

            for neighbor in neighbors:
                diffusion_values[neighbor] += diffusion_values[node] / len(neighbors)

            for neighbor in neighbors:
                queue.append((neighbor, step + 1))

        return diffusion_values

    def compute(self, graph1, graph2, source_node):
        """
        Compare the diffusion processes on the two graphs.

        Parameters:
        source_node (int): The starting node for the diffusion process
        steps (int): The number of steps to run the diffusion process
        metric (str): The distance metric to use. Options: 'l1', 'l2'. Default is 'l1'.

        Returns:
        float: The distance between the two diffusion processes
        """
        diff1 = self.computeDiffusion(graph1, source_node, self.steps)
        diff2 = self.computeDiffusion(graph2, source_node, self.steps)

        if self.metric == 'l1':
            return sum(abs(diff1[node] - diff2[node]) for node in graph1.nodes())
        elif self.metric == 'l2':
            return sum((diff1[node] - diff2[node])**2 for node in graph1.nodes())**0.5
        else:
            raise ValueError("Invalid metric. Choose 'l1' or 'l2'.")
    def example(self):
      G1 = nx.erdos_renyi_graph(10, 0.3, seed=42)
      G2 = nx.erdos_renyi_graph(10, 0.35, seed=42)
      steps = 5
      diffusion_distance = DiffusionDistance(steps)
      source_node = 0
      l1_distance = diffusion_distance.compute(G1, G2,source_node)
      diffusion_distance = DiffusionDistance(steps,metric='l2')
      l2_distance = diffusion_distance.compute(G1, G2,source_node)
      print(f"L1 distance between diffusion processes: {l1_distance:.4f}")
      print(f"L2 distance between diffusion processes: {l2_distance:.4f}")
'''
from typing import Dict, Set, List, Tuple
from collections import defaultdict, deque
import random
from math import exp
class DiffusionDistance(Distance):
    """
    A class to compare diffusion processes on two graphs.
    """

    def __init__(self, steps =  5, metric='l1')-> None:
        """
        Initialize the DiffusionDistance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        super().__init__()
        self.type='graph'

        self.steps = steps
        self.metric = metric
        
    def compute_hitting_times(self, graph) -> Dict[str, Dict[str, float]]:
        hitting_times = defaultdict(dict)
        nodes = list(graph.nodes)
        
        for target in nodes:
            distances = {node: float('inf') for node in nodes}
            distances[target] = 0
            queue = deque([(target, 0)])
            
            while queue:
                current, dist = queue.popleft()
                neighbors = (graph.adj_list[current].keys() if graph.weighted 
                           else graph.adj_list[current])
                
                for neighbor in neighbors:
                    weight = (1.0 if not graph.weighted 
                            else graph.adj_list[current][neighbor])
                    new_dist = dist + weight
                    
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        queue.append((neighbor, new_dist))
            
            hitting_times[target] = distances
            
        return hitting_times

    def compute_diffusion_kernel(self, graph, beta: float = 1.0,max_iterations=100,epsilon = 1e-10) -> Dict[str, Dict[str, float]]:
        transition = Graph.get_transition_matrix(graph)
        kernel = defaultdict(dict)
        
        for i in graph.nodes:
            vector = {node: 1.0 if node == i else 0.0 for node in graph.nodes}
            
            for _ in range(max_iterations):
                new_vector = Graph.multiply_matrix_vector(transition, vector)
                new_vector = {k: v * exp(-beta) for k, v in new_vector.items()}
                
                diff = sum(abs(new_vector[node] - vector[node]) for node in graph.nodes)
                if diff < epsilon:
                    kernel[i] = new_vector
                    break
                    
                vector = new_vector
            
            kernel[i] = vector
            
        return kernel

    def compare_graphs(self, graph1, graph2) -> Dict[str, float]:
        results = {}
        
        # Compare stationary distributions
        stat1 = Graph().compute_stationary_distribution(graph1)
        stat2 = Graph().compute_stationary_distribution(graph2)
        all_nodes = graph1.nodes.union(graph2.nodes)
        
        stat_distance = sum(abs(stat1.get(node, 0) - stat2.get(node, 0)) 
                          for node in all_nodes)
        results['stationary_distance'] = stat_distance
        
        # Compare hitting times
        hit1 = self.compute_hitting_times(graph1)
        hit2 = self.compute_hitting_times(graph2)
        common_nodes = graph1.nodes.intersection(graph2.nodes)
        
        if common_nodes:
            hit_distance = sum(abs(hit1[i][j] - hit2[i][j]) 
                             for i in common_nodes 
                             for j in common_nodes 
                             if hit1[i][j] != float('inf') and hit2[i][j] != float('inf'))
            results['hitting_time_distance'] = hit_distance / len(common_nodes)
        
        # Compare diffusion kernels
        kernel1 = self.compute_diffusion_kernel(graph1)
        kernel2 = self.compute_diffusion_kernel(graph2)
        
        if common_nodes:
            kernel_distance = sum(abs(kernel1[i][j] - kernel2[i][j]) 
                                for i in common_nodes 
                                for j in common_nodes)
            results['kernel_distance'] = kernel_distance / len(common_nodes)
        
        return results

    def simulate_diffusion(self, graph, start_nodes: Set[str], 
                         steps: int) -> List[Set[str]]:
        infected = set(start_nodes)
        history = [infected.copy()]
        
        for _ in range(steps):
            new_infected = infected.copy()
            
            for node in infected:
                neighbors = (graph.adj_list[node].keys() if graph.weighted 
                           else graph.adj_list[node])
                
                for neighbor in neighbors:
                    if neighbor not in infected:
                        prob = (1.0 if not graph.weighted 
                               else graph.adj_list[node][neighbor])
                        if random.random() < prob:
                            new_infected.add(neighbor)
            
            infected = new_infected
            history.append(infected.copy())
        
        return history

    def compare_diffusion_processes(self, graph1, graph2, 
                                  start_nodes: Set[str], 
                                  steps: int, 
                                  num_simulations: int = 10) -> Dict[str, float]:
        total_diff = 0
        max_diff = float('-inf')
        min_diff = float('inf')
        
        for _ in range(num_simulations):
            hist1 = self.simulate_diffusion(graph1, start_nodes, steps)
            hist2 = self.simulate_diffusion(graph2, start_nodes, steps)
            
            diff = sum(len(set1.symmetric_difference(set2)) 
                      for set1, set2 in zip(hist1, hist2)) / steps
            
            total_diff += diff
            max_diff = max(max_diff, diff)
            min_diff = min(min_diff, diff)
        
        return {
            'average_difference': total_diff / num_simulations,
            'max_difference': max_diff,
            'min_difference': min_diff
        }        
    def example(self):
      # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "A", 1.5)

      graph2 = Graph(directed=False, weighted=True)
      graph2.add_edge("A", "B", 2.0)
      graph2.add_edge("B", "C", 1.0)
      graph2.add_edge("C", "D", 1.0)
      graph2.add_edge("D", "E", 1.0)

      comparator = DiffusionDistance()
    
      # Compare basic properties
      results = comparator.compare_graphs(graph1, graph2)
      print("Graph comparison results:", results)
    
      # Compare diffusion processes
      start_nodes = {"A"}
      diffusion_results = comparator.compare_diffusion_processes(
        graph1, graph2, start_nodes, steps=5, num_simulations=10
    )
      print("Diffusion comparison results:", diffusion_results)

#claude ai
from typing import Dict, Set, List, Tuple
from collections import defaultdict
import math

class GraphKernelDistance(Distance):
         
    def __init__(self, max_iterations: int = 100, tolerance: float = 1e-10)-> None:
        super().__init__()
        self.type='graph'
        self.max_iterations = max_iterations
        self.tolerance = tolerance

    def compute_heat_kernel(self, graph, t: float = 1.0) -> Dict[str, Dict[str, float]]:
        kernel = defaultdict(dict)
        laplacian = Graph.compute_laplacian(graph)
        
        for start_node in graph.nodes:
            vector = {node: 1.0 if node == start_node else 0.0 for node in graph.nodes}
            result = vector.copy()
            factorial = 1
            power = vector.copy()
            
            for k in range(1, self.max_iterations):
                factorial *= k
                power = Graph.multiply_matrix_vector(laplacian, power)
                term = {node: ((-t) ** k) * val / factorial 
                       for node, val in power.items()}
                
                max_change = 0.0
                for node in graph.nodes:
                    result[node] += term[node]
                    max_change = max(max_change, abs(term[node]))
                
                if max_change < self.tolerance:
                    break
            
            kernel[start_node] = result
        
        return kernel
    
    def compute_random_walk_kernel(self, graph, lambda_param: float = 0.1) -> Dict[str, Dict[str, float]]:
        transition = graph.get_transition_matrix()
        kernel = defaultdict(dict)
        
        for start_node in graph.nodes:
            vector = {node: 1.0 if node == start_node else 0.0 for node in graph.nodes}
            result = {node: lambda_param * val for node, val in vector.items()}
            current = vector.copy()
            current_lambda = lambda_param
            
            for _ in range(self.max_iterations):
                current_lambda *= lambda_param
                current = Graph.multiply_matrix_vector(transition, current)
                
                max_change = 0.0
                for node in graph.nodes:
                    change = current_lambda * current[node]
                    result[node] += change
                    max_change = max(max_change, abs(change))
                
                if max_change < self.tolerance:
                    break
            
            kernel[start_node] = result
        
        return kernel
    
    def compute_kernel_distance(self, graph1, graph2, kernel_type: str = 'heat', 
                              **kernel_params) -> float:
        if kernel_type == 'heat':
            t = kernel_params.get('t', 1.0)
            kernel1 = self.compute_heat_kernel(graph1, t)
            kernel2 = self.compute_heat_kernel(graph2, t)
        else:
            lambda_param = kernel_params.get('lambda_param', 0.1)
            kernel1 = self.compute_random_walk_kernel(graph1, lambda_param)
            kernel2 = self.compute_random_walk_kernel(graph2, lambda_param)
        
        common_nodes = graph1.nodes.intersection(graph2.nodes)
        if not common_nodes:
            return float('inf')
        
        distance = 0.0
        for i in common_nodes:
            for j in common_nodes:
                diff = kernel1[i][j] - kernel2[i][j]
                distance += diff * diff
        
        return math.sqrt(distance)
    
    def compute_multiple_kernel_distances(self, graph1, graph2) -> Dict[str, float]:
        return {
            'heat_kernel_t_1': self.compute_kernel_distance(
                graph1, graph2, kernel_type='heat', t=1.0
            ),
            'heat_kernel_t_0.1': self.compute_kernel_distance(
                graph1, graph2, kernel_type='heat', t=0.1
            ),
            'random_walk_lambda_0.1': self.compute_kernel_distance(
                graph1, graph2, kernel_type='random_walk', lambda_param=0.1
            ),
            'random_walk_lambda_0.01': self.compute_kernel_distance(
                graph1, graph2, kernel_type='random_walk', lambda_param=0.01
            )
        }
    def example(self):
    
      # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "A", 1.5)

      graph2 = Graph(weighted=True)
      graph2.add_edge("A", "B", 2.0)
      graph2.add_edge("B", "C", 1.0)
      graph2.add_edge("C", "A", 1.0)

      kernel_distance = GraphKernelDistance()
    
      # Compute single kernel distance
      distance = kernel_distance.compute_kernel_distance(graph1, graph2, 'heat', t=1.0)
      print(f"Heat kernel distance (t=1.0): {distance}")
    
      # Compute multiple kernel distances
      distances = kernel_distance.compute_multiple_kernel_distances(graph1, graph2)
      for name, dist in distances.items():
        print(f"{name}: {dist}")
        
class FrobeniusDistance(Distance):
    def __init__(self)-> None:
        super().__init__()
        self.type='graph'
    '''
    def compute(self, graph1, graph2):
        if len(graph1.nodes) != len(graph2.nodes):
            raise ValueError("Graphs must have the same number of nodes")

        distance = 0
        matrix1 = graph1.adj_list
        matrix2 = graph2.adj_list
        
        for i in range(len(matrix1)):
            for j in range(len(matrix1[i])):
                diff = matrix1[i][j] - matrix2[i][j]
                distance += diff * diff
        
        return distance ** 0.5
    '''
    def compute(self,g1: 'Graph',g2: 'Graph') -> float:
        """
        Calculate the Frobenius distance between this graph and another graph.
        The Frobenius distance is defined as the Frobenius norm of the difference 
        between the adjacency matrices of the two graphs.
        
        Args:
            other (Graph): Another graph to compare with
            
        Returns:
            float: The Frobenius distance between the two graphs
            
        Raises:
            ValueError: If the graphs have different nodes or incompatible properties
            
        Example:
            >>> g1 = Graph()
            >>> g1.add_edge('A', 'B', 1.0)
            >>> g2 = Graph()
            >>> g2.add_edge('A', 'B', 2.0)
            >>> distance = g1.frobenius_distance(g2)
        """
        # Check if graphs have the same properties
        if g1.directed != g2.directed:
            raise ValueError("Cannot compare directed with undirected graphs")
        if g1.weighted != g2.weighted:
            raise ValueError("Cannot compare weighted with unweighted graphs")
            
        # Ensure both graphs have the same nodes
        if g1.nodes != g2.nodes:
            raise ValueError("Graphs must have the same set of nodes")
            
        # Get adjacency matrices
        matrix1 = g1.get_adjacency_matrix()
        matrix2 = g2.get_adjacency_matrix()
        
        # Calculate Frobenius norm of the difference
        sum_squares = 0.0
        for i in range(len(matrix1)):
            for j in range(len(matrix1[0])):
                diff = matrix1[i][j] - matrix2[i][j]
                sum_squares += diff * diff
                
        return sum_squares**0.5
         
    def example(self):
      """
      Test the Frobenius distance calculation between graphs
      """
      # Test 1: Identical graphs
      g1 = Graph(weighted=True)
      g1.add_edge('A', 'B', 1.0)
      g1.add_edge('B', 'C', 2.0)
    
      # Test 3: Different structure
      print("Test : Different structure of graph")
      g4 = Graph(weighted=True)
      g4.add_edge('A', 'B', 1.0)
      g4.add_edge('B', 'C', 2.0)
      g4.add_edge('A', 'C', 1.5)  # Additional edge
    
      g1.add_node('C')  # Ensure both graphs have same nodes
      distance = self.compute(g1,g4)
      print(f"Distance between graphs with different structure: {distance}")
'''ne fonctionne pas avec la structure dict
class PatternBasedDistance(Distance):
    def __init__(self,motif_size=3)-> None:
        super().__init__()
        self.type='graph'

        self.motif_size = motif_size

    def compute(self, graph1, graph2):
        motifs1 = graph1.count_motifs(self.motif_size)
        motifs2 = graph2.count_motifs(self.motif_size)
        return self._calculate_distance(motifs1, motifs2)

    def _calculate_distance(self, motifs1, motifs2):
        all_motifs = set(motifs1.keys()).union(set(motifs2.keys()))
        distance = 0
        for motif in all_motifs:
            freq1 = motifs1.get(motif, 0)
            freq2 = motifs2.get(motif, 0)
            distance += abs(freq1 - freq2)
        return distance
        
    def example(self):
       # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "A", 1.5)

      graph2 = Graph(weighted=True)
      graph2.add_edge("A", "B", 2.0)
      graph2.add_edge("B", "C", 1.0)
      graph2.add_edge("C", "A", 1.0)

      #graph1 = Graph(nodes1, edges1)
      #graph2 = Graph(nodes2, edges2)

      pattern_distance = self.compute(graph1, graph2)

      print(f"La distance basée sur les motifs entre les deux graphes est: {pattern_distance}")
 '''
from typing import Dict, Set, List, Tuple, DefaultDict
from collections import defaultdict, deque

class PatternBasedDistance(Distance):

    def __init__(self, max_pattern_size: int = 4)-> None:
        super().__init__()

        self.max_pattern_size = max_pattern_size
        self.patterns_cache = {}
    
    def _get_neighbors(self, graph, node) -> Set[str]:
        if graph.weighted:
            return set(graph.adj_list[node].keys())
        return graph.adj_list[node]
    
    def _find_cycles(self, graph, node: str, size: int) -> List[Set[str]]:
        cycles = []
        visited = {node}
        path = [node]
        
        def dfs(current: str, start: str, depth: int):
            if depth == size - 1:
                neighbors = self._get_neighbors(graph, current)
                if start in neighbors:
                    cycles.append(set(path))
                return
            
            for neighbor in self._get_neighbors(graph, current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(neighbor, start, depth + 1)
                    path.pop()
                    visited.remove(neighbor)
        
        dfs(node, node, 0)
        return cycles
    
    def _find_paths(self, graph, node: str, length: int) -> List[List[str]]:
        paths = []
        path = [node]
        
        def dfs(current: str, depth: int):
            if depth == length:
                paths.append(path[:])
                return
            
            for neighbor in self._get_neighbors(graph, current):
                if neighbor not in path:
                    path.append(neighbor)
                    dfs(neighbor, depth + 1)
                    path.pop()
        
        dfs(node, 1)
        return paths
    
    def _find_stars(self, graph, node: str, size: int) -> List[Set[str]]:
        neighbors = self._get_neighbors(graph, node)
        if len(neighbors) < size - 1:
            return []
        
        stars = []
        from itertools import combinations
        for star_neighbors in combinations(neighbors, size - 1):
            stars.append({node} | set(star_neighbors))
        
        return stars
    
    def _compute_pattern_frequency(self, graph, pattern_type: str, size: int) -> DefaultDict[int, float]:
        cache_key = (id(graph), pattern_type, size)
        if cache_key in self.patterns_cache:
            return self.patterns_cache[cache_key]
        
        patterns = defaultdict(float)
        total_patterns = 0
        
        for node in graph.nodes:
            if pattern_type == 'cycle':
                found_patterns = self._find_cycles(graph, node, size)
            elif pattern_type == 'path':
                found_patterns = [set(path) for path in self._find_paths(graph, node, size)]
            else:  # star
                found_patterns = self._find_stars(graph, node, size)
            
            for pattern in found_patterns:
                pattern_hash = len(pattern)  # Simplified hash
                patterns[pattern_hash] += 1
                total_patterns += 1
        
        if total_patterns > 0:
            for key in patterns:
                patterns[key] /= total_patterns
        
        self.patterns_cache[cache_key] = patterns
        return patterns
    
    def _compute_weighted_pattern_frequency(self, graph, pattern_type: str, size: int) -> DefaultDict[int, float]:
        if not graph.weighted:
            return self._compute_pattern_frequency(graph, pattern_type, size)
        
        patterns = defaultdict(float)
        total_weight = 0
        
        for node in graph.nodes:
            if pattern_type == 'cycle':
                found_patterns = self._find_cycles(graph, node, size)
            elif pattern_type == 'path':
                found_patterns = [set(path) for path in self._find_paths(graph, node, size)]
            else:  # star
                found_patterns = self._find_stars(graph, node, size)
            
            for pattern in found_patterns:
                pattern_hash = len(pattern)  # Simplified hash
                pattern_weight = 0
                
                pattern_list = list(pattern)
                for i in range(len(pattern_list)):
                    for j in range(i + 1, len(pattern_list)):
                        u, v = pattern_list[i], pattern_list[j]
                        if v in graph.adj_list[u]:
                            pattern_weight += graph.adj_list[u][v]
                
                patterns[pattern_hash] += pattern_weight
                total_weight += pattern_weight
        
        if total_weight > 0:
            for key in patterns:
                patterns[key] /= total_weight
        
        return patterns
    
    def compute_pattern_vector(self, graph) -> Dict[str, DefaultDict[int, float]]:
        pattern_vector = {}
        
        for pattern_type in ['cycle', 'path', 'star']:
            for size in range(3, self.max_pattern_size + 1):
                key = f"{pattern_type}_{size}"
                pattern_vector[key] = self._compute_weighted_pattern_frequency(
                    graph, pattern_type, size
                )
        
        return pattern_vector
    
    def compute(self, graph1, graph2, 
                        pattern_weights: Dict[str, float] = None) -> Dict[str, float]:
        if pattern_weights is None:
            pattern_weights = {
                'cycle': 1.0,
                'path': 1.0,
                'star': 1.0
            }
        
        vector1 = self.compute_pattern_vector(graph1)
        vector2 = self.compute_pattern_vector(graph2)
        
        distances = {}
        
        # L1 distance
        l1_distance = 0
        for key in vector1:
            pattern_type = key.split('_')[0]
            weight = pattern_weights.get(pattern_type, 1.0)
            
            all_patterns = set(vector1[key].keys()) | set(vector2[key].keys())
            for pattern in all_patterns:
                diff = abs(vector1[key].get(pattern, 0) - vector2[key].get(pattern, 0))
                l1_distance += weight * diff
        distances['l1'] = l1_distance
        
        # L2 distance
        l2_distance = 0
        for key in vector1:
            pattern_type = key.split('_')[0]
            weight = pattern_weights.get(pattern_type, 1.0)
            
            all_patterns = set(vector1[key].keys()) | set(vector2[key].keys())
            for pattern in all_patterns:
                diff = vector1[key].get(pattern, 0) - vector2[key].get(pattern, 0)
                l2_distance += weight * (diff * diff)
        distances['l2'] = math.sqrt(l2_distance)
        
        return distances
    
    def compare_specific_patterns(self, graph1, graph2, 
                                pattern_type: str, 
                                size: int) -> Dict[str, float]:
        freq1 = self._compute_weighted_pattern_frequency(graph1, pattern_type, size)
        freq2 = self._compute_weighted_pattern_frequency(graph2, pattern_type, size)
        
        all_patterns = set(freq1.keys()) | set(freq2.keys())
        
        l1_distance = sum(abs(freq1.get(p, 0) - freq2.get(p, 0)) for p in all_patterns)
        l2_distance = (sum((freq1.get(p, 0) - freq2.get(p, 0)) ** 2 
                                  for p in all_patterns))**0.5
        
        return {
            'l1_distance': l1_distance,
            'l2_distance': l2_distance,
            'pattern_count_1': len(freq1),
            'pattern_count_2': len(freq2)
        }

    def example(self):
    
      # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "D", 1.5)
      graph1.add_edge("D", "A", 1.0)
      graph1.add_edge("A", "C", 2.0)

      graph2 = Graph(weighted=True)
      graph2.add_edge("A", "B", 1.0)
      graph2.add_edge("B", "C", 1.0)
      graph2.add_edge("C", "D", 1.0)
      graph2.add_edge("D", "A", 1.0)

      pattern_distance = PatternBasedDistance(max_pattern_size=4)
    
      # Compare all patterns
      distances = pattern_distance.compute(
        graph1, graph2,
        pattern_weights={'cycle': 1.5, 'path': 1.0, 'star': 0.5}
    )
      print("Overall distances:", distances)
    
      # Compare specific pattern type
      cycle_comparison = pattern_distance.compare_specific_patterns(
        graph1, graph2, 'cycle', 4
    )
      print("Cycle pattern comparison:", cycle_comparison)
    
import zlib

class GraphCompressionDistance(Distance):
    def __init__(self)-> None:
        """
        Initialize the GraphCompressionDistance class with two graphs.
        Each graph is represented as an adjacency matrix, which is a list of lists.

        :param graph1: Adjacency matrix of the first graph
        :param graph2: Adjacency matrix of the second graph
        """
        super().__init__()
        self.type='graph'
        
    def compress(self, data):
        """
        Compress the data using zlib compression and return the compressed size.

        :param data: String representation of the graph
        :return: Length of the compressed data
        """
        compressed_data = zlib.compress(data.encode('utf-8'))
        return len(compressed_data)

    def combined_compression(self,graph1,graph2):
        """
        Compress the combined adjacency matrices of both graphs.

        :return: Length of the compressed combined adjacency matrix
        """
        combined_matrix = graph1.adjacency_to_string() + graph2.adjacency_to_string()
        return self.compress(combined_matrix)

    def compute(self, graph1, graph2):
        """
        Compute the Graph Compression Distance between the two graphs.

        :return: Compression distance between the two graphs
        """
        graph1_compressed_size = self.compress(graph1.adjacency_to_string())
        graph2_compressed_size = self.compress(graph2.adjacency_to_string())
        combined_compressed_size = self.combined_compression(graph1,graph2)

        distance = combined_compressed_size - min(graph1_compressed_size, graph2_compressed_size)
        return distance
        
    def example(self):
      # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "D", 1.5)
      graph1.add_edge("D", "A", 1.0)
      graph1.add_edge("A", "C", 2.0)

      graph2 = Graph(weighted=True)
      graph2.add_edge("A", "B", 1.0)
      graph2.add_edge("B", "C", 1.0)
      graph2.add_edge("C", "D", 1.0)
      graph2.add_edge("D", "A", 1.0)
      
      distance_calculator = GraphCompressionDistance().compute(graph1, graph2)
      print(f"Graph Compression Distance: {distance_calculator}")
      
'''ne fonctionne pas avec la structure de graph dict      
class DegreeDistributionDistance(Distance):
    def __init__(self)-> None:
        """
        Initializes the DegreeDistributionDistance class with two graphs.

        :param graph1: First graph, represented as an adjacency list or edge list.
        :param graph2: Second graph, represented as an adjacency list or edge list.
        """
        super().__init__()
        self.type='graph'


    def compare_distributions(self, dist1, dist2):
        """
        Compares two degree distributions using a simple difference metric.

        :param dist1: Degree distribution of the first graph.
        :param dist2: Degree distribution of the second graph.
        :return: A floating-point value representing the difference between the distributions.
        """
        all_degrees = set(dist1.keys()).union(set(dist2.keys()))
        difference = 0.0
        for degree in all_degrees:
            count1 = dist1.get(degree, 0)
            count2 = dist2.get(degree, 0)
            difference += abs(count1 - count2)
        return difference

    def compute(self, graph1, graph2):
        """
        Computes the degree distribution distance between the two graphs.

        :return: A floating-point value representing the distance between the degree distributions of the two graphs.
        """
        dist1 = Graph.compute_degree_distribution(graph1)
        dist2 = Graph.compute_degree_distribution(graph2)
        return self.compare_distributions(dist1, dist2)
        

'''
from collections import defaultdict
from typing import Dict, Set

class DegreeDistributionDistance(Distance):
    def __init__(self)-> None:
      
        super().__init__()
        self.type='graph'
        self.reset()

    def reset(self):
        self.degrees1 = {}
        self.degrees2 = {}
        self.distance = 0.0

    def compute(self, graph1: Graph, graph2: Graph) -> float:
        self.reset()
        
        # Verify that both graphs are of the same type
        if graph1.weighted != graph2.weighted or graph1.directed != graph2.directed:
            raise ValueError("Graphs must be of the same type (both weighted or both unweighted, both directed or both undirected)")
        
        # Compute degree distributions
        self.degrees1 = Graph.compute_degrees(graph1)
        self.degrees2 = Graph.compute_degrees(graph2)
        
        # Get all unique degrees
        all_degrees = set(list(self.degrees1.keys()) + list(self.degrees2.keys()))
        
        # Calculate L1 distance
        self.distance = 0.0
        for degree in all_degrees:
            prob1 = self.degrees1.get(degree, 0.0)
            prob2 = self.degrees2.get(degree, 0.0)
            self.distance += abs(prob1 - prob2)
        
        return self.distance

    def get_distributions(self):
        return self.degrees1, self.degrees2

    def example(self):
      # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "D", 1.5)
      graph1.add_edge("D", "A", 1.0)
      graph1.add_edge("A", "C", 2.0)

      graph2 = Graph(weighted=True)
      graph2.add_edge("A", "B", 1.0)
      graph2.add_edge("B", "C", 1.0)
      
      distance=self.compute(graph1,graph2)
      print(f"Graph DegreeDistributionDistance: {distance}")

from collections import defaultdict
from typing import Dict, Set, List, Tuple
import random

class CommunityStructureDistance(Distance):
    def __init__(self)-> None:
      
        super().__init__()
        self.type='graph'
        self.reset()

    def reset(self):
        # Reset computed values
        self.communities1 = {}
        self.communities2 = {}
        self.distance = 0.0

    def modularity(self, graph: Graph, communities: Dict[str, int]) -> float:
        # Calculate modularity Q = 1/2m * sum(Aij - kikj/2m)δ(ci,cj)
        if not graph.nodes:
            return 0.0

        total_weight = 0
        node_degrees = defaultdict(float)

        # Calculate total weight and node degrees
        for node in graph.nodes:
            for neighbor, weight in graph.adj_list[node].items():
                if graph.weighted:
                    w = weight
                else:
                    w = 1.0
                node_degrees[node] += w
                if not graph.directed:
                    total_weight += w / 2
                else:
                    total_weight += w

        if total_weight == 0:
            return 0.0

        modularity = 0.0
        for node in graph.nodes:
            for neighbor in graph.adj_list[node]:
                if communities[node] == communities[neighbor]:
                    if graph.weighted:
                        actual = graph.adj_list[node][neighbor]
                    else:
                        actual = 1.0
                    expected = node_degrees[node] * node_degrees[neighbor] / (2.0 * total_weight)
                    modularity += (actual - expected)

        modularity /= (2.0 * total_weight)
        return modularity

    def detect_communities(self, graph: Graph) -> Dict[str, int]:
        # Implementation of Louvain method for community detection
        communities = {node: idx for idx, node in enumerate(graph.nodes)}
        n_communities = len(communities)
        
        improvement = True
        while improvement:
            improvement = False
            
            # Phase 1: Modularity optimization
            for node in graph.nodes:
                current_community = communities[node]
                neighbor_communities = {}
                
                # Calculate gain for moving to each neighbor's community
                for neighbor in graph.adj_list[node]:
                    neighbor_community = communities[neighbor]
                    if neighbor_community not in neighbor_communities:
                        # Remove node from its current community
                        communities[node] = neighbor_community
                        gain = self.modularity(graph, communities)
                        communities[node] = current_community
                        neighbor_communities[neighbor_community] = gain
                
                # Find best community
                best_community = current_community
                best_gain = 0.0
                
                for community, gain in neighbor_communities.items():
                    if gain > best_gain:
                        best_gain = gain
                        best_community = community
                
                if best_community != current_community:
                    communities[node] = best_community
                    improvement = True
            
            if not improvement:
                break
            
            # Phase 2: Community aggregation
            new_communities = {}
            idx = 0
            for old_community in set(communities.values()):
                new_communities[old_community] = idx
                idx += 1
            
            for node in communities:
                communities[node] = new_communities[communities[node]]

        return communities

    def compute(self, graph1: Graph, graph2: Graph) -> float:
        # Reset previous computations
        self.reset()
        
        # Verify graphs are compatible
        if graph1.weighted != graph2.weighted or graph1.directed != graph2.directed:
            raise ValueError("Graphs must be of the same type")

        # Detect communities in both graphs
        self.communities1 = self.detect_communities(graph1)
        self.communities2 = self.detect_communities(graph2)

        # Convert to community size distributions
        dist1 = self._get_community_size_distribution(self.communities1)
        dist2 = self._get_community_size_distribution(self.communities2)

        # Calculate L1 distance between distributions
        all_sizes = set(list(dist1.keys()) + list(dist2.keys()))
        
        distance = 0.0
        for size in all_sizes:
            prob1 = dist1.get(size, 0.0)
            prob2 = dist2.get(size, 0.0)
            distance += abs(prob1 - prob2)

        return distance

    def _get_community_size_distribution(self, communities: Dict[str, int]) -> Dict[int, float]:
        # Count community sizes
        community_sizes = defaultdict(int)
        for community_id in communities.values():
            community_sizes[community_id] += 1
        
        # Convert to size distribution
        size_distribution = defaultdict(float)
        total_nodes = len(communities)
        
        for community_id, size in community_sizes.items():
            size_distribution[size] += 1
        
        # Normalize
        for size in size_distribution:
            size_distribution[size] /= total_nodes
            
        return dict(size_distribution)

    def get_communities(self):
        return self.communities1, self.communities2
        
    def example(self):
      # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "D", 1.5)
      graph1.add_edge("D", "A", 1.0)
      graph1.add_edge("A", "C", 2.0)

      graph2 = Graph(weighted=True)
      graph2.add_edge("A", "B", 1.0)
      graph2.add_edge("B", "C", 1.0)
      graph2.add_edge("C", "D", 1.0)
      # Compare community structures
      csd = CommunityStructureDistance()
      distance = csd.compute(graph1, graph2)
      print(f"Community structure distance: {distance}")

      # Get detected communities if needed
      communities1, communities2 = csd.get_communities()
      print("Communities in graph 1:", communities1)
      print("Communities in graph 2:", communities2)
