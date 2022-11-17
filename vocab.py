"""
vocab.py

Includes functions to load in a dictionary from a txt file and to reduce 
this dictionary to only include words based on a specified alphabet.

@author: Sanjana Marce
"""

"""
load_dictionary: loads dictionary into list from txt file

@param: str - filename: txt file with each valid word on a new line
@return: list
"""
def load_dictionary(filename):
	f = open(filename, 'r')
	content = f.read()
	dictionary = content.split('\n')
	f.close()
	return dictionary

"""
reduce_vocab: reduces a list of words from the dictionary to only 
those words made up of characters in the provided alphabet

@param: list - vocab: list of words in original dictionary
@param: list - alphabet: list of characters by which to trim the input vocab
@return: list
"""
def reduce_vocab(vocab, alphabet):
	reduced = [word for word in vocab if all(char in alphabet for char in word)]
	return reduced
