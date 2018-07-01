#Author - Achal Agarwal

from tqdm import tqdm as progress
import json
from temp.clusterer import get_cluster_index, cleanItem

def get_local_data_for_testing():
    with open('data_chunk_6.json', mode='r') as f:
        data = json.load(f)
    batch_cluster(data)

def map_term(term,master_dict,cluster_leaders):
    words = term.split()
    final_word = ""
    for word in words:
        final_word += cluster_leaders[master_dict[word]] + ' '
    return final_word.strip()

def batch_cluster(data):
    try:
        with open('preprocessed_dict.json', mode='r') as f:
            master_dict = json.load(f)
    except FileNotFoundError:
        master_dict = {}

    try:
        with open('preprocessed_clusters.json', mode='r') as f:
            cluster_terms = json.load(f)
    except FileNotFoundError:
        cluster_terms = []


    terms = []

    for term in data:
            terms.append(term)
        # terms.append(d['searchTerms'])
    clean_terms = list(map(cleanItem, terms))
    clean_terms = list(filter(lambda x: x,clean_terms))
    # cluster_terms = []
    # master_dict = {}
    # print(clean_terms)
    print(master_dict)
    for term in progress(clean_terms):
        # print('t ',term)
        words = term.split()

        for word in words:

            if word in master_dict:
                match_index = master_dict[word]
            else:
                # print('w' , words)
                match_index = get_cluster_index(word,cluster_terms)
                master_dict[word] = match_index
    cluster_leaders = []
    for cluster_term in cluster_terms:
        leader = None
        max_score = 0
        for term_score in cluster_term:
            score = term_score[1]
            if score > max_score:
                max_score = score
                leader = term_score[0]
        cluster_leaders.append(leader)

    # for term in data:
    #     new_terms = []
    #     for term in d['searchTerms']:
    #         new_terms.append(map_term(cleanItem(term),master_dict,cluster_leaders))
    #     d['searchTerms'] = new_terms

            # d['searchTerms'] = map_term(cleanItem(d['searchTerms']),master_dict,cluster_leaders)
    # with open('preprocessed_dict.json', 'w') as outfile:
    #     json.dump(master_dict, outfile)
    # with open('preprocessed_clusters.json', 'w') as outfile:
    #     json.dump(cluster_terms, outfile)
    return cluster_leaders

# get_local_data_for_testing()
