from .mainClass import *
from .vectorDistance import Euclidean

from typing import List, Dict, Set, Tuple, TypeVar, Callable

#claude ai
T = TypeVar('T')
class Levenshtein(Distance):
	def __init__(self, insert_cost: float = 1.0, delete_cost: float = 1.0, replace_cost: float = 1.0):
		super().__init__()
		self.type='text'

		self.insert_cost = insert_cost
		self.delete_cost = delete_cost
		self.replace_cost = replace_cost
		self.equality_func = lambda x, y: x == y


	def compute(self, s1: List[T], s2: List[T]) -> float:
		m: int = len(s1)
		n: int = len(s2)
        
		# Initialisation de la matrice
		dp: List[List[float]] = [[0.0 for _ in range(n + 1)] for _ in range(m + 1)]
        
		# Remplissage de la première ligne et de la première colonne
		for i in range(m + 1):
			dp[i][0] = i * self.delete_cost
		for j in range(n + 1):
			dp[0][j] = j * self.insert_cost
        
		# Calcul de la distance
		for i in range(1, m + 1):
			for j in range(1, n + 1):
				if self.equality_func(s1[i-1], s2[j-1]):
					dp[i][j] = dp[i-1][j-1]
				else:
					dp[i][j] = min(
						dp[i-1][j] + self.delete_cost,  # Suppression
						dp[i][j-1] + self.insert_cost,  # Insertion
						dp[i-1][j-1] + self.replace_cost  # Remplacement
						)
        
		return dp[m][n]

	@staticmethod
	def levenshtein_distance_words(sentence1: str, sentence2: str) -> float:
			words1 = sentence1.split()
			words2 = sentence2.split()
			lev = Levenshtein()
			return lev.compute(words1, words2)



'''
class Levenshtein(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		
	def compute(self,s1: str, s2: str) -> int:
		
		dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

		for i in range(len(s1) + 1):
			dp[i][0] = i
		for j in range(len(s2) + 1):
			dp[0][j] = j

		for i in range(1, len(s1) + 1):
			for j in range(1, len(s2) + 1):
				if s1[i - 1] == s2[j - 1]:
					cost = 0
				else:
					cost = 1
				dp[i][j] = min(dp[i - 1][j] + 1,        # Suppression
                           dp[i][j - 1] + 1,        # Insertion
                           dp[i - 1][j - 1] + cost) # Substitution

		return dp[len(s1)][len(s2)]
		
	def exemple(self):
		self.obj1_exemple = "kitten"
		self.obj2_exemple = "sitting"
		super().exemple()
'''
class DamerauLevenshtein(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='str'

	def compute(self,s1 :str, s2 :str) -> int:
		d = {}
		lenstr1 = len(s1)
		lenstr2 = len(s2)

		for i in range(-1, lenstr1 + 1):
			d[(i, -1)] = i + 1
		for j in range(-1, lenstr2 + 1):
			d[(-1, j)] = j + 1

		for i in range(lenstr1):
			for j in range(lenstr2):
				cost = 0 if s1[i] == s2[j] else 1
				d[(i, j)] = min(
					d[(i - 1, j)] + 1,  # suppresion
					d[(i, j - 1)] + 1,  # insertion
					d[(i - 1, j - 1)] + cost,  # substitution
				)
				if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
					d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)  # transposition

		return d[lenstr1 - 1, lenstr2 - 1]
		
	def exemple(self):
		self.obj1_exemple = "ca"
		self.obj2_exemple = "abc"

		super().exemple()
		
#claude ai
from typing import List, Union, Dict

class Cosine(Distance):
	def __init__(self)-> None:
		super().__init__()
		#self.type='vec_float'
		self.type='text'
		
	@staticmethod
	def string_to_vector(text: str) -> Dict[str, int]:
		"""Converts a string into a word frequency vector."""
		words: List[str] = text.lower().split()
		return {word: words.count(word) for word in set(words)}

	@staticmethod
	def dot_product(v1: Dict[str, Union[int, float]], v2: Dict[str, Union[int, float]]) -> float:
		"""Calculates the dot product of two vectors."""
		return sum(v1.get(key, 0) * v2.get(key, 0) for key in set(v1) | set(v2))

	@staticmethod
	def magnitude(vector: Dict[str, Union[int, float]]) -> float:
		"""Calculates the magnitude of a vector."""
		return sum(value ** 2 for value in vector.values())**0.5

	@classmethod
	def cosine_similarity(cls, v1: Dict[str, Union[int, float]], v2: Dict[str, Union[int, float]]) -> float:
		"""Calculates the cosine similarity between two vectors."""
		dot_prod: float = cls.dot_product(v1, v2)
		mag1: float = cls.magnitude(v1)
		mag2: float = cls.magnitude(v2)
        
		if mag1 == 0 or mag2 == 0:
			return 0.0
        
		return dot_prod / (mag1 * mag2)

	@classmethod
	def compute(cls, v1: Union[str, List[float]], v2: Union[str, List[float]]) -> float:
		"""Calculates the cosine distance between two vectors or strings."""
		if isinstance(v1, str) and isinstance(v2, str):
			v1_dict: Dict[str, int] = cls.string_to_vector(v1)
			v2_dict: Dict[str, int] = cls.string_to_vector(v2)
		elif isinstance(v1, list) and isinstance(v2, list):
			v1_dict: Dict[str, float] = {str(i): val for i, val in enumerate(v1)}
			v2_dict: Dict[str, float] = {str(i): val for i, val in enumerate(v2)}
		else:
			raise ValueError("Inputs must be either two strings or two lists of floats.")
        
		similarity: float = cls.cosine_similarity(v1_dict, v2_dict)
		return 1.0 - similarity

