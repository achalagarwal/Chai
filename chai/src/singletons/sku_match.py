from src.Utils import Pickler
from src.Utils.logger import logger


class SkuSingleton:

    __object = None

    def __init__(self):

        if SkuSingleton.__object is None:
            logger.info('UNPICKLING SKU MATCHING NOTEBOOK')
            SkuSingleton.__object = Pickler.unpickle_data('./src/sku_matchbook.pickle')

    def get_obj(self):

        return SkuSingleton.__object