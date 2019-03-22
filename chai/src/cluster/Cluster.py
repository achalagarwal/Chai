from chai.src.cluster.cluster_utils import match_score as get_match_score


class Cluster:
    '''Clusters are the primary blocks of the complete NER model.\n
    They work on individual words i.e. each word is considered separately before cluster assignment \n
    Clusters are defined with the help of their leader, and may contain more than one leader terms. Clusters contain a prefix trie to enable fast matching, the matching algorithm is plug and play ready and a paramter for tuning the strictness of the cluster is also available '''

    def __init__(self, leader_term):

        # stores cluster leader
        self.leader = leader_term

        # stores dict of term and score
        self.term_dict = {leader_term: 1}

        # stores all corpus (leader) terms in cluster
        self.leader_terms = set()
        self.leader_terms.add(leader_term)

        # prefix trie for quick check
        self.prefix_trie = {}
        self.add_to_trie(leader_term)

    @property
    def name(self):
        ''' Returns the name i.e. the current leader of the cluster

            Params: None
        '''
        return self.leader

    def has_term(self, term):
        '''
            Checks if a term is in the set of terms

            Params: term -> the term which needs to be checked
        '''

        if term in self.term_dict:
            return True
        else:
            return False

    def add_term(self, term, score=1):
        ''' Adds a term to the cluster

        :param term: the term that needs to be added to the cluster
        :param score: the score for the term that needs to be added

        '''
        prev_term_score = self.term_dict.get(term, 0)
        self.term_dict[term] = prev_term_score + score
        self.add_to_trie(term)
        return 1

    def add_to_trie(self, term):
        '''
        A helper function for adding a term to a cluster, reursively adds

        :param term: the term whose prefixes need to be added in the trie

        '''
        if not term:
            return 1

        if term in self.prefix_trie:
            return 0

        # else

        self.prefix_trie[term] = 1
        return self.add_to_trie(term[:-1])

    def match_score(self, term):
        '''
        Returns the score of a term's match in a cluster

        :param term: the term whose cluster match score needs to be computed
        '''
        if self.has_term(term):
            return 100

        # else
        return self.fuzzy_match_score(term)

    def fuzzy_match_score(self, term):
        '''
        Helper Function called by *match_score* to compute the score for a new term

        :param term: the term which needs to be scored

        '''
        threshold_score = 80

        for cluster_term in self.get_sorted_terms()[:11]:

            match_score = get_match_score(cluster_term, term)

            if match_score > threshold_score:
                return match_score

            threshold_score += 1

        return get_match_score(self.leader, term)

    def add_leader(self, leader_term):
        '''
        Adds leader term to the cluster

        :param leader_term: the leader term which needs to be added

        '''
        # if self.add_term(leader_term) == 1:
        #     self.leader_terms.add(leader_term)

        self.add_term(leader_term)
        self.leader_terms.add(leader_term)

        return 1

    def update_leader(self):
        '''
        Updates the leader of the cluster to the term with the highest scoreself.




        '''

        temp_leader = self.leader
        temp_max = self.term_dict[temp_leader]

        for term in self.leader_terms:
            term_score = self.term_dict[term]

            if term_score > temp_max:
                temp_max = term_score
                temp_leader = term

        if self.leader is not temp_leader:
            self.leader = temp_leader

        return 1

    def is_leader(self, term):

        if term in self.leader_terms:
            return True

        # else
        return False

    def get_sorted_terms(self):

        term_list = list(self.term_dict.keys())
        term_list.sort(key=lambda x: self.term_dict[x], reverse=True)

        return term_list

    def is_in_trie(self, term):

        return term in self.prefix_trie

    def quick_match_score(self, term):

        score = len(term)

        while score > 0:
            if self.is_in_trie(term[0:score]):
                return score
            score -= 1

        return score

    def __repr__(self):

        return '\nCluster Name: ' + self.name + '\n' + \
            'Followed By: ' + str(self.leader_terms) + '\n' + \
            'Terms: ' + str(self.term_dict.items()) + '\n'
