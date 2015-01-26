# Alation Code Challenge

For this code challenge, I modeled my solutions after Vijay Ramakrishnan's, whose code can be found [here](https://github.com/vijay120/Alation).

1. Given a list of one million <string name, int score> pairs where names are valid Java variable names, write two programs and try to optimize their efficiency:

  a. A construction program that produces an index structure D.

  b. A Query Server Program that reads in serialized D and then accepts user queries such that for each query s, it responds with the top 10 names (ranked by score) that start with s or contains ‘_s’ (so for example, both “revenue” and “yearly_revenue” match the prefix “rev”). Query answering should run in sub-linear time (in terms of the number of names in the input).

2. You have a 100 GB text file and a Linux box with 4GB of RAM and 4 cores. Write a program/script that outputs a file listing the frequency of all words in the file (i.e. a TSV file with two columns <word, frequency>). Note that the set of words in the file may not fit in memory.

---

I took a few liberties with the parameters of the first question since I didn't write it in Java, namely interpreting the <string name, int score> pairs as Python tuples, as well as assuming that the list of tuples is comma-delimited. 

I used an implementation of `StringTrie` from the `pyTrie` library in order to achieve sub-linear query answering, as well as the cPickle library for fast serialization of the trie. You'll need to run `pip install pytrie` for the program to work.

To run the code, first call `python indexing.py` to generate the `trie.pickle` file. Then call `python query_server.py`, which will prompt you to enter your query. Delete the included `test.txt` file and rename your input file to `test.txt` to run the program with your own file.

When prompted by the (Cmd) prompt, type in 'query <your query>' (without the single-quotes). The program doesn't handle errors particularly well. For instance, if there are fewer than 10 matching prefixes found in the trie, the program crashes. Control-D exits the prompt without throwing an ugly 'KeyboardInterrupt' message. 

This problem took me about 5 hours. 

---

For the second problem, which took me about 4 hours, I decided to utilize Python's Multiprocessing library, one of the two available options for spawning multiple processes that Python's standard library offers (the other being the Threading library). The workflow I ended up going with was to have the `main()` function running on one processor, with the three other processors running the `processChunk()` function. 

The `main()` function does the work of reading in chunks of the input file, keeping track of the how much of the input file has been read, and passing the chunks along to an available processor. Each `processChunk()` does the work of stripping out punctuation from the chunk, caching the words into a local Python dictionary, and then writing each key, value pair to our redis store once all the words from the chunk have been processed. 

The redis store is persisted to disk and takes care of race conditions in the case that we have multiple processes writing to it at the same time. 

In order to run the code, you'll need to have a redis server running on localhost:6379, as well as redis-rdb-tools installed, which can be found [here](https://github.com/sripathikrishnan/redis-rdb-tools). Once the program has completed, call `rdb --command json dump.rdb` from the redis-server directory in order to convert the dump.rdb binary into valid JSON. Don't forget to change the name of your input file to `data.txt` and make sure you spin up a new redis store.

The runtime of this program is O(n), since all operations are linear. Judging from the profile returned by cProfiler, calling Python's `lower()` to convert every word into lower-case and `translate()` to strip out all of the punctuation are relatively costly. C would undoubtedly handle it much faster.
