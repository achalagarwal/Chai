from src.Utils.sku_utils import extract_alcohol_liquid_quantity
from src.master import Tagger
from sys import maxsize
from src.Utils import logger
from src.expression import Item
from src.singletons import sku_match
logger = logger.logger
Tagger = Tagger.Tagger
sku_matcher_singleton = sku_match.SkuSingleton()
matcher = sku_matcher_singleton.get_obj()
# matcher = None

class AlcoholLimit:

    def __init__(self, strategy, matcher):

        self.strategy = strategy

        # add dict for matching common tags
        self.metric_dict = {'beer': {'pint': 330, 'can': 500},
                            'others': {'quarter': 180, 'half': 375, 'full': 750, 'magnum': 1500}}

        self.alcohol_tagger = Tagger(matcher)

        self.terms = ['beer', 'wine', 'brandy', 'gin', 'rum', 'vodka', 'breezer', 'tequila', 'whisky']

        for term in self.terms:
            self.alcohol_tagger.add_term(term)

        self.min_term_dict = {}
        self.max_term_dict = {}

        for term in self.terms:
            self.max_term_dict[term] = 0
            self.min_term_dict[term] = 0

        self.matcher = matcher

        self.broad_categories = ['hard_liquor', 'wine', 'beer', 'toddy']
        self.category_limit = {'hard_liquor': 4000, 'wine': 9000, 'beer': 18000, 'toddy': 2500}
        self.min_category_dict = {}
        self.max_category_dict = {}

        for category in self.broad_categories:
            self.max_category_dict[category] = 0
            self.min_category_dict[category] = 0

        self.term_category = {'beer': 'beer', 'wine': 'wine', 'brandy': 'hard_liquor', 'gin': 'hard_liquor', 'rum': 'hard_liquor', 'vodka': 'hard_liquor', 'breezer': 'beer', 'tequila': 'hard_liquor', 'whisky': 'hard_liquor'}

        self.default_quantities = {'beer': (330, 650),
                                   'wine': (375, 1000),
                                   'brandy': (180, 1000),
                                   'gin': (180, 1000),
                                   'rum': (180, 1000),
                                   'vodka': (180, 1000),
                                   'breezer': (180, 650),
                                   'tequila': (180, 1000),
                                   'whisky': (180, 1000)}

    def update_values(self, tag, lower, upper):
        if lower < upper:
            print("Type: ", tag + "\nLower Bound (mls) : ", lower, "\nUpper Bound (mls) : ", upper)
        elif lower == upper:
            print("Type: ", tag + "\nQuantity (mls) : ", lower)
        self.min_term_dict[tag] += lower
        self.max_term_dict[tag] += upper
        self.min_category_dict[self.term_category[tag]] += lower
        self.max_category_dict[self.term_category[tag]] += upper
        return tag, lower, upper

    def update_default_values(self, alcohol_tag):

        min_q, max_q = self.default_quantities[alcohol_tag]

        return self.update_values(alcohol_tag, min_q, max_q)

    def get_ml(self, quantity, metric):

        if metric in self.metric_dict:
            return self.metric_dict[metric]

        if 'm' in metric:
            return quantity

        return 1000 * quantity

    # def hit_item(self, item):
    #
    #     # if item.get_subtag() == 'Grocery':
    #     #     logger.info("%s has the subtag Grocery and hence ignored", item.get_name())
    #     #     return
    #
    #     try:
    #         assert item in self.matcher.item_list
    #     except AssertionError:
    #         self.matcher.add_item(item)
    #
    #     min_ml = maxsize
    #     max_ml = 0
    #     flag = False
    #     item_tag = self.alcohol_tagger.tag_item(item)
    #
    #     if item_tag is None:
    #
    #         logger.info("%s was not detected to be a standard alcohol", item.get_name())
    #         return None, 0, 0
    #
    #     quantity, metric = extract_alcohol_liquid_quantity(item, self.metric_dict.get(item_tag, self.metric_dict['others']))
    #
    #     if quantity:
    #         min_ml = self.get_ml(quantity, metric)
    #         max_ml = min_ml
    #         flag = True
    #
    #     if quantity is None:
    #
    #         item_sku_list = self.matcher.match_item(item)
    #         if not item_sku_list:
    #             return self.update_default_values(item_tag)
    #         max_score = max([x[1] for x in item_sku_list])
    #         item_sku_list = list(filter(lambda x: x[1] == max_score, item_sku_list))
    #         item_sku_list = list(map(lambda x: x[0], item_sku_list))
    #
    #         for sku in item_sku_list:
    #
    #             quantity, metric = extract_alcohol_liquid_quantity(sku, self.metric_dict)
    #
    #             if quantity is None:
    #                 continue
    #
    #             flag = True
    #
    #             ml = self.get_ml(quantity, metric)
    #
    #             min_ml = min(min_ml, ml)
    #             max_ml = max(max_ml, ml)
    #
    #     if flag:
    #         return self.update_values(item_tag, min_ml, max_ml)
    #
    #     else:
    #         return self.update_default_values(item_tag)

    def check_order(self, order):

        for order_item in order:
            self.strategy.hit_item(Item.Item(name=order_item, subtag='Alcohol'))
        
        return 1

    def get_order_details(self, order):

        order_details = []

        for order_item in order:
            item_tag, item_lower, item_upper = self.strategy.hit_item(Item.Item(name=order_item, subtag='Alcohol'))
            order_details.append({'alcohol_type': item_tag, 'min': item_lower, 'max': item_upper})

        return order_details



