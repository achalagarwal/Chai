
# coding: utf-8
# from fuzzywuzzy import fuzz

# from autocorrect import spell
# import spacy
# nlp = spacy.load('en_core_web_lg')
import re
from src.Utils.Pickler import pickle_dict,unpickle_dict
import json
from src.expression.Sku import Sku
import csv
# from sys import maxsize
# import csv
from time import time
from tqdm import tqdm as progress
# from scoring_utils import *
# from Utils.sku_utils import *


def getDistance(word1, word2):
    # return typo_distance(word1, word2)
    return distance.get_jaro_distance(word1, word2, winkler=True, scaling=0.1)


def getCSV(data, filename="data.csv"):
    assert(data)
    cols = len(data[0])
    cols = [x for x in range(cols)]
    with open(filename, 'wt') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(cols)
        for row in data:
            csv_out.writerow(row)


def getTypoCSV(data):
    # data = [('smith, bob', 2), ('carol', 3), ('ted', 4), ('alice', 5)]
    with open('typos.csv', 'wt') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Suggested Spelling', 'Current Spelling', 'Item Name', 'Score'])
        for row in data:
            csv_out.writerow(row)


def find_min_char_index(char, word, index=0):
    min = len(word)
    found = False
    for i in range(len(word)):
        if word[i] == char:
            found = True
            if abs(i - index) < abs(min - index):
                min = i
    if found:
        return abs(min - index)
    else:
        return -1


def isVowel(char):
    char = char.lower()
    return char == 'a' or char == 'e' or char == 'i' or char == 'o' or char == 'u'


def get_decay(prev_decay):
    if prev_decay > 0.8:
        return prev_decay - 0.05

    if prev_decay > 0.6:
        return prev_decay - 0.03

    if prev_decay > 0.4:
        return prev_decay - 0.01

    return prev_decay


def helper_typo_distance(incorrect,correct):
    sum_first = 0
    decay = 1
    penalty = max(len(incorrect), len(incorrect))
    for i in range(len(correct)):

        char_index = find_min_char_index(correct[i],incorrect,i)

        if char_index == -1:
            sum_first += 0.2 * 1 / penalty
            continue
        if isVowel(correct[i]):
            sum_first += 0.9*decay * char_index
            decay = get_decay(decay)
            continue
        if not isVowel(correct[i]):
            sum_first += decay*char_index
            decay = get_decay(decay)
            continue

    return sum_first

def typo_distance(incorrect, correct):
    # sum_first = 0
    # decay = 1
    # penalty = max(len(incorrect), len(incorrect))
    # for i in range(len(correct)):
    #
    #     char_index = find_min_char_index(correct[i],incorrect,i)
    #
    #     if char_index == -1:
    #         sum_first += 0.2 * 1 / penalty
    #         continue
    #     if isVowel(correct[i]):
    #         sum_first += 0.9*decay * char_index
    #         decay = get_decay(decay)
    #         continue
    #     if not isVowel(correct[i]):
    #         sum_first += decay*char_index
    #         decay = get_decay(decay)
    #         continue
    #
    # if recurse:
    #     return min(sum_first, typo_distance(correct,incorrect,False))
    # else:
    #     return sum_first

    return min(helper_typo_distance(incorrect,correct),helper_typo_distance(correct, incorrect))
    # sum_second = 0
    # decay = 1
    # for i in range(len(incorrect)):
    #     if find_min_char_index(incorrect[i], correct, i) == -1:
    #         sum_second += 0.2 * 1 / penalty
    #         continue
    #     if not isVowel(incorrect[i]):
    #         sum_second += decay*find_min_char_index(incorrect[i], correct, i)
    #         decay = get_decay(decay)
    #     elif isVowel(incorrect[i]):
    #         sum_second += 0.9 * decay * find_min_char_index(incorrect[i], correct, i)
    #         decay = get_decay(decay)
    #
    # return min(sum_first, sum_second)




def getLinearSpan(words):

    # start = time()
    span = []
    for i in range(len(words)):

        for j in range(i, len(words)):
            vec = []
            for k in range(len(words) - j):
                vec.append(words[i+k])
            span.append(vec)

    # for vec in span:
    #     print(vec)
    # end = time()
    # print("Time taken - ",end - start)
    return span


