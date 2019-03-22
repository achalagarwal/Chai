class Scorer:

    def __init__(self,initial_score = 0,initial_incrementer= 1,decay_function = None, decay_factor = 2):
        self._score = initial_score
        self._incrementer = initial_incrementer
        self._decay_function = None
        # self.__set_score(initial_score)
        # self.__set_incrementer(incrementer)
        if decay_function:
            self._decay_function = decay_function
        else:
            self._decay_function = lambda x: x/decay_factor

    @property
    def score(self):
        return self._score

    @property
    def increment(self):
        self._score += self._incrementer

    @property
    def __incrementer(self):
        return self._incrementer

    @property
    def __decay_function(self):
        return self._decay_function
    @property
    def decay(self):
        self._incrementer = self._decay_function(self._incrementer)

    @score.setter
    def __set_score(self,initial_score):
        self._score = initial_score

    @__incrementer.setter
    def __set_incrementer(self, initial_incrementer):
        self._incrementer = initial_incrementer

    @__decay_function.setter
    def __set_decay(self, initial_decay_function):
        self._decay_function = initial_decay_function

    def __repr__(self):
         return str(self._score)
