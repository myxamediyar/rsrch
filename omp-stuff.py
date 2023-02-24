import numpy as np
import heapq

#similar letters are mapped to the same letter
def getAsci(char):
    char = char.lower()
    a = [set("ÀÁÂÃÄÅàáâãäå"), set("ÈÉÊËèéêë"), "ÌÍÎÏìíîï", set("ÒÓÔÕÖØòóôõöø"), set("ÙÚÛÜùúûüÝýÿ")]
    d = {0 : "a", 1: "e", 2: "i", 3: "o", 4: "u"}
    for i, j in enumerate(a):
        if char in j:
            char = d[i]
    return ord(char)

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
    text = text.split()
    ompRes = []
    wordAuto = autocorr(word) / len(word)
    autoDot = np.sqrt(np.dot(wordAuto, wordAuto))
    for i in text:
        resCor = corr(word, i) / len(i)
        resDot = np.sqrt(np.dot(resCor, resCor))
        ompRes.append(resDot)
    print("OMP:", ompRes)
    return heapq.nlargest(count, ompRes), autoDot

text = "dajbefa dafnkja abcdef abdecf àbcdef loool chefCurry"
word = "abcdef"

print(findClosest(word, text, 2))