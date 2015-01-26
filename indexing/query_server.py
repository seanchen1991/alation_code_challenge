import cmd
import cPickle as pickle
from pytrie import StringTrie

class QueryHandler(cmd.Cmd):

    # Initialize our `QueryHandler` class with our trie by calling `do_load()`
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.do_load()

    def do_load(self):
        inputfilename = 'trie.pickle'
        with open(inputfilename, 'rb') as handle:
            self.trie = pickle.load(handle)
        return self.trie

    def do_query(self, query):
        if query:
            counter = 0
            results = []

            # Returns an iterator over the entries in our trie whose prefixes match `query`
            iter = self.trie.iter_prefix_items(query)
            while counter < 10:
                results.append(next(iter))
                counter += 1

            # Sort our results by value
            results = sorted(results, key=lambda t: t[1], reverse=True)
            for i in range(10):
                print results[i]
        else:
            print "Please enter a valid query."

    def do_EOF(self, line):
        return True


if __name__ == "__main__":
    QueryHandler().cmdloop()
