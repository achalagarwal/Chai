from chai.src.corpus.Corpus import Corpus


def main():

    print("Hi, Welcome to Chai Interactive")
    print("You are in the 'Corpus' Interactive Mode")
    corpus_name = input("Please Enter the name of your Corpus")
    corpus = Corpus(corpus_name)

    print("Please Enter the 'Standard Terms' for the corpus")

    standard_term = input()

    while not standard_term == '':
        corpus.add_leader(standard_term)
        standard_term = input()

    print("Listed Below are the clusters in the Corpus, ", corpus.name)

    for cluster in corpus.clusters:
        print(cluster)

    print("We will match your terms to clusters")
    term = input("Enter term")

    while not term == '':
        term_cluster = corpus.match_term_cluster(term)
        if not term_cluster:
            print(term, ' was not matched with any existing clusters')

        else:
            print(term, ' was matched to cluster ', term_cluster.name)
        term = input("Enter term")


if __name__ == '__main__':
    main()