def importBigBasketDataFromFile(filename):
    json_data = open("/Users/achal/Downloads/all_big_basket.json").read()
    data = json.loads(json_data, encoding=None, cls=None, object_hook=None,
                      parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None)
    items = []
    for key in data:
        item_name = data[key]['item_name']
        items.append(item_name)

    return items


def import_madhuloka_data(filename):
    json_data = open("./"+filename).read()
    data = json.loads(json_data, encoding=None, cls=None, object_hook=None,
                      parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None)
    return data


def importSKUDataFromFile(fileName):
    json_data = open(fileName).read().splitlines()
    objects = []
    for data in json_data:
        objects.append(json.loads(data))

    return objects


def cleanSKUData(data):
    extract_tuple = []
    extract_name_tag = []
    extract_id = []
    extract_subtag = []

    for object in data:
        # extract_tuple.append((object["_id"]["$oid"], object["name"]))
        extract_name_tag.append((object["name"], object["suggest"]["contexts"]["subTag"], object['_id']['$oid']))
        # extract_id.append(object["_id"]["$oid"])


    extract_tuple = set(extract_tuple)
    extract_id = set(extract_id)
    extract_name_tag = set(extract_name_tag)


    # print(len(extract_name_tag))
    # print(len(extract_id))
    # print(len(extract_tuple))
    return extract_name_tag


def extract_number_from_string(string, keyword):
    pattern = re.escape(keyword) + r'":\s*"(.+?)"'
    matches = re.findall(pattern, string)
    if not matches:
        pattern = re.escape(keyword) + r'":\s*(.+?)\}'
        matches.extend(re.findall(pattern, string))
    if not matches:
        pattern = re.escape(keyword) + r'":\s*(.+?)"'
        matches.extend(re.findall(pattern, string))

    numbers = []
    for match in matches:
        try:
            numbers.append(int(match))
        except ValueError:
           return []
    return numbers

def extractFromString(string, keyword='product'):
    # list_of_products = literal_eval(string)

    # my_regex = r"\b(?=\w)" + re.escape(TEXTO) + r"\b(?!\w)"
    pattern = re.escape(keyword)+r'":\s*"(.+?)",'
    # pattern = keyword+'":\s*"(.+?)",'
    # pattern = re.escape(pattern)
    # pattern = r'product":\s*"(.+?)",'
    matches = re.findall(pattern, string)

    return matches

def get_info_from_order_form(orderform):

    orderform_data = json.loads(orderform[0])
    products = []
    for product in orderform_data:
        userid = orderform[1]
        try:
            dzerid = product['meta']['location']['dzid']
        except KeyError:
            dzerid = None
        try:
            subtag = product['meta']['subTag']
        except KeyError:
            subtag = orderform[2]
        products.append((userid, product['product'], subtag, float(product['quantity']), dzerid))

        # try:
        #     dzerid = product[]
    # dzerid = extractFromString(orderform[0], keyword='dzid')
    # # subtag = extractFromString(order[0], keyword='subTag')
    # if dzerid:
    #     dzerid = dzerid[0]
    # else:
    #     dzerid = None

    # subtag = orderform[2]

    return products
def getInfoFromOrder(order):
    # products = None
    # userid = None
    # dzerid = None
    # try:
    #     tuple_data = literal_eval(order)
    #     products = tuple_data[0]
    #     # products = literal_eval(order[0])
    #     userid = tuple_data[1]
    #     products = [product['product'] for product in products]
    #
    #     # for product in products:
    #     #     items.append((product['product'],userid))
    # except:
    #     pass
    products = extractFromString(order[0])
    dzerid = extractFromString(order[0], keyword='dzid')
    # subtag = extractFromString(order[0], keyword='subTag')
    if dzerid:
        dzerid = dzerid[0]
    else:
        dzerid = None
    userid = order[1]
    subtag = order[2]



        # for product in products:
        #     items.append((product,userid))

    return products,userid, dzerid,subtag


