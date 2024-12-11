from .mainClass import *
from .tools import TreeNode

class ByteLevelDistance(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='file'

		"""
		This class computes the byte-level distance between two files by comparing
		the bytes of both files and summing their absolute differences.
		"""

	def compute(self, file_path1: str, file_path2: str) -> int:
		"""
		Compute the byte-level distance between two files.

		:param file_path1: Path to the first file.
		:param file_path2: Path to the second file.
		:return: The byte-level distance as an integer.
		"""
		with open(file_path1, 'rb') as file1, open(file_path2, 'rb') as file2:
			data1: bytes = file1.read()
			data2: bytes = file2.read()

		# Take the minimum length of both files to avoid out-of-bound errors
		min_length: int = min(len(data1), len(data2))

		# Calculate byte-level distance by summing the absolute differences between byte values
		# a adapter avec ses distances :#############################################################
		#Hamming Distance : Compare deux fichiers au niveau binaire ou des octets en comptant le nombre de bits différents.
		#Levenshtein Distance (Edit Distance) : Mesure le nombre minimum d'opérations nécessaires pour transformer un fichier en un autre (insertion, suppression, ou substitution de caractères/bytes).
		#Jaccard Index : Compare la similarité entre deux ensembles d’octets ou de segments en calculant le rapport des éléments en commun.
		#Manhattan Distance : Somme des différences absolues entre les octets correspondants des deux fichiers.
		#Euclidean Distance : Racine carrée de la somme des carrés des différences des octets entre deux fichiers.
		distance: int = sum(abs(data1[i] - data2[i]) for i in range(min_length))

		# If the files have different lengths, add the extra bytes from the longer file
		distance += abs(len(data1) - len(data2))

		return distance

import hashlib

class HashComparison(Distance):

	"""
	This class computes the cryptographic hash (MD5 or SHA256) of two files and compares them to determine similarity.
	"""

	def __init__(self, algorithm: str = 'md5') -> None:
		"""
		Initializes the class with the selected hashing algorithm (default is 'md5').
		Supported algorithms: 'md5', 'sha256'
		"""
		super().__init__()
		self.type='file'

		self.algorithm: str = algorithm.lower()

	def _compute_hash(self, file_path: str) -> str:
		"""
		Computes the hash of the given file using the specified algorithm.
        
		:param file_path: The path to the file.
		:return: The computed hash in hexadecimal form.
		"""
		hash_func = None
		if self.algorithm == 'md5':
			hash_func = hashlib.md5()
		elif self.algorithm == 'sha256':
			hash_func = hashlib.sha256()
		else:
			raise ValueError(f"Unsupported algorithm: {self.algorithm}")

		with open(file_path, 'rb') as file:
			while chunk := file.read(4096):
				hash_func.update(chunk)

		return hash_func.hexdigest()

	def compute(self, file_path1: str, file_path2: str) -> bool:
		"""
		Compares the hash values of two files.
        
		:param file_path1: The path to the first file.
		:param file_path2: The path to the second file.
		:return: True if the files have the same hash, False otherwise.
		"""
		hash1: str = self._compute_hash(file_path1)
		hash2: str = self._compute_hash(file_path2)

		return hash1 == hash2



import zlib
from typing import Union

class NormalizedCompression(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='file'

		"""
		A class to compute the Normalized Compression Distance (NCD) between two files.
		The NCD is based on the change in compression size when two files are concatenated.
		"""

	def _compress(self, data: Union[bytes, str]) -> int:
		"""
		Compresses the input data using zlib and returns the size of the compressed data.

		:param data: The input data (as bytes or string) to be compressed.
		:return: The size of the compressed data in bytes.
		"""
		if isinstance(data, str):
			data = data.encode('utf-8')
		compressed_data: bytes = zlib.compress(data)
		return len(compressed_data)

	def compute(self, file1_data: Union[bytes, str], file2_data: Union[bytes, str]) -> float:
		"""
		Computes the Normalized Compression Distance (NCD) between two files.

		:param file1_data: The content of the first file as bytes or string.
		:param file2_data: The content of the second file as bytes or string.
		:return: The NCD between the two files as a float value.
		"""
		# Compress file1 and file2 individually
		Cx: int = self._compress(file1_data)
		Cy: int = self._compress(file2_data)

		# Compress the concatenation of file1 and file2
		Cxy: int = self._compress(file1_data + file2_data)

		# Compute the Normalized Compression Distance
		NCD: float = (Cxy - min(Cx, Cy)) / max(Cx, Cy)

		return NCD


import zlib
from typing import Union

class KolmogorovComplexity(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='file'

		"""
		A class to approximate the Kolmogorov Complexity between two files.
		It measures the amount of shared information between the files based on their compressibility.
		"""

	def _compress(self, data: Union[bytes, str]) -> int:
		"""
		Compresses the input data using zlib and returns the size of the compressed data.

		:param data: The input data (as bytes or string) to be compressed.
		:return: The size of the compressed data in bytes.
		"""
		if isinstance(data, str):
			data = data.encode('utf-8')
		compressed_data: bytes = zlib.compress(data)
		return len(compressed_data)

	def compute(self, file1_data: Union[bytes, str], file2_data: Union[bytes, str]) -> float:
		"""
		Computes the Kolmogorov complexity between two files based on their compressibility.

		:param file1_data: The content of the first file as bytes or string.
		:param file2_data: The content of the second file as bytes or string.
		:return: The Kolmogorov complexity as a float value.
		"""
		# Compress file1 and file2 individually
		Cx: int = self._compress(file1_data)
		Cy: int = self._compress(file2_data)

		# Compress the concatenation of file1 and file2
		Cxy: int = self._compress(file1_data + file2_data)

		# Approximate the Kolmogorov complexity (shared information)
		kolmogorov_complexity: float = (Cxy - min(Cx, Cy)) / max(Cx, Cy)

		return kolmogorov_complexity


import subprocess
from typing import List, Dict

class DynamicBinaryInstrumentation(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='file'

		"""
		A class to simulate Dynamic Binary Instrumentation (DBI) for measuring the difference in execution behavior
		between two executable files.
		"""

	def _run_and_trace(self, executable_path: str) -> List[str]:
		"""
		Executes the binary and collects a simplified trace of its execution.
        
		:param executable_path: Path to the executable binary file.
		:return: A list of strings representing the trace (a simplified simulation).
		"""
		try:
			# Run the executable and capture the output (simulating the behavior tracing)
			process = subprocess.Popen([executable_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			stdout, stderr = process.communicate()
            
			# Convert stdout and stderr to strings and split them into lines for "trace" simulation
			output_trace: List[str] = stdout.decode('utf-8').splitlines() + stderr.decode('utf-8').splitlines()
			return output_trace
		except Exception as e:
			print(f"Error executing {executable_path}: {e}")
		return []

	def compute(self, executable1: str, executable2: str) -> Dict[str, int]:
		"""
		Compares the execution behavior of two executable files by analyzing their traces.

		:param executable1: Path to the first executable file.
		:param executable2: Path to the second executable file.
		:return: A dictionary with the number of unique and common trace lines.
		"""
		# Run both executables and collect their traces
		trace1: List[str] = self._run_and_trace(executable1)
		trace2: List[str] = self._run_and_trace(executable2)

		# Compare traces: unique to each and common
		unique_to_trace1: int = len(set(trace1) - set(trace2))
		unique_to_trace2: int = len(set(trace2) - set(trace1))
		common_traces: int = len(set(trace1) & set(trace2))

		# Return the comparison result
		return {
			"unique_to_executable1": unique_to_trace1,
			"unique_to_executable2": unique_to_trace2,
			"common_trace_lines": common_traces
			}
	def example(self):
		# Paths to the two executable files (this is just an example, adapt paths for real executables)
		executable1: str = "../sample/script1"
		executable2: str = "../sample/script2"

		# Compare the execution behavior of the two executables
		behavior_comparison: Dict[str, int] = self.compute(executable1, executable2)

		# Print the comparison results
		print(f"Behavior Comparison Results: {behavior_comparison}")

'''
import subprocess
from typing import List, Tuple

class SystemCallTraceDistance:
    def __init__(self, trace1: List[str], trace2: List[str]) -> None:
        """
        Initialize the SystemCallTraceDistance class with two system call traces.

        :param trace1: A list of system calls for the first executable.
        :param trace2: A list of system calls for the second executable.
        """
        self.trace1 = trace1
        self.trace2 = trace2

    def get_trace(self, executable_path: str) -> List[str]:
        """
        Run the executable and capture its system call trace using strace.

        :param executable_path: Path to the executable file.
        :return: A list of system calls made by the executable.
        """
        try:
            # Run the executable with strace to capture the system call trace
            result = subprocess.run(
                ['strace', '-c', executable_path],
                stderr=subprocess.PIPE, 
                text=True
            )
            # Extract system call trace from stderr
            trace_output = result.stderr.splitlines()
            return trace_output
        except Exception as e:
            print(f"Error capturing system call trace: {e}")
            return []

    def compute_distance(self) -> float:
        """
        Compute the distance between the two system call traces.
        
        The distance is calculated based on the difference in system calls.
        
        :return: A floating-point value representing the distance between the two traces.
        """
        set_trace1 = set(self.trace1)
        set_trace2 = set(self.trace2)

        # Calculate the Jaccard distance between the two system call sets
        intersection = len(set_trace1.intersection(set_trace2))
        union = len(set_trace1.union(set_trace2))

        if union == 0:
            return 1.0  # No system calls in either trace, return max distance
        return 1.0 - (intersection / union)

    @staticmethod
    def compare_executables(executable1: str, executable2: str) -> Tuple[float, List[str], List[str]]:
        """
        Compare the system call traces of two executables and compute the distance.

        :param executable1: Path to the first executable.
        :param executable2: Path to the second executable.
        :return: A tuple containing the distance and the traces of both executables.
        """
        distance_calculator = SystemCallTraceDistance([], [])
        
        # Capture system call traces for both executables
        trace1 = distance_calculator.get_trace(executable1)
        trace2 = distance_calculator.get_trace(executable2)
        
        # Initialize the calculator with the captured traces
        distance_calculator.trace1 = trace1
        distance_calculator.trace2 = trace2
        
        # Compute the system call trace distance
        distance = distance_calculator.compute_distance()
        
        return distance, trace1, trace2


if __name__ == "__main__":
    # Example usage comparing two executables
    executable_path_1: str = "./script1"
    executable_path_2: str = "./script2"
    
    distance, trace1, trace2 = SystemCallTraceDistance.compare_executables(executable_path_1, executable_path_2)
    
    print(f"System call trace distance: {distance}")
    print(f"Trace 1: {trace1}")
    print(f"Trace 2: {trace2}")
'''
import os
from typing import Tuple

class FileMetadataComparison(Distance):

	def __init__(self) -> None:
		"""
		Initialize the FileMetadataComparison class with the metadata of two files.

		:param file1_metadata: Metadata of the first file (size, creation time, modification time, permissions).
		:param file2_metadata: Metadata of the second file (size, creation time, modification time, permissions).
		"""
		super().__init__()
		self.type='file'

	def get_metadata(self, file_path: str) -> Tuple[int, float, float, int]:
		"""
		Get the metadata of a file.

		:param file_path: Path to the file.
		:return: A tuple containing the file size, creation time, modification time, and permissions.
		"""
		try:
			# Get file size in bytes
			file_size: int = os.path.getsize(file_path)
            
			# Get file creation time (Unix timestamp)
			file_creation_time: float = os.path.getctime(file_path)
            
			# Get file modification time (Unix timestamp)
			file_modification_time: float = os.path.getmtime(file_path)
            
			# Get file permissions (mode)
			file_permissions: int = os.stat(file_path).st_mode

			return file_size, file_creation_time, file_modification_time, file_permissions
		except Exception as e:
			print(f"Error retrieving metadata for {file_path}: {e}")
		return (0, 0.0, 0.0, 0)
		
	@staticmethod
	def compute_metadata_similarity(file1_metadata,file2_metadata) -> float:
		"""
		Compute the similarity between the metadata of two files.

		:return: A floating-point value representing the similarity between the metadata of the two files.
		"""
		size_similarity: float = 1.0 if file1_metadata[0] == file2_metadata[0] else 0.0
		creation_time_similarity: float = 1.0 if file1_metadata[1] == file2_metadata[1] else 0.0
		modification_time_similarity: float = 1.0 if file1_metadata[2] == file2_metadata[2] else 0.0
		permissions_similarity: float = 1.0 if file1_metadata[3] == file2_metadata[3] else 0.0
        
		# Average similarity score
		return (size_similarity + creation_time_similarity + modification_time_similarity + permissions_similarity) / 4

	def compute(self,file1_path: str, file2_path: str) -> Tuple[float, Tuple[int, float, float, int], Tuple[int, float, float, int]]:
		"""
		Compare the metadata of two files.

		:param file1_path: Path to the first file.
		:param file2_path: Path to the second file.
		:return: A tuple containing the similarity score and the metadata of both files.
		"""
        
		# Get metadata for both files
		file1_metadata = self.get_metadata(file1_path)
		file2_metadata = self.get_metadata(file2_path)
                
		# Compute the similarity between the two files' metadata
		similarity = self.compute_metadata_similarity(file1_metadata,file2_metadata)
        
		return 1 - similarity#, file1_metadata, file2_metadata

from typing import Optional, Tuple

class FileTypeDistance(Distance):

	def __init__(self) -> None:
		"""
		Initialize the FileTypeDistance class with the types of two files.

		:param file1_type: File type or signature of the first file.
		:param file2_type: File type or signature of the second file.
		"""
		super().__init__()
		self.type='file'
		
	@staticmethod
	def get_file_signature(file_path: str) -> Optional[str]:
		"""
		Get the file type or signature based on the file's magic bytes.

		:param file_path: Path to the file.
		:return: The file type or signature as a string, or None if it cannot be determined.
		"""
		try:
			with open(file_path, 'rb') as f:
				# Read the first few bytes of the file (magic number)
				file_header: bytes = f.read(8)

			# Dictionary of common file signatures (magic numbers)
			magic_dict = {
				b'\xFF\xD8\xFF': "JPEG",
				b'\x89PNG': "PNG",
				b'\x25\x50\x44\x46': "PDF",
				b'\x50\x4B\x03\x04': "ZIP",
				b'\x1F\x8B': "GZIP",
				b'\x49\x49\x2A\x00': "TIFF",
				b'\x4D\x5A': "EXE",
			}

			# Check for known signatures
			for magic, file_type in magic_dict.items():
				if file_header.startswith(magic):
					return file_type

			return None
		except Exception as e:
			print(f"Error reading file {file_path}: {e}")
		return None

	def compute(self,file_path1,file_path2) -> float:
		"""
		Compute the distance between the file types of two files.

		:return: A floating-point value representing the distance between the file types (1.0 for same, 0.0 for different).
		"""
		return 0.0 if self.get_file_signature(file_path1) == self.get_file_signature(file_path2) else 1.0

	@staticmethod
	def compare_files(file1_path: str, file2_path: str) -> Tuple[float, Optional[str], Optional[str]]:
		"""
		Compare the types of two files.

		:param file1_path: Path to the first file.
		:param file2_path: Path to the second file.
		:return: A tuple containing the similarity score and the file types of both files.
		"""
		comparator = FileTypeDistance(None, None)
        
		# Get file types based on their signatures
		file1_type = comparator.get_file_signature(file1_path)
		file2_type = comparator.get_file_signature(file2_path)
        
		# Initialize the comparator with the retrieved file types
		comparator.file1_type = file1_type
		comparator.file2_type = file2_type
        
		# Compute the similarity between the two files' types
		similarity = comparator.compute_file_type_similarity()
        
		return similarity, file1_type, file2_type

from typing import Any, Dict, List, Tuple

class TreeEditDistance(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='file'

	def _edit_distance(self, tree1: TreeNode, tree2: TreeNode) -> int:
		"""
		Recursively computes the tree edit distance between two nodes.

		:param tree1: The root node of the first tree.
		:param tree2: The root node of the second tree.
		:return: The edit distance between the two trees.
		"""
		if tree1 is None and tree2 is None:
			return 0
		if tree1 is None:
			return 1 + sum(self._edit_distance(None, child) for child in tree2.children)
		if tree2 is None:
			return 1 + sum(self._edit_distance(child, None) for child in tree1.children)
        
		cost: int = 0 if tree1.value == tree2.value else 1

		dist_matrix: List[List[int]] = [[0] * (len(tree2.children) + 1) for _ in range(len(tree1.children) + 1)]
        
		# Initialize the distance matrix
		for i in range(1, len(tree1.children) + 1):
			dist_matrix[i][0] = dist_matrix[i - 1][0] + self._edit_distance(tree1.children[i - 1], None)
		for j in range(1, len(tree2.children) + 1):
			dist_matrix[0][j] = dist_matrix[0][j - 1] + self._edit_distance(None, tree2.children[j - 1])

		# Fill the distance matrix
		for i in range(1, len(tree1.children) + 1):
			for j in range(1, len(tree2.children) + 1):
				dist_matrix[i][j] = min(
					dist_matrix[i - 1][j] + self._edit_distance(tree1.children[i - 1], None),  # Deletion
					dist_matrix[i][j - 1] + self._edit_distance(None, tree2.children[j - 1]),  # Insertion
					dist_matrix[i - 1][j - 1] + self._edit_distance(tree1.children[i - 1], tree2.children[j - 1])  # Substitution
				)
        
		return cost + dist_matrix[len(tree1.children)][len(tree2.children)]

	def compute(self, tree1: TreeNode, tree2: TreeNode) -> int:
		"""
		Computes the tree edit distance between two trees.

		:param tree1: The root of the first tree.
		:param tree2: The root of the second tree.
		:return: The tree edit distance between the two trees.
		"""
		return self._edit_distance(tree1, tree2)

	@staticmethod
	def parse_tree_from_dict(data: Dict) -> TreeNode:
		"""
		Parses a tree structure from a dictionary (e.g., from JSON or XML).

		:param data: The dictionary representing the tree structure.
		:return: The root TreeNode of the parsed tree.
		"""
		if isinstance(data, dict):
			root_value = list(data.keys())[0]
			children_data = data[root_value]
			children = [TreeEditDistance.parse_tree_from_dict(child) for child in children_data] if isinstance(children_data, list) else []
			return TreeNode(root_value, children)
		else:
			return TreeNode(data)
	def example(self):
		# Example usage with JSON-like data structures
		tree_data_1: Dict = {"root": [{"child1": []},{"child2": [{"grandchild1": []}]}]}
		tree_data_2: Dict = {"root": [{"child1": []},{"child3": [{"grandchild1": []}]}]}

		tree1: TreeNode = TreeEditDistance.parse_tree_from_dict(tree_data_1)
		tree2: TreeNode = TreeEditDistance.parse_tree_from_dict(tree_data_2)

		ted = TreeEditDistance()
		distance: int = ted.compute(tree1, tree2)

		print(f"Tree Edit Distance: {distance}")

import zlib
from typing import Union

class ZlibBasedDistance(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='file'

		"""
		Initializes the ZlibBasedDistance class to compare the structural differences
		between two files using zlib compression.
		"""

	def compress_data(self, data: bytes) -> int:
		"""
		Compresses the given data using zlib and returns the compressed size.

		:param data: The data to be compressed, in bytes.
		:return: The size of the compressed data.
		"""
		compressed_data: bytes = zlib.compress(data)
		return len(compressed_data)

	def compute(self, file1: Union[str, bytes], file2: Union[str, bytes]) -> float:
		"""
		Computes the Zlib-based distance between two files by comparing the compression
		size of the concatenated files with the individual compressed sizes.

		:param file1: Path to the first file or the raw byte data of the first file.
		:param file2: Path to the second file or the raw byte data of the second file.
		:return: The Zlib-based distance as a float value.
		"""
		if isinstance(file1, str):
			with open(file1, 'rb') as f1:
				data1: bytes = f1.read()
		else:
			data1: bytes = file1

		if isinstance(file2, str):
			with open(file2, 'rb') as f2:
				data2: bytes = f2.read()
		else:
			data2: bytes = file2

		compressed_size_1: int = self.compress_data(data1)
		compressed_size_2: int = self.compress_data(data2)

		combined_data: bytes = data1 + data2
		compressed_combined_size: int = self.compress_data(combined_data)

		distance: float = (compressed_combined_size - min(compressed_size_1, compressed_size_2)) / max(compressed_size_1, compressed_size_2)

		return distance


