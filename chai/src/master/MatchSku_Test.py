from src.master.Match import MatchSku
from src.corpus import Corpus
from src.expression import Sku


def test_whether_sku_matchbook_adds_sku_correctly():

    test_matchbook = MatchSku()
    test_sku_corpus = Corpus.Corpus('sku')
    test_matchbook.add_corpus(test_sku_corpus)
    test_name = 'sku match book tests'
    test_sku = Sku.Sku(sku_name=test_name)
    test_matchbook.add_sku(test_sku)

    for term in test_name.split():
        assert term in test_matchbook.term_dict
        term_cluster = test_matchbook.corpora[0].corpus_dict[term]
        assert term_cluster.leader == term
        assert term in test_sku.term_cluster
        assert test_sku.term_cluster[term] == term_cluster


