"""
trie.py

Defines the TrieNode and Trie classes and their associated functions

@author: Sanjana Marce
"""

"""
TrieNode 

Class that specifies one node on a Trie with its associated variables 
- char: the character of this TrieNode
- eow: whether a valid word ends at this node
- children: a list of nodes pointing to children TrieNodes of this TrieNode
"""
class TrieNode:
    	
	def __init__(self, char, alph_len):
	    # character associated with this Trie node
		self.char = char
	    # flag for if a valid word ends at this node
		self.eow = False
	    # list of children nodes for next character from this character,
	    # initialized to an empty list
		self.children = [None]*alph_len
		# dynamic count for total children leaf use to calculate prob
		self.leafs = 1

"""
Trie 

Class that specifies a Trie via a pointer to its root
"""
class Trie:
	def __init__(self, alphabet):
		self.root = TrieNode('', len(alphabet))
		self.alphabet = alphabet
		self.idx_dict = self.get_index_dict(alphabet)

	"""
	get_index_dict: generates a dictionary mapping characters in the alphabet
	of letters that words in the Trie may contain to their indices in the
	array of children TrieNodes associated with each TrieNode
	
	@param: list - alphabet: list of characters that may appear in the Trie
	@return: dict
	
	"""
	def get_index_dict(self, alphabet):
		alph_to_idx = {alphabet[idx]: idx for idx in range(len(alphabet))}
		return alph_to_idx
	
	"""
	add_word: adds a single input word into the structure of this Trie 
	(following existing paths if any prefixes of the word exists in the Trie already)
	
	@param: str - word: word to add to the Trie
	@post: word has been added to the Trie
	"""
	def add_word(self, word):
		curr_node = self.root

		for char in word:
			idx = self.idx_dict[char]
			next_node = curr_node.children[idx]
			curr_node.leafs += 1
			if next_node == None:
				added_node = TrieNode(char, len(self.alphabet))
				curr_node.children[idx] = added_node
				curr_node = added_node
			else:
				curr_node = next_node
		curr_node.eow = True

	"""
	construct: given a list of words adds each word into this Trie's structure
	
	@param: list - vocab: list of words to add
	@post: this Trie now includes all the words in vocab
	"""
	def construct(self, vocab):
		for word in vocab:
			self.add_word(word)

	"""
	is_valid: traverses this Trie searching for the input word and whether any words in 
	this Trie have the input word as a prefix
	
	@param: str - word
	@return: -1 if no words in the dictionary start with the input word
	         0 if word is a valid entry in the dictionary
		 1 if word is a prefix to valid words in the dictionary but is not a valid word itself 
	"""
	def is_valid(self, word):
		curr_node = self.root
		for char in word:
			idx = self.idx_dict[char]
			if curr_node.children[idx] == None:
				return -1
			else:
				curr_node = curr_node.children[idx]
		if curr_node.eow == True:
			return 0
		return 1

	def get_prefix_leafs(self, prefix):
		curr_node = self.root
		for char in prefix:
			idx = self.idx_dict[char]
			if curr_node.children[idx] == None:
				return -1
			else:
				curr_node = curr_node.children[idx]
		
		if curr_node == None:
			return 0
		else:
			return curr_node.leafs

	def get_prob(self, prefix):
		return round(float(self.get_prefix_leafs(prefix) / self.get_total_word()), 2)

	def get_total_word(self):
		return self.root.leafs