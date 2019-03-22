from fuzzywuzzy import fuzz
from sys import maxsize


def is_valid_word(word):
    if len(word) < 3:
        return False

    for char in word:
        if str(char).isdigit():
            return False

    return not is_invalid_word(word)


def clean_words(words):
    cleaned_words = list(filter(lambda x: not is_invalid_word(x), words))

    return cleaned_words


def is_invalid_word(word):

    num_words = ["one", "two", "three", "four", "five", "hlf", "six", "seven", "some", "eight",
                 "nine", "ten", "twenty", "thirty", "fourty", "fifty", "hundred", "a", "full", "half", "quarter"]
    units = ["kg", "KG", "gm", "grm", "kilo", "gram", "kilos", "g", "pack", "bottled", "crate",
             "basket", "litre", "cans" "carton", "tablet", "scoop", "l", "bunch", "portion", "case",
             "portion", "liter", "mg", "ml", "cm", "pc", "no", "dozen", "peice", "piece", "box",
             "boxes", "ltr", "bottle", "Rs", "packet", "\"", "slice", "pkt", "strip", "percent",
             "metre", "meter", "inches", "inch", "%", "feet", "ft", "pack", "plate", "kgs", "KGs",
             "gms", "grms", "grams", "g", "packs", "baskets", "litres", "cartons", "tablets", "portions",
             "cases", "liters", "mgs", "cms", "pcs", "nos", "dozens", "peices", "boxes", "ltrs", "pint",
             "pints", "bottles", "bags", "packets", "\"", "slices", "pkts", "strips", "qty", "metres", "meters",
             "inches", "%", "fts", "packs", "plates", "m", "magnum"]
    probable_other = ["the", "to", "up", "from",
                      "for", "is", "there", "and", "wid", "n"]
    joining_words = ["no", "without", "(", ")", "all", "not", "or", "with"]

    flag = word in num_words or word in probable_other or word in joining_words or word in units

    return word in 'pieces' or word in 'kilos' or word in 'kgs' \
           or word in 'rupees' or word in 'rs' or word in 'packets'\
           or word in 'dozens' or word in 'ltrs' or word in 'litres' \
           or 'gms' == word or word in 'mls' or word in 'pcs' or 'litre' == word or word in 'grams'\
           or flag


def remove_special_symbols(string):
    string = string.replace('\\', ' ')
    string = string.replace('\'', ' ')
    string = string.replace('/', ' ')
    string = string.replace('-', ' ')
    string = string.replace(';', ' ')
    string = string.replace(',', ' ')

    return string


def clean_word(word):
    word = word.lower()
    cleaned_word = ''
    flag = True
    for i in range(len(word)):
        if word[i].isalpha() and flag:
            cleaned_word+=word[i]
            continue
        if word[i].isalpha() and not flag:
            flag = True
            cleaned_word+=' '+word[i]
            continue
        if (not word[i].isalpha()) and not flag:
            cleaned_word += word[i]
            continue
        if (not word[i].isalpha()) and flag:
            flag = False
            cleaned_word += ' ' + word[i]

    return cleaned_word


def clean_item_with_meta(item):
    item = remove_special_symbols(item)
    words = item.split()
    words = list(map(clean_word, words))
    meta_words = []
    term_words = []

    for word in words:
        if is_valid_word(word):
            term_words.append(word)
        else:
            meta_words.append(word)


    # meta_words = list(filter(lambda x: not is_valid_word(x), words))
    # term_words = list(filter(is_valid_word, words))
    return (" ".join(term_words)).strip(), separate_meta_data(" ".join(meta_words)).strip()


def clean_item(item):
    item = remove_special_symbols(item)
    words = item.split()
    words = list(map(clean_word, words))
    words = list(filter(is_valid_word, words))
    return (" ".join(words)).strip()


def get_linear_span(words):
    span = []

    for i in range(len(words)):
        temp = words[i:]

        for j in range(len(temp)):
            span.append(temp[0:j+1])

    return span


def get_min_item_edit_distance(item, span):
    item_words = item.split()
    dist = 0
    item_words_matched = []
    sku_words_matched = []

    for word in item_words:
        tolerance = 0.014
        word_distance, best_vec = get_min_word_edit_distance(word, span)
        if word_distance < tolerance:

            dist += word_distance
            item_words_matched.append(word)
            sku_words_matched.append(get_str_from_vec(best_vec))

        else:

            dist += 1

    return dist, item_words_matched, sku_words_matched


