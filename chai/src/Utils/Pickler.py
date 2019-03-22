import _pickle as pickle
from chai.src import master
from sys import path
import os
from chai.src.Utils.logger import logger
path.append('./src/master')
path.append('./src')

logger.info("PATH %s", os.getcwd())


def pickle_data(data, filename):

    try:
        with open(filename,'wb') as handle:
            pickle.dump(data,handle)
    except MemoryError:
        return 0

    return 1


def unpickle_data(filename):

    try:
        with open(filename, 'rb') as handle:
            b = pickle.load(handle)
    except MemoryError:
        return None

    return b


def pickle_dict(dictionary,filename):

    try:
        with open(filename,'wb') as handle:
            pickle.dump(dictionary,handle)
    except MemoryError:
        return 0

    return 1


def unpickle_dict(filename):

    try:
        with open(filename, 'rb') as handle:
            b = pickle.load(handle)
    except MemoryError:
        return None

    return b
