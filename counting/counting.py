import cProfile
import string
import redis
import multiprocessing as mp
    
# The function that handles caching and writing to our redis instance, which we run across three of the four available processors
def processChunk(inputstring):
    database = redis.StrictRedis(host='localhost', port=6379, db=0)
    cache = {}
    count = 0
    # Treat lower- and upper-case forms of a word as the same word
    inputstring = inputstring.lower()
    # Removes all punctuation from our inputstring
    inputstring = inputstring.translate(None, string.punctuation)
    wordList = inputstring.split()
    for word in wordList:
        count += 1
        try:
            cache[word] += 1
        except KeyError:
            cache[word] = 1
    for key, value in cache.iteritems():
        original = database.get(key)
        if not original:
            database.set(key,value)
        else:
            database.set(key,value+int(original))
    return count

# A helper function used by `main()` to keep track of how much of the text file we've read through
def findLastDelim(inputstring):
    i = -1
    for char in reversed(inputstring):
        if char in string.whitespace:
            return i
        i -= 1
    return
    
# Our `main()` reads in a chunk of 'data.txt' and hands it off to one of our processes        
def main():
    inputfilename = 'data.txt'
    leftover = ''
    totalcount = 0
    pool = mp.Pool(processes=3)
    with open(inputfilename, 'r') as f:
        while True:
            chunk = f.read(1024)
            if chunk == '':
                break
            lastDelimIndex = findLastDelim(chunk)
            data = string.strip(leftover + chunk[:lastDelimIndex])
            leftover = string.strip(chunk[lastDelimIndex:])
            result = pool.apply_async(processChunk, args=(data,))
            totalcount += result.get(timeout=1)
    print totalcount

cProfile.run('print main(); print')

if __name__ == "__main__":
    main()
