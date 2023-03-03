from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import numpy as np
from collections import defaultdict

#region oldstuff
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

# print(findClosest(word, text, 2))
#endregion oldstuff

def countoccur(word):
    word = word.strip()
    res = np.array([0] * 26)
    for i in word:
        res[getAsci(i) % 26] += 1
    return res
def dist(x, y):
    return np.sqrt(abs(np.sum(x - y)))
def replacewith(word):
    word = word.lower().split()
    d = {"robert": "bob"}
    res = ""
    for i in word:
        if i in d:
            res += d[i] + " "
        else:
            res += i + " "
    return res

#Run OMP with word and text, find "count" matches (upperbound)
def mymatch(df_1, df_2, key1, key2, cutoff=1, limit=2, func=countoccur):
    #TO DO: count occurences of letters, run OMP
    #cuz if our word is [1,0,0,1] and text is [1,0,0,1,0,0,0,1,1,0] if we do
    #text - word shift 0 we get [0,0,0,0,0,0,0,1,1,0], make sure its max(subtraction, 0)
    arr1 = df_1[key1].to_numpy()
    arr2 = df_2[key2].to_numpy()
    res = defaultdict(list)
    lim = defaultdict(lambda : 0)
    for i in arr1:
        word1 = func(i)
        if lim[i] >= limit:
            continue
        for j in arr2:
            if lim[i] >= limit:
                break
            if pd.notna(j) and dist(word1, func(replacewith(j))) < cutoff:
                res[i].append(j)
                lim[i] += 1
    ret = ""
    for i in res.keys():
        ret += f'{i}: {res[i]}\n'
    return ret[:-1]

# Create two example dataframes
df1 = pd.DataFrame({'Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
                    'Age': [30, 25, 40],
                    'City': ['New York', 'San Francisco', 'Chicago']})
df2 = pd.DataFrame({'Full Name': ['John Doe', 'Jane Smith', 'Robert Johnson'],
                    'Salary': [50000, 60000, 70000]})

# Define a function to do the fuzzy matching
def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=2):
    """
    :param df_1: the left dataframe to join
    :param df_2: the right dataframe to join
    :param key1: the key column of the left dataframe
    :param key2: the key column of the right dataframe
    :param threshold: the minimum score for a match to be considered
    :param limit: the maximum number of matches to return
    :return: a merged dataframe
    """
    s = df_2[key2].tolist()

    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))
    df_1['matches'] = m

    m2 = df_1['matches'].apply(lambda x: [i[0] for i in x if i[1] >= threshold])
    df_1['matches'] = m2

    # explode and merge
    res = df_1.explode('matches').merge(df_2, left_on='matches', right_on=key2)
    res.drop('matches', axis=1, inplace=True)
    return res

# print("----------")
# # Call the function to do the fuzzy matching join
# result = fuzzy_merge(df1, df2, 'Name', 'Full Name', threshold=70)
# print(result)
# print("----------")
# result2 = mymatch(df1, df2, 'Name', 'Full Name', 1)
# print(result2)
# print("----------")

df_pb = pd.read_csv("./bio_grouped_new.csv")
df_fg = pd.read_csv("./fgquery.csv")
df_pb["name"] = df_pb["NAME_FIRST"] + " " + df_pb["NAME_LAST"]
f1 = func=lambda x: np.array(toIntLi(toBin(x)))
print(mymatch(df_fg.head(120), df_pb.head(120), "personLabel", "name", cutoff = 0.5, limit=1, func=f1))
#todo: pad stuff