class AlcoholLimitBangalore(AlcoholLimit):

    def __init__(self, matcher):

        super().__init__(self, matcher)

        self.category_limit = {'hard_liquor': 4000, 'wine': 9000, 'beer': 18000, 'toddy': 2500}

    def hit_item(self, item):

        # if item.get_subtag() == 'Grocery':
        #     logger.info("%s has the subtag Grocery and hence ignored", item.get_name())
        #     return

        self.matcher.add_item(item)

        min_ml = maxsize
        max_ml = 0
        flag = False
        item_tag = self.alcohol_tagger.tag_item(item)

        if item_tag is None:
            logger.info("%s was not detected to be a standard alcohol", item.get_name())
            return None, 0, 0

        quantity, metric = extract_alcohol_liquid_quantity(item, self.metric_dict.get(item_tag,
                                                                                      self.metric_dict['others']))

        if quantity:
            min_ml = self.get_ml(quantity, metric)
            max_ml = min_ml
            flag = True

        if quantity is None:

            item_sku_list = self.matcher.match_item(item)
            if not item_sku_list:
                return self.update_default_values(item_tag)
            max_score = max([x[1] for x in item_sku_list])
            item_sku_list = list(filter(lambda x: x[1] == max_score, item_sku_list))
            item_sku_list = list(map(lambda x: x[0], item_sku_list))

            for sku in item_sku_list:

                quantity, metric = extract_alcohol_liquid_quantity(sku, self.metric_dict)

                if quantity is None:
                    continue

                flag = True

                ml = self.get_ml(quantity, metric)

                min_ml = min(min_ml, ml)
                max_ml = max(max_ml, ml)

        if flag:
            return self.update_values(item_tag, min_ml, max_ml)

        else:
            return self.update_default_values(item_tag)

    def get_rule_details(self):

        rule_details = []
        flag = True

        for category in self.broad_categories:
            if self.max_category_dict[category] > self.category_limit[category]:
                flag = False
                rule_details.append({'category': category,
                                     'rule_limit': self.category_limit[category],
                                     'ordered_quantity': self.max_category_dict[category],
                                     'out_of_limits': True})
            else:
                rule_details.append({'category': category,
                                     'rule_limit': self.category_limit[category],
                                     'ordered_quantity': self.max_category_dict[category],
                                     'out_of_limits': False})

        return flag, rule_details


