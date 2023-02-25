import numpy as np
import heapq

#similar letters are mapped to the same letter
def getAsci(char):
    char = char.lower()
    a = [set("ÀÁÂÃÄÅàáâãäå"), set("ÈÉÊËèéêë"), set("ÌÍÎÏìíîï"), set("ÒÓÔÕÖØòóôõöø"), set("ÙÚÛÜùúûüÝýÿ")]
    d = {0 : "a", 1: "e", 2: "i", 3: "o", 4: "u"}
    for i, j in enumerate(a):
        if char in j:
            char = d[i]
    return ord(char)
def normalize(word):
    if type(word) == str:
        word = toIntLi(toBin(word))
    norm = np.sqrt(np.dot(word, word))
    return word / norm


def toBin(word):
    res = ""
    for i in word:
        i = getAsci(i) 
        res += str(i) #in binary, left shift
    return res
def toIntLi(binWord):
    return [int(i) for i in binWord]
def autocorr(word):
    if type(word) == str:
        word = toIntLi(toBin(word))
    res = np.correlate(word, word)
    return res
def corr(word1, word2):
    if type(word1) == str:
        word1 = toIntLi(toBin(word1))
    if type(word2) == str:
        word2 = toIntLi(toBin(word2))
    return np.correlate(word1, word2)

#run OMP-esque circorr, find "count" closest (upperbound)
def findClosest(word, text, count):
    # text = text.split()
    # ompRes = []
    # wordAuto = autocorr(word) / len(word)
    # autoDot = np.sqrt(np.dot(wordAuto, wordAuto))
    # for i in text:
    #     resCor = corr(word, i) / max(len(i), len(word))
    #     resDot = np.sqrt(np.dot(resCor, resCor))
    #     ompRes.append((i, resDot))
    # print(ompRes)
    # return (word, autoDot), heapq.nlargest(count, ompRes, key=lambda x: x[1])
    print(1)

text = "dajbefa dafnkja abcdef abdecf àbcdef loool chefCurry LOOOL"
word = "abcdef"

print(findClosest(word, text, 2))

#Run OMP with word and text, find "count" matches (upperbound)
def omp(word, text, count):
    #TO DO: count occurences of letters, run OMP
    #cuz if our word is [1,0,0,1] and text is [1,0,0,1,0,0,0,1,1,0] if we do
    #text - word shift 0 we get [0,0,0,0,0,0,0,1,1,0], make sure its max(subtraction, 0)
    print(1)