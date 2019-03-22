from fuzzywuzzy import fuzz


def match_score(term1, term2):

    assert(len(term1.split()) == 1 == len(term2.split()))

    return fuzz.ratio(term1, term2)