class AlcoholLimitGurgaon(AlcoholLimit):

    def __init__(self, matcher):

        super().__init__(self, matcher)

        # TODO add rules
        self.category_limit = {}
        for category in self.broad_categories:
            self.category_limit[category] = 2

    def hit_item(self, item):

        self.matcher.add_item(item)
        item_tag = self.alcohol_tagger.tag_item(item)

        if item_tag is None:
            logger.info("%s was not detected to be a standard alcohol", item.get_name())
            return None, 0, 0

        return self.update_values(item_tag, 1, 1)

    def get_rule_details(self):
        rule_details = []
        flag = True

        for category in self.broad_categories:
            if self.max_category_dict[category] > self.category_limit[category]:
                flag = False
                rule_details.append({'category': category,
                                     'rule_limit': self.category_limit[category],
                                     'ordered_units': self.max_category_dict[category],
                                     'out_of_limits': True})
            else:
                rule_details.append({'category': category,
                                     'rule_limit': self.category_limit[category],
                                     'ordered_units': self.max_category_dict[category],
                                     'out_of_limits': False})

        return flag, rule_details


class AlcoholLimitPune(AlcoholLimit):

    def __init__(self, matcher):

        super().__init__(self,matcher)

        self.terms = ['beer', 'wine', 'brandy', 'gin', 'rum', 'vodka', 'breezer', 'tequila', 'whisky']
        self.category_limit = {'beer': 7800,
                               'wine': 9000,
                               'brandy': 4500,
                               'gin': 4500,
                               'rum': 3900,
                               'vodka': 4500,
                               'breezer': 9000,
                               'tequila': 4500,
                               'whisky': 4500}

    def hit_item(self, item):

        self.matcher.add_item(item)
        min_ml = maxsize
        max_ml = 0
        flag = False
        item_tag = self.alcohol_tagger.tag_item(item)

        if item_tag is None:
            logger.info("%s was not detected to be a standard alcohol", item.get_name())
            return None, 0, 0

        quantity, metric = extract_alcohol_liquid_quantity(item, self.metric_dict.get(item_tag,
                                                                                      self.metric_dict['others']))

        if quantity:
            min_ml = self.get_ml(quantity, metric)
            max_ml = min_ml
            flag = True

        if quantity is None:

            item_sku_list = self.matcher.match_item(item)
            if not item_sku_list:
                return self.update_default_values(item_tag)
            max_score = max([x[1] for x in item_sku_list])
            item_sku_list = list(filter(lambda x: x[1] == max_score, item_sku_list))
            item_sku_list = list(map(lambda x: x[0], item_sku_list))

            for sku in item_sku_list:

                quantity, metric = extract_alcohol_liquid_quantity(sku, self.metric_dict)

                if quantity is None:
                    continue

                flag = True

                ml = self.get_ml(quantity, metric)

                min_ml = min(min_ml, ml)
                max_ml = max(max_ml, ml)

        if flag:
            return self.update_values(item_tag, min_ml, max_ml)

        else:
            return self.update_default_values(item_tag)
        pass

    def get_rule_details(self):

        rule_details = []
        flag = True

        for term in self.terms:
            if self.max_term_dict[term] > self.category_limit[term]:
                flag = False
                rule_details.append({'category': term,
                                     'rule_limit': self.category_limit[term],
                                     'ordered_units': self.max_term_dict[term],
                                     'out_of_limits': True})
            else:
                rule_details.append({'category': term,
                                     'rule_limit': self.category_limit[term],
                                     'ordered_units': self.max_term_dict[term],
                                     'out_of_limits': False})

        return flag, rule_details


def hit_order(order, city_id):

    strategy = get_strategy(city_id)
    # self.hit_item = strategy.hit_item

    order_details = strategy.get_order_details(order)

    order_bound = {'min': strategy.min_term_dict, 'max': strategy.max_term_dict}
    broad_order_bound = {'min': strategy.min_category_dict, 'max': strategy.max_category_dict}

    order_valid_flag, rule_details = strategy.get_rule_details()

    return order_valid_flag, rule_details, order_details, order_bound, broad_order_bound


def get_strategy(city_id):

    if city_id == 1:
        logger.info("Bangalore Rules Applied")
        return AlcoholLimitBangalore(matcher)
    if city_id == 2:
        logger.info("Gurgaon Rules Applied")
        return AlcoholLimitGurgaon(matcher)
    if city_id == 3:
        logger.info("Pune Rules Applied")
        return AlcoholLimitPune(matcher)
    else:
        logger.info("Not a valid city id hence Bangalore Rules Applied")
        return AlcoholLimitBangalore(matcher)



