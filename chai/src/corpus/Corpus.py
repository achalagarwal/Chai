# create Class for Cache -> Cache Clusters
from chai.src.cluster.Cluster import Cluster
from chai.src.Utils.Pickler import pickle_data
from tqdm import tqdm as progress


class Corpus:

    def __init__(self, name):

        # stores defining name of the corpus
        self.name = name

        # stores list of Clusters in Corpus
        self.clusters = []

        # stores dict with all terms mapped to a Cluster in clusters
        self.corpus_dict = {}

        # cache set of terms that were not matched for future use
        self.unused_dict = {}

        # dict with unused terms matched to temporary best cluster
        self.temp_dict = {}

        # corpus threshold for matching terms to clusters
        self.threshold = 80

        # stores a cleaning function for each corpus
        self.clean_item = None

    def has_term(self, term):

        if term in self.corpus_dict:
            return True

        # else

        return False

    def match_term_cluster(self, term):

        # add logic for max(average + leader) if required

        if term in self.unused_dict:
            self.unused_dict[term] += 1
            return self.temp_dict.get(term, None)

        if term in self.corpus_dict:
            return self.corpus_dict[term]

        eligible_clusters, quick_score = self.get_eligible_clusters(term)

        # else

        max_score = 0
        term_cluster = None

        while quick_score > 0:

            for cluster in eligible_clusters:
                match_score = cluster.match_score(term)

                if match_score > max_score:
                    max_score = match_score
                    term_cluster = cluster

            if max_score > self.threshold:
                return term_cluster

            quick_score -= 1
            eligible_clusters = self.get_specific_clusters(term, quick_score)

        self.temp_dict[term] = term_cluster
        self.unused_dict[term] = 1
        return None

    def add_cluster(self, cluster):

        assert cluster not in self.clusters

        self.clusters.append(cluster)

        return 1

    def add_term_to_cluster(self, term, cluster, score=1):

        # return if the cluster is not a good match
        # if term in self.unused_dict:
        #     return 0

        cluster.add_term(term, score=score)

        self.corpus_dict[term] = cluster

        return 1

    def add_term(self, term):

        cluster = self.match_term_cluster(term)

        if cluster is None:
            return 0

        if term not in self.unused_dict:
            self.add_term_to_cluster(term, cluster)

        return 1

    def fix_cache(self, cluster):

        temp_terms = []

        for term, score in self.unused_dict.items():
            term_match_score = cluster.match_score(term)
            if term_match_score > self.threshold:
                self.add_term_to_cluster(term, cluster, score=score)
                temp_terms.append(term)

        for term in temp_terms:
            self.unused_dict.pop(term)
            self.temp_dict.pop(term)

        return temp_terms

    def create_cluster(self, leader):
        new_cluster = Cluster(leader)
        self.add_cluster(new_cluster)
        self.corpus_dict[leader] = new_cluster
        return self.fix_cache(new_cluster)

    def add_leader(self, leader):

        if leader in self.unused_dict:
            return self.create_cluster(leader)

        if leader in self.corpus_dict:
            self.corpus_dict[leader].add_leader(leader)
            return []

        cluster = self.match_term_cluster(leader)

        if cluster is None:
            return self.create_cluster(leader)

        self.corpus_dict[leader] = cluster
        cluster.add_leader(leader)

        return []

    def pickle_corpus(self, filename):

        return pickle_data(self, filename)

    def add_leader_list(self, leader_list):

        for leader in progress(leader_list):
            self.add_leader(leader)

        return 1

    def add_term_list(self, term_list):

        for term in progress(term_list):
            self.add_term(term)

        return 1

    def reset_scores(self):

        for term in self.unused_dict:
            self.unused_dict[term] = 0

        for cluster in self.clusters:
            cluster.reset_scores()

        return 1

    def get_specific_clusters(self, term, score):

        specific_clusters = list(filter(lambda x: x.quick_match_score(term) == score, self.clusters))

        return specific_clusters

    def get_eligible_clusters(self, term):
        max_quick_score = 1
        eligible_clusters = []

        for cluster in self.clusters:

            temp_quick_score = cluster.quick_match_score(term)

            if temp_quick_score > max_quick_score:
                max_quick_score = temp_quick_score
                eligible_clusters = [cluster]

            elif temp_quick_score == max_quick_score:
                eligible_clusters.append(cluster)

        return eligible_clusters, max_quick_score

    def get_cached_term_cluster(self, term):

        if term in self.corpus_dict:
            return self.corpus_dict[term]

        return None
