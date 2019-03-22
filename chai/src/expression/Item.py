from src.Utils.sku_utils import clean_item_with_meta
from src.cluster import Cluster


class Item:

    def __init__(self, user_id='Test', name='Test', subtag='', quantity=1, dzer_id='Test'):

        # stores name of the item
        self.name = name

        # stores the subtag of the item
        self.subtag = subtag

        # stores the subtag of the item
        self.quantity = quantity

        # stores the subtag of the item
        self.dzer_id = dzer_id

        # stores the subtag of the item
        self.user_id = user_id

        # stores the cleaned name and the meta data of the item
        self.clean_name, self.meta_data = clean_item_with_meta(name)

        # stores the list of terms in the item
        self.terms = self.clean_name.split()

        # maps term to a cluster
        self.term_cluster = {}

        # maps cluster to a list of terms (ordered)
        self.cluster_terms = {}

    def add_cluster(self, term, cluster):

        assert term in self.terms
        # assert type(cluster) is Cluster.Cluster

        self.term_cluster[term] = cluster

        cluster_terms = self.cluster_terms.get(cluster, [])
        cluster_terms.append(term)
        self.cluster_terms[cluster] = cluster_terms

        return 1

    def get_subtag(self):

        return self.subtag

    def get_name(self):

        return self.name