def match_item_to_raw_data(item,data):
    data = list(filter(lambda x: helper_eligible_pair(x, item), data))
    best, best_sku_matched, best_items_matched = getMatch(item, data)
    # print(best)
    if not best:
        return None

    # all_matched = set(best)
    best_zipped = list(zip(best,best_sku_matched,best_items_matched))
    best_zipped = list(filter(lambda x: is_good_match(
        x[0], item, x[1], x[2]), best_zipped))
    if not best_zipped:
        return None
    [best,best_sku_matched,best_items_matched] = [list(t) for t in list(zip(*best_zipped))]
    best = get_better_from_best(item, best, best_sku_matched, best_items_matched)
    # print(best)
    return best
def match_item_to_sku(item_data_tuple_with_uid_dzid_tag,sku_data_tuple_with_tag):

    sku_data_tuple_with_tag = list(filter(lambda x: is_eligible_pair(x, item_data_tuple_with_uid_dzid_tag), sku_data_tuple_with_tag))

    data = sku_data_tuple_with_tag
    data  = list(map(lambda x: x[0],data))
    item = item_data_tuple_with_uid_dzid_tag[0]

    best, best_sku_matched, best_items_matched = getMatch(item, data)
    # print(best)
    if not best:
        return None

    # all_matched = set(best)
    best_zipped = list(zip(best,best_sku_matched,best_items_matched))
    best_zipped = list(filter(lambda x: is_good_match(
        x[0], item, x[1], x[2]), best_zipped))
    if not best_zipped:
        return None
    [best,best_sku_matched,best_items_matched] = [list(t) for t in list(zip(*best_zipped))]
    best = get_better_from_best(item, best, best_sku_matched, best_items_matched)
    # print(best)
    return best

