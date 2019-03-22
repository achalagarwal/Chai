from chai.src.Utils.scorer import Scorer
from fuzzywuzzy import fuzz
from copy import deepcopy


def get_score(item, sku):

    # # print(item.name, ' -> ', sku._name)
    item_sku_term_map = {}

    sku_clusters_copy = {}
    for cluster, term_list in sku.cluster_terms.items():
        sku_clusters_copy[cluster] = deepcopy(term_list)

    for term in item.terms:

        term_cluster = item.term_cluster.get(term, None)

        if term_cluster is None:
            item_sku_term_map[term] = None
            continue

        mapped_term_list = sku_clusters_copy.get(term_cluster, None)
        if not mapped_term_list:
            item_sku_term_map[term] = None
            continue
        item_sku_term_map[term] = mapped_term_list[0]
        mapped_term_list.pop(0)

    sku_item_term_map = {}

    item_clusters_copy = {}
    for cluster, term_list in item.cluster_terms.items():
        item_clusters_copy[cluster] = deepcopy(term_list)

    for term in sku.terms:

        term_cluster = sku.term_cluster.get(term, None)

        if term_cluster is None:
            sku_item_term_map[term] = None
            continue

        mapped_term_list = item_clusters_copy.get(term_cluster, None)
        if not mapped_term_list:
            sku_item_term_map[term] = None
            continue
        sku_item_term_map[term] = mapped_term_list[0]
        mapped_term_list.pop(0)

    # print(item_sku_term_map)
    # print(sku_item_term_map)

    score = 0

    sequential = get_sequential_score(item, sku, item_sku_term_map)
    user_query = get_user_query_score(item, sku, item_sku_term_map)
    brand_word = get_brand_word_score(item, sku, sku_item_term_map)
    root_words = get_root_words_score(item, sku, sku_item_term_map)
    meta_match = get_meta_match_score(item, sku)
    match_ratio = get_match_ratio_score(item, sku)

    score += sequential + user_query + brand_word + root_words + meta_match + match_ratio

    return score


def get_sequential_score(item, sku, item_sku_term_map):

    scorer = Scorer(initial_score=0, initial_incrementer=1, decay_function=None, decay_factor=2)
    prev_index = -1

    for item_term in item.terms:

        sku_mapped_term = item_sku_term_map[item_term]
        if sku_mapped_term is None:
            scorer.decay
            continue
        sku_term_index = sku.terms.index(sku_mapped_term)
        if sku_term_index >= prev_index:
            scorer.increment
            prev_index = sku_term_index
            continue
        if prev_index > sku_term_index:
            scorer.decay
            prev_index = sku_term_index
            continue

    # print('get_sequential_score', scorer.score)
    return scorer.score


# scores based on the psychology that the user types in descending order of term importance
def get_user_query_score(item, sku, item_sku_term_map):

    scorer = Scorer(initial_score=0, initial_incrementer=1, decay_function=None, decay_factor=2)

    for item_term in item.terms:

        if item_sku_term_map[item_term]:
            scorer.increment
        scorer.decay

    # print('get_user_based_score', scorer.score)
    return scorer.score


# scores based on the convention that the brand name of a product is mentioned in the starting
def get_brand_word_score(item, sku, sku_item_term_map):

    scorer = Scorer(initial_score=0, initial_incrementer=2, decay_function=None, decay_factor=2)

    for sku_term in sku.terms:

        if sku_item_term_map[sku_term]:
            scorer.increment
        scorer.decay

    # print('get_brand_word_score', scorer.score)
    return scorer.score


# scores based on the contra-position of the brand word logic i.e. the product root word is present in the end
def get_root_words_score(item, sku, sku_item_term_map):

    scorer = Scorer(initial_score=0, initial_incrementer=1, decay_function=None, decay_factor=2)

    for sku_term in sku.terms[::-1]:

        if sku_item_term_map[sku_term]:
            scorer.increment

        scorer.decay

    # print('get_root_word_score', scorer.score)
    return scorer.score


# scores based on the meta data match of the item and sku
def get_meta_match_score(item, sku):

    item_meta_data = item.meta_data.split()
    sku_meta_data = sku.meta_data.split()
    score = 0

    for item_meta_term in item_meta_data:
        for sku_meta_term in sku_meta_data:
            temp_fuzz = fuzz.ratio(item_meta_term, sku_meta_term)
            if temp_fuzz >= 75:
                score += temp_fuzz/100
                break

    # score = fuzz.token_sort_ratio(item_meta_data, sku_meta_data)/20

    # print('get_meta_match_score', score)
    return score


def get_match_ratio_score(item, sku):

    item_clusters = set(item.cluster_terms.keys())
    sku_clusters = set(sku.cluster_terms.keys())
    match_clusters = item_clusters.intersection(sku_clusters)

    score = int(min(len(match_clusters)/len(sku.terms), len(match_clusters)/len(item_clusters))*10) + 1

    # print('get_match_ratio_score', score)
    return score


