from collections import OrderedDict
from src.Utils.sku_utils import clean_item_with_meta
from fuzzywuzzy import fuzz


class AutoComplete:

    def __init__(self, match_book):

        # assert type(match_book) is Match.MatchSku

        self._matchbook = match_book

        self._lru_cache = OrderedDict()

        self._lru_size = 100000

        self._query_list = []

    def get_from_cache(self, key):
        try:
            value = self._lru_cache.pop(key)
            self._lru_cache[key] = value
            return value
        except KeyError:
            return -1

    def set_in_cache(self, key, value):
        try:
            self._lru_cache.pop(key)
        except KeyError:
            if len(self._lru_cache) >= self._lru_size:
                self._lru_cache.popitem(last=False)
        self._lru_cache[key] = value

    # def get_cached_results(self, query):
    #
    #     if query == '':
    #         return []
    #
    #     return self._lru_cache.get(query, self.get_cached_results(query[0:-1]))

    @staticmethod
    def get_cluster_match_score(sku, query_clusters):

        sku_clusters = set(sku.cluster_terms.keys())
        match_clusters = query_clusters.intersection(sku_clusters)
        if not match_clusters:
            return 0

        return int(min(len(match_clusters) / len(sku.terms), len(match_clusters) / len(query_clusters)) * 10) + 1

    @staticmethod
    def get_meta_match_score(query, sku):

        sku_meta = sku.meta_data
        query_terms, query_meta = clean_item_with_meta(query)
        score = 0

        for query_meta_term in query_meta:
            for sku_meta_term in sku_meta:
                temp_fuzz = fuzz.ratio(query_meta_term, sku_meta_term)
                if temp_fuzz >= 75:
                    score += temp_fuzz / 100
                    break

        return score

    def hit_query(self, query, limit=10):

        cached_value = self.get_from_cache(query)

        # if value == -1 then no results in cache
        if not cached_value == -1:
            return cached_value

        terms = query.split()
        query_clusters = set()

        # Handling Last Term separately
        last_term = terms[-1]
        last_term_cluster = self._matchbook.get_term_cluster(last_term)
        if last_term_cluster:
            query_clusters.add(last_term_cluster)
            last_term_score = 1
            last_term_sku = self._matchbook.cluster_dict[last_term_cluster]
        else:
            last_term_score = 0.5
            last_term_sku, last_term_clusters = self._matchbook.get_sku_with_clusters_from_term_prefix_clusters(last_term)
            query_clusters = query_clusters.union(last_term_clusters)

        # Dict to store all relevant sku information
        sku_info = {}

        # Handling all the other terms
        for term in terms[0:-1]:
            term_cluster = self._matchbook.get_term_cluster(term)
            if term_cluster is None:
                continue
            query_clusters.add(term_cluster)
            term_sku_set = self._matchbook.cluster_dict[term_cluster]
            for sku in term_sku_set:
                if sku in sku_info:
                    sku_info[sku]['count'] += 1
                else:
                    sku_info[sku] = {'count': 1, 'cluster_match_score': 0, 'meta_match_score': 0}

        for sku in last_term_sku:
            if sku in sku_info:
                sku_info[sku]['count'] += last_term_score
            else:
                sku_info[sku] = {'count': last_term_score, 'cluster_match_score': 0, 'meta_match_score': 0}

        # Update two scores for the SKUs in sku_info
        for sku in sku_info.keys():
            sku_info[sku]['cluster_match_score'] = AutoComplete.get_cluster_match_score(sku, query_clusters)
            sku_info[sku]['meta_match_score'] = AutoComplete.get_meta_match_score(query, sku)

        # zip all the scores with the sku
        sku_zip = [(sku, info) for sku, info in sku_info.items()]

        # Sort based on count
        sku_zip.sort(key=lambda x:x[1]['count'], reverse=True)

        # truncating sku list to limit paramter

        has_dict = {}

        truncated_zip = []

        # remove SKUs with the same name
        for sku, info in sku_zip:
            if sku.get_name() in has_dict:
                continue
            has_dict[sku.get_name()] = info
            truncated_zip.append((sku, info))

        # Sort based on meta match score
        truncated_zip.sort(key=lambda x: x[1]['meta_match_score'], reverse=True)

        # Sort based on Popularity
        truncated_zip.sort(key=lambda x: x[0]._popularity, reverse=True)

        # Limit results to 10
        limited_zip = truncated_zip[0:limit+1]

        # Update Cache
        self.set_in_cache(query, limited_zip)

        return limited_zip



