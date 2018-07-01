#Author - Achal Agarwal

from fuzzywuzzy import fuzz



def is_eligible(cluster, word):
    print('cluster = ' , cluster)
    return True
def get_cluster_index(word, data):
    print('entered')
    index = -1

    # data = list(filter(lambda x: is_eligible(x, word),data))
    print(data)
    for i in range(len(data)):
        best = 0
        if not is_eligible(data[i], word):
            continue
        threshold = 89
        max = 0
        for j in range(len(data[i])):
            w_t = data[i][j]
            threshold = 89 + j
            w = w_t[0]
            score = fuzz.ratio(w,word)
            if score>threshold and score>max:
                max = score

        if max > best:
            index = i
            best = max


    if index >= 0:
        flag = False
        for w_t in data[index]:
            w = w_t[0]
            if w==word:
                w_t_new = (w,w_t[1]+1)
                # w_t[1] += 1
                data[index][data[index].index(w_t)] = w_t_new
                flag = True
                break
        if not flag:
            data[index].append((word,1))
    if index == -1:
        data.append([(word,1)])
        index = len(data) -1
    return index

def isValidWord(word):
    #if len(word) < 3:
     #   return False

    #for char in word:
    #    if str(char).isdigit():
    #        return False

    try:
        float(word)
        return False
    except ValueError:
        pass

    return not isInvalidWord(word)
    # return True


def isInvalidWord(word):
    word = word.lower()
    return word == 'pieces' or word == 'kilos' or word == 'kgs' or word == 'rupees' or word == 'rs' or word == 'packets' or word == 'dozens' or word == 'ltrs' or word == 'litres' or 'gms' == word or word == 'mls'  or word == 'pcs'  or word == 'litre' or word == 'grams'

def remove_special_symbols(str):
    str = str.replace('\\', ' ')
    str = str.replace('\'', ' ')
    str = str.replace('/', ' ')
    str = str.replace('-', ' ')
    str = str.replace(';', ' ')
    return str

def cleanWord(word):
    word = word.lower()
    cleanedWord = ""
    return ''.join(list(filter(lambda x: str(x).isalpha() or str(x)=='\'', word)))

def cleanItem(item):
    item  = remove_special_symbols(item)

    # cleanedItem = ""

    words = item.split()
    # words = list(map(cleanWord,words))
    words = list(filter(isValidWord, words))
    # cleanWordList = []


    return (" ".join(words)).strip()
