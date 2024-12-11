
cpdef class MarkovChainKullbackLeibler:

    cpdef list[float] def compute(self, matrix, tolerance=1e-10, max_iterations=1000):

    cpdef float def kl_divergence(self, p, q):

    cpdef float def kullback_leibler_distance(self):

cpdef class MarkovChainWasserstein:

    cpdef double def compute(self):

    cpdef float def _compute_wasserstein_greedy(self, pi_P, pi_Q):

cpdef class MarkovChainTotalVariation:

    cpdef float def total_variation_distance(self, pi_P, pi_Q):

    cpdef double def compute(self):

cpdef class MarkovChainHellinger:

    cpdef def hellinger_distance(self, pi_P, pi_Q):

    cpdef double def compute(self):

cpdef class MarkovChainJensenShannon:

    cpdef float def kl_divergence(self, p, q):

    cpdef float def jensen_shannon_divergence(self, pi_P, pi_Q):

    cpdef double def compute(self):

cpdef class MarkovChainFrobenius:

    cpdef double def compute(self):

cpdef class MarkovChainSpectral:

    cpdef def eigenvalues_2x2(self, matrix):

    cpdef double def compute(self):



