from chai.src.Utils.sku_utils import clean_item_with_meta, get_linear_span, get_min_item_edit_distance, is_eligible_pair
from chai.src.cluster import Cluster


class Sku:

    def __init__(self, sku_name, sku_subtag='', sku_id='', sku_meta=''):

        # stores the sku id
        self._id = sku_id

        # stores original Name
        self._name = sku_name

        # stores cleaned item name and meta data :- acronyms, quantity, measurements
        self._clean_name, self.meta_data = clean_item_with_meta(sku_name + ' ' + sku_meta)

        # validate item
        try:
            assert self._name
        except AssertionError:
            print(sku_name)

        # final popularity that is released
        self._popularity = 0

        # score is for cluster leader
        self._score = 0

        # stores raw count with debuffed quantity
        self._count = 0

        # computes and stores span for use in match_distance
        self._span = get_linear_span(self._name.split())

        # stores subtag for better match
        self._subtag = sku_subtag

        # stores set of dzer ids with count of matches
        self._dzer_ids = {}

        # stores the set of user ids who have ordered the item (for count purposes)
        self._user_ids = set()

        # stores the terms in the clean name
        self.terms = self._clean_name.split()

        # maps term to a cluster
        self.term_cluster = {}

        # maps cluster to a list of terms (ordered)
        self.cluster_terms = {}

        # flag to set an sku object as disabled
        self._disabled = False

        return

    def update_count(self, quantity):
        try:
            assert quantity > 0
        except AssertionError:
            # print(quantity)
            quantity = 1.0

        self._count += 1

        if 10 < quantity:
            self._count += 1
        elif 8 < quantity:
            self._count += 0.8
        elif 5 < quantity:
            self._count += 0.5
        elif 2 < quantity:
            self._count += 0.2
        elif 1 < quantity:
            self._count += 0.1

        return

    def match_distance(self, item_name):

        # clean_item = clean_item(item_name)

        return get_min_item_edit_distance(item_name, self._span)

    def update_score(self, score):

        assert(self._count > 0)

        # update score based on past count
        self._score += score * self._count / 100

        return

    def setup_popularity(self):

        self._popularity = self._score

        return 1

    def update_popularity(self, popularity):

        self._popularity += popularity * self._count / 100

        return

    def add_user(self, user_id):

        self._user_ids.add(user_id)
        return 1

    def add_dzer(self, dzer_id):

        prev_count = self._dzer_ids.get(dzer_id, 0)
        self._dzer_ids[dzer_id] = prev_count + 1
        return 1

    def add_cluster(self, term, cluster):

        assert term in self.terms
        assert type(cluster) is Cluster.Cluster

        self.term_cluster[term] = cluster

        cluster_terms = self.cluster_terms.get(cluster, [])
        cluster_terms.append(term)
        self.cluster_terms[cluster] = cluster_terms

        return 1

    def is_eligible(self, item_name, item_subtag=''):

        return is_eligible_pair((self._name, self._subtag), (item_name, item_subtag))

    def __repr__(self):
        return self._name + '\n' + \
               self._subtag + '\n' + \
               str(round(self._popularity, 3)) + '\n' + \
               str(len(self._user_ids)) + '\n'

    def get_subtag(self):

        return self._subtag

    def get_name(self):

        return self._name