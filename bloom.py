
"""
Implement a BloomFilter Key Value Store Class in Python. The idea
is to keep N (argument to init) most frequently used members in RAM
and the entire data structure on disk. To be specific, you have to use
collections.ordereddict to store dict of size N in RAM and shelve module
to store data on disk.

RAM = The ordered dict
Disk = shelf

Context = one hit wonder
Objects = strings (for simplicity)

My understanding of the question :
    Bloomfilter uses couple of hash functions to figure if the word should be stored in the RAM.
    After the Bloomfilter has made its decision it provides us the word to be stored. This Word
    can be a repeated word too as the Bloomfilter itself isn't aware of the words in the RAM.
    If the word is a repeated, we will increment the frequency counter otherwise if the word
    is new, we will eliminate the word with least frequency from the RAM and store
    the new word with frequency 1.
    Disk at all times will store the whole data.
"""
from collections import OrderedDict
import shelve

class BloomStore:
    
    def __init__(self,n):
        
        self.capacity = n
        self.orderedDict = OrderedDict()
        
    def add(self,new_item):
        
        """
        if item exists -> increase count
        if item doesnt exist -> remove the least frequent in case the capacity is exceeded
        """
        
        if self.orderedDict.get(new_item) != None: # None if item doesnt exist
            self.orderedDict[new_item] += 1
            
            
        else:
            if len(self.orderedDict) >= self.capacity:
                self.move_to_disk(new_item)
            else:
                self.orderedDict[new_item] = 1 
                self.shelf_data((new_item,1))
                    
            
    def move_to_disk(self,new_item):

        least_frequent = min(self.orderedDict.items(), key=lambda x: x[1]) 
        #we can also use FIFO in case frequencies are same
        del self.orderedDict[least_frequent[0]]
        self.shelf_data(least_frequent)
        self.orderedDict[new_item] = 1 
        
    def shelf_data(self,least_frequent):
        
        key = least_frequent[0]
        current_frequency = least_frequent[1]
        
        with shelve.open('shelf') as s:
            #check if key exists, if it does, increase counter otherwise add new key
            if key in s:
                
                s[key] = current_frequency + s[key]
             
            else:
                s[key] = 1
     
       # TEST 
# bloom = BloomStore(3)
# bloom.add("satyam")
# bloom.add("shivam")
# bloom.add("parallel")
# bloom.add("satyam")
# bloom.add("shivam")
# bloom.add("parallel")
# bloom.add("parallel")
# bloom.add("satyam")
# bloom.add("dots")
# bloom.add("ggn")
# bloom.add("ggn")
# bloom.add("xyz")   # ggn replaced by xyz

# print(bloom.orderedDict)


"""
###     Bag Of Words    ###
A. A word2index which holds the index of every word in the array.
B. An index2word which gives word on a given index.
C. A method which takes an index and returns the vector with count of the word at index at 0s for all other word in vocabulary
D. Constructor to create an empty Bag Of Words.
E. Method for adding one word at a time in Bag of Words.
F. Method getvectors which takes a list of words as inputs and returns their Array Represenetation as output.
(so for example the total number of words in Bag Of Words is 4 and Apple is the third word and Ball 
is the second word, 
getvectors(["Apple","Ball"]) will return[[0,0,1,0],[0,1,0,0]] )
"""

class BagOfWords:
    
    def __init__(self):
        self.bag = []
        self.word2index = {}
        self.index2word = {}
        
    def add_to_bag(self,new_word):
        
        # check, if the word is new : append | else : increment counter in bag at the word index
        if new_word in self.word2index:
            index = self.word2index.get(new_word)
            self.bag[index] +=1
        else:
            append_index = len(self.bag)             #no need to subtract 1 
            self.bag.append(1)                       #appends 1 to the end
            self.word2index[new_word] = append_index #index in bag
            self.index2word[append_index] = new_word 
        
    def getVectors(self,word_list):
        
        # CASE : when the word isn't in the bag
        
        result = []
        for word in word_list:
            vector = [0] * len(self.bag)
            index_of_word = self.word2index.get(word)
            count_of_word = self.bag[index_of_word]
            vector[index_of_word] = count_of_word
            result.append(vector)
        return result

# bagOfWords = BagOfWords()
# bagOfWords.add_to_bag("satyam")
# bagOfWords.add_to_bag("satyam")
# bagOfWords.add_to_bag("parallel")
# bagOfWords.add_to_bag("shivam")

# print(bagOfWords.index2word)
# print(bagOfWords.word2index)
# print(bagOfWords.bag)
# print(bagOfWords.getVectors(["satyam","shivam"]))
        
        
    