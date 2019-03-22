from src.cluster import Cluster

Cluster = Cluster.Cluster


# 01) Test whether a term is getting added to the cache with its cluster score whenever get score is called
# 02)   "     "    a term's score is getting retrieved from the cache if available in the cache
# 03)   "     "    the match score returned is justifiable
# 04)   "     "    the add_term is adding a term to the cluster
# 05)   "     "    the add_term uses the cache to check if the term has been added before and return appropriately
# 06)   "     "    the scores of each term in dict is getting incremented correctly
# 07)   "     "    the prefix trie is breaking term in to its prefixes and adding all
# 09)   "     "    the cluster leader update is working
# 10)   "     "    the get_sorted terms is working correctly
# 11)   "     "    the an item is getting added to the prefix trie
# 12)   "     "    the add_term adds term in to the prefix trie

# 01

def test_whether_a_term_is_getting_added_to_the_term_cache_when_add_term_is_called_and_its_score_is_likewise_updated():

    cluster = Cluster('leader')
    cluster.add_term('lead')
    assert 'lead' in cluster.term_dict
    cluster.add_term('lead')
    assert cluster.term_dict['lead'] == 2


def test_whether_the_add_term_is_adding_appropriately_to_prefix_trie():

    cluster = Cluster('leader')
    assert 'leader' in cluster.prefix_trie
    assert 'leade' in cluster.prefix_trie
    assert 'lead' in cluster.prefix_trie
    assert 'lea' in cluster.prefix_trie
    assert 'le' in cluster.prefix_trie
    assert 'l' in cluster.prefix_trie

    cluster.add_term('peader')
    assert 'peader' in cluster.prefix_trie
    assert 'peade' in cluster.prefix_trie
    assert 'pead' in cluster.prefix_trie
    assert 'pea' in cluster.prefix_trie
    assert 'pe' in cluster.prefix_trie
    assert 'p' in cluster.prefix_trie


def test_whether_cluster_leader_update_is_working():

    cluster = Cluster('leader')
    cluster.add_leader('fake_leader')
    cluster.add_leader('fake_leader')
    assert cluster.leader == 'leader'
    cluster.update_leader()
    assert cluster.leader == 'fake_leader'


def test_whether_add_leader_adds_to_prefix_trie():

    cluster = Cluster('leader')
    cluster.add_leader('fake_leader')
    assert 'fake_leader' in cluster.term_dict
    assert 'fake' in cluster.prefix_trie


def test_whether_quick_match_score_is_correct():

    cluster = Cluster('leader')
    assert cluster.quick_match_score('lead') == 4
    assert cluster.quick_match_score('peader') == 0
