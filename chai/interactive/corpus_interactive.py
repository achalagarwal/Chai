from chai.src.corpus.Corpus import Corpus
from chai.src.master.Match import MatchSku


def main():

    print("Hi, Welcome to Chai Interactive")
    print("You are in the 'Single Corpus' Interactive Mode")
    corpus_name = input("Please Enter the name of your Corpus")
    corpus = Corpus(corpus_name)

    print("Please Enter the 'Standard Terms' for the corpus")

    standard_term = input()

    while not standard_term == '':
        corpus.add_leader(standard_term)
        standard_term = input()
    


