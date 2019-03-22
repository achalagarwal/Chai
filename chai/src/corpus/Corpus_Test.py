from src.corpus import Corpus
from src.cluster import Cluster
test_term = 'thistermwillneverbeavalidtermforobviousreasonsanditsmeantfortesting'
# 1) Chec


def test_whether_match_term_caches_information():

    test_corpus = Corpus.Corpus('test')
    test_corpus.match_term_cluster(test_term)
    assert test_term in test_corpus.unused_dict


def test_whether_add_term_to_corpus_works_as_intended():

    test_corpus = Corpus.Corpus('test')
    test_cluster = Cluster.Cluster('theclusterwhichwillnotmatchwithtest_termbutlinktemporarily')
    test_corpus.add_cluster(test_cluster)
    test_corpus.add_term(test_term)
    assert test_term in test_corpus.unused_dict
    assert test_corpus.temp_dict[test_term] == test_cluster
    assert not test_cluster.has_term(test_term)


def test_whether_add_leader_works_as_intended():

    test_corpus = Corpus.Corpus('test')
    test_term = 'unknown'
    test_corpus.add_term(test_term)
    test_corpus.add_term(test_term)
    test_corpus.add_leader('unknowns')

    assert test_term not in test_corpus.temp_dict
    assert test_term not in test_corpus.unused_dict
    assert test_term in test_corpus.corpus_dict

    assigned_cluster = test_corpus.corpus_dict[test_term]
    assert test_term in assigned_cluster.term_dict
    assert assigned_cluster.term_dict[test_term] == 2


