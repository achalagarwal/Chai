from chai.src.expression import Sku
from chai.src.Utils import sku_utils, scoring_utils


class Match:

    def __init__(self):
        pass


class MatchSku(Match):

    def __init__(self):

        super().__init__()
        # stores the list of corpus
        self.corpora = []

        # stores the dict of terms mapped to their corpus
        self.term_dict = {}

        # dict mapping a cluster to its possible sku objects
        self.cluster_dict = {}

        # stores set of sku objects in the Match class
        self.sku_set = set()

        # stores list of items
        # self.item_list = []

        # caches the unused terms added in the Match Class
        self.unused_dict = {}

        # stores the items that were simply learning and haven't been used for updating popularity
        self.pending_updates = set()

        # caches the item name to a list of sku objects with score
        self.item_name_cache = {}

    def add_corpus(self, corpus):

        # assert type(corpus) is Corpus.Corpus
        self.corpora.append(corpus)
        return 1

    def add_leader_term(self, leader, sku):

        leader_corpus = self.match_term_corpus(leader)

        if leader_corpus is None:
            # select appropriate corpus to add leader to
            leader_corpus = self.corpora[0]

        # add leader term to cache
        self.term_dict[leader] = leader_corpus

        # add new leader to corpus and get unused terms that got matched when new leader was added
        temp_terms = leader_corpus.add_leader(leader)

        # remove those terms from unused cache
        for term in temp_terms:
            self.unused_dict.pop(term, None)

        # get the cluster to which the leader term belongs
        leader_cluster = leader_corpus.match_term_cluster(leader)

        # add relevant information to sku object
        sku.add_cluster(leader, leader_cluster)

        cluster_sku_set = self.cluster_dict.get(leader_cluster, set())
        cluster_sku_set.add(sku)
        self.cluster_dict[leader_cluster] = cluster_sku_set

        return 1

    def match_term_corpus(self, term):

        if term in self.unused_dict:
            self.unused_dict[term] += 1
            return None

        if term in self.term_dict:
            term_corpus = self.term_dict[term]

            term_corpus.add_term(term)
            # term_cluster = term_corpus.get_cached_term_cluster(term)
            return term_corpus

        # else

        term_corpus = None

        for corpus in self.corpora:
            success_flag = corpus.add_term(term)

            if success_flag == 1:
                term_corpus = corpus
                break

        if term_corpus is None:
            self.unused_dict[term] = 1
            return None

        term_corpus.add_term(term)
        return term_corpus

    def add_term(self, term, item):

        term_corpus = self.match_term_corpus(term)

        if term_corpus is None:
            return 0

        term_cluster = term_corpus.match_term_cluster(term)
        item.add_cluster(term, term_cluster)
        # term_corpus.add_term(term)

        self.term_dict[term] = term_corpus

        return 1

    def add_sku(self, sku):

        assert type(sku) is Sku.Sku

        self.sku_set.add(sku)

        for term in sku.terms:
            self.add_leader_term(term, sku)

    def add_item(self, item):

        # self.item_list.append(item)

        for term in item.terms:
            self.add_term(term, item)

    def match_item(self, item, learning_flag=False):

        # sku list containing score i.e. count of common clusters
        sku_list = self.get_sku_list_from_item_clusters(item)
        if not sku_list:
            return []
        max_score = max([x[1] for x in sku_list])

        if max_score == 0:
            return []

        sku_list = list(filter(lambda x: x[1] == max_score, sku_list))

        sku_list = list(map(lambda x: x[0], sku_list))
        # print(sku_list)
        sku_list = list(filter(lambda x: sku_utils.meets_match_count_threshold(item, x), sku_list))
        sku_list = list(map(lambda x: (x, scoring_utils.get_score(item, x)), sku_list))
        sku_list.sort(key=(lambda x: x[1]), reverse=True)

        for sku in sku_list:
            sku[0].add_dzer(item.dzer_id)
            sku[0].add_user(item.user_id)

        multiplier = len(sku_list)
        for sku in sku_list:
            sku[0].update_count(item.quantity)
            if learning_flag:
                sku[0].update_score(sku[1] * multiplier)
                self.pending_updates.add(sku[0])
            else:
                sku[0].update_popularity(sku[1] * multiplier)
            multiplier /= 2

        return sku_list

    def batch_update_sku(self):

        for sku in self.pending_updates:
            sku.setup_popularity()

        return 1

    def get_term_cluster(self, term):

        term_corpus = self.match_term_corpus(term)
        if term_corpus is None:
            return None

        return term_corpus.match_term_cluster(term)

    def get_sku_list_from_item_clusters(self, item):

        if item.name in self.item_name_cache:
            return self.item_name_cache[item.name]

        sku_score_dict = {}

        for item_term in item.terms:
            item_term_cluster = self.get_term_cluster(item_term)
            if item_term_cluster is None:
                continue

            item.add_cluster(item_term, item_term_cluster)
            item_term_sku_set = self.cluster_dict[item_term_cluster]
            for sku in item_term_sku_set:
                if sku in sku_score_dict:
                    sku_score_dict[sku] += 1
                else:
                    sku_score_dict[sku] = 1

        item_sku_with_score = [(k, v) for k, v in sku_score_dict.items()]
        item_sku_with_score.sort(key=lambda x: x[1], reverse=True)

        self.item_name_cache[item.name] = item_sku_with_score

        return item_sku_with_score

    def add_and_match_item_list(self, item_list):

        for item in item_list:
            self.add_item(item)
            self.match_item(item, learning_flag=True)
        self.batch_update_sku()
        return 1

    def get_sku_with_clusters_from_term_prefix_clusters(self, term):

        # term_cluster = self.get_term_cluster(term)

        # if term_cluster:
        #     return self.cluster_dict[term_cluster]

        eligible_clusters, score = self.corpora[0].get_eligible_clusters(term)

        if score < 0.5 * len(term) and score < 3:
            return set(), set()

        eligible_skus = []

        for cluster in eligible_clusters:
            eligible_skus.extend(self.cluster_dict[cluster])

        return set(eligible_skus), set(eligible_clusters)
        # return reduce(lambda a, b: a.union(b), eligible_skus)









