from Utils import logger
logger = logger.logger


class Tagger:

    def __init__(self, matcher):

        self.terms = []

        self.term_cluster_map = {}

        self.cluster_term_map = {}

        self.clusters = set()

        self.settings_dict = {'cluster_limit': 1, 'hit_item': True, 'subtags': ['Alcohol']}

        self.matcher = matcher

    def add_term(self, term):

        term_corpus = self.matcher.match_term_corpus(term)

        if not term_corpus:
            return 0

        term_cluster = term_corpus.match_term_cluster(term)

        if term_cluster is None:
            return 0
        self.cluster_term_map[term_cluster] = term
        self.terms.append(term)
        self.term_cluster_map[term] = term_cluster
        self.clusters.add(term_cluster)

        return 1

    def add_cluster(self, cluster):

        cluster_leader = cluster.leader
        self.terms.append(cluster_leader)
        self.term_cluster_map[cluster_leader] = cluster
        self.clusters.add(cluster)
        self.cluster_term_map[cluster] = cluster_leader

        return 1

    def tag_item(self, item):

        tag = None

        if self.settings_dict['hit_item']:

            tag = self.extract_tag(item)

        if not tag:

            tag = self.generic_function_1(item)

        return tag

    def generic_function_1(self, item):

        tag = None

        item_sku_list = self.matcher.match_item(item)

        for sku in item_sku_list:
            tag = self.extract_tag(sku[0])
            if tag:
                return tag

        return tag

    def generic_function_2(self, item):

        tag = None

        item_sku_list = self.matcher.match_item(item)

        for sku in item_sku_list:
            tag = self.extract_tag(sku[0])
            if tag:
                return tag

        return tag

    def extract_tag(self, expression):

        # assert type(expression) is Expression

        valid_subtags = self.settings_dict['subtags']

        if expression.get_subtag() not in valid_subtags:
            return None

        expression_clusters = set(expression.cluster_terms.keys())

        matched_clusters = list(expression_clusters.intersection(self.clusters))

        try:
            assert len(matched_clusters) <= self.settings_dict['cluster_limit']
        except AssertionError:
            logger.debug("%s has cluster limit violations :: %s", expression.get_name(), matched_clusters)

        if matched_clusters:
            return self.cluster_term_map[matched_clusters[0]]
        return None