class CosineInverse(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='text'
		
	def compute(self,vec1 :list, vec2 :list)-> float:
		return 1-Cosine().compute(vec1,vec2)
		
class CosineTF(Distance):

    def __init__(self)-> None:
      super().__init__()
      self.type='text'
    """
    A class to compute the Cosine Similarity between two text documents based on term frequency vectors.
    """


    def _tokenize(self, document: str) -> List[str]:
        """
        Tokenizes the document into individual words (tokens).
        
        :param document: The input document as a string.
        :return: A list of tokens (words) from the document.
        """
        return document.lower().split()

    def _compute_term_frequencies(self, tokens: List[str]) -> Dict[str, int]:
        """
        Computes the term frequency (TF) of each token in the document.
        
        :param tokens: A list of tokens extracted from the document.
        :return: A dictionary where keys are tokens and values are their frequencies in the document.
        """
        term_frequencies: Dict[str, int] = {}
        for token in tokens:
            if token in term_frequencies:
                term_frequencies[token] += 1
            else:
                term_frequencies[token] = 1
        return term_frequencies

    def _dot_product(self, vec1: Dict[str, int], vec2: Dict[str, int]) -> float:
        """
        Computes the dot product of two term frequency vectors.
        
        :param vec1: The first term frequency vector as a dictionary.
        :param vec2: The second term frequency vector as a dictionary.
        :return: The dot product of the two vectors.
        """
        dot_product: float = 0.0
        for term, freq in vec1.items():
            if term in vec2:
                dot_product += freq * vec2[term]
        return dot_product

    def _magnitude(self, vec: Dict[str, int]) -> float:
        """
        Computes the magnitude (Euclidean norm) of a term frequency vector.
        
        :param vec: A term frequency vector as a dictionary.
        :return: The magnitude of the vector.
        """
        magnitude: float = math.sqrt(sum(freq ** 2 for freq in vec.values()))
        return magnitude

    def compute(self, document1: str, document2: str) -> float:
        """
        Computes the Cosine Similarity between two documents.
        
        :param document1: The first document as a string.
        :param document2: The second document as a string.
        :return: The cosine similarity score between 0 and 1.
        """
        # Tokenize both documents
        tokens1: List[str] = self._tokenize(document1)
        tokens2: List[str] = self._tokenize(document2)

        # Compute term frequencies
        tf1: Dict[str, int] = self._compute_term_frequencies(tokens1)
        tf2: Dict[str, int] = self._compute_term_frequencies(tokens2)

        # Compute the dot product of the two vectors
        dot_product: float = self._dot_product(tf1, tf2)

        # Compute the magnitude of each vector
        magnitude1: float = self._magnitude(tf1)
        magnitude2: float = self._magnitude(tf2)

        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        # Compute and return the cosine similarity
        cosine_similarity: float = dot_product / (magnitude1 * magnitude2)
        return cosine_similarity
'''    
import math
from collections import Counter

class TFIDFDistance(Distance):

    def __init__(self, corpus: List[str]) -> None:
        """
        Initialisation de la classe TFIDFDistance.
        
        :param corpus: Liste de documents (chaîne de caractères) utilisés pour calculer les fréquences globales des termes.
        """
        super().__init__()
        self.type='text'
        self.corpus = corpus
        self.term_frequencies = self._compute_term_frequencies(corpus)
        self.document_frequencies = self._compute_document_frequencies(corpus)

    def _compute_term_frequencies(self, corpus: List[str]) -> List[Dict[str, int]]:
        """
        Calcule la fréquence des termes pour chaque document du corpus.
        
        :param corpus: Liste de documents.
        :return: Liste de dictionnaires de fréquences de termes pour chaque document.
        """
        term_frequencies = [Counter(doc.split()) for doc in corpus]
        return term_frequencies

    def _compute_document_frequencies(self, corpus: List[str]) -> Dict[str, int]:
        """
        Calcule la fréquence inverse des documents (DF) pour chaque terme du corpus.
        
        :param corpus: Liste de documents.
        :return: Dictionnaire de fréquence inverse des documents pour chaque terme.
        """
        doc_freq: Dict[str, int] = {}
        for document in corpus:
            unique_terms = set(document.split())
            for term in unique_terms:
                doc_freq[term] = doc_freq.get(term, 0) + 1
        return doc_freq

    def _compute_tf_idf(self, document: str) -> Dict[str, float]:
        """
        Calcule les valeurs TF-IDF pour un document donné.
        
        :param document: Chaîne de caractères représentant un document.
        :return: Dictionnaire des valeurs TF-IDF pour chaque terme du document.
        """
        term_freq: Dict[str, int] = Counter(document.split())
        total_terms = len(document.split())
        tf_idf: Dict[str, float] = {}
        
        for term, freq in term_freq.items():
            tf = freq / total_terms
            idf = math.log(len(self.corpus) / (1 + self.document_frequencies.get(term, 0)))
            tf_idf[term] = tf * idf

        return tf_idf

    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Calcule la similarité cosinus entre deux vecteurs TF-IDF.
        
        :param vec1: Premier vecteur TF-IDF.
        :param vec2: Deuxième vecteur TF-IDF.
        :return: Valeur de similarité cosinus.
        """
        intersection = set(vec1.keys()).intersection(vec2.keys())
        dot_product = sum(vec1[term] * vec2[term] for term in intersection)
        
        norm1 = math.sqrt(sum([value ** 2 for value in vec1.values()]))
        norm2 = math.sqrt(sum([value ** 2 for value in vec2.values()]))
        
        if not norm1 or not norm2:
            return 0.0
        
        return dot_product / (norm1 * norm2)

    def compare(self, text1: str, text2: str) -> float:
        """
        Compare deux textes en utilisant la distance TF-IDF (Cosine Similarity).
        
        :param text1: Premier document à comparer.
        :param text2: Deuxième document à comparer.
        :return: Valeur de la similarité entre 0 et 1 (plus elle est proche de 1, plus les documents sont similaires).
        """
        tf_idf1 = self._compute_tf_idf(text1)
        tf_idf2 = self._compute_tf_idf(text2)
        return self._cosine_similarity(tf_idf1, tf_idf2)
'''


class TFIDF(Distance):

    def __init__(self,corpus: List[str]=[
    "the cat sat on the mat",
    "the dog sat on the mat",
    "the dog chased the cat"
])-> None:
      super().__init__()
      self.type='text'
      self.corpus=corpus
    """
    A class to compute the similarity between two documents based on TF-IDF (Term Frequency-Inverse Document Frequency).
    """

    def _tokenize(self, document: str) -> List[str]:
        """
        Tokenizes the document into individual words (tokens).
        
        :param document: The input document as a string.
        :return: A list of tokens (words) from the document.
        """
        return document.lower().split()

    def _compute_term_frequencies(self, tokens: List[str]) -> Dict[str, int]:
        """
        Computes the term frequency (TF) of each token in the document.
        
        :param tokens: A list of tokens extracted from the document.
        :return: A dictionary where keys are tokens and values are their frequencies in the document.
        """
        term_frequencies: Dict[str, int] = {}
        for token in tokens:
            if token in term_frequencies:
                term_frequencies[token] += 1
            else:
                term_frequencies[token] = 1
        return term_frequencies

    def _compute_document_frequencies(self, documents: List[List[str]]) -> Dict[str, int]:
        """
        Computes the document frequency (DF) for each token across multiple documents.
        
        :param documents: A list of tokenized documents (each document is a list of tokens).
        :return: A dictionary where keys are tokens and values are the number of documents containing the token.
        """
        document_frequencies: Dict[str, int] = {}
        for tokens in documents:
            unique_tokens: Set[str] = set(tokens)
            for token in unique_tokens:
                if token in document_frequencies:
                    document_frequencies[token] += 1
                else:
                    document_frequencies[token] = 1
        return document_frequencies

    def _compute_tfidf(self, term_freq: Dict[str, int], doc_freq: Dict[str, int], total_docs: int) -> Dict[str, float]:
        """
        Computes the TF-IDF value for each token in the document.
        
        :param term_freq: Term frequency for a document.
        :param doc_freq: Document frequency for all documents.
        :param total_docs: Total number of documents.
        :return: A dictionary where keys are tokens and values are their TF-IDF values.
        """
        tfidf: Dict[str, float] = {}
        for term, freq in term_freq.items():
            tf: float = freq / sum(term_freq.values())
            idf: float = math.log(total_docs / (1 + doc_freq.get(term, 0)))
            tfidf[term] = tf * idf
        return tfidf

    def _dot_product(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Computes the dot product of two TF-IDF vectors.
        
        :param vec1: The first TF-IDF vector as a dictionary.
        :param vec2: The second TF-IDF vector as a dictionary.
        :return: The dot product of the two vectors.
        """
        dot_product: float = 0.0
        for term, value in vec1.items():
            if term in vec2:
                dot_product += value * vec2[term]
        return dot_product

    def _magnitude(self, vec: Dict[str, float]) -> float:
        """
        Computes the magnitude (Euclidean norm) of a TF-IDF vector.
        
        :param vec: A TF-IDF vector as a dictionary.
        :return: The magnitude of the vector.
        """
        magnitude: float = math.sqrt(sum(value ** 2 for value in vec.values()))
        return magnitude

    def compute(self, document1: str, document2: str) -> float:
        """
        Computes the TF-IDF similarity (cosine similarity) between two documents based on a corpus of documents.
        
        :param document1: The first document as a string.
        :param document2: The second document as a string.
        :param corpus: A list of documents representing the corpus.
        :return: The TF-IDF similarity score between 0 and 1.
        """
        # Tokenize both documents and the corpus
        tokens1: List[str] = self._tokenize(document1)
        tokens2: List[str] = self._tokenize(document2)
        tokenized_corpus: List[List[str]] = [self._tokenize(doc) for doc in self.corpus]

        # Add the documents to the corpus for frequency calculations
        tokenized_corpus.append(tokens1)
        tokenized_corpus.append(tokens2)

        # Compute term frequencies for both documents
        tf1: Dict[str, int] = self._compute_term_frequencies(tokens1)
        tf2: Dict[str, int] = self._compute_term_frequencies(tokens2)

        # Compute document frequencies from the corpus
        doc_freq: Dict[str, int] = self._compute_document_frequencies(tokenized_corpus)

        # Total number of documents
        total_docs: int = len(tokenized_corpus)

        # Compute TF-IDF vectors for both documents
        tfidf1: Dict[str, float] = self._compute_tfidf(tf1, doc_freq, total_docs)
        tfidf2: Dict[str, float] = self._compute_tfidf(tf2, doc_freq, total_docs)

        # Compute the dot product of the two TF-IDF vectors
        dot_product: float = self._dot_product(tfidf1, tfidf2)

        # Compute the magnitude of each TF-IDF vector
        magnitude1: float = self._magnitude(tfidf1)
        magnitude2: float = self._magnitude(tfidf2)

        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        # Compute and return the TF-IDF cosine similarity
        tfidf_similarity: float = dot_product / (magnitude1 * magnitude2)
        return tfidf_similarity
        
    def example(self):
      # Exemple d'utilisation

      text1 = "the cat is sitting on the mat"
      text2 = "the dog is sitting on the mat"

      tfidf_distance = TFIDF()
      similarity_score: float = tfidf_distance.compute(text1, text2)

      print(f"TF-IDF Similarity: {similarity_score}")



class SimHash(Distance):

    def __init__(self)-> None:
      super().__init__()
      self.type='text'
    """
    A class to compute the SimHash of a document and to compare the SimHash values of two documents
    to measure their similarity.
    """

    def _hash(self, token: str) -> int:
        """
        Converts a token (string) into a 64-bit integer hash.

        :param token: The input string (token) to be hashed.
        :return: A 64-bit integer hash of the input token.
        """
        return int.from_bytes(token.encode('utf-8'), 'little') % (1 << 64)

    def _tokenize(self, document: str) -> List[str]:
        """
        Tokenizes the document into individual words (or tokens).

        :param document: The input document as a string.
        :return: A list of tokens (words) from the document.
        """
        return document.split()

    def _compute_weights(self, tokens: List[str]) -> Dict[str, int]:
        """
        Computes the weight of each token based on its frequency in the document.

        :param tokens: A list of tokens extracted from the document.
        :return: A dictionary where keys are tokens and values are their frequencies (weights).
        """
        token_weights: Dict[str, int] = {}
        for token in tokens:
            if token in token_weights:
                token_weights[token] += 1
            else:
                token_weights[token] = 1
        return token_weights

    def _compute_simhash(self, token_weights: Dict[str, int]) -> int:
        """
        Computes the SimHash value from the token weights using a weighted hash for each token.

        :param token_weights: A dictionary of token weights.
        :return: A 64-bit integer representing the SimHash value.
        """
        bit_vector: List[int] = [0] * 64

        for token, weight in token_weights.items():
            token_hash: int = self._hash(token)

            for i in range(64):
                # Extract each bit from the 64-bit hash
                bit = (token_hash >> i) & 1
                # Adjust the bit vector based on the weight
                if bit == 1:
                    bit_vector[i] += weight
                else:
                    bit_vector[i] -= weight

        # Convert bit_vector into a 64-bit SimHash
        simhash_value: int = 0
        for i in range(64):
            if bit_vector[i] > 0:
                simhash_value |= (1 << i)

        return simhash_value

    def compute(self, document: str) -> int:
        """
        Computes the SimHash value of a given document.

        :param document: The input document as a string.
        :return: A 64-bit integer representing the SimHash value.
        """
        tokens: List[str] = self._tokenize(document)
        token_weights: Dict[str, int] = self._compute_weights(tokens)
        simhash_value: int = self._compute_simhash(token_weights)
        return 1 - simhash_value
        
    def example(self):
      simhash = SimHash()

      # Two example documents
      doc1: str = "This is a sample document."
      doc2: str = "This is another sample document."

      # Compute similarity between the two documents
      score: float = simhash.compute(doc1)

      # Print similarity score (0 means completely different, 1 means identical)
      print(f"Similarity score between documents: {score}")




#from typing import Optional
#from gensim.models import KeyedVectors
#from gensim.similarities import WmdSimilarity
#from gensim.corpora.dictionary import Dictionary

#import gensim.downloader as api

# Import and download stopwords from NLTK.
#from nltk.corpus import stopwords
#from nltk import download
'''
class WordMoversDistance(Distance):

    def __init__(self) -> None:
        """
        Initialize the WordMoversDistance class with a pre-trained word embedding model and a corpus of texts.

        :param model: A pre-trained word embedding model (e.g., Word2Vec or GloVe).
        :param texts: A list of text documents to be compared.
        """
        super().__init__()
        self.type='text'
        #download('stopwords')  # Download stopwords list.
        #self.stop_words = stopwords.words('english')
        self.stop_words = Text.stopwords
        self.model = api.load('word2vec-google-news-300')
        #or download -> https://www.kaggle.com/datasets/leadbest/googlenewsvectorsnegative300?resource=download


    def preprocess(self,sentence):
        return [w for w in sentence.lower().split() if w not in self.stop_words]
        

    def compute_distance(self, text1: str, text2: str) -> Optional[float]:
        """
        Compute the Word Mover's Distance between two text documents.

        :param text1: The first text document.
        :param text2: The second text document.
        :return: The Word Mover's Distance between the two documents, or None if it cannot be computed.
        """
        tokens1: List[str] = self.preprocess(text1)
        tokens2: List[str] = self.preprocess(text2)
                
        if tokens1 and tokens2:
            return self.model.wmdistance(tokens1, tokens2)
        return None

    def compute(self,text1: str, text2: str) -> Optional[float]:
        """
        Compare two text files using Word Mover's Distance and a pre-trained word embedding model.

        :param text1: first text.
        :param text2: second text.
        :return: The Word Mover's Distance between the two text files, or None if it cannot be computed.
        """
        try:
            # Load the pre-trained word embedding model
            #model: KeyedVectors = KeyedVectors.load_word2vec_format(model_path, binary=True)

            # Compute and return the Word Mover's Distance
            return self.model.wmdistance(text1, text2)

        except Exception as e:
            print(f"Error processing files: {e}")
            return None
            
    def example(self):
      # Example usage comparing two text

      str1: str= 'Obama speaks to the media in Illinois'
      str2: str = 'The president greets the press in Chicago'

      wmd_distance: Optional[float] = WordMoversDistance().compute(str1, str2)


      if wmd_distance is not None:
        print(f"Word Mover's Distance between files: {wmd_distance}")
      else:
        print("Could not compute Word Mover's Distance.")
'''

#claude ai
from typing import List, Dict
from math import sqrt

class WordMoversDistance(Distance):

    """
    Calculates the Word Movers Distance (WMD) between two text documents.
    
    WMD measures the semantic distance between two texts by considering
    the embeddings of the words and the minimum amount of distance
    the words in one text need to "travel" to the other text.
    """
    
    def __init__(self, word_embeddings: Dict[str, List[float]]=None):
        """
        Initialize the Word Movers Distance calculator.
        
        Args:
            word_embeddings (Dict[str, List[float]]): Pre-trained word embeddings,
                where the keys are words and the values are the corresponding
                embedding vectors.
        """
        self.type='text'
        
        if word_embeddings==None:
           self.word_embeddings = {
        "dog": [0.1, 0.2, 0.3],
        "cat": [0.2, 0.1, 0.4],
        "house": [0.3, 0.4, 0.1],
        "home": [0.4, 0.3, 0.2],
        "the": [0.1, 0.1, 0.1],
        "and": [0.2, 0.2, 0.2]
    }
        else:
          self.word_embeddings = word_embeddings
    
    def compute(self, text1: str, text2: str) -> float:
        """
        Compute the Word Movers Distance between two text documents.
        
        Args:
            text1 (str): First text document
            text2 (str): Second text document
        
        Returns:
            float: Word Movers Distance between the two texts
        """
        # Tokenize and preprocess the texts
        tokens1 = self._preprocess_text(text1)
        tokens2 = self._preprocess_text(text2)
        
        # Compute the Word Movers Distance
        distance = self._compute_word_movers_distance(tokens1, tokens2)
        
        return distance
    
    def _preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess the input text by tokenizing and filtering out
        words that are not present in the word embeddings.
        
        Args:
            text (str): Input text
        
        Returns:
            List[str]: List of preprocessed tokens
        """
        tokens = text.lower().split()
        filtered_tokens = [token for token in tokens if token in self.word_embeddings]
        
        return list(set(filtered_tokens))
    
    def _compute_word_movers_distance(self, tokens1: List[str], tokens2: List[str]) -> float:
        """
        Compute the Word Movers Distance between two lists of tokens.
        
        Args:
            tokens1 (List[str]): Tokens from the first text
            tokens2 (List[str]): Tokens from the second text
        
        Returns:
            float: Word Movers Distance between the two sets of tokens
        """
        total_distance = 0.0
        for token1 in tokens1:
            min_distance = float('inf')
            for token2 in tokens2:
                distance = self._compute_vector_distance(self.word_embeddings[token1], self.word_embeddings[token2])
                min_distance = min(min_distance, distance)
            total_distance += min_distance
        
        # Normalize the distance by the sum of the token counts
        norm = len(tokens1)+len(tokens2)
        return total_distance / norm
    
    def _compute_vector_distance(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Compute the Euclidean distance between two vectors.
        
        Args:
            vec1 (List[float]): First vector
            vec2 (List[float]): Second vector
        
        Returns:
            float: Euclidean distance between the two vectors
        """
        return sqrt(sum((x - y)**2 for x, y in zip(vec1, vec2)))
    
    def similarity_score(self, text1: str, text2: str) -> float:
        """
        Compute a similarity score between 0 and 1.
        
        Args:
            text1 (str): First text document
            text2 (str): Second text document
        
        Returns:
            float: Similarity score (1 = identical, 0 = completely different)
        """
        distance = self.compute(text1, text2)
        max_distance = self._compute_max_distance(text1, text2)
        
        return 1.0 - (distance / max_distance) if max_distance > 0 else 1.0
    
    def _compute_max_distance(self, text1: str, text2: str) -> float:
        """
        Calculate the maximum possible Word Movers Distance between two texts.
        
        Args:
            text1 (str): First text document
            text2 (str): Second text document
        
        Returns:
            float: Maximum possible Word Movers Distance
        """
        tokens1 = self._preprocess_text(text1)
        tokens2 = self._preprocess_text(text2)
        
        max_distance = sum(self._compute_vector_distance(self.word_embeddings[token1], self.word_embeddings[token2])
                           for token1 in tokens1 for token2 in tokens2)
        
        return max_distance
    def example(self) -> None:
      # Example pre-trained word embeddings
      self.word_embeddings = {
        "dog": [0.1, 0.2, 0.3],
        "cat": [0.2, 0.1, 0.4],
        "house": [0.3, 0.4, 0.1],
        "home": [0.4, 0.3, 0.2],
        "the": [0.1, 0.1, 0.1],
        "and": [0.2, 0.2, 0.2]
    }
        
      # Example texts
      text1 = "The dog played in the house"
      text2 = "The cat is at home"
    
      # Calculate distance and similarity
      distance = self.compute(text1, text2)
      similarity = self.similarity_score(text1, text2)
    
      print(f"Word Movers Distance: {distance:.2f}")
      print(f"Similarity Score: {similarity:.2f}")
    
# Example usage
def main():
    # Example pre-trained word embeddings
    word_embeddings = {
        "dog": [0.1, 0.2, 0.3],
        "cat": [0.2, 0.1, 0.4],
        "house": [0.3, 0.4, 0.1],
        "home": [0.4, 0.3, 0.2],
        "the": [0.1, 0.1, 0.1],
        "and": [0.2, 0.2, 0.2]
    }
    
    # Create Word Movers Distance calculator
    wmd = WordMoversDistance(word_embeddings)
    
    # Example texts
    text1 = "The dog played in the house"
    text2 = "The cat is at home"
    
    # Calculate distance and similarity
    distance = wmd.calculate_distance(text1, text2)
    similarity = wmd.similarity_score(text1, text2)
    
    print(f"Word Movers Distance: {distance:.2f}")
    print(f"Similarity Score: {similarity:.2f}")

if __name__ == "__main__":
    main()


try:
    import torch
    TORCH_INSTALLED = True
except ImportError:
    TORCH_INSTALLED = False
    torch = None
# Type conditionnel en fonction de la disponibilité de torch
TensorType = Union[torch.Tensor, 'NoneType'] if TORCH_INSTALLED else Optional['Any']

try:
    from transformers import BertTokenizer, BertModel
except ImportError:
    BertTokenizer = None  
    BertModel = None  

class BERTBasedDistance(Distance):

    def __init__(self, model_name: str = "bert-base-uncased") -> None:
        """
        Initialize the BERTBasedDistance class with a BERT model and tokenizer.

        :param model_name: The name of the pre-trained BERT model to use.
        """
        super().__init__()
        self.type='text'
        self.tokenizer: BertTokenizer = BertTokenizer.from_pretrained(model_name)
        self.model: BertModel = BertModel.from_pretrained(model_name)

    def _encode_text(self, text: str) -> TensorType:
        """
        Encode a text into a BERT embedding.

        :param text: The input text to encode.
        :return: A tensor representing the embedding of the input text.
        """
        inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)  # Mean pooling over the sequence length

    def compute_distance(self, text1: str, text2: str) -> float:
        """
        Compute the cosine similarity between the BERT embeddings of two texts.

        :param text1: The first text document.
        :param text2: The second text document.
        :return: The cosine similarity between the embeddings of the two documents.
        """
        embedding1: torch.Tensor = self._encode_text(text1)
        embedding2: torch.Tensor = self._encode_text(text2)

        # Cosine similarity between the two embeddings
        similarity: float = torch.nn.functional.cosine_similarity(embedding1, embedding2).item()
        return similarity

    @staticmethod
    def compute(text1: str, text2: str) -> Optional[float]:
        """
        Compare two text files using BERT embeddings to calculate semantic similarity.

        :param file1_path: Path to the first text file.
        :param file2_path: Path to the second text file.
        :return: The similarity score between the two text files based on BERT embeddings.
        """
        try:

            # Initialize BERTBasedDistance object
            bert_distance = BERTBasedDistance()

            # Compute and return the similarity score
            return bert_distance.compute_distance(text1, text2)

        except Exception as e:
            print(f"Error processing files: {e}")
            return None
            
class Jaro(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='str'

	def compute(self,s1 :str, s2 :str) -> float:
		"""
		Calculate the Jaro similarity between two strings.
    
		:param s1: The first string
		:param s2: The second string
		:return: Jaro similarity between the two strings
		"""
		if s1 == s2:
			return 1.0

		len_s1 = len(s1)
		len_s2 = len(s2)

		if len_s1 == 0 or len_s2 == 0:
			return 0.0

		match_distance = max(len_s1, len_s2) // 2 - 1

		s1_matches = [False] * len_s1
		s2_matches = [False] * len_s2

		matches = 0
		transpositions = 0

		for i in range(len_s1):
			start = max(0, i - match_distance)
			end = min(i + match_distance + 1, len_s2)

			for j in range(start, end):
				if s2_matches[j]:
					continue
				if s1[i] != s2[j]:
					continue
				s1_matches[i] = True
				s2_matches[j] = True
				matches += 1
				break

		if matches == 0:
			return 0.0

		k = 0
		for i in range(len_s1):
			if not s1_matches[i]:
				continue
			while not s2_matches[k]:
				k += 1
			if s1[i] != s2[k]:
				transpositions += 1
			k += 1

		return (matches / len_s1 + matches / len_s2 + (matches - transpositions // 2) / matches) / 3.0
		
	def exemple(self):
		self.obj1_exemple = "martha"
		self.obj2_exemple = "marhta"
		super().exemple()
		
class JaroWinkler(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='text'

	def compute(self,s1 :str, s2 :str, p=0.1) -> float:
		"""
		Calculate the Jaro-Winkler distance between two strings.
    
		:param s1: The first string
		:param s2: The second string
		:param p: The scaling factor, usually 0.1
		:return: Jaro-Winkler distance between the two strings
		"""
		jaro_sim = Jaro().calculate(s1, s2)

		prefix_length = 0
		max_prefix_length = 4

		for i in range(min(len(s1), len(s2))):
			if s1[i] == s2[i]:
				prefix_length += 1
			else:
				break
			if prefix_length == max_prefix_length:
				break

		jaro_winkler_sim = jaro_sim + (prefix_length * p * (1 - jaro_sim))
		return jaro_winkler_sim
		
	def exemple(self):
		self.obj1_exemple = "martha"
		self.obj2_exemple = "marhta"
		super().exemple()

class OverlapCoefficient(Distance):

    def __init__(self) -> None:
      super().__init__()
      self.type='vec_word'

    def compute(self, set1: List[str], set2: List[str]) -> float:
        """
        Calcule le coefficient de chevauchement (Overlap Coefficient) entre deux ensembles de mots.
        
        :param set1: Premier ensemble de mots.
        :param set2: Deuxième ensemble de mots.
        :return: Coefficient de chevauchement entre les deux ensembles, entre 0 et 1.
        """
        set1=set(set1)
        set2=set(set2)
        if not set1 or not set2:
            return 0.0
        
        # Calcul de l'intersection des deux ensembles
        intersection_size: int = len(set1.intersection(set2))
        
        # Taille du plus petit ensemble
        min_size: int = min(len(set1), len(set2))
        
        # Coefficient de chevauchement
        overlap_coefficient: float = intersection_size / min_size
        
        return overlap_coefficient


class SorensenDice(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='text'
		
	def compute(self,str1 :str, str2 :str) -> float:
		# Convert strings to sets of bigrams
		bigrams1 = {str1[i:i+2] for i in range(len(str1) - 1)}
		bigrams2 = {str2[i:i+2] for i in range(len(str2) - 1)}
    
		# Calculate the intersection and the sizes of the sets
		intersection = len(bigrams1 & bigrams2)
		size1 = len(bigrams1)
		size2 = len(bigrams2)
    
		# Calculate the Sørensen-Dice coefficient
		sorensen_dice_coeff = 2 * intersection / (size1 + size2)
    
		# The distance is 1 minus the coefficient
		distance = 1 - sorensen_dice_coeff
    
		return distance
		
	def exemple(self):
		self.obj1_exemple = "night"
		self.obj2_exemple = "nacht"

		super().exemple()
		
from collections import Counter
import math

class BagOfWordsDistance(Distance):

    def __init__(self) -> None:
      super().__init__()
      self.type='text'
      
    def compute(self, text1: str, text2: str) -> float:
        """
        Calcule la distance entre deux textes en utilisant la représentation Bag-of-Words.

        :param text1: Premier texte.
        :param text2: Deuxième texte.
        :return: Distance entre les deux textes, entre 0 et 1.
        """
        # Création des sacs de mots pour les deux textes
        bow1: Dict[str, int] = self._text_to_bow(text1)
        bow2: Dict[str, int] = self._text_to_bow(text2)

        # Union de tous les mots dans les deux textes
        all_words: List[str] = list(set(bow1.keys()).union(set(bow2.keys())))

        # Vecteurs de fréquences des mots pour chaque texte
        vec1: List[int] = [bow1.get(word, 0) for word in all_words]
        vec2: List[int] = [bow2.get(word, 0) for word in all_words]

        # Calcul de la distance entre les deux vecteurs (utilisation de la distance euclidienne ici)
        distance: float = Euclidean().compute(vec1, vec2)
        
        return distance

    def _text_to_bow(self, text: str) -> Dict[str, int]:
        """
        Convertit un texte en un sac de mots (Bag of Words).

        :param text: Texte à convertir.
        :return: Dictionnaire représentant la fréquence de chaque mot dans le texte.
        """
        # Découper le texte en mots
        words: List[str] = text.lower().split()
        
        # Créer un sac de mots avec les fréquences de chaque mot
        bow: Dict[str, int] = dict(Counter(words))
        
        return bow
'''       
from gensim.models import FastText

#obliger pour param init 
sentences = [["the", "cat", "sat", "on", "the", "mat"], ["the", "dog", "sat", "on", "the", "mat"]]
model = FastText(sentences, vector_size=100, window=5, min_count=1, sg=1)
'''
# Importation conditionnelle de gensim
try:
    from gensim.models import FastText
    gensim_installed = True
except ImportError:
    gensim_installed = False
    FastText = None  # Définir FastText comme None si gensim n'est pas installé

# Utilisation de FastText uniquement si gensim est installé
def create_fasttext_model():
    if not gensim_installed:
        raise ImportError("FastText nécessite gensim. Veuillez installer gensim en utilisant 'pip install gensim'.")
    
    # Exemple d'utilisation de FastText pour entraîner un modèle
    sentences = [["the", "cat", "sat", "on", "the", "mat"], ["the", "dog", "sat", "on", "the", "mat"]]
    model = FastText(sentences, vector_size=100, window=5, min_count=1, sg=1)
    return model

# Test de la création du modèle
try:
    if gensim_installed:
     model = create_fasttext_model()
     print("Le modèle FastText a été créé avec succès.")
     class FastTextDistance(Distance):

      def __init__(self, model: FastText=model) -> None:
        """
        Initialisation de la classe FastTextDistance.

        :param model: Modèle FastText pré-entraîné.
        """
        super().__init__()
        
        self.model: FastText = model

        self.type='text'

      def compute(self, text1: str, text2: str) -> float:
        """
        Calcule la distance entre deux textes en utilisant les vecteurs de mots FastText.

        :param text1: Premier texte.
        :param text2: Deuxième texte.
        :return: Distance cosinus entre les deux textes.
        """
        # Obtenir la moyenne des vecteurs de mots pour chaque texte
        vector1: List[float] = self._get_sentence_vector(text1)
        vector2: List[float] = self._get_sentence_vector(text2)

        # Calcul de la similarité cosinus entre les deux vecteurs
        distance: float = Cosine().compute(vector1, vector2)
        
        return distance

      def _get_sentence_vector(self, text: str) -> List[float]:
        """
        Obtenir la moyenne des vecteurs FastText pour un texte donné.

        :param text: Texte à convertir en vecteur.
        :return: Vecteur moyen du texte.
        """
        words: List[str] = text.lower().split()
        word_vectors: List[List[float]] = [self.model.wv[word].tolist() for word in words if word in self.model.wv]

        # Si aucun mot n'est trouvé dans le modèle, retourner un vecteur nul de la taille appropriée
        if not word_vectors:
            return [0.0] * self.model.vector_size

        # Calculer la moyenne des vecteurs de mots
        sentence_vector: List[float] = [0.0] * self.model.vector_size
        for vector in word_vectors:
            for i in range(len(vector)):
                sentence_vector[i] += vector[i]

        # Diviser chaque élément par le nombre de vecteurs pour obtenir la moyenne
        sentence_vector = [v / len(word_vectors) for v in sentence_vector]
        return sentence_vector
    else:
        print("gensim n'est pas installé, l'utilisation de FastText est désactivée.")
except ImportError as e:
    print(f"Erreur: {e}")
    
        
class Dice(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_str'

	def compute(self,list1 :list, list2 :list)-> float:
		"""
		Calculate the Dice distance between two sets.
    
		:param set1: The first set (a set of elements)
		:param set2: The second set (a set of elements)
		:return: Dice distance between the two sets
		"""
		set1=set(list1)
		set2=set(list2)
		intersection = len(set1.intersection(set2))
		total_elements = len(set1) + len(set2)
    
		if total_elements == 0:
			return 0.0
    
		dice_coefficient = (2 * intersection) / total_elements
    
		return 1 - dice_coefficient
		
		
class Tversky(Distance):
	
	def __init__(self,alpha=0.5, beta=0.5)-> None:
		super().__init__()
		self.alpha=alpha
		self.beta=beta
		self.type='vec_str'
	def compute(self,set1 :set, set2 :set )-> float:
		"""
		Calcule la distance de Tversky entre deux ensembles.
    
		:param set1: Premier ensemble
		:param set2: Deuxième ensemble
		:param alpha: Paramètre de pondération pour |A - B|
		:param beta: Paramètre de pondération pour |B - A|
		:return: Distance de Tversky
		"""
		# Taille de l'intersection des ensembles
		intersection = len(set1 & set2)
    
		# Taille des éléments uniques à chaque ensemble
		unique_to_set1 = len(set1 - set2)
		unique_to_set2 = len(set2 - set1)
    
		# Calcul du coefficient de Tversky
		tversky_coeff = intersection / (intersection + self.alpha * unique_to_set1 + self.beta * unique_to_set2)
    
		# La distance est 1 moins le coefficient de Tversky
		distance = 1 - tversky_coeff
    
		return distance
		
	def example(self):
		self.obj1_example =  {'a', 'b', 'c', 'd'}
		self.obj2_example = {'c', 'd', 'e', 'f'}
		distance=self.compute(self.obj1_example,self.obj2_example)
		print(f"{self.__class__.__name__} distance between {self.obj1_example} and {self.obj2_example} is {distance:.2f}")
		
class NgramDistance(Distance):

    def __init__(self, n: int=3) -> None:
        """
        Initialise la classe avec la longueur des n-grams.

        :param n: Longueur des n-grams.
        """
        super().__init__()
        self.type='text'
        self.n: int = n

    def compute(self, text1: str, text2: str) -> float:
        """
        Calcule la distance N-gram entre deux textes.

        :param text1: Premier texte à comparer.
        :param text2: Deuxième texte à comparer.
        :return: Distance entre les deux textes basée sur les n-grams.
        """
        # Convertir les textes en ensembles de n-grams
        ngrams1: Set[str] = self._get_ngrams(text1)
        ngrams2: Set[str] = self._get_ngrams(text2)

        # Calcul de la distance Jaccard (intersection / union des n-grams)
        intersection_size: int = len(ngrams1 & ngrams2)
        union_size: int = len(ngrams1 | ngrams2)

        if union_size == 0:
            return 1.0  # Si l'union est vide, les textes sont complètement différents.

        # Distance de Jaccard (1 - similarité)
        distance: float = 1 - (intersection_size / union_size)
        return distance

    def _get_ngrams(self, text: str) -> Set[str]:
        """
        Génère les n-grams à partir d'un texte donné.

        :param text: Texte à convertir en n-grams.
        :return: Ensemble des n-grams du texte.
        """
        text = text.lower().replace(" ", "")  # Simplifier le texte
        ngrams: Set[str] = set()

        for i in range(len(text) - self.n + 1):
            ngram: str = text[i:i + self.n]
            ngrams.add(ngram)

        return ngrams

class SmithWaterman(Distance):

    def __init__(self, match_score: int=2, mismatch_penalty: int=1, gap_penalty: int=2) -> None:
        """
        Initialise la classe avec les paramètres de score de correspondance, de pénalité de mismatch et de pénalité de gap.

        :param match_score: Score attribué pour une correspondance entre deux caractères.
        :param mismatch_penalty: Pénalité pour une différence entre deux caractères.
        :param gap_penalty: Pénalité pour l'introduction d'un gap (trou).
        """
        super().__init__()
        self.type='text'
        self.match_score: int = match_score
        self.mismatch_penalty: int = mismatch_penalty
        self.gap_penalty: int = gap_penalty

    def compute(self, seq1: str, seq2: str) -> Tuple[int, List[List[int]]]:
        """
        Calcule l'alignement optimal entre deux chaînes à l'aide de l'algorithme Smith-Waterman.

        :param seq1: Première séquence à comparer.
        :param seq2: Deuxième séquence à comparer.
        :return: Le score d'alignement optimal et la matrice de score.
        """
        len1: int = len(seq1)
        len2: int = len(seq2)

        # Initialisation de la matrice de score avec des zéros
        score_matrix: List[List[int]] = [[0 for _ in range(len2 + 1)] for _ in range(len1 + 1)]

        # Variables pour suivre le score maximal
        max_score: int = 0

        # Remplissage de la matrice de score
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                match: int = self.match_score if seq1[i - 1] == seq2[j - 1] else self.mismatch_penalty
                score_diag: int = score_matrix[i - 1][j - 1] + match
                score_up: int = score_matrix[i - 1][j] + self.gap_penalty
                score_left: int = score_matrix[i][j - 1] + self.gap_penalty
                score_matrix[i][j] = max(0, score_diag, score_up, score_left)

                # Mise à jour du score maximal
                max_score = max(max_score, score_matrix[i][j])

        return max_score, score_matrix

    def traceback(self, score_matrix: List[List[int]], seq1: str, seq2: str) -> Tuple[str, str]:
        """
        Effectue le traceback pour trouver l'alignement optimal.

        :param score_matrix: La matrice de score calculée par l'algorithme Smith-Waterman.
        :param seq1: Première séquence à aligner.
        :param seq2: Deuxième séquence à aligner.
        :return: Les deux séquences alignées.
        """
        align1: str = ""
        align2: str = ""

        # Trouver la position avec le score maximal
        max_i, max_j = 0, 0
        max_score: int = 0
        for i in range(len(score_matrix)):
            for j in range(len(score_matrix[0])):
                if score_matrix[i][j] > max_score:
                    max_score = score_matrix[i][j]
                    max_i, max_j = i, j

        i, j = max_i, max_j

        # Effectuer le traceback
        while i > 0 and j > 0 and score_matrix[i][j] > 0:
            if score_matrix[i][j] == score_matrix[i - 1][j - 1] + (self.match_score if seq1[i - 1] == seq2[j - 1] else self.mismatch_penalty):
                align1 = seq1[i - 1] + align1
                align2 = seq2[j - 1] + align2
                i -= 1
                j -= 1
            elif score_matrix[i][j] == score_matrix[i - 1][j] + self.gap_penalty:
                align1 = seq1[i - 1] + align1
                align2 = "-" + align2
                i -= 1
            else:
                align1 = "-" + align1
                align2 = seq2[j - 1] + align2
                j -= 1

        return align1, align2
    def example(self):
      # Exemple d'utilisation
      seq1: str = "AGACTG"
      seq2: str = "GACTTAC"

      sw = SmithWaterman(match_score=2, mismatch_penalty=-1, gap_penalty=-2)

      # Calcul de la distance
      max_score, score_matrix = sw.compute(seq1, seq2)
      print(f"Max Alignment Score: {max_score}")

      # Effectuer le traceback
      aligned_seq1, aligned_seq2 = sw.traceback(score_matrix, seq1, seq2)
      print(f"Aligned Sequence 1: {aligned_seq1}")
      print(f"Aligned Sequence 2: {aligned_seq2}")

 #claude ai      
from typing import List, Tuple, Union, Optional
from difflib import SequenceMatcher

class RatcliffObershelp(Distance):
      
    """
    A class implementing the Ratcliff/Obershelp pattern matching algorithm
    to measure the similarity between sequences.
    
    The algorithm finds the longest common substring and then recursively 
    processes the remaining unmatched regions on both sides of the match.
    The similarity is calculated as:
    
    similarity = 2 * (number of matching characters) / (total length of both strings)
    """
    
    def __init__(self, case_sensitive: bool=True)-> None:
        """
        Initialize the RatcliffObershelp calculator.
        
        Args:
            case_sensitive: Whether string comparisons should be case sensitive
        """
        super().__init__()
        self.type='text'
        
        self.case_sensitive = case_sensitive
    
    def _preprocess(self, sequence: str) -> str:
        """
        Preprocess the input sequence based on case sensitivity setting.
        
        Args:
            sequence: Input string to preprocess
            
        Returns:
            Preprocessed string
        """
        if not self.case_sensitive:
            return sequence.lower()
        return sequence
    
    def _find_longest_common_substring(self, str1: str, str2: str) -> Tuple[int, int, int]:
        """
        Find the longest common substring between two strings.
        
        Args:
            str1: First string
            str2: Second string
            
        Returns:
            Tuple containing (start index in str1, start index in str2, length of match)
        """
        max_length = 0
        best_match = (0, 0, 0)
        
        # Create matrix for dynamic programming approach
        matrix = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
        
        # Fill the matrix and find the longest common substring
        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                if str1[i-1] == str2[j-1]:
                    matrix[i][j] = matrix[i-1][j-1] + 1
                    if matrix[i][j] > max_length:
                        max_length = matrix[i][j]
                        best_match = (i - max_length, j - max_length, max_length)
        
        return best_match
    
    def _get_matching_blocks(self, str1: str, str2: str) -> List[Tuple[int, int, int]]:
        """
        Recursively find all matching blocks between two strings.
        
        Args:
            str1: First string
            str2: Second string
            
        Returns:
            List of tuples containing (index1, index2, length) for each matching block
        """
        matches: List[Tuple[int, int, int]] = []
        
        def _find_matches(start1: int, end1: int, start2: int, end2: int) -> None:
            """
            Recursive helper function to find matching blocks.
            
            Args:
                start1: Start index in first string
                end1: End index in first string
                start2: Start index in second string
                end2: End index in second string
            """
            sub1 = str1[start1:end1]
            sub2 = str2[start2:end2]
            
            if not sub1 or not sub2:
                return
            
            i, j, n = self._find_longest_common_substring(sub1, sub2)
            if n == 0:
                return
            
            # Add the match to our list
            match = (start1 + i, start2 + j, n)
            matches.append(match)
            
            # Recursively process the regions before and after the match
            _find_matches(start1, start1 + i, start2, start2 + j)
            _find_matches(start1 + i + n, end1, start2 + j + n, end2)
        
        _find_matches(0, len(str1), 0, len(str2))
        return sorted(matches)
    
    def compute(self, seq1: str, seq2: str) -> float:
        """
        Calculate the Ratcliff/Obershelp distance between two sequences.
        
        Args:
            seq1: First sequence
            seq2: Second sequence
            
        Returns:
            float: Similarity score between 0 and 1
            
        Raises:
            ValueError: If either input is empty
        """
        if not seq1 or not seq2:
            raise ValueError("Input sequences cannot be empty")
        
        # Preprocess sequences
        str1 = self._preprocess(seq1)
        str2 = self._preprocess(seq2)
        
        # Find all matching blocks
        matches = self._get_matching_blocks(str1, str2)
        
        # Calculate total length of matches
        matching_chars = sum(length for _, _, length in matches)
        
        # Calculate similarity
        return 1 - 2.0 * matching_chars / (len(str1) + len(str2))
    
    def quick_ratio(self, seq1: str, seq2: str) -> float:
        """
        Calculate similarity using Python's built-in SequenceMatcher.
        This is faster but may give slightly different results.
        
        Args:
            seq1: First sequence
            seq2: Second sequence
            
        Returns:
            float: Similarity score between 0 and 1
        """
        str1 = self._preprocess(seq1)
        str2 = self._preprocess(seq2)
        return SequenceMatcher(None, str1, str2).ratio()
        
    def example(self):
      self.obj1_example = "the quick brown fox jumps over the lazy dog"
      self.obj2_example = "the fast brown fox leaps over the sleepy cat"
      distance=self.compute(self.obj1_example,self.obj2_example)
      print(f"{self.__class__.__name__} distance between {self.obj1_example} and {self.obj2_example} is {distance}")
		

class Gestalt(RatcliffObershelp):
	def __init__(self)-> None:
		super().__init__()
		
from collections import Counter
import math

class BLEUScore(Distance):

    def __init__(self, n_gram: int = 4, smoothing: bool = True) -> None:
        """
        Initialise la classe BLEU Score avec le paramètre du n-gram et le choix de la méthode de lissage.

        :param n_gram: Le maximum n-gram à prendre en compte (par défaut 4).
        :param smoothing: Si le lissage est appliqué ou non (par défaut True).
        """
        super().__init__()
        self.type='text'
        self.n_gram = n_gram
        self.smoothing = smoothing

    def _extract_ngrams(self, text: List[str], n: int) -> List[Tuple[str]]:
        """
        Extrait les n-grams d'une liste de mots donnée.

        :param text: La liste des mots d'un texte.
        :param n: La longueur des n-grams à extraire.
        :return: Une liste de tuples représentant les n-grams.
        """
        return [tuple(text[i:i + n]) for i in range(len(text) - n + 1)]

    def _modified_precision(self, hypothesis: List[str], references: List[List[str]], n: int) -> float:
        """
        Calcule la précision modifiée pour un n-gram spécifique.

        :param hypothesis: La liste des mots dans le texte généré.
        :param references: La liste de listes de mots dans les textes de référence.
        :param n: La longueur du n-gram à prendre en compte.
        :return: La précision modifiée pour le n-gram.
        """
        hyp_ngrams = Counter(self._extract_ngrams(hypothesis, n))
        max_ref_ngrams = Counter()

        for reference in references:
            ref_ngrams = Counter(self._extract_ngrams(reference, n))
            for ngram in ref_ngrams:
                max_ref_ngrams[ngram] = max(max_ref_ngrams[ngram], ref_ngrams[ngram])

        clipped_count = 0
        total_count = sum(hyp_ngrams.values())

        for ngram in hyp_ngrams:
            clipped_count += min(hyp_ngrams[ngram], max_ref_ngrams[ngram])

        if total_count == 0:
            return 0.0

        return clipped_count / total_count

    def _brevity_penalty(self, hypothesis: List[str], references: List[List[str]]) -> float:
        """
        Calcule la pénalité de longueur (brevity penalty).

        :param hypothesis: La liste des mots dans le texte généré.
        :param references: La liste de listes de mots dans les textes de référence.
        :return: La pénalité de longueur.
        """
        hyp_len = len(hypothesis)
        ref_lens = [len(ref) for ref in references]
        closest_ref_len = min(ref_lens, key=lambda ref_len: (abs(ref_len - hyp_len), ref_len))

        if hyp_len > closest_ref_len:
            return 1.0
        elif hyp_len == 0:
            return 0.0
        else:
            return math.exp(1 - closest_ref_len / hyp_len)

    def compute(self, hypothesis: List[str], references: List[List[str]]) -> float:
        """
        Calcule le BLEU Score pour un texte généré donné par rapport à plusieurs textes de référence.

        :param hypothesis: La liste des mots dans le texte généré.
        :param references: La liste de listes de mots dans les textes de référence.
        :return: Le BLEU Score.
        """
        precisions: List[float] = []
        for n in range(1, self.n_gram + 1):
            precision = self._modified_precision(hypothesis, references, n)
            if self.smoothing and precision == 0:
                precision = 1e-9  # Smoothing pour éviter les zéros
            precisions.append(precision)

        # Moyenne géométrique des précisions
        score = math.exp(sum(math.log(p) for p in precisions) / self.n_gram)

        # Appliquer la pénalité de longueur (brevity penalty)
        bp = self._brevity_penalty(hypothesis, references)

        return score * bp

class ROUGEScore(Distance):

    def __init__(self, n_gram: int = 2) -> None:
        """
        Initializes the ROUGEScore class with a specified n-gram length.

        :param n_gram: The length of the n-gram to be considered (default is 2).
        """
        super().__init__()
        self.type='text'
        self.n_gram = n_gram

    def _extract_ngrams(self, text: List[str], n: int) -> List[Tuple[str]]:
        """
        Extracts n-grams from a given list of words.

        :param text: List of words from a text.
        :param n: The n-gram length to extract.
        :return: A list of n-grams (as tuples of words).
        """
        return [tuple(text[i:i + n]) for i in range(len(text) - n + 1)]

    def _ngram_overlap(self, reference: List[str], hypothesis: List[str], n: int) -> Tuple[int, int]:
        """
        Calculates the overlap of n-grams between the reference and the hypothesis text.

        :param reference: List of words from the reference text.
        :param hypothesis: List of words from the hypothesis text.
        :param n: The n-gram length to consider.
        :return: A tuple (overlap count, reference n-gram count).
        """
        ref_ngrams = Counter(self._extract_ngrams(reference, n))
        hyp_ngrams = Counter(self._extract_ngrams(hypothesis, n))

        overlap_count = 0
        for ngram in hyp_ngrams:
            overlap_count += min(hyp_ngrams[ngram], ref_ngrams.get(ngram, 0))

        return overlap_count, sum(ref_ngrams.values())

    def _recall(self, overlap: int, total: int) -> float:
        """
        Calculates the recall for a given overlap count.

        :param overlap: The number of overlapping n-grams between the reference and hypothesis.
        :param total: The total number of n-grams in the reference.
        :return: The recall score.
        """
        if total == 0:
            return 0.0
        return overlap / total

    def compute(self, hypothesis: List[str], references: List[List[str]]) -> Dict[str, float]:
        """
        Computes the ROUGE-N score for the hypothesis against multiple references.

        :param hypothesis: List of words from the hypothesis text.
        :param references: List of lists of words from the reference texts.
        :return: A dictionary containing recall and F1 scores for n-grams.
        """
        recall_scores = []

        for reference in references:
            overlap, ref_count = self._ngram_overlap(reference, hypothesis, self.n_gram)
            recall = self._recall(overlap, ref_count)
            recall_scores.append(recall)

        best_recall = max(recall_scores)

        return {
            'recall': best_recall,
        }
    def example(self):
      # Example usage:
      hypothesis: List[str] = "the cat is on the mat".split()
      references: List[List[str]] = [
    "the cat is on the mat".split(),
    "there is a cat on the mat".split()
]

      # Create an instance of the ROUGEScore class with bigrams (n=2)
      rouge = ROUGEScore(n_gram=2)

      # Compute the ROUGE-N score
      rouge_n_score: Dict[str, float] = rouge.compute(hypothesis, references)
      print(f"ROUGE-N Score: {rouge_n_score}")
      
term_similarity_matrix: Dict[Tuple[str, str], float] = {
    ("cat", "cat"): 1.0,
    ("cat", "dog"): 0.5,
    ("dog", "dog"): 1.0,
    ("mat", "mat"): 1.0,
    ("on", "on"): 1.0,
    ("is", "is"): 1.0
}      
class SoftCosine(Distance):

    def __init__(self, term_similarity_matrix: Dict[Tuple[str, str], float]=term_similarity_matrix) -> None:
        """
        Initializes the SoftCosineSimilarity class with a term similarity matrix.

        :param term_similarity_matrix: A dictionary that stores pairwise term similarity scores.
        """
        super().__init__()
        self.type='text'
        self.term_similarity_matrix = term_similarity_matrix

    def _compute_term_frequency(self, document: List[str]) -> Dict[str, int]:
        """
        Computes the term frequency for each word in the document.

        :param document: A list of words from the document.
        :return: A dictionary with terms as keys and their frequencies as values.
        """
        term_freq: Dict[str, int] = {}
        for term in document:
            term_freq[term] = term_freq.get(term, 0) + 1
        return term_freq

    def _compute_magnitude(self, term_freq: Dict[str, int]) -> float:
        """
        Computes the magnitude of a document vector based on term frequencies.

        :param term_freq: A dictionary of term frequencies.
        :return: The magnitude of the document vector.
        """
        magnitude: float = 0.0
        for term, freq in term_freq.items():
            magnitude += freq ** 2
        return math.sqrt(magnitude)

    def compute(self, doc1: List[str], doc2: List[str]) -> float:
        """
        Computes the Soft Cosine Similarity between two documents.

        :param doc1: A list of words from the first document.
        :param doc2: A list of words from the second document.
        :return: The Soft Cosine Similarity score.
        """
        # Step 1: Compute term frequencies for both documents
        term_freq1 = self._compute_term_frequency(doc1)
        term_freq2 = self._compute_term_frequency(doc2)

        # Step 2: Calculate the numerator (dot product with similarity adjustment)
        numerator: float = 0.0
        for term1, freq1 in term_freq1.items():
            for term2, freq2 in term_freq2.items():
                similarity = self.term_similarity_matrix.get((term1, term2), 0.0)
                numerator += freq1 * freq2 * similarity

        # Step 3: Calculate magnitudes for both documents
        magnitude1: float = self._compute_magnitude(term_freq1)
        magnitude2: float = self._compute_magnitude(term_freq2)

        # Step 4: Calculate the denominator (product of magnitudes)
        denominator: float = magnitude1 * magnitude2

        # Step 5: Return the Soft Cosine Similarity
        if denominator == 0:
            return 0.0
        return numerator / denominator

from typing import List, Dict

# Importation conditionnelle de scikit-learn
try:
    from sklearn.decomposition import LatentDirichletAllocation as LDA
    from sklearn.decomposition import TruncatedSVD as LSA
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    sklearn_installed = True
except ImportError:
    sklearn_installed = False
    # Si scikit-learn n'est pas installé, définir les classes et fonctions comme None
    LDA = None
    LSA = None
    CountVectorizer = None
    TfidfVectorizer = None

class TopicModeling(Distance):

    def __init__(self, method: str = 'LDA', num_topics: int = 10) -> None:
        """
        Initializes the TopicModelingDistance class with the specified topic modeling method (LDA or LSA).

        :param method: The topic modeling method ('LDA' or 'LSA').
        :param num_topics: The number of topics to be generated by the model.
        """
        super().__init__()
        
        if not sklearn_installed and methode=='LDA':
          raise ImportError("LDA nécessite scikit-learn. Veuillez installer scikit-learn en utilisant 'pip install scikit-learn'.")
        if not sklearn_installed and methode=='LSA':
          raise ImportError("LSA nécessite scikit-learn. Veuillez installer scikit-learn en utilisant 'pip install scikit-learn'.")
 
        self.type='text'
        self.method: str = method
        self.num_topics: int = num_topics
        self.vectorizer = None
        self.model = None

    def fit(self, documents: List[str]) -> None:
        """
        Fits the topic model to the provided documents.

        :param documents: A list of text documents.
        """

        if self.method == 'LDA':
            self.vectorizer = CountVectorizer(stop_words='english')
            doc_term_matrix = self.vectorizer.fit_transform(documents)
            self.model = LDA(n_components=self.num_topics, random_state=42)
        elif self.method == 'LSA':
            self.vectorizer = TfidfVectorizer(stop_words='english')
            doc_term_matrix = self.vectorizer.fit_transform(documents)
            self.model = LSA(n_components=self.num_topics, random_state=42)
        
        # Fit the model to the document-term matrix
        self.model.fit(doc_term_matrix)

    def _get_topic_distribution(self, document: str) -> List[float]:
        """
        Computes the topic distribution for a single document.

        :param document: The document for which the topic distribution is computed.
        :return: A list representing the topic distribution.
        """
        doc_vector = self.vectorizer.transform([document])
        if self.method == 'LDA':
            return self.model.transform(doc_vector)[0].tolist()
        elif self.method == 'LSA':
            return self.model.transform(doc_vector)[0].tolist()

    def euclidean_distance(self, dist1: List[float], dist2: List[float]) -> float:
        """
        Computes the Euclidean distance between two topic distributions.

        :param dist1: The topic distribution of the first document.
        :param dist2: The topic distribution of the second document.
        :return: The Euclidean distance as a float.
        """
        distance: float = sum((a - b) ** 2 for a, b in zip(dist1, dist2)) ** 0.5
        return distance

    def compute(self, doc1: str, doc2: str) -> float:
        """
        Computes the distance between two documents based on their topic distributions.

        :param doc1: The first document.
        :param doc2: The second document.
        :return: The distance between the two documents' topic distributions.
        """
        # Get topic distributions for both documents
        topic_dist1 = self._get_topic_distribution(doc1)
        topic_dist2 = self._get_topic_distribution(doc2)

        # Compute the distance (Euclidean distance)
        return self.euclidean_distance(topic_dist1, topic_dist2)
        
    def example(self):
      # Example usage:
      documents: List[str] = [
    "The cat sat on the mat.",
    "Dogs are great companions.",
    "Cats and dogs are popular pets.",
    "I love my pet cat and dog."
]

      # Initialize TopicModelingDistance with LDA and 5 topics
      topic_model_distance = TopicModeling(method='LDA', num_topics=5)

      # Fit the model to a list of documents
      topic_model_distance.fit(documents)

      # Compute the distance between two new documents
      doc1: str = "The cat sat on the mat."
      doc2: str = "Dogs are great companions."
      distance: float = topic_model_distance.compute(doc1, doc2)
      print(f"Topic Distance (LDA): {distance}")

      # You can also use LSA by changing the method
      lsa_model_distance = TopicModeling(method='LSA', num_topics=5)
      lsa_model_distance.fit(documents)
      distance_lsa: float = lsa_model_distance.compute(doc1, doc2)
      print(f"Topic Distance (LSA): {distance_lsa}")

class AlignmentBasedMeasures(Distance):

    def __init__(self) -> None:
      super().__init__()
      self.type='text'
    def align_texts(self, text1: str, text2: str) -> List[Tuple[str, str]]:
        """
        Aligns two texts at the word level by using dynamic programming to find the optimal alignment.

        :param text1: The first text as a string.
        :param text2: The second text as a string.
        :return: A list of tuples representing the aligned words from both texts.
        """
        words1: List[str] = text1.split()
        words2: List[str] = text2.split()

        # Initialize DP table for alignment
        dp: List[List[int]] = [[0] * (len(words2) + 1) for _ in range(len(words1) + 1)]
        alignment: List[Tuple[str, str]] = []

        # Fill DP table (Levenshtein-like)
        for i in range(1, len(words1) + 1):
            dp[i][0] = i
        for j in range(1, len(words2) + 1):
            dp[0][j] = j

        for i in range(1, len(words1) + 1):
            for j in range(1, len(words2) + 1):
                cost = 0 if words1[i - 1] == words2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1,    # Deletion
                               dp[i][j - 1] + 1,    # Insertion
                               dp[i - 1][j - 1] + cost)  # Substitution

        # Backtrack to find the alignment
        i, j = len(words1), len(words2)
        while i > 0 or j > 0:
            if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (0 if words1[i - 1] == words2[j - 1] else 1):
                alignment.append((words1[i - 1], words2[j - 1]))
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
                alignment.append((words1[i - 1], "-"))  # Deletion
                i -= 1
            else:
                alignment.append(("-", words2[j - 1]))  # Insertion
                j -= 1

        alignment.reverse()  # Reverse to get the correct order
        return alignment

    def compute(self, text1: str, text2: str) -> float:
        """
        Computes an alignment score based on the number of aligned words.

        :param text1: The first text.
        :param text2: The second text.
        :return: A float representing the alignment score (higher is better).
        """
        aligned: List[Tuple[str, str]] = self.align_texts(text1, text2)
        matches: int = sum(1 for word1, word2 in aligned if word1 == word2)
        total_words: int = max(len(text1.split()), len(text2.split()))
        
        return matches / total_words


class GappyNGram(Distance):

    def __init__(self, n: int=3, gap_size: int=1) -> None:
        """
        Initializes the GappyNGramDistance class with the given n-gram length and gap size.

        :param n: The length of the n-gram.
        :param gap_size: The size of the allowed gap between the elements of the n-gram.
        """
        super().__init__()
        self.type='text'
        self.n: int = n
        self.gap_size: int = gap_size

    def generate_gappy_ngrams(self, text: str) -> Set[Tuple[str, ...]]:
        """
        Generates the gappy n-grams for a given text.

        :param text: The input text.
        :return: A set of gappy n-grams, where each n-gram is represented as a tuple of strings.
        """
        words: List[str] = text.split()
        gappy_ngrams: Set[Tuple[str, ...]] = set()

        for i in range(len(words) - self.n + 1):
            for j in range(1, self.gap_size + 2):
                if i + j * (self.n - 1) < len(words):
                    gappy_ngram: Tuple[str, ...] = tuple(words[i + k * j] for k in range(self.n))
                    gappy_ngrams.add(gappy_ngram)

        return gappy_ngrams

    def compute(self, text1: str, text2: str) -> float:
        """
        Computes the Gappy N-gram similarity between two texts.

        :param text1: The first text.
        :param text2: The second text.
        :return: The similarity score between the two sets of gappy n-grams (from 0 to 1).
        """
        ngrams1: Set[Tuple[str, ...]] = self.generate_gappy_ngrams(text1)
        ngrams2: Set[Tuple[str, ...]] = self.generate_gappy_ngrams(text2)

        intersection: Set[Tuple[str, ...]] = ngrams1.intersection(ngrams2)
        union: Set[Tuple[str, ...]] = ngrams1.union(ngrams2)

        if not union:  # Handle division by zero when both n-gram sets are empty
            return 1.0 if not intersection else 0.0

        return len(intersection) / len(union)

class SoftJaccardSimilarity(Distance):

    def __init__(self, threshold: float=0.5) -> None:
        """
        Initializes the Soft Jaccard Similarity class with a similarity threshold.

        :param threshold: The minimum similarity between two words to be considered as a match (between 0 and 1).
        """
        super().__init__()
        self.type='text'
        self.threshold: float = threshold

    def word_similarity(self, word1: str, word2: str) -> float:
        """
        Calculates the similarity between two words based on their character-level similarity.
        This function can be replaced with more complex similarity measures (e.g., Levenshtein distance, cosine similarity).

        :param word1: The first word.
        :param word2: The second word.
        :return: A similarity score between 0 and 1.
        """
        set1: Set[str] = set(word1)
        set2: Set[str] = set(word2)

        intersection_size: int = len(set1.intersection(set2))
        union_size: int = len(set1.union(set2))

        return intersection_size / union_size if union_size != 0 else 0.0

    def compute(self, text1: str, text2: str) -> float:
        """
        Calculates the Soft Jaccard Similarity between two texts.

        :param text1: The first text.
        :param text2: The second text.
        :return: The soft Jaccard similarity score between the two sets of words (between 0 and 1).
        """
        words1: List[str] = text1.split()
        words2: List[str] = text2.split()

        matched_words: Set[Tuple[str, str]] = set()
        for word1 in words1:
            for word2 in words2:
                if self.word_similarity(word1, word2) >= self.threshold:
                    matched_words.add((word1, word2))

        # Intersection is the number of matched pairs
        intersection_size: int = len(matched_words)
        # Union is the total number of unique words from both sets
        union_size: int = len(set(words1).union(set(words2)))

        return intersection_size / union_size if union_size != 0 else 0.0

class MongeElkan(Distance):
    def __init__(self, base_distance: Callable[[str, str], float]=Levenshtein()) -> None:
        """
        Initialise la classe avec une fonction de distance de base.

        :param base_distance: Fonction de distance de base entre deux sous-éléments (par ex. Levenshtein).
        """
        super().__init__()
        self.type='text'
        self.base_distance: Callable[[str, str], float] = base_distance

    def compute(self, set1: List[str], set2: List[str]) -> float:
        """
        Calcule la distance Monge-Elkan entre deux ensembles de mots ou sous-éléments.

        :param set1: Premier ensemble de mots (texte décomposé en liste de mots ou caractères).
        :param set2: Deuxième ensemble de mots.
        :return: La distance Monge-Elkan calculée.
        """
        if not set1 or not set2:
            return float('inf')

        total_distance: float = 0.0
        for word1 in set1:
            min_distance: float = min(self.base_distance(word1, word2) for word2 in set2)
            total_distance += min_distance

        return total_distance / len(set1)

from typing import List, Dict
import math
from collections import Counter

class JensenShannonDivergence(Distance):
    def __init__(self) -> None:
        """
        Initialise la classe avec une fonction de distance de base.

        :param base_distance: Fonction de distance de base entre deux sous-éléments (par ex. Levenshtein).
        """
        super().__init__()
        self.type='text'
        
    def compute(self, dist1: List[float], dist2: List[float]) -> float:
        """
        Calcule la Jensen-Shannon Divergence entre deux distributions de probabilités.

        :param dist1: Première distribution de probabilités (somme égale à 1).
        :param dist2: Deuxième distribution de probabilités (somme égale à 1).
        :return: La divergence Jensen-Shannon entre les deux distributions.
        """
        if len(dist1) != len(dist2):
            raise ValueError("Les distributions doivent avoir la même longueur")

        # Calcul de la distribution moyenne
        avg_dist: List[float] = [(p1 + p2) / 2 for p1, p2 in zip(dist1, dist2)]

        # Calcul de la divergence KL pour les deux distributions par rapport à la distribution moyenne
        kl_div1: float = self._kl_divergence(dist1, avg_dist)
        kl_div2: float = self._kl_divergence(dist2, avg_dist)

        # La Jensen-Shannon Divergence est la moyenne des deux divergences KL
        return (kl_div1 + kl_div2) / 2

    def _kl_divergence(self, dist_p: List[float], dist_q: List[float]) -> float:
        """
        Calcule la Kullback-Leibler Divergence entre deux distributions.

        :param dist_p: Distribution de probabilité p.
        :param dist_q: Distribution de probabilité q.
        :return: La divergence KL entre les distributions p et q.
        """
        divergence: float = 0.0
        for p, q in zip(dist_p, dist_q):
            if p > 0 and q > 0:
                divergence += p * math.log(p / q)
        return divergence

    def text_to_distribution(self, text: str, vocabulary: List[str]) -> List[float]:
        """
        Convertit un texte en distribution de probabilités basée sur la fréquence des mots dans un vocabulaire.

        :param text: Le texte à convertir.
        :param vocabulary: La liste des mots qui composent le vocabulaire.
        :return: Une distribution de probabilités (liste de fréquences normalisées).
        """
        # Tokenize le texte
        word_counts: Dict[str, int] = Counter(text.split())

        # Crée une distribution basée sur le vocabulaire
        dist: List[float] = [word_counts.get(word, 0) for word in vocabulary]

        # Normalise la distribution pour que la somme soit égale à 1
        total_count: float = sum(dist)
        if total_count > 0:
            dist = [count / total_count for count in dist]

        return dist
        
    def example(self):
      # Exemple d’utilisation avec des textes 
      text1: str = 'The quick brown fox jumps over the lazy dog' 
      text2: str = 'The fast brown fox leaps over the lazy dog'
      # Vocabulaire global (tous les mots apparaissant dans les textes)
      vocabulary: List[str] = list(set(text1.split()) | set(text2.split()))
      # Créer une instance de la classe Jensen-Shannon Divergence 
      js_divergence = JensenShannonDivergence()
      # Convertir les textes en distributions de probabilités
      dist1: List[float] = js_divergence.text_to_distribution(text1, vocabulary)
      dist2: List[float] = js_divergence.text_to_distribution(text2, vocabulary)
      # Calculer la Jensen-Shannon Divergence entre les deux textes 
      divergence: float = js_divergence.compute(dist1, dist2) 
      print(f"Jensen-Shannon Divergence: {divergence}")