def get_min_word_edit_distance(word, span):
    min_dist = maxsize
    best_vec = []
    for vec in span:
        computed_distance = compute_edit_distance(word, vec)
        if computed_distance < min_dist:
            min_dist = computed_distance
            best_vec = vec

    return min_dist, best_vec


def get_str_from_vec(vec):

    return (" ".join(vec)).strip()


def compute_edit_distance(word, vec):
    string = get_str_from_vec(vec)

    return 1/(1 + fuzz.ratio(word, string))
    # return 1/(0.1+func(word, str))
    # return (typo_distance(word, str) + edit_distance(word, str)) / 2
    # # return min(edit_distance(word,str),typo_distance(word,str))


def helper_eligible_pair(item1, item2):
    sku_words = item1.split()
    item_words = item2.split()
    if set(sku_words).intersection(set(item_words)):
        return True

    sku_chars = list(map(lambda x: x[0], sku_words))
    item_chars = list(map(lambda x: x[0], item_words))

    for i_char in item_chars:
        for s_char in sku_chars:
            if i_char == s_char:
                # if distance.get_jaro_distance(item_words[item_chars.index(i_char)], sku_words[sku_chars.index(s_char)],winkler = False, scaling=0.1) > 90:
                #     return True
                if fuzz.ratio(item_words[item_chars.index(i_char)], sku_words[sku_chars.index(s_char)]) > 90:
                    return True

    # sku_chars = list(map(lambda x: x[1], sku_words))
    # item_chars = list(map(lambda x: x[1], item_words))
    #
    # for i_char in item_chars:
    #     for s_char in sku_chars:
    #         if i_char == s_char:
    #             if fuzz.ratio(item_words[item_chars.index(i_char)],sku_words[sku_chars.index(s_char)]) >= 90:
    #                 return True
    #

    return False

    # for word in item_words:
    #     for inner_word in sku_words:
    #         if fuzz.ratio(word,inner_word) >= 90:
    #             return True
    #
    # return False


# sku = item1
# item = item2

def flipper(flag, option1, option2):
    if flag == option1:
        return option2
    if flag == option2:
        return option1

    raise(ValueError, "The flag must take either of two values")


def separate_meta_data(string):

    status = 'ALPHABET'
    separated_string = ""
    for char in string:
        if str(char).isalpha() and status == 'ALPHABET':
            separated_string += char
            continue
        if not str(char).isalpha() and status == 'SPECIAL':
            separated_string += char
            continue
        if (str(char).isalpha() and status == 'SPECIAL') or (not str(char).isalpha() and status == 'ALPHABET'):
            separated_string += ' ' + char
            status = flipper(status, 'SPECIAL', 'ALPHABET')
            continue

    return separated_string.strip()


def is_eligible_pair(item1, item2):
    if not item1[1] == '' and not item2[1] == '':
        if not item1[1] == item2[1]:
            if item1[1] == 'Paan' or item2[1] == 'Paan':
                if 'cig' in item1[1] or 'cig' in item2[1]:
                    return helper_eligible_pair(item1[0], item2[0])
            return False

    return helper_eligible_pair(item1[0], item2[0])


def meets_match_count_threshold(item, sku):

    item_clusters = set(item.term_cluster.values())
    sku_clusters = set(sku.term_cluster.values())
    matched_clusters = item_clusters.intersection(sku_clusters)

    if len(item_clusters) == 0:
        return False

    if len(matched_clusters) / len(item_clusters) > 0.65:
        return True
    if len(matched_clusters) / len(sku_clusters) > 0.65:
        return True
    return False


def is_liquid_unit(word):
    units = ["litre", "l", "liter", "ml", "ltr", "litres", "liters", "m"]
    return word in units


def extract_alcohol_liquid_quantity(expression, additional_dict={}):

    expression_meta = expression.meta_data.split()

    for i in range(len(expression_meta)):
        term = expression_meta[i]
        if is_liquid_unit(term):
            try:
                value = float(expression_meta[i-1])
                return value, term
            except ValueError:
                continue

    for term in expression_meta:
        if term in additional_dict:
            return additional_dict[term], "ml"

    return None, None