def getCustomOrderFormDataFromFile(filename):

    orders = []
    with open(filename, newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in progress(reader):
            if row['sub_tag'] == 'Food' or row['sub_tag'] == 'SAMPLING_PROMO_BUY' or row['sub_tag'] == 'Flowers' or row['sub_tag'] == 'Sports' or row['sub_tag'] == 'Pets' or row['sub_tag'] == ['Exploratory - Buy'] or row['sub_tag'] == 'Stationary':
                continue
            orders.append((row['list_items'],row['id'],row['sub_tag']))

    items = []
    for orderform in progress(orders):
        try:
            products = get_info_from_order_form(orderform)
            for product in products:
                # items.append((clean_item(product),userid,dzerid,subtag))
                items.append(product)
        except:
            continue

    return items

def getOrderFormDataFromFile(filename):

    orders = []
    with open(filename, newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            orders.append((row['list_items'],row['uuid']))

    items = []
    for order in orders:
        products, userid = getInfoFromOrder(order)
        if not products:
            continue
        for product in products:
            items.append((clean_item(product), userid))

        # try:
        #     tuple_data = literal_eval(order)
        #     products = tuple_data[0]
        #     # products = literal_eval(order[0])
        #     userid = tuple_data[1]
        #
        #     for product in products:
        #         items.append((product['product'],userid))
        # except:
        #     products = extractFromString(order[0])
        #     userid = order[1]
        #     for product in products:
        #         items.append((product,userid))

    return items





def printVector(vec):
    print("Printing Vector")
    for v in vec:
        print(v)

    return "Printed Vector"






def helperGetElligiblePair(item1, item2):
    if is_eligible_pair(item1, item2):
        return item1
    return None

# Create Sku Objects for  Sku (name,tag) list


def get_sku_list_csv(sku_list):
    tuple_list = []
    for sku in sku_list:
        tuple_list.append(tuple(str(sku).splitlines()))

    getCSV(tuple_list, 'popularity.csv')


def get_name_dict_from_class_dict(class_dict):
    name_dict = {}

    for k,v in class_dict.items():
        sku_names = []
        for sku in v[:-1]:
            sku_names.append(sku._original_name)
        name_dict[k] = sku_names

    return name_dict

def get_class_dict_from_name_dict(name_dict, sku_list):

    sku_name_list = []
    for sku in sku_list:
        sku_name_list.append(sku._original_name)

    class_dict = {}

    for item_name_tag,sku_names in name_dict.items():
        skus = []
        for sku_name in sku_names:
            skus.append(get_corresponding_sku_object(sku_name,sku_name_list,sku_list))
        skus.append(0)
        class_dict[item_name_tag] = skus

    return class_dict


def extract_skus_from_name_dict(item_name_tag, item_dict, sku_list):

    sku_name_list = item_dict[item_name_tag]
    skus = []
    for sku_name in sku_name_list:
        skus.append(get_corresponding_sku_object(sku_name, sku_names, sk))

def test_pickled_data():
    item_dict = unpickle_dict('dict')
    items = getCustomOrderFormDataFromFile('big_data.csv')
    sku_list = get_sku_list()

    for item in progress(items):
        try:
            sku_name_list = item_dict[item[0:2]]
        except KeyError:
            continue
        for sku_name in sku_name_list:
            sku = get_corresponding_sku_object(sku_name,sku_list)
            sku.update_count(1)
            sku.update_score(1)
            sku.update_popularity(1)

    get_sku_list_csv(sku_list)
    return True
def get_sku_list():
    raw_sku_list = cleanSKUData(importSKUDataFromFile('auto.json'))
    sku_list = build_sku_list(raw_sku_list)
    return sku_list
def test_cluster_popularity():

    # test_pickled_data()
    # from sys import exit
    # exit()
    sku_list = get_sku_list()
    # / Users / achal / Dunzo / Data / dunzo_tasks_raised_1stJan_dump.csv
    items = getCustomOrderFormDataFromFile('/Users/achal/Dunzo/Data/dunzo_tasks_raised_1stJan_dump.csv')
    try:
        item_dict = unpickle_dict('dict')
    except FileNotFoundError:
        item_dict = {}
    class_dict = get_class_dict_from_name_dict(item_dict,sku_list)
    master_dict = tag_and_score(items, sku_list, class_dict)
    pickle_dict(get_name_dict_from_class_dict(master_dict),'dict')
    # test = unpickle_dict('dict')
    # print(test)
    sort_sku_list(sku_list)
    get_sku_list_csv(sku_list)


    # printVector(sku_list)

#list of the worst matches
#meta data score
#category

def get_corresponding_sku_object(sku_name, sku_names, sku_list):



    return sku_list[sku_names.index(sku_name)]


def build_sku_list(sku_name_tag):

    sku_list = []

    for sku in sku_name_tag:
        assert(len(sku) == 2)
        sku_name = sku[0]
        sku_subtag = sku[1]
        sku_list.append(Sku(sku_name=sku_name,sku_subtag=sku_subtag))

    return sku_list


def sort_sku_list(sku_list):

    sku_list.sort(key=lambda x: x._popularity, reverse=True)

    return


def tag_and_score(items,sku_list, item_dict={}):

    # item_dict = {}

    for item in progress(items):

        item_name_tag_tuple = item[0:2]
        if item_name_tag_tuple in item_dict:
            item_match_list = item_dict[item_name_tag_tuple]

            # The last index of the list stores the frequency of the exact item
            item_match_list[-1] += 1
            continue

        # else
        item_match_list = get_match(item, sku_list, func = None)
        item_match_list.append(1)
        item_dict[item_name_tag_tuple] = item_match_list

    for item,item_match_list in item_dict.items():

        score = 1
        frequency = item_match_list[-1]

        # removing the frequency from the list
        item_match_list = item_match_list[:-1]

        if not item_match_list:
            continue

        decay = 1/len(item_match_list)
        item_match_list.sort(key=lambda x: x._score,reverse=True)

        for sku in item_match_list:
            sku.update_popularity(score*frequency)
            score -= decay

    return item_dict

def get_match(item, sku_list, func = None):

    min = 10000
    matched_sku_words_list = []
    matched_item_words = []
    matched_sku = []

    item_name = item[0]
    item_tag = item[1]
    item_count = item[2]
    sku_list = list(filter(lambda x: x.is_eligible(item_name,item_tag),sku_list))

    for sku in sku_list:
        distance, item_words_matched, sku_words_matched = sku.match_distance(item_name)
        if distance < min:
            min = distance
            matched_sku = [sku]
            matched_item_words = [item_words_matched]
            matched_sku_words_list = [sku_words_matched]
        elif distance == min:
            matched_sku.append(sku)
            matched_item_words.append(item_words_matched)
            matched_sku_words_list.append(sku_words_matched)


    match_zipped = list(zip(matched_sku,matched_sku_words_list,matched_item_words))
    match_zipped = list(filter(lambda x: is_good_match(x[0]._name, item_name, x[1], x[2]), match_zipped))

    if not match_zipped:
        return []

    [best,best_sku_matched,best_items_matched] = [list(t) for t in list(zip(*match_zipped))]
    matched_sku_with_score = get_better_from_best(item_name, best, best_sku_matched, best_items_matched)

    matches = []

    for match_with_score in matched_sku_with_score:
        match = match_with_score[0]
        matches.append(match)
        score = match_with_score[1]
        match.update_count(item_count)
        match.update_score(score)




    return matches


def getMatch(item, data, func=getDistance):

    # print("Item is ", item)
    # if  not 'thumbs' in item.lower():
    #     return []

    min = 10000
    best = []
    best_indices = []
    best_items_matched = []
    best_sku_matched = []
    # start = time()
    for sku in data:
        if sku == None:
            continue
        # if not 'thums' in sku:
        #     continue
        span = get_linear_span(sku.split())
        distance, item_words_matched, sku_words_matched = get_min_item_edit_distance(item, span)
        if distance < min:
            min = distance
            best = []
            best_indices = []
            best_items_matched = []
            best_sku_matched = []
            best_items_matched.append(item_words_matched)
            best_sku_matched.append(sku_words_matched)
            best.append(sku)
            best_indices.append(data.index(sku))
        elif distance == min:
            best.append(sku)
            best_indices.append(data.index(sku))
            best_sku_matched.append(sku_words_matched)
            best_items_matched.append(item_words_matched)

    # end = time()
    # print("Time taken is ", end - start)

    # check if words are being used, else best = None

    # updated_best = []
    #
    # temp_best = ""
    # maximum = 0
    #
    # for i in range(len(best)):
    #     items = len(clean_words(item.split()))
    #     skus = len(clean_words(best[i].split()))
    #
    #     if len(best_sku_matched[i]) >= 0.5*skus and len(best_items_matched[i]) >= 0.5*items:
    #         updated_best.append(best[i])
    #     # else:
    #     #     pass
    #     #     # print("Eliminating ", best[i])
    #     if max(len(best_sku_matched[i]), len(best_items_matched[i])) > maximum:
    #         maximum = max(len(best_sku_matched[i]), len(best_items_matched[i]))
    #         temp_best = best[i]
    #
    # if not updated_best:
    #     if len(temp_best) > 0:
    #         # print("Choosing Sub optimal value ",temp_best)
    #         updated_best.append(temp_best)

    # if not updated_best and not func == edit_distance:
    #         # print("Switching to Edit Distance")
    #         return getMatch(item,data,edit_distance)
        # doc = nlp(sku)

    return best, best_sku_matched, best_items_matched




def getLower(word):
    return word.lower()


def getData():
    items = getCustomOrderFormDataFromFile("orderform.csv")

    # items = list(map(clean_item, items))


    data = cleanSKUData(importSKUDataFromFile('auto.json'))

    # data = list(map(getLower, data))

    # getCSV(list(data),"newnew")
    # print(data)
    # with open("sku_data.json", "w") as f:

    return data, items


def getSKUMatch(item):
    data, items = getData()

    item = items[0]

    val = computeMatchWeight(item, data)


def computeMatchWeight(item, data):
    item_words = item.split()
    for sku in data:
        sku_words = sku.split()
        getMatch()
# for sku in data:
#     pattern = 'u\''+ sku + '\''
# #     print(pattern)
#     doc = nlp(sku)
#     for token in doc:
#         print(token.text,token.pos_, token.dep_)
#     print("\n")


def curateData():
    data, items = getData()
    file = open("data.txt", "w")
    for d in data:
        file.write(d)
        file.write("\n")



    # sku_words = set(item1.split())
    # item_words = set(item2[0].split())
    # if sku_words.intersection(item_words):
    #     return True
    #
    # for word in item_words:
    #     for inner_word in sku_words:
    #         if fuzz.ratio(word,inner_word) >= 90:
    #             return True
    #
    # return False
    # chars1 = set(word[0] for word in words1)
    # chars2 = set(word[0] for word in words2)
    # return chars1.intersection(chars2)
    # common_words = words1.intersection(words2
    # return flag


def load_english_words():
    word_file = open('words.txt', 'r', encoding='iso-8859-1')

    s = list([line.rstrip('\n') for line in word_file])

    return s


def extractWords(data):
    words = set()
    for item in data:
        for word in item.split():
            words.add(word)
    return words


def minimalSimilarity(word1, word2):

    if not have_similar_length(word1, word2):
        return False

    if word1[0] == word2[0]:
        return True

    l1 = len(set(word1))
    l2 = len(set(word2))
    l = min(l1, l2)

    chars1 = set(word1)
    chars2 = set(word2)
    chars = chars1.intersection(chars2)

    if len(chars) > 0.5 * l:
        return True

    return False


def getAlternate(item, dict, similar):
    # words = extractWords(data)

    output = []

    for word in item.split():
        magic_value = 0.9

        if 'milk' in word:
            continue

        if 'johnson' in word:
            continue

        if word in dict:
            continue

        sword = spell(word)

        if sword == word:
            continue

        # printVector(words)
        similar_words = set(filter(lambda x: minimalSimilarity(x, word), similar))
        similar_dicts = set(filter(lambda x: minimalSimilarity(x, word), dict))

        # if word == sword:
        #     print("debug")

        match = []

        if sword in similar_words:
            if word in similar_words:
                # match.append(sword)
                # print("For item ", item, " the word ", word, " may be a misspelling of ", sword)
                magic_value -= 0.3
                output.append((sword, word, item, getDistance(word, sword)))
            else:
                # print("For item ", item, " the word ", word, " could be a misspelling of ", sword)
                magic_value -= 0.1
                output.append((sword, word, item, getDistance(word, sword)))

        magic_value -= 0.1

        if not word in similar_words:

            min_dist = 1.5
            best_match = None

            for s in similar_words:
                dist = typo_distance(s, word)
                if dist < min_dist:
                    min_dist = dist
                    best_match = s

            magic_value -= min_dist/3

            if best_match:
                output.append((best_match, word, item, getDistance(word, best_match)))
                # continue

        continue

        # for m in match:
        #     if not m == word:
        #         print("For item ", item, " the word ", word, " could be a typo of ", m)
        #
        # continue
        # if word == 'sausags' or word == 'stella':
        #     print("debug")
        #
        # # print(word, " is in consideration")
        # # printVector(elligible_words)
        # if (not word in similar_words) and (not word in similar_dicts):
        #     if spell(word) in similar_words:
        #         print("For item ", item," the word ", word, " could be a misspelling of ", spell(word))
        #     else:
        #         for w in similar_words:
        #             dist = typo_distance(w,word)
        #             if dist > 0 and dist <= 1.5 and have_similar_length(word, w):
        #                 print("For item ", item," the word ", word, " could be a misspelling of ", w)
        #                 break
        #         print("For item ", item, " the word ", word, " could be a misspelling of ", spell(word))
        # continue
        # if not word in elligible_words:
        #     for w in elligible_words:
        #         dist = typo_distance(w,word)
        #         if dist > 0 and dist <= 1.5 and have_similar_length(word, w):
        #             print("For item ", item," the word ", word, " could be a misspelling of ", w)
    return output


def have_similar_length(word1, word2):
    l1 = len(word1)
    l2 = len(word2)
    tolerance = 1 + 0.2 * (l1+l2)/2
    return abs(l1 - l2) <= tolerance


def getTypos():
    all = []
    data_bb = importBigBasketDataFromFile("all_big_basket.json")
    data_bb = list(map(clean_item, data_bb))
    data_ma = get_alcohol_data()
    data_ma = list(map(clean_item, data_ma))
    data_dict = load_english_words()
    bad, dont = getData()
    bad = set(map(clean_item, bad))
    print("data received")
    total = len(bad)
    percentage = 1
    count = 0
    for i in bad:

        count += 1
        # if not 'protien' in i:
        #     continue
        data_bigb = list(filter(lambda x: is_eligible_pair(x, i), data_bb))
        data_bigb = extractWords(data_bigb)
        data_ma = list(filter(lambda x: is_eligible_pair(x, i), data_ma))
        data_ma = extractWords(data_ma)
        data_similar = data_ma | data_bigb
        # print("debug")
        # temp_data = temp_data | data
        # printVector(temp_data)
        input = getAlternate(i, data_dict, data_similar)
        for xyz in input:
            print(xyz[0], xyz[1], xyz[2], xyz[3])
        all.extend(input)
        if int(100*count/total) > percentage:
            percentage = 100*count/total
            print(percentage, ' %')

    getTypoCSV(set(all))
    # best = getMatch(i, temp_data)
    #
    # print("Item is",i)
    # for match in best:
    #     print(match)
    # print("***")


def get_alcohol_data():
    data = import_madhuloka_data('m.json')
    items = []
    for item in data:
        items.append(item["name"])
    return items

def populate(item,sku_matches,sku_list,sku_count):
    pass

def printPercentage(count, total):
    print(round(count/total * 100, 3), " %")


def is_good_match(sku_name, itemname, list1, list2):
    # try:
    #     assert(len(list1) == len(list2))
    # except:
    #     print("******************************")

    # count = 0

    words = itemname.split()
    if not words:
        return False
    if len(words) == 1:
        words = sku_name.split()
        if not words:
            return False
        return fuzz.ratio(words[-1],itemname) >= 90

    count = len(list(filter(lambda x: getDistance(x[0],x[1]) > 0.85,list(zip(list1,list2)))))

    item_word_count = len(itemname.split())
    sku_word_count = len(sku_name.split())

    if count/item_word_count >= 0.75:
        return True

    if count/sku_word_count >= 0.75:
        return True


    # for i in range(len(list1)):
    #     if getDistance(list1[i], list2[i]) > 0.85:
    #         count += 1

    flag = (count >= 0.55*max(len(sku_name.split()), len(itemname.split()))) or (count >= 0.70 * min(len(sku_name.split()), len(itemname.split())))
    # if not flag:
    #     print(sku_name,itemname)
    return flag

    # print(item1," <-> ", item2, " has typo ", typo_distance(item1, item2))


def merge_list_of_lists(list_of_lists):
    masterlist = set()
    for l in list_of_lists:
        for word in l:
            masterlist.add(word)

    return list(masterlist)



def get_better_from_best(item, best, best_sku_matched, best_items_matched):
    # print('*',item,best,best_sku_matched,best_items_matched)
    item_words = item.split()
    filter1 = []
    max_score = 0
    # print(item)
    # print(best_sku_matched)

    for match in best:
        # match_words = match.split()
        match_words = match._name.split()
        sku_matched = best_sku_matched[best.index(match)]
        sku_matched_extract = [l.split()[0] for l in sku_matched]
        sku_matched = merge_list_of_lists(sku_matched)
        score1 = get_sequential_score(sku_matched_extract,match_words)
        score2 = get_brand_word_score(sku_matched,match_words)
        score3 = get_root_word_score(sku_matched,match_words)
        score4 = get_match_count_score(sku_matched,match_words)
        # print(score1,score2,score3,score4)
        total_score = score1 + score2 + score3 + score4

        # prev_match_index = -1
        # score = 0
        #
        # for i in range(len(item_words)):
        #     if item_words[i] not in best_items_matched:
        #         continue
        #     matched_index = best_items_matched.index(item_words[i])
        #     match_in_sku = sku_matched[matched_index][0]
        #     check_index = match_words.index(match_in_sku)
        #     if check_index >= prev_match_index:
        #         score += 1
        #         prev_match_index = check_index

        if total_score >= max_score * 1.5:
            filter1 = [(match,total_score)]
        if max_score*0.8 <= total_score < max_score*1.5:
            filter1.append((match,total_score))
            filter1 = list(filter(lambda x: x[1]>= 0.8 * total_score ,filter1))
        if total_score < max_score * 0.8:
            pass
        max_score = max(max_score,total_score)
    # filter1 = [f[0] for f in filter1]
    # print(set(best).difference(set(filter1)))
    return filter1



def main():

    all_items = []
    all_missed = []
    categories = []
    category_count = []
    # alcohol()
    # from sys import exit
    # exit()

    # debug()
    # # from sys import exit
    # exit()

    data, orderform = getData()
    print(len(data))
    data = set(data)
    original_data = list(data)
    data_user_sets = []
    original_data_names = []
    for sku in original_data:
        data_user_sets.append(set())


    for sku in original_data:
        original_data_names.append(sku[0])
    data = []
    # data_unique_users = []
    # for t in original_data:
    #     data.append(t[0])

    print(len(original_data))
    original_data = [(clean_item(t[0]), t[1]) for t in original_data]
    data_names = [o[0] for o in original_data]
    # data = list(map(clean_item, data))
    # print(len(data))


    count_arr = np.zeros(shape = (len(original_data),1), dtype=int)
    # printVector(data)
    # from sys import exit
    # exit()
    # data = set(data)
    items = []
    for v in orderform:
        items.append((v[0],v[3]))

    print(len(items))
    items = [(clean_item(t[0]), t[1]) for t in items]
    print(len(items))
    total = len(items)
    print(total)
    count = 0
    obtained = 0
    start = time()

    item_index = -1

    for item in progress(items[100:500]):
        data = original_data
        item_index += 1
        # if 'vimal pan' not in item:
        #     continue
        userid = orderform[item_index][1]

        count += 1
        itemname = item[0]
        item_tag = item[1]
        data = list(filter(lambda x: is_eligible_pair(x, item), data))
        data = [d[0] for d in data]
        item = item[0]
        best, best_sku_matched, best_items_matched = getMatch(item, data)
        # best = get_close_matches(item, data, n=2, cutoff=0.7)
        # process.extract(, choices, processor=default_processor, scorer=default_scorer, limit=5)
        # best = process.extract(item, data,scorer=fuzz.token_set_ratio, limit=2)
        # best = [b[0] for b in best]
        if not best:
            continue

        all_matched = set(best)

        best = list(filter(lambda x: is_good_match(
            x, item, best_sku_matched[best.index(x)], best_items_matched[best.index(x)]), best))

        best = get_better_from_best(item, best, best_sku_matched, best_items_matched)
        # missed = all_matched.intersection(set(best))

        if not best:
            for miss in all_matched:
                all_missed.append((item, miss))

        # best = is_best_match(item,best)
        if best:
            obtained += 1

            # print("Item: ",item)

            for match in best:
                index = data_names.index(match)
                count_arr[index] += 1
                data_user_sets[index].add(userid)
                # print(match)
                all_items.append((item, original_data[index],match))
                category = original_data[index][1]

                if category not in categories:
                    categories.append(category)
                    category_count.append(0)

                c_index = categories.index(category)
                category_count[c_index] += 1


        if count % 500 == 0:
            end = time()
            printPercentage(count, total)
            print("Time taken till now", end - start)
            start = time()

        # if obtained == 100:
        #     break


        # print("Obtained", obtained)

    # all_items = []
    for u in data_user_sets[60]:
        print(u)
    data_user_sets = [len(s) for s in data_user_sets]

    print("Obtained", obtained)
    getCSV(list(zip(original_data_names, count_arr.tolist(),data_user_sets)), filename="check.csv")
    # getCSV(all_missed, filename="check1.csv")
    getCSV(all_items, filename="check2.csv")
    getCSV(list(zip(categories,category_count)), filename="check3.csv")
    # # print(match)

    # print("***")

#
# data,items = getData()
# print(1)
# data

# items = getData()
# cProfile.run('test_cluster_popularity()','profiler')

#
# if __name__ == "__main__":
#     cProfile.run('main()','profiler')
