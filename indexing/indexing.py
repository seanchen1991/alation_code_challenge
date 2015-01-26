from ast import literal_eval
from pytrie import StringTrie
import cPickle as pickle

# A helper function which reads in the file and populates a list with all the tuples in the list
def readTuples(file):
    result = []
    with open(file, 'r') as f:
        for line in f:
            result.extend(literal_eval(line.strip()))
    return result

# Contructs a trie from the list of tuples
def constructTrie(list):
    trie = StringTrie()
    for item in list:
        trie.__setitem__(item[0], item[1])
    return trie

# Serializes our trie using the cPickle library and outputs it to 'trie.pickle'
def main():
    inputfilename = 'test.txt'
    result = readTuples(inputfilename)
    trie = constructTrie(result)
    with open('trie.pickle', 'wb') as handle:
        pickle.dump(trie, handle)

if __name__ == "__main__":
    main()